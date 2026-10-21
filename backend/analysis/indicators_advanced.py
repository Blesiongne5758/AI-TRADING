"""
Advanced Technical Indicators
Ichimoku Cloud, Fibonacci Retracement, dan indikator advanced lainnya
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from loguru import logger


class AdvancedIndicators:
    """Advanced technical indicators untuk analisis mendalam"""

    def __init__(self):
        logger.info("📊 Advanced Indicators initialized")

    def calculate_ichimoku(
        self,
        df: pd.DataFrame,
        tenkan_period: int = 9,
        kijun_period: int = 26,
        senkou_b_period: int = 52,
        displacement: int = 26
    ) -> Dict:
        """
        Calculate Ichimoku Cloud (Ichimoku Kinko Hyo)
        
        Components:
        - Tenkan-sen (Conversion Line): (Highest High + Lowest Low) / 2 for tenkan_period
        - Kijun-sen (Base Line): (Highest High + Lowest Low) / 2 for kijun_period
        - Senkou Span A (Leading Span A): (Tenkan + Kijun) / 2, displaced forward
        - Senkou Span B (Leading Span B): (Highest High + Lowest Low) / 2 for senkou_b_period, displaced forward
        - Chikou Span (Lagging Span): Close price displaced backward
        
        Args:
            df: DataFrame dengan kolom 'high', 'low', 'close'
            tenkan_period: Periode Tenkan-sen (default: 9)
            kijun_period: Periode Kijun-sen (default: 26)
            senkou_b_period: Periode Senkou Span B (default: 52)
            displacement: Displacement untuk Senkou spans (default: 26)
            
        Returns:
            Dictionary dengan semua Ichimoku components
        """
        try:
            # Tenkan-sen (Conversion Line)
            tenkan_sen = (
                df['high'].rolling(window=tenkan_period).max() +
                df['low'].rolling(window=tenkan_period).min()
            ) / 2

            # Kijun-sen (Base Line)
            kijun_sen = (
                df['high'].rolling(window=kijun_period).max() +
                df['low'].rolling(window=kijun_period).min()
            ) / 2

            # Senkou Span A (Leading Span A)
            senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(displacement)

            # Senkou Span B (Leading Span B)
            senkou_span_b = (
                (df['high'].rolling(window=senkou_b_period).max() +
                 df['low'].rolling(window=senkou_b_period).min()) / 2
            ).shift(displacement)

            # Chikou Span (Lagging Span)
            chikou_span = df['close'].shift(-displacement)

            # Current values
            current_price = df['close'].iloc[-1]
            current_tenkan = tenkan_sen.iloc[-1]
            current_kijun = kijun_sen.iloc[-1]
            current_senkou_a = senkou_span_a.iloc[-1]
            current_senkou_b = senkou_span_b.iloc[-1]

            # Determine cloud color (bullish or bearish)
            cloud_bullish = current_senkou_a > current_senkou_b

            # Determine price position relative to cloud
            if current_price > current_senkou_a and current_price > current_senkou_b:
                price_position = "ABOVE_CLOUD"
                signal = "BULLISH"
            elif current_price < current_senkou_a and current_price < current_senkou_b:
                price_position = "BELOW_CLOUD"
                signal = "BEARISH"
            else:
                price_position = "INSIDE_CLOUD"
                signal = "NEUTRAL"

            # Determine TK cross (Tenkan-Kijun cross)
            if current_tenkan > current_kijun:
                tk_cross = "BULLISH"
            elif current_tenkan < current_kijun:
                tk_cross = "BEARISH"
            else:
                tk_cross = "NEUTRAL"

            return {
                "tenkan_sen": current_tenkan,
                "kijun_sen": current_kijun,
                "senkou_span_a": current_senkou_a,
                "senkou_span_b": current_senkou_b,
                "chikou_span": chikou_span.iloc[-1] if not pd.isna(chikou_span.iloc[-1]) else None,
                "cloud_bullish": cloud_bullish,
                "price_position": price_position,
                "signal": signal,
                "tk_cross": tk_cross,
                "score": self._ichimoku_score(price_position, tk_cross, cloud_bullish)
            }

        except Exception as e:
            logger.error(f"Error calculating Ichimoku: {e}")
            return {"signal": "NEUTRAL", "score": 0}

    def _ichimoku_score(self, price_position: str, tk_cross: str, cloud_bullish: bool) -> int:
        """Calculate Ichimoku score (-100 to +100)"""
        score = 0

        # Price position (40 points)
        if price_position == "ABOVE_CLOUD":
            score += 40
        elif price_position == "BELOW_CLOUD":
            score -= 40

        # TK cross (30 points)
        if tk_cross == "BULLISH":
            score += 30
        elif tk_cross == "BEARISH":
            score -= 30

        # Cloud color (30 points)
        if cloud_bullish:
            score += 30
        else:
            score -= 30

        return score

    def calculate_fibonacci_retracement(
        self,
        df: pd.DataFrame,
        lookback_period: int = 100
    ) -> Dict:
        """
        Calculate Fibonacci Retracement levels
        
        Levels: 0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%
        
        Args:
            df: DataFrame dengan kolom 'high', 'low', 'close'
            lookback_period: Period untuk find swing high/low
            
        Returns:
            Dictionary dengan Fibonacci levels dan analysis
        """
        try:
            # Find swing high and low
            recent_data = df.tail(lookback_period)
            swing_high = recent_data['high'].max()
            swing_low = recent_data['low'].min()

            # Calculate Fibonacci levels
            diff = swing_high - swing_low

            fib_levels = {
                "0.0%": swing_high,
                "23.6%": swing_high - (diff * 0.236),
                "38.2%": swing_high - (diff * 0.382),
                "50.0%": swing_high - (diff * 0.500),
                "61.8%": swing_high - (diff * 0.618),
                "78.6%": swing_high - (diff * 0.786),
                "100.0%": swing_low
            }

            # Current price
            current_price = df['close'].iloc[-1]

            # Determine position relative to Fibonacci levels
            if current_price > fib_levels["23.6%"]:
                position = "ABOVE_23.6"
                signal = "BULLISH"
            elif current_price > fib_levels["38.2%"]:
                position = "BETWEEN_23.6_38.2"
                signal = "NEUTRAL"
            elif current_price > fib_levels["50.0%"]:
                position = "BETWEEN_38.2_50.0"
                signal = "NEUTRAL"
            elif current_price > fib_levels["61.8%"]:
                position = "BETWEEN_50.0_61.8"
                signal = "BEARISH"
            else:
                position = "BELOW_61.8"
                signal = "BEARISH"

            # Find nearest Fibonacci level
            distances = {level: abs(current_price - price) for level, price in fib_levels.items()}
            nearest_level = min(distances, key=distances.get)

            return {
                "swing_high": swing_high,
                "swing_low": swing_low,
                "fib_levels": fib_levels,
                "current_price": current_price,
                "position": position,
                "signal": signal,
                "nearest_level": nearest_level,
                "distance_to_nearest": distances[nearest_level],
                "score": self._fibonacci_score(position)
            }

        except Exception as e:
            logger.error(f"Error calculating Fibonacci: {e}")
            return {"signal": "NEUTRAL", "score": 0}

    def _fibonacci_score(self, position: str) -> int:
        """Calculate Fibonacci score (-100 to +100)"""
        if position == "ABOVE_23.6":
            return 60
        elif position == "BETWEEN_23.6_38.2":
            return 30
        elif position == "BETWEEN_38.2_50.0":
            return 0
        elif position == "BETWEEN_50.0_61.8":
            return -30
        else:  # BELOW_61.8
            return -60

    def calculate_pivot_points(self, df: pd.DataFrame) -> Dict:
        """
        Calculate Pivot Points (Classic)
        
        Pivot Point = (High + Low + Close) / 3
        Resistance 1 = (2 * Pivot) - Low
        Support 1 = (2 * Pivot) - High
        Resistance 2 = Pivot + (High - Low)
        Support 2 = Pivot - (High - Low)
        
        Args:
            df: DataFrame dengan kolom 'high', 'low', 'close'
            
        Returns:
            Dictionary dengan pivot points dan analysis
        """
        try:
            # Use previous day's data
            prev_high = df['high'].iloc[-2]
            prev_low = df['low'].iloc[-2]
            prev_close = df['close'].iloc[-2]

            # Calculate Pivot Point
            pivot = (prev_high + prev_low + prev_close) / 3

            # Calculate support and resistance levels
            r1 = (2 * pivot) - prev_low
            s1 = (2 * pivot) - prev_high

            r2 = pivot + (prev_high - prev_low)
            s2 = pivot - (prev_high - prev_low)

            r3 = prev_high + 2 * (pivot - prev_low)
            s3 = prev_low - 2 * (prev_high - pivot)

            # Current price
            current_price = df['close'].iloc[-1]

            # Determine position
            if current_price > r2:
                position = "ABOVE_R2"
                signal = "VERY_BULLISH"
            elif current_price > r1:
                position = "BETWEEN_R1_R2"
                signal = "BULLISH"
            elif current_price > pivot:
                position = "BETWEEN_PIVOT_R1"
                signal = "SLIGHTLY_BULLISH"
            elif current_price > s1:
                position = "BETWEEN_S1_PIVOT"
                signal = "SLIGHTLY_BEARISH"
            elif current_price > s2:
                position = "BETWEEN_S2_S1"
                signal = "BEARISH"
            else:
                position = "BELOW_S2"
                signal = "VERY_BEARISH"

            return {
                "pivot": pivot,
                "r1": r1,
                "r2": r2,
                "r3": r3,
                "s1": s1,
                "s2": s2,
                "s3": s3,
                "current_price": current_price,
                "position": position,
                "signal": signal,
                "score": self._pivot_score(position)
            }

        except Exception as e:
            logger.error(f"Error calculating Pivot Points: {e}")
            return {"signal": "NEUTRAL", "score": 0}

    def _pivot_score(self, position: str) -> int:
        """Calculate Pivot Points score (-100 to +100)"""
        scores = {
            "ABOVE_R2": 80,
            "BETWEEN_R1_R2": 50,
            "BETWEEN_PIVOT_R1": 20,
            "BETWEEN_S1_PIVOT": -20,
            "BETWEEN_S2_S1": -50,
            "BELOW_S2": -80
        }
        return scores.get(position, 0)

    def calculate_vwap(self, df: pd.DataFrame) -> Dict:
        """
        Calculate Volume Weighted Average Price (VWAP)
        
        VWAP = Cumulative(Price * Volume) / Cumulative(Volume)
        
        Args:
            df: DataFrame dengan kolom 'high', 'low', 'close', 'volume'
            
        Returns:
            Dictionary dengan VWAP dan analysis
        """
        try:
            # Calculate typical price
            typical_price = (df['high'] + df['low'] + df['close']) / 3

            # Calculate cumulative values
            cumulative_tp_volume = (typical_price * df['volume']).cumsum()
            cumulative_volume = df['volume'].cumsum()

            # Calculate VWAP
            vwap = cumulative_tp_volume / cumulative_volume

            current_vwap = vwap.iloc[-1]
            current_price = df['close'].iloc[-1]

            # Determine signal
            if current_price > current_vwap * 1.02:
                signal = "BULLISH"
                score = 40
            elif current_price < current_vwap * 0.98:
                signal = "BEARISH"
                score = -40
            else:
                signal = "NEUTRAL"
                score = 0

            return {
                "vwap": current_vwap,
                "current_price": current_price,
                "price_vs_vwap": ((current_price - current_vwap) / current_vwap) * 100,
                "signal": signal,
                "score": score
            }

        except Exception as e:
            logger.error(f"Error calculating VWAP: {e}")
            return {"signal": "NEUTRAL", "score": 0}

    def calculate_atr_trailing_stop(
        self,
        df: pd.DataFrame,
        atr_period: int = 14,
        multiplier: float = 2.0
    ) -> Dict:
        """
        Calculate ATR-based Trailing Stop
        
        ATR = Average True Range (volatility measure)
        Trailing Stop = Price - (ATR * multiplier)
        
        Args:
            df: DataFrame dengan kolom 'high', 'low', 'close'
            atr_period: ATR period (default: 14)
            multiplier: ATR multiplier (default: 2.0)
            
        Returns:
            Dictionary dengan trailing stop dan analysis
        """
        try:
            # Calculate ATR
            high_low = df['high'] - df['low']
            high_close = np.abs(df['high'] - df['close'].shift())
            low_close = np.abs(df['low'] - df['close'].shift())

            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = np.max(ranges, axis=1)

            atr = true_range.rolling(window=atr_period).mean()

            # Calculate trailing stop
            current_price = df['close'].iloc[-1]
            current_atr = atr.iloc[-1]

            # For long positions
            trailing_stop_long = current_price - (current_atr * multiplier)

            # For short positions
            trailing_stop_short = current_price + (current_atr * multiplier)

            # Determine trend
            if current_price > df['close'].shift(1).iloc[-1]:
                trend = "UPTREND"
                recommended_stop = trailing_stop_long
            else:
                trend = "DOWNTREND"
                recommended_stop = trailing_stop_short

            return {
                "atr": current_atr,
                "trailing_stop_long": trailing_stop_long,
                "trailing_stop_short": trailing_stop_short,
                "recommended_stop": recommended_stop,
                "trend": trend,
                "distance_percent": abs(current_price - recommended_stop) / current_price * 100
            }

        except Exception as e:
            logger.error(f"Error calculating ATR Trailing Stop: {e}")
            return {"trend": "UNKNOWN", "recommended_stop": 0}

    def calculate_all(self, df: pd.DataFrame) -> Dict:
        """
        Calculate semua advanced indicators
        
        Args:
            df: DataFrame dengan OHLCV data
            
        Returns:
            Dictionary dengan semua advanced indicators
        """
        logger.info("📊 Calculating advanced indicators...")

        results = {
            "ichimoku": self.calculate_ichimoku(df),
            "fibonacci": self.calculate_fibonacci_retracement(df),
            "pivot_points": self.calculate_pivot_points(df),
            "vwap": self.calculate_vwap(df),
            "atr_trailing_stop": self.calculate_atr_trailing_stop(df)
        }

        # Calculate overall score
        scores = [
            results["ichimoku"]["score"],
            results["fibonacci"]["score"],
            results["pivot_points"]["score"],
            results["vwap"]["score"]
        ]

        overall_score = sum(scores) / len(scores)

        if overall_score > 40:
            overall_signal = "STRONG_BULLISH"
        elif overall_score > 10:
            overall_signal = "BULLISH"
        elif overall_score > -10:
            overall_signal = "NEUTRAL"
        elif overall_score > -40:
            overall_signal = "BEARISH"
        else:
            overall_signal = "STRONG_BEARISH"

        results["overall"] = {
            "score": overall_score,
            "signal": overall_signal
        }

        logger.info(f"✅ Advanced indicators calculated: {overall_signal} (score: {overall_score:.1f})")

        return results
