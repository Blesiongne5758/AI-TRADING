"""
Advanced Technical Indicators
Ichimoku Cloud, Fibonacci Retracement, dan indikator advanced lainnya
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from loguru import logger


class AdvancedIndicators:
    """
    Advanced technical indicators
    
    Features:
    - Ichimoku Cloud (complete system)
    - Fibonacci Retracement levels
    - Pivot Points
    - VWAP (Volume Weighted Average Price)
    - ATR Trailing Stop
    """
    
    def __init__(self):
        """Initialize advanced indicators"""
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
        
        Args:
            df: DataFrame with OHLC data
            tenkan_period: Tenkan-sen period (default 9)
            kijun_period: Kijun-sen period (default 26)
            senkou_b_period: Senkou Span B period (default 52)
            displacement: Cloud displacement (default 26)
            
        Returns:
            Dictionary with Ichimoku components
        """
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
        
        # Determine cloud color
        cloud_bullish = current_senkou_a > current_senkou_b
        
        # Determine price position
        if current_price > current_senkou_a and current_price > current_senkou_b:
            price_position = "ABOVE_CLOUD"
            signal = "BULLISH"
        elif current_price < current_senkou_a and current_price < current_senkou_b:
            price_position = "BELOW_CLOUD"
            signal = "BEARISH"
        else:
            price_position = "INSIDE_CLOUD"
            signal = "NEUTRAL"
        
        # Determine TK cross
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
        
        Args:
            df: DataFrame with OHLC data
            lookback_period: Period to find swing high/low
            
        Returns:
            Dictionary with Fibonacci levels
        """
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
    
    def calculate_pivot_points(
        self,
        df: pd.DataFrame
    ) -> Dict:
        """
        Calculate Pivot Points (Classic)
        
        Args:
            df: DataFrame with OHLC data
            
        Returns:
            Dictionary with pivot points
        """
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
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Dictionary with VWAP data
        """
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
    
    def calculate_atr_trailing_stop(
        self,
        df: pd.DataFrame,
        atr_period: int = 14,
        multiplier: float = 2.0
    ) -> Dict:
        """
        Calculate ATR-based Trailing Stop
        
        Args:
            df: DataFrame with OHLC data
            atr_period: ATR period
            multiplier: ATR multiplier
            
        Returns:
            Dictionary with trailing stop data
        """
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
    
    def calculate_all(self, df: pd.DataFrame) -> Dict:
        """
        Calculate all advanced indicators
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Dictionary with all advanced indicators
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


# === USAGE EXAMPLE ===

def example_usage():
    """Example how to use AdvancedIndicators"""
    import pandas as pd
    import numpy as np
    
    # Create sample data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=200, freq='h')
    
    # Simulate price data
    base_price = 50000
    prices = [base_price + np.random.normal(0, 100) for _ in range(200)]
    
    df = pd.DataFrame({
        "timestamp": dates,
        "open": prices,
        "high": [p * 1.01 for p in prices],
        "low": [p * 0.99 for p in prices],
        "close": prices,
        "volume": [1000 + np.random.normal(0, 100) for _ in range(200)]
    })
    
    # Calculate advanced indicators
    indicators = AdvancedIndicators()
    results = indicators.calculate_all(df)
    
    print("\n📊 Advanced Indicators:")
    print(f"\n   Ichimoku Cloud:")
    print(f"     Signal: {results['ichimoku']['signal']}")
    print(f"     Score: {results['ichimoku']['score']}")
    print(f"     Price Position: {results['ichimoku']['price_position']}")
    
    print(f"\n   Fibonacci Retracement:")
    print(f"     Signal: {results['fibonacci']['signal']}")
    print(f"     Score: {results['fibonacci']['score']}")
    print(f"     Position: {results['fibonacci']['position']}")
    print(f"     Nearest Level: {results['fibonacci']['nearest_level']}")
    
    print(f"\n   Pivot Points:")
    print(f"     Signal: {results['pivot_points']['signal']}")
    print(f"     Score: {results['pivot_points']['score']}")
    print(f"     Position: {results['pivot_points']['position']}")
    
    print(f"\n   VWAP:")
    print(f"     Signal: {results['vwap']['signal']}")
    print(f"     Price vs VWAP: {results['vwap']['price_vs_vwap']:+.2f}%")
    
    print(f"\n   ATR Trailing Stop:")
    print(f"     Trend: {results['atr_trailing_stop']['trend']}")
    print(f"     Recommended Stop: ${results['atr_trailing_stop']['recommended_stop']:,.2f}")
    print(f"     Distance: {results['atr_trailing_stop']['distance_percent']:.2f}%")
    
    print(f"\n   Overall:")
    print(f"     Signal: {results['overall']['signal']}")
    print(f"     Score: {results['overall']['score']:.1f}")


if __name__ == "__main__":
    example_usage()
