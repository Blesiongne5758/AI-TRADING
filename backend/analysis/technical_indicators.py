"""
Technical Indicators Calculator
Menghitung RSI, MACD, EMA, Bollinger Bands, dan Volume Analysis

Dependencies:
    - pandas: Data manipulation
    - ta: Technical analysis library (lebih simple dari TA-Lib)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from loguru import logger


class TechnicalIndicators:
    """
    Menghitung indikator teknikal dari data candlestick
    
    Contoh penggunaan:
        ti = TechnicalIndicators()
        indicators = ti.calculate_all(candles_df)
        print(indicators['rsi'])  # 65.5
        print(indicators['signal'])  # 'BUY'
    """
    
    def __init__(self):
        """Initialize technical indicators calculator"""
        pass
    
    def calculate_all(self, df: pd.DataFrame) -> Dict:
        """
        Hitung semua indikator teknikal
        
        Args:
            df: DataFrame dengan kolom [timestamp, open, high, low, close, volume]
        
        Returns:
            Dictionary dengan semua indikator dan signal
        
        Example:
            {
                'rsi': 65.5,
                'rsi_signal': 'NEUTRAL',
                'macd': 125.5,
                'macd_signal': 'BUY',
                'ema_20': 42500.0,
                'ema_50': 42000.0,
                'ema_200': 40000.0,
                'bb_upper': 43000.0,
                'bb_middle': 42500.0,
                'bb_lower': 42000.0,
                'volume_ratio': 1.5,
                'signal': 'BUY',
                'confidence': 75
            }
        """
        if len(df) < 200:
            logger.warning(f"Data terlalu sedikit ({len(df)} candles), butuh minimal 200")
            return self._empty_indicators()
        
        try:
            # Hitung semua indikator
            rsi = self._calculate_rsi(df)
            macd = self._calculate_macd(df)
            ema = self._calculate_ema(df)
            bb = self._calculate_bollinger_bands(df)
            volume = self._calculate_volume_analysis(df)
            
            # Gabungkan semua hasil
            indicators = {
                **rsi,
                **macd,
                **ema,
                **bb,
                **volume,
            }
            
            # Generate signal dari semua indikator
            signal, confidence = self._generate_signal(indicators)
            indicators['signal'] = signal
            indicators['confidence'] = confidence
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return self._empty_indicators()
    
    def _calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> Dict:
        """
        Hitung RSI (Relative Strength Index)
        
        RSI mengukur kecepatan dan perubahan pergerakan harga
        - RSI > 70: Overbought (potensi turun)
        - RSI < 30: Oversold (potensi naik)
        - RSI 30-70: Netral
        
        Args:
            df: DataFrame dengan kolom 'close'
            period: Periode RSI (default 14)
        
        Returns:
            Dictionary dengan rsi value dan signal
        """
        try:
            # Hitung RSI manual (lebih reliable dari library)
            delta = df['close'].diff()
            
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            rsi_value = rsi.iloc[-1]
            
            # Tentukan signal
            if rsi_value > 70:
                rsi_signal = 'SELL'  # Overbought
            elif rsi_value < 30:
                rsi_signal = 'BUY'  # Oversold
            else:
                rsi_signal = 'NEUTRAL'
            
            return {
                'rsi': round(rsi_value, 2),
                'rsi_signal': rsi_signal,
            }
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return {'rsi': 50.0, 'rsi_signal': 'NEUTRAL'}
    
    def _calculate_macd(self, df: pd.DataFrame, 
                        fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """
        Hitung MACD (Moving Average Convergence Divergence)
        
        MACD mengukur momentum dan trend
        - MACD > Signal Line: Bullish (potensi naik)
        - MACD < Signal Line: Bearish (potensi turun)
        
        Args:
            df: DataFrame dengan kolom 'close'
            fast: Periode EMA cepat (default 12)
            slow: Periode EMA lambat (default 26)
            signal: Periode signal line (default 9)
        
        Returns:
            Dictionary dengan macd value dan signal
        """
        try:
            # Hitung EMA
            ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
            ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
            
            # MACD line
            macd_line = ema_fast - ema_slow
            
            # Signal line
            signal_line = macd_line.ewm(span=signal, adjust=False).mean()
            
            # Histogram
            histogram = macd_line - signal_line
            
            macd_value = macd_line.iloc[-1]
            signal_value = signal_line.iloc[-1]
            histogram_value = histogram.iloc[-1]
            
            # Tentukan signal
            if macd_value > signal_value and histogram_value > 0:
                macd_signal = 'BUY'
            elif macd_value < signal_value and histogram_value < 0:
                macd_signal = 'SELL'
            else:
                macd_signal = 'NEUTRAL'
            
            return {
                'macd': round(macd_value, 2),
                'macd_signal_line': round(signal_value, 2),
                'macd_histogram': round(histogram_value, 2),
                'macd_signal': macd_signal,
            }
            
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return {'macd': 0.0, 'macd_signal_line': 0.0, 'macd_histogram': 0.0, 'macd_signal': 'NEUTRAL'}
    
    def _calculate_ema(self, df: pd.DataFrame) -> Dict:
        """
        Hitung EMA (Exponential Moving Average)
        
        EMA memberikan weight lebih besar pada data terbaru
        - Price > EMA 20 > EMA 50 > EMA 200: Strong uptrend
        - Price < EMA 20 < EMA 50 < EMA 200: Strong downtrend
        
        Args:
            df: DataFrame dengan kolom 'close'
        
        Returns:
            Dictionary dengan EMA values dan signal
        """
        try:
            # Hitung EMA untuk berbagai periode
            ema_20 = df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
            ema_50 = df['close'].ewm(span=50, adjust=False).mean().iloc[-1]
            ema_200 = df['close'].ewm(span=200, adjust=False).mean().iloc[-1]
            
            current_price = df['close'].iloc[-1]
            
            # Tentukan signal berdasarkan alignment
            if current_price > ema_20 > ema_50 > ema_200:
                ema_signal = 'BUY'  # Strong uptrend
            elif current_price < ema_20 < ema_50 < ema_200:
                ema_signal = 'SELL'  # Strong downtrend
            else:
                ema_signal = 'NEUTRAL'
            
            return {
                'ema_20': round(ema_20, 2),
                'ema_50': round(ema_50, 2),
                'ema_200': round(ema_200, 2),
                'ema_signal': ema_signal,
            }
            
        except Exception as e:
            logger.error(f"Error calculating EMA: {e}")
            return {'ema_20': 0.0, 'ema_50': 0.0, 'ema_200': 0.0, 'ema_signal': 'NEUTRAL'}
    
    def _calculate_bollinger_bands(self, df: pd.DataFrame, 
                                    period: int = 20, std_dev: int = 2) -> Dict:
        """
        Hitung Bollinger Bands
        
        Bollinger Bands mengukur volatilitas
        - Price dekat upper band: Overbought
        - Price dekat lower band: Oversold
        - Bands menyempit: Low volatility (potensi breakout)
        
        Args:
            df: DataFrame dengan kolom 'close'
            period: Periode SMA (default 20)
            std_dev: Standard deviation multiplier (default 2)
        
        Returns:
            Dictionary dengan BB values dan signal
        """
        try:
            # Hitung middle band (SMA)
            middle = df['close'].rolling(window=period).mean()
            
            # Hitung standard deviation
            std = df['close'].rolling(window=period).std()
            
            # Hitung upper dan lower bands
            upper = middle + (std * std_dev)
            lower = middle - (std * std_dev)
            
            bb_upper = upper.iloc[-1]
            bb_middle = middle.iloc[-1]
            bb_lower = lower.iloc[-1]
            
            current_price = df['close'].iloc[-1]
            
            # Tentukan signal
            if current_price > bb_upper:
                bb_signal = 'SELL'  # Overbought
            elif current_price < bb_lower:
                bb_signal = 'BUY'  # Oversold
            else:
                bb_signal = 'NEUTRAL'
            
            # Hitung bandwidth (volatilitas)
            bandwidth = (bb_upper - bb_lower) / bb_middle * 100
            
            return {
                'bb_upper': round(bb_upper, 2),
                'bb_middle': round(bb_middle, 2),
                'bb_lower': round(bb_lower, 2),
                'bb_bandwidth': round(bandwidth, 2),
                'bb_signal': bb_signal,
            }
            
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return {'bb_upper': 0.0, 'bb_middle': 0.0, 'bb_lower': 0.0, 'bb_bandwidth': 0.0, 'bb_signal': 'NEUTRAL'}
    
    def _calculate_volume_analysis(self, df: pd.DataFrame, period: int = 20) -> Dict:
        """
        Analisis Volume
        
        Volume mengkonfirmasi strength dari pergerakan harga
        - Volume tinggi + price naik: Strong bullish
        - Volume tinggi + price turun: Strong bearish
        - Volume rendah: Weak movement
        
        Args:
            df: DataFrame dengan kolom 'volume' dan 'close'
            period: Periode untuk average volume (default 20)
        
        Returns:
            Dictionary dengan volume metrics dan signal
        """
        try:
            # Hitung average volume
            avg_volume = df['volume'].rolling(window=period).mean().iloc[-1]
            current_volume = df['volume'].iloc[-1]
            
            # Hitung volume ratio
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
            
            # Hitung price change
            price_change = df['close'].iloc[-1] - df['close'].iloc[-2]
            
            # Tentukan signal
            if volume_ratio > 1.5:  # Volume tinggi
                if price_change > 0:
                    volume_signal = 'BUY'  # Strong bullish
                else:
                    volume_signal = 'SELL'  # Strong bearish
            else:
                volume_signal = 'NEUTRAL'  # Volume rendah/normal
            
            return {
                'volume_current': round(current_volume, 2),
                'volume_avg': round(avg_volume, 2),
                'volume_ratio': round(volume_ratio, 2),
                'volume_signal': volume_signal,
            }
            
        except Exception as e:
            logger.error(f"Error calculating volume analysis: {e}")
            return {'volume_current': 0.0, 'volume_avg': 0.0, 'volume_ratio': 1.0, 'volume_signal': 'NEUTRAL'}
    
    def _generate_signal(self, indicators: Dict) -> tuple:
        """
        Generate trading signal dari semua indikator
        
        Menggunakan voting system:
        - Setiap indikator vote BUY/SELL/NEUTRAL
        - Signal final berdasarkan majority vote
        - Confidence berdasarkan consensus
        
        Args:
            indicators: Dictionary dengan semua indikator
        
        Returns:
            Tuple (signal, confidence)
        """
        try:
            # Kumpulkan semua signals
            signals = [
                indicators.get('rsi_signal', 'NEUTRAL'),
                indicators.get('macd_signal', 'NEUTRAL'),
                indicators.get('ema_signal', 'NEUTRAL'),
                indicators.get('bb_signal', 'NEUTRAL'),
                indicators.get('volume_signal', 'NEUTRAL'),
            ]
            
            # Hitung votes
            buy_votes = signals.count('BUY')
            sell_votes = signals.count('SELL')
            neutral_votes = signals.count('NEUTRAL')
            
            # Tentukan signal final
            total_votes = len(signals)
            
            if buy_votes > sell_votes and buy_votes > neutral_votes:
                signal = 'BUY'
                confidence = int((buy_votes / total_votes) * 100)
            elif sell_votes > buy_votes and sell_votes > neutral_votes:
                signal = 'SELL'
                confidence = int((sell_votes / total_votes) * 100)
            else:
                signal = 'HOLD'
                confidence = int((neutral_votes / total_votes) * 100)
            
            return signal, confidence
            
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return 'HOLD', 0
    
    def _empty_indicators(self) -> Dict:
        """Return empty indicators dictionary"""
        return {
            'rsi': 50.0,
            'rsi_signal': 'NEUTRAL',
            'macd': 0.0,
            'macd_signal_line': 0.0,
            'macd_histogram': 0.0,
            'macd_signal': 'NEUTRAL',
            'ema_20': 0.0,
            'ema_50': 0.0,
            'ema_200': 0.0,
            'ema_signal': 'NEUTRAL',
            'bb_upper': 0.0,
            'bb_middle': 0.0,
            'bb_lower': 0.0,
            'bb_bandwidth': 0.0,
            'bb_signal': 'NEUTRAL',
            'volume_current': 0.0,
            'volume_avg': 0.0,
            'volume_ratio': 1.0,
            'volume_signal': 'NEUTRAL',
            'signal': 'HOLD',
            'confidence': 0,
        }
