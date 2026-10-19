"""
Technical Indicators Calculator
Menghitung indikator teknikal dari data candlestick (OHLCV)
"""
import pandas as pd
import pandas_ta as ta
from typing import Dict, List, Optional
from loguru import logger


class TechnicalAnalyzer:
    """Menghitung dan menginterpretasi indikator teknikal"""

    def __init__(self):
        # Parameter indikator (bisa disesuaikan per strategi)
        self.params = {
            "rsi_period": 14,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
            "ema_short": 20,
            "ema_medium": 50,
            "ema_long": 200,
            "bb_period": 20,
            "bb_std": 2,
        }

    def calculate_all(self, candles: List[Dict]) -> Optional[Dict]:
        """
        Menghitung SEMUA indikator teknikal dari data candle
        
        Args:
            candles: List of OHLCV dictionaries dari database
            
        Returns:
            Dictionary berisi semua indikator + interpretasi, atau None jika data tidak cukup
        """
        if len(candles) < self.params["ema_long"]:
            logger.warning(
                f"⚠️  Data tidak cukup: {len(candles)} candles, "
                f"butuh minimal {self.params['ema_long']} untuk EMA 200"
            )
            return None

        # Konversi ke DataFrame
        df = pd.DataFrame(candles)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Hitung semua indikator
        indicators = self._calculate_indicators(df)
        
        # Interpretasi setiap indikator
        interpretation = self._interpret_indicators(indicators, df)

        return {
            "indicators": indicators,
            "interpretation": interpretation,
            "latest_price": float(df["close"].iloc[-1]),
            "timestamp": df.index[-1].isoformat(),
        }

    def _calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """Menghitung semua indikator teknikal"""
        p = self.params
        result = {}

        # 1. RSI (Relative Strength Index)
        rsi = ta.rsi(df["close"], length=p["rsi_period"])
        result["rsi"] = {
            "value": float(rsi.iloc[-1]),
            "period": p["rsi_period"],
        }

        # 2. MACD (Moving Average Convergence Divergence)
        macd = ta.macd(
            df["close"],
            fast=p["macd_fast"],
            slow=p["macd_slow"],
            signal=p["macd_signal"],
        )
        result["macd"] = {
            "macd": float(macd.iloc[-1, 0]),
            "histogram": float(macd.iloc[-1, 1]),
            "signal": float(macd.iloc[-1, 2]),
            "params": f"{p['macd_fast']},{p['macd_slow']},{p['macd_signal']}",
        }

        # 3. EMA (Exponential Moving Average) - 3 periode
        ema_short = ta.ema(df["close"], length=p["ema_short"])
        ema_medium = ta.ema(df["close"], length=p["ema_medium"])
        ema_long = ta.ema(df["close"], length=p["ema_long"])

        result["ema"] = {
            "ema_20": float(ema_short.iloc[-1]),
            "ema_50": float(ema_medium.iloc[-1]),
            "ema_200": float(ema_long.iloc[-1]),
        }

        # 4. Bollinger Bands
        bb = ta.bbands(df["close"], length=p["bb_period"], std=p["bb_std"])
        result["bollinger"] = {
            "upper": float(bb.iloc[-1, 0]),
            "middle": float(bb.iloc[-1, 1]),
            "lower": float(bb.iloc[-1, 2]),
            "bandwidth": float(
                (bb.iloc[-1, 0] - bb.iloc[-1, 2]) / bb.iloc[-1, 1] * 100
            ),
            "params": f"{p['bb_period']},{p['bb_std']}",
        }

        # 5. Volume Analysis
        volume_sma = ta.sma(df["volume"], length=20)
        current_volume = float(df["volume"].iloc[-1])
        avg_volume = float(volume_sma.iloc[-1])

        result["volume"] = {
            "current": current_volume,
            "average_20": avg_volume,
            "ratio": current_volume / avg_volume if avg_volume > 0 else 0,
        }

        # 6. ATR (Average True Range) - untuk volatility & stop-loss
        atr = ta.atr(df["high"], df["low"], df["close"], length=14)
        result["atr"] = {
            "value": float(atr.iloc[-1]),
            "atr_percent": float(atr.iloc[-1] / df["close"].iloc[-1] * 100),
        }

        return result

    def _interpret_indicators(self, indicators: Dict, df: pd.DataFrame) -> Dict:
        """
        Menginterpretasi setiap indikator menjadi sinyal bullish/bearish
        Return: Dict dengan skor per indikator (-100 sampai +100)
        """
        interpretation = {}
        price = float(df["close"].iloc[-1])

        # === RSI ===
        rsi = indicators["rsi"]["value"]
        if rsi < 30:
            interpretation["rsi"] = {
                "signal": "OVERSOLD",
                "score": 80,  # Bullish
                "reason": f"RSI {rsi:.1f} < 30 → potensi rebound",
            }
        elif rsi > 70:
            interpretation["rsi"] = {
                "signal": "OVERBOUGHT",
                "score": -80,  # Bearish
                "reason": f"RSI {rsi:.1f} > 70 → potensi koreksi",
            }
        elif rsi < 45:
            interpretation["rsi"] = {
                "signal": "WEAK",
                "score": 20,
                "reason": f"RSI {rsi:.1f} → momentum lemah",
            }
        elif rsi > 55:
            interpretation["rsi"] = {
                "signal": "STRONG",
                "score": -20,
                "reason": f"RSI {rsi:.1f} → momentum kuat tapi rawan jenuh",
            }
        else:
            interpretation["rsi"] = {
                "signal": "NEUTRAL",
                "score": 0,
                "reason": f"RSI {rsi:.1f} → netral",
            }

        # === MACD ===
        macd_hist = indicators["macd"]["histogram"]
        macd_line = indicators["macd"]["macd"]
        macd_signal = indicators["macd"]["signal"]
        prev_hist = float(
            ta.macd(
                df["close"],
                fast=self.params["macd_fast"],
                slow=self.params["macd_slow"],
                signal=self.params["macd_signal"],
            ).iloc[-2, 1]
        )

        if macd_hist > 0 and prev_hist <= 0:
            interpretation["macd"] = {
                "signal": "BULLISH_CROSSOVER",
                "score": 90,
                "reason": "MACD histogram baru crossover ke positif → sinyal beli kuat",
            }
        elif macd_hist < 0 and prev_hist >= 0:
            interpretation["macd"] = {
                "signal": "BEARISH_CROSSOVER",
                "score": -90,
                "reason": "MACD histogram baru crossover ke negatif → sinyal jual kuat",
            }
        elif macd_hist > 0:
            interpretation["macd"] = {
                "signal": "BULLISH",
                "score": 40,
                "reason": "MACD histogram positif → tren naik",
            }
        else:
            interpretation["macd"] = {
                "signal": "BEARISH",
                "score": -40,
                "reason": "MACD histogram negatif → tren turun",
            }

        # === EMA TREND ===
        ema20 = indicators["ema"]["ema_20"]
        ema50 = indicators["ema"]["ema_50"]
        ema200 = indicators["ema"]["ema_200"]

        if price > ema20 > ema50 > ema200:
            interpretation["ema"] = {
                "signal": "STRONG_UPTREND",
                "score": 85,
                "reason": "Harga > EMA20 > EMA50 > EMA200 → uptrend kuat",
            }
        elif price < ema20 < ema50 < ema200:
            interpretation["ema"] = {
                "signal": "STRONG_DOWNTREND",
                "score": -85,
                "reason": "Harga < EMA20 < EMA50 < EMA200 → downtrend kuat",
            }
        elif price > ema200:
            interpretation["ema"] = {
                "signal": "UPTREND",
                "score": 40,
                "reason": "Harga di atas EMA200 → tren jangka panjang naik",
            }
        else:
            interpretation["ema"] = {
                "signal": "DOWNTREND",
                "score": -40,
                "reason": "Harga di bawah EMA200 → tren jangka panjang turun",
            }

        # === BOLLINGER BANDS ===
        bb_upper = indicators["bollinger"]["upper"]
        bb_lower = indicators["bollinger"]["lower"]
        bb_middle = indicators["bollinger"]["middle"]

        if price <= bb_lower:
            interpretation["bollinger"] = {
                "signal": "OVERSOLD",
                "score": 70,
                "reason": f"Harga ({price:.2f}) menyentuh lower band → potensi bounce",
            }
        elif price >= bb_upper:
            interpretation["bollinger"] = {
                "signal": "OVERBOUGHT",
                "score": -70,
                "reason": f"Harga ({price:.2f}) menyentuh upper band → potensi pullback",
            }
        elif price < bb_middle:
            interpretation["bollinger"] = {
                "signal": "BEARISH",
                "score": -20,
                "reason": "Harga di bawah middle band → tekanan jual",
            }
        else:
            interpretation["bollinger"] = {
                "signal": "BULLISH",
                "score": 20,
                "reason": "Harga di atas middle band → tekanan beli",
            }

        # === VOLUME ===
        vol_ratio = indicators["volume"]["ratio"]
        if vol_ratio > 2.0:
            interpretation["volume"] = {
                "signal": "VERY_HIGH",
                "score": 50,  # Netral tapi konfirmasi kuat
                "reason": f"Volume {vol_ratio:.1f}x rata-rata → konfirmasi sinyal kuat",
            }
        elif vol_ratio > 1.5:
            interpretation["volume"] = {
                "signal": "HIGH",
                "score": 30,
                "reason": f"Volume {vol_ratio:.1f}x rata-rata → aktivitas tinggi",
            }
        elif vol_ratio < 0.5:
            interpretation["volume"] = {
                "signal": "LOW",
                "score": -30,
                "reason": f"Volume {vol_ratio:.1f}x rata-rata → sinyal lemah",
            }
        else:
            interpretation["volume"] = {
                "signal": "NORMAL",
                "score": 0,
                "reason": f"Volume {vol_ratio:.1f}x rata-rata → normal",
            }

        return interpretation

    def get_suggested_stop_loss(
        self, price: float, atr: float, direction: str
    ) -> Dict:
        """
        Menghitung suggested stop-loss berdasarkan ATR
        direction: 'long' atau 'short'
        """
        multiplier = 2.0  # 2x ATR untuk stop-loss
        sl_distance = atr * multiplier

        if direction == "long":
            stop_loss = price - sl_distance
        else:
            stop_loss = price + sl_distance

        return {
            "stop_loss": stop_loss,
            "distance": sl_distance,
            "distance_percent": (sl_distance / price) * 100,
            "atr_multiplier": multiplier,
        }
