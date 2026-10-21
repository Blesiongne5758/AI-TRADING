"""
Strategy Runner - Execute trading strategy candle-by-candle
"""
import pandas as pd
from typing import List, Dict, Optional, Callable
from datetime import datetime
from loguru import logger
from analysis.technical_indicators import TechnicalAnalyzer
from analysis.sentiment_analysis import SentimentAnalyzer
from analysis.signal_generator import SignalGenerator


class StrategyRunner:
    """Run trading strategy on historical data"""

    def __init__(
        self,
        initial_balance: float = 10000.0,
        max_risk_per_trade: float = 0.02,
        trading_fee: float = 0.001,
    ):
        """
        Initialize strategy runner

        Args:
            initial_balance: Starting balance
            max_risk_per_trade: Max risk per trade (e.g., 0.02 = 2%)
            trading_fee: Trading fee per trade (e.g., 0.001 = 0.1%)
        """
        self.initial_balance = initial_balance
        self.max_risk_per_trade = max_risk_per_trade
        self.trading_fee = trading_fee

        # Analysis components
        self.tech_analyzer = TechnicalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer(use_finbert=False)
        self.signal_generator = SignalGenerator()

        # State
        self.balance = initial_balance
        self.positions: List[Dict] = []
        self.trades: List[Dict] = []
        self.equity_curve: List[Dict] = []

    async def run(
        self,
        candles_df: pd.DataFrame,
        news_data: Optional[List[Dict]] = None,
        strategy_func: Optional[Callable] = None,
    ) -> Dict:
        """
        Run strategy on historical data

        Args:
            candles_df: DataFrame with OHLCV data
            news_data: List of news articles (optional)
            strategy_func: Custom strategy function (optional)

        Returns:
            Dictionary with backtest results
        """
        logger.info(f"Starting backtest with {len(candles_df)} candles")

        # Reset state
        self.balance = self.initial_balance
        self.positions = []
        self.trades = []
        self.equity_curve = []

        # Run candle-by-candle
        for i in range(len(candles_df)):
            current_candle = candles_df.iloc[i]
            current_time = candles_df.index[i]

            # Get historical data up to current candle (no look-ahead bias)
            historical_data = candles_df.iloc[: i + 1]

            # Get news up to current time
            current_news = []
            if news_data:
                current_news = [
                    n
                    for n in news_data
                    if datetime.fromtimestamp(n["published_date"] / 1000) <= current_time
                ]

            # Check existing positions
            await self._check_positions(current_candle, current_time)

            # Generate signal if no open position
            if not self.positions:
                if strategy_func:
                    # Use custom strategy
                    signal = strategy_func(historical_data, current_news)
                else:
                    # Use default AI strategy
                    signal = await self._generate_signal(
                        historical_data, current_news
                    )

                # Execute signal
                if signal and signal.get("action") in ["BUY", "STRONG_BUY", "SELL", "STRONG_SELL"]:
                    await self._execute_signal(signal, current_candle, current_time)

            # Record equity
            equity = self._calculate_equity(current_candle)
            self.equity_curve.append(
                {
                    "timestamp": current_time,
                    "equity": equity,
                    "balance": self.balance,
                    "open_positions": len(self.positions),
                }
            )

        # Close any remaining positions at last candle
        if self.positions:
            last_candle = candles_df.iloc[-1]
            last_time = candles_df.index[-1]
            for pos in self.positions[:]:
                await self._close_position(pos, last_candle["close"], last_time, "BACKTEST_END")

        logger.info(
            f"Backtest completed: {len(self.trades)} trades, "
            f"Final equity: ${self._calculate_equity(candles_df.iloc[-1]):,.2f}"
        )

        return {
            "trades": self.trades,
            "equity_curve": self.equity_curve,
            "final_balance": self.balance,
            "total_trades": len(self.trades),
        }

    async def _generate_signal(
        self, candles_df: pd.DataFrame, news_data: List[Dict]
    ) -> Optional[Dict]:
        """Generate trading signal using AI analysis"""
        try:
            # Need at least 200 candles for analysis
            if len(candles_df) < 200:
                return None

            # Technical analysis
            candles_list = candles_df.reset_index().to_dict("records")
            tech_result = self.tech_analyzer.calculate_all(candles_list)
            if not tech_result:
                return None

            # Sentiment analysis
            sentiment_result = self.sentiment_analyzer.analyze_news_batch(news_data)

            # Generate signal
            signal = self.signal_generator.generate_signal(
                symbol="BACKTEST",
                timeframe="1h",
                technical_analysis=tech_result,
                sentiment_analysis=sentiment_result,
            )

            return signal

        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return None

    async def _execute_signal(
        self, signal: Dict, candle: pd.Series, timestamp: datetime
    ):
        """Execute trading signal"""
        try:
            action = signal.get("action")
            suggested_actions = signal.get("suggested_actions", {})

            if action in ["BUY", "STRONG_BUY"]:
                side = "LONG"
            elif action in ["SELL", "STRONG_SELL"]:
                side = "SHORT"
            else:
                return

            # Calculate position size based on risk
            entry_price = candle["close"]
            stop_loss = suggested_actions.get("stop_loss", entry_price * 0.98)
            take_profit = suggested_actions.get("take_profit", entry_price * 1.04)

            # Calculate risk per unit
            if side == "LONG":
                risk_per_unit = entry_price - stop_loss
            else:
                risk_per_unit = stop_loss - entry_price

            if risk_per_unit <= 0:
                return

            # Calculate position size
            max_risk_amount = self.balance * self.max_risk_per_trade
            quantity = max_risk_amount / risk_per_unit

            # Apply trading fee
            position_value = quantity * entry_price
            fee = position_value * self.trading_fee

            if position_value + fee > self.balance:
                logger.warning("Insufficient balance for trade")
                return

            # Deduct fee from balance
            self.balance -= fee

            # Create position
            position = {
                "side": side,
                "entry_price": entry_price,
                "quantity": quantity,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "entry_time": timestamp,
                "entry_fee": fee,
            }

            self.positions.append(position)

            logger.debug(
                f"Opened {side} position @ ${entry_price:,.2f}, "
                f"Qty: {quantity:.6f}, Fee: ${fee:.2f}"
            )

        except Exception as e:
            logger.error(f"Error executing signal: {e}")

    async def _check_positions(self, candle: pd.Series, timestamp: datetime):
        """Check if any positions hit stop-loss or take-profit"""
        positions_to_close = []

        for pos in self.positions:
            if pos["side"] == "LONG":
                # Check stop-loss
                if candle["low"] <= pos["stop_loss"]:
                    positions_to_close.append((pos, pos["stop_loss"], "STOP_LOSS"))
                # Check take-profit
                elif candle["high"] >= pos["take_profit"]:
                    positions_to_close.append((pos, pos["take_profit"], "TAKE_PROFIT"))
            else:  # SHORT
                # Check stop-loss
                if candle["high"] >= pos["stop_loss"]:
                    positions_to_close.append((pos, pos["stop_loss"], "STOP_LOSS"))
                # Check take-profit
                elif candle["low"] <= pos["take_profit"]:
                    positions_to_close.append((pos, pos["take_profit"], "TAKE_PROFIT"))

        # Close positions
        for pos, exit_price, reason in positions_to_close:
            await self._close_position(pos, exit_price, timestamp, reason)

    async def _close_position(
        self, position: Dict, exit_price: float, timestamp: datetime, reason: str
    ):
        """Close a position"""
        try:
            entry_price = position["entry_price"]
            quantity = position["quantity"]
            side = position["side"]

            # Calculate PnL
            if side == "LONG":
                pnl = (exit_price - entry_price) * quantity
            else:
                pnl = (entry_price - exit_price) * quantity

            # Apply trading fee
            exit_value = quantity * exit_price
            fee = exit_value * self.trading_fee
            pnl_after_fee = pnl - fee

            # Update balance
            self.balance += exit_value - fee

            # Record trade
            trade = {
                "side": side,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "quantity": quantity,
                "entry_time": position["entry_time"],
                "exit_time": timestamp,
                "pnl": pnl_after_fee,
                "pnl_percent": (pnl_after_fee / (entry_price * quantity)) * 100,
                "entry_fee": position.get("entry_fee", 0),
                "exit_fee": fee,
                "reason": reason,
            }

            self.trades.append(trade)

            # Remove from open positions
            if position in self.positions:
                self.positions.remove(position)

            logger.debug(
                f"Closed {side} position @ ${exit_price:,.2f}, "
                f"PnL: ${pnl_after_fee:+,.2f} ({trade['pnl_percent']:+.2f}%), "
                f"Reason: {reason}"
            )

        except Exception as e:
            logger.error(f"Error closing position: {e}")

    def _calculate_equity(self, current_candle: pd.Series) -> float:
        """Calculate total equity (balance + unrealized PnL)"""
        equity = self.balance

        for pos in self.positions:
            if pos["side"] == "LONG":
                unrealized_pnl = (current_candle["close"] - pos["entry_price"]) * pos["quantity"]
            else:
                unrealized_pnl = (pos["entry_price"] - current_candle["close"]) * pos["quantity"]

            equity += unrealized_pnl

        return equity
