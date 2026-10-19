"""
Signal Generator
Menggabungkan technical indicators dan sentiment analysis menjadi trading signal

Dependencies:
    - pandas: Data manipulation
    - TechnicalAnalyzer: Dari technical_indicators.py
    - SentimentAnalyzer: Dari sentiment_analysis.py
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger

from .technical_indicators import TechnicalAnalyzer
from .sentiment_analysis import SentimentAnalyzer


class SignalGenerator:
    """
    Menghasilkan trading signals dari analisis teknikal dan sentimen
    
    Contoh penggunaan:
        generator = SignalGenerator()
        signal = generator.generate(candles_list, news_texts)
        print(signal['action'])  # 'BUY'
        print(signal['confidence'])  # 75
        print(signal['reasons'])  # ['RSI oversold', 'MACD bullish', ...]
    """
    
    def __init__(self, use_ml_sentiment: bool = False):
        """
        Initialize signal generator
        
        Args:
            use_ml_sentiment: Gunakan ML untuk sentiment analysis
        """
        self.technical = TechnicalAnalyzer()
        self.sentiment = SentimentAnalyzer(use_ml=use_ml_sentiment)
    
    def generate(self, candles: List[Dict], 
                 news_texts: Optional[List[str]] = None,
                 symbol: str = "UNKNOWN",
                 timeframe: str = "UNKNOWN") -> Dict:
        """
        Generate trading signal dari candles dan news
        
        Args:
            candles: List of OHLCV dictionaries dari database
            news_texts: List of news texts (optional)
            symbol: Trading pair (e.g., "BTC/USDT")
            timeframe: Timeframe (e.g., "1h")
        
        Returns:
            Dictionary dengan signal details
        
        Example:
            {
                'symbol': 'BTC/USDT',
                'timeframe': '1h',
                'timestamp': '2024-01-15 10:00:00',
                'action': 'BUY',
                'confidence': 75,
                'price': 42500.0,
                'reasons': [
                    'RSI oversold (28)',
                    'MACD bullish crossover',
                    'EMA alignment bullish',
                    'News sentiment bullish (+0.65)'
                ],
                'technical': {...},
                'interpretation': {...},
                'sentiment': {...},
                'risk_management': {
                    'stop_loss': 41500.0,
                    'take_profit': 44500.0,
                    'risk_reward_ratio': 2.0
                }
            }
        """
        try:
            # 1. Calculate technical indicators dengan interpretasi
            technical_result = self.technical.calculate_all(candles)
            
            if technical_result is None:
                logger.warning(f"❌ Data tidak cukup untuk {symbol} {timeframe}")
                return self._empty_signal(symbol, timeframe, "Data tidak cukup (butuh 200+ candles)")
            
            # 2. Analyze sentiment (if news provided)
            if news_texts and len(news_texts) > 0:
                sentiment = self.sentiment.analyze_multiple(news_texts)
            else:
                sentiment = self.sentiment._neutral_sentiment()
            
            # 3. Generate final signal dari interpretation scores
            action, confidence, reasons = self._combine_signals(
                technical_result['interpretation'], sentiment
            )
            
            # 4. Calculate risk management dengan ATR
            current_price = technical_result['latest_price']
            atr = technical_result['indicators']['atr']['value']
            risk_management = self._calculate_risk_management(
                current_price, atr, action
            )
            
            # 5. Build result
            result = {
                'symbol': symbol,
                'timeframe': timeframe,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'action': action,
                'confidence': confidence,
                'price': round(current_price, 2),
                'reasons': reasons,
                'technical': technical_result['indicators'],
                'interpretation': technical_result['interpretation'],
                'sentiment': sentiment,
                'risk_management': risk_management,
            }
            
            logger.info(
                f"📊 Signal generated: {symbol} {timeframe} - "
                f"{action} ({confidence}% confidence)"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return self._empty_signal(symbol, timeframe, str(e))
    
    def _combine_signals(self, interpretation: Dict, sentiment: Dict) -> tuple:
        """
        Gabungkan interpretation scores dan sentiment menjadi signal final
        
        Menggunakan weighted scoring:
        - Technical interpretation: 70% weight
        - Sentiment analysis: 30% weight
        
        Args:
            interpretation: Dict dengan scores per indikator (-100 to +100)
            sentiment: Sentiment analysis dict
        
        Returns:
            Tuple (action, confidence, reasons)
        """
        reasons = []
        
        # ========================================
        # 1. Technical Analysis (70% weight)
        # ========================================
        tech_scores = []
        
        # Kumpulkan scores dari semua indikator
        for indicator_name, data in interpretation.items():
            score = data.get('score', 0)
            signal = data.get('signal', 'NEUTRAL')
            reason = data.get('reason', '')
            
            tech_scores.append(score)
            
            # Tambahkan reason jika signal kuat
            if abs(score) >= 40:
                reasons.append(reason)
        
        # Calculate average technical score (-100 to +100)
        if len(tech_scores) > 0:
            avg_tech_score = sum(tech_scores) / len(tech_scores)
        else:
            avg_tech_score = 0
        
        # Normalize ke -1.0 to +1.0
        tech_score_normalized = avg_tech_score / 100
        
        # ========================================
        # 2. Sentiment Analysis (30% weight)
        # ========================================
        sentiment_score = sentiment.get('score', 0)
        sentiment_label = sentiment.get('label', 'NEUTRAL')
        
        if sentiment_label == 'BULLISH':
            reasons.append(f"News sentiment bullish ({sentiment_score:+.2f})")
        elif sentiment_label == 'BEARISH':
            reasons.append(f"News sentiment bearish ({sentiment_score:+.2f})")
        
        # ========================================
        # 3. Combine with weights
        # ========================================
        # Technical: 70%, Sentiment: 30%
        final_score = (tech_score_normalized * 0.7) + (sentiment_score * 0.3)
        
        # Determine action
        if final_score > 0.2:
            action = 'BUY'
        elif final_score < -0.2:
            action = 'SELL'
        else:
            action = 'HOLD'
        
        # Calculate confidence (0-100)
        confidence = int(abs(final_score) * 100)
        confidence = min(100, max(0, confidence))
        
        # Add summary reason
        if action == 'BUY':
            reasons.insert(0, f"Strong buy signal (score: {final_score:+.2f})")
        elif action == 'SELL':
            reasons.insert(0, f"Strong sell signal (score: {final_score:+.2f})")
        else:
            reasons.insert(0, f"Weak signal, hold recommended (score: {final_score:+.2f})")
        
        return action, confidence, reasons
    
    def _calculate_risk_management(self, price: float, atr: float, action: str) -> Dict:
        """
        Calculate risk management parameters menggunakan ATR
        
        Args:
            price: Current price
            atr: Average True Range
            action: BUY, SELL, or HOLD
        
        Returns:
            Dictionary dengan risk management parameters
        """
        if action == 'HOLD':
            return {
                'stop_loss': 0.0,
                'take_profit': 0.0,
                'risk_reward_ratio': 0.0,
                'position_size_percent': 0.0,
                'atr': atr,
            }
        
        # Gunakan ATR untuk stop-loss (2x ATR)
        sl_result = self.technical.get_suggested_stop_loss(price, atr, 'long' if action == 'BUY' else 'short')
        stop_loss = sl_result['stop_loss']
        
        # Take profit: 2.5x risk (risk/reward ratio 2.5:1)
        risk_distance = abs(price - stop_loss)
        reward_distance = risk_distance * 2.5
        
        if action == 'BUY':
            take_profit = price + reward_distance
        else:  # SELL
            take_profit = price - reward_distance
        
        # Calculate risk/reward ratio
        risk_reward_ratio = reward_distance / risk_distance if risk_distance > 0 else 0
        
        # Position size: 10% of portfolio (default)
        position_size_percent = 10.0
        
        return {
            'stop_loss': round(stop_loss, 2),
            'take_profit': round(take_profit, 2),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'position_size_percent': position_size_percent,
            'atr': round(atr, 2),
            'stop_loss_distance_percent': round(sl_result['distance_percent'], 2),
        }
    
    def _empty_signal(self, symbol: str, timeframe: str, error_msg: str = "") -> Dict:
        """Return empty signal dictionary"""
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'HOLD',
            'confidence': 0,
            'price': 0.0,
            'reasons': [f'Error generating signal: {error_msg}'] if error_msg else ['No signal generated'],
            'technical': {},
            'interpretation': {},
            'sentiment': {},
            'risk_management': {
                'stop_loss': 0.0,
                'take_profit': 0.0,
                'risk_reward_ratio': 0.0,
                'position_size_percent': 0.0,
                'atr': 0.0,
                'stop_loss_distance_percent': 0.0,
            },
        }
