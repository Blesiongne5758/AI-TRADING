"""
Strategy Runner
Menjalankan strategi trading candle-by-candle dengan integritas tinggi
"""
import pandas as pd
from typing import Dict, List, Optional, Callable
from datetime import datetime
from loguru import logger
from dataclasses import dataclass, field


@dataclass
class BacktestTrade:
    """Representasi satu trade dalam backtest"""
    id: int
    symbol: str
    side: str  # 'long' atau 'short'
    entry_time: datetime
    entry_price: float
    quantity: float
    stop_loss: float
    take_profit: float
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None
    pnl: float = 0.0
    pnl_percent: float = 0.0
    fee: float = 0.0
    holding_period: Optional[float] = None  # dalam jam


@dataclass
class BacktestResult:
    """Hasil lengkap backtest"""
    symbol: str
    timeframe: str
    start_date: datetime
    end_date: datetime
    initial_balance: float
    final_balance: float
    trades: List[BacktestTrade] = field(default_factory=list)
    equity_curve: List[Dict] = field(default_factory=list)
    parameters: Dict = field(default_factory=dict)


class StrategyRunner:
    """Menjalankan strategi trading pada data historis"""

    def __init__(
        self,
        initial_balance: float = 10000.0,
        trading_fee_percent: float = 0.1,
        max_risk_per_trade: float = 2.0,
    ):
        self.initial_balance = initial_balance
        self.trading_fee_percent = trading_fee_percent
        self.max_risk_per_trade = max_risk_per_trade

    def run_backtest(
        self,
        data: pd.DataFrame,
        symbol: str,
        timeframe: str,
        strategy_func: Callable,
        strategy_params: Dict = None,
    ) -> BacktestResult:
        """
        Menjalankan backtest candle-by-candle
        
        PENTING: Strategi hanya boleh melihat data hingga candle saat ini.
        Tidak boleh melihat candle masa depan (lookahead bias prevention).
        
        Args:
            data: DataFrame OHLCV historis
            symbol: Trading pair
            timeframe: Interval candle
            strategy_func: Function yang menerima (data_slice, params) dan return signal
            strategy_params: Parameter strategi (untuk optimization)
            
        Returns:
            BacktestResult dengan semua trades dan equity curve
        """
        if strategy_params is None:
            strategy_params = {}

        logger.info(f"🔬 Running backtest: {symbol} [{timeframe}]")
        logger.info(f"   Data: {len(data)} candles ({data.index[0]} → {data.index[-1]})")
        logger.info(f"   Strategy params: {strategy_params}")

        # State
        balance = self.initial_balance
        available_balance = self.initial_balance
        position: Optional[BacktestTrade] = None
        trades: List[BacktestTrade] = []
        equity_curve: List[Dict] = []
        trade_id = 0

        # Minimum data untuk indikator (EMA 200 butuh 200 candle)
        min_candles = 200

        # Loop candle-by-candle (NO LOOKAHEAD!)
        for i in range(min_candles, len(data)):
            current_candle = data.iloc[i]
            current_time = data.index[i]
            current_price = current_candle["close"]

            # Data yang tersedia untuk strategi (hanya sampai candle saat ini)
            historical_slice = data.iloc[:i+1]

            # === 1. Cek Exit Conditions (jika ada posisi terbuka) ===
            if position is not None:
                exit_result = self._check_exit_conditions(
                    position=position,
                    high=current_candle["high"],
                    low=current_candle["low"],
                    close=current_price,
                )

                if exit_result:
                    # Close position
                    position.exit_time = current_time
                    position.exit_price = exit_result["exit_price"]
                    position.exit_reason = exit_result["exit_reason"]
                    position.holding_period = (
                        (current_time - position.entry_time).total_seconds() / 3600
                    )

                    # Hitung PnL
                    if position.side == "long":
                        gross_pnl = (position.exit_price - position.entry_price) * position.quantity
                    else:
                        gross_pnl = (position.entry_price - position.exit_price) * position.quantity

                    # Fee exit
                    exit_value = position.exit_price * position.quantity
                    exit_fee = exit_value * (self.trading_fee_percent / 100)
                    position.fee += exit_fee
                    position.pnl = gross_pnl - exit_fee
                    position.pnl_percent = (position.pnl / (position.entry_price * position.quantity)) * 100

                    # Update balance
                    available_balance += (position.entry_price * position.quantity) + position.pnl
                    balance = available_balance

                    trades.append(position)
                    position = None

            # === 2. Generate Signal (hanya jika tidak ada posisi) ===
            if position is None:
                try:
                    signal = strategy_func(historical_slice, strategy_params)
                except Exception as e:
                    logger.debug(f"Strategy error at {current_time}: {e}")
                    signal = None

                # Eksekusi jika ada signal
                if signal and signal.get("action") in ["BUY", "SELL"]:
                    position = self._open_position(
                        signal=signal,
                        symbol=symbol,
                        entry_time=current_time,
                        entry_price=current_price,
                        balance=available_balance,
                        trade_id=trade_id,
                    )
                    if position:
                        trade_id += 1
                        # Reserve margin
                        position_value = position.entry_price * position.quantity
                        entry_fee = position_value * (self.trading_fee_percent / 100)
                        position.fee = entry_fee
                        available_balance -= (position_value + entry_fee)

            # === 3. Record Equity ===
            unrealized_pnl = 0.0
            if position is not None:
                if position.side == "long":
                    unrealized_pnl = (current_price - position.entry_price) * position.quantity
                else:
                    unrealized_pnl = (position.entry_price - current_price) * position.quantity

            equity_curve.append({
                "timestamp": current_time,
                "balance": balance + unrealized_pnl,
                "price": current_price,
                "in_position": position is not None,
            })

        # Close posisi yang masih terbuka di akhir backtest
        if position is not None:
            last_candle = data.iloc[-1]
            position.exit_time = data.index[-1]
            position.exit_price = last_candle["close"]
            position.exit_reason = "BACKTEST_END"
            
            if position.side == "long":
                gross_pnl = (position.exit_price - position.entry_price) * position.quantity
            else:
                gross_pnl = (position.entry_price - position.exit_price) * position.quantity
            
            exit_fee = (position.exit_price * position.quantity) * (self.trading_fee_percent / 100)
            position.pnl = gross_pnl - exit_fee
            position.pnl_percent = (position.pnl / (position.entry_price * position.quantity)) * 100
            trades.append(position)
            available_balance += (position.entry_price * position.quantity) + position.pnl

        result = BacktestResult(
            symbol=symbol,
            timeframe=timeframe,
            start_date=data.index[0],
            end_date=data.index[-1],
            initial_balance=self.initial_balance,
            final_balance=available_balance,
            trades=trades,
            equity_curve=equity_curve,
            parameters=strategy_params,
        )

        logger.info(f"✅ Backtest complete: {len(trades)} trades")
        logger.info(f"   Final balance: ${result.final_balance:,.2f}")
        logger.info(f"   Return: {((result.final_balance/self.initial_balance)-1)*100:+.2f}%")

        return result

    def _check_exit_conditions(
        self, position: BacktestTrade, high: float, low: float, close: float
    ) -> Optional[Dict]:
        """Cek apakah posisi harus ditutup (SL/TP hit)"""
        if position.side == "long":
            # Cek SL dulu (prioritas)
            if low <= position.stop_loss:
                return {"exit_price": position.stop_loss, "exit_reason": "STOP_LOSS"}
            # Cek TP
            if high >= position.take_profit:
                return {"exit_price": position.take_profit, "exit_reason": "TAKE_PROFIT"}
        else:  # short
            if high >= position.stop_loss:
                return {"exit_price": position.stop_loss, "exit_reason": "STOP_LOSS"}
            if low <= position.take_profit:
                return {"exit_price": position.take_profit, "exit_reason": "TAKE_PROFIT"}

        return None

    def _open_position(
        self,
        signal: Dict,
        symbol: str,
        entry_time: datetime,
        entry_price: float,
        balance: float,
        trade_id: int,
    ) -> Optional[BacktestTrade]:
        """Membuka posisi baru"""
        side = "long" if signal["action"] == "BUY" else "short"
        position_size_percent = signal.get("position_size_percent", 10)
        position_value = balance * (position_size_percent / 100)
        quantity = position_value / entry_price

        return BacktestTrade(
            id=trade_id,
            symbol=symbol,
            side=side,
            entry_time=entry_time,
            entry_price=entry_price,
            quantity=quantity,
            stop_loss=signal["stop_loss"],
            take_profit=signal["take_profit"],
        )


# === CONTOH STRATEGI (untuk testing) ===

def strategy_rsi_macd_ema(data: pd.DataFrame, params: Dict) -> Optional[Dict]:
    """
    Contoh strategi: RSI + MACD + EMA
    BUY jika: RSI < 30 AND MACD crossover up AND price > EMA200
    SELL jika: RSI > 70 AND MACD crossover down
    """
    import pandas_ta as ta

    # Parameters (bisa di-optimize)
    rsi_period = params.get("rsi_period", 14)
    rsi_oversold = params.get("rsi_oversold", 30)
    rsi_overbought = params.get("rsi_overbought", 70)

    if len(data) < 200:
        return None

    close = data["close"]
    
    # Hitung indikator
    rsi = ta.rsi(close, length=rsi_period)
    macd = ta.macd(close, fast=12, slow=26, signal=9)
    ema200 = ta.ema(close, length=200)

    if rsi.iloc[-1] != rsi.iloc[-1]:  # NaN check
        return None

    current_price = float(close.iloc[-1])
    current_rsi = float(rsi.iloc[-1])
    current_macd_hist = float(macd.iloc[-1, 1])
    prev_macd_hist = float(macd.iloc[-2, 1])
    current_ema200 = float(ema200.iloc[-1])

    # ATR untuk SL/TP
    atr = ta.atr(data["high"], data["low"], close, length=14)
    current_atr = float(atr.iloc[-1])

    # BUY signal
    if (current_rsi < rsi_oversold and 
        current_macd_hist > 0 and prev_macd_hist <= 0 and
        current_price > current_ema200):
        
        sl = current_price - (current_atr * 2)
        tp = current_price + (current_atr * 4)  # RR 1:2
        
        return {
            "action": "BUY",
            "stop_loss": sl,
            "take_profit": tp,
            "position_size_percent": 10,
        }

    # SELL signal (untuk close long atau open short)
    if current_rsi > rsi_overbought and current_macd_hist < 0 and prev_macd_hist >= 0:
        return {"action": "SELL"}

    return None
