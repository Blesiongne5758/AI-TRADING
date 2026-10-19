"""
Signal Generator
Menggabungkan technical indicators dan sentiment analysis menjadi trading signal

Dependencies:
    - pandas: Data manipulation
    - TechnicalIndicators: Dari technical_indicators.py
    - SentimentAnalyzer: Dari sentiment_analysis.py
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger

from .technical_indicators import TechnicalIndicators
from .sentiment_analysis import SentimentAnalyzer


class SignalGenerator:
    """
    Menghasilkan trading signals dari analisis teknikal dan sentimen
    
    Contoh penggunaan:
        generator = SignalGenerator()
        signal = generator.generate(candles_df, news_texts)
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
        self.technical = TechnicalIndicators()
        self.sentiment = SentimentAnalyzer(use_ml=use_ml_sentiment)
    
    def generate(self, candles_df: pd.DataFrame, 
                 news_texts: Optional[List[str]] = None,
                 symbol: str = "UNKNOWN",
                 timeframe: str = "UNKNOWN") -> Dict:
        """
        Generate trading signal dari candles dan news
        
        Args:
            candles_df: DataFrame dengan candlestick data
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
                'sentiment': {...},
                'risk_management': {
                    'stop_loss': 41500.0,
                    'take_profit': 44500.0,
                    'risk_reward_ratio': 2.0
                }
            }
        """
        try:
            # 1. Calculate technical indicators
            technical = self.technical.calculate_all(candles_df)
            
            # 2. Analyze sentiment (if news provided)
            if news_texts and len(news_texts) > 0:
                sentiment = self.sentiment.analyze_multiple(news_texts)
            else:
                sentiment = self.sentiment._neutral_sentiment()
            
            # 3. Generate final signal
            action, confidence, reasons = self._combine_signals(
                technical, sentiment
            )
            
            # 4. Calculate risk management
            current_price = candles_df['close'].iloc[-1]
            risk_management = self._calculate_risk_management(
                current_price, action
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
                'technical': technical,
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
            return self._empty_signal(symbol, timeframe)
    
    def _combine_signals(self, technical: Dict, sentiment: Dict) -> tuple:
        """
        Gabungkan technical dan sentiment signals
        
        Menggunakan weighted voting system:
        - Technical indicators: 70% weight
        - Sentiment analysis: 30% weight
        
        Args:
            technical: Technical indicators dict
            sentiment: Sentiment analysis dict
        
        Returns:
            Tuple (action, confidence, reasons)
        """
        reasons = []
        
        # ========================================
        # 1. Technical Analysis (70% weight)
        # ========================================
        tech_signals = []
        
        # RSI
        rsi = technical.get('rsi', 50)
        rsi_signal = technical.get('rsi_signal', 'NEUTRAL')
        if rsi_signal == 'BUY':
            tech_signals.append(1)
            reasons.append(f"RSI oversold ({rsi:.1f})")
        elif rsi_signal == 'SELL':
            tech_signals.append(-1)
            reasons.append(f"RSI overbought ({rsi:.1f})")
        else:
            tech_signals.append(0)
        
        # MACD
        macd_signal = technical.get('macd_signal', 'NEUTRAL')
        if macd_signal == 'BUY':
            tech_signals.append(1)
            reasons.append("MACD bullish crossover")
        elif macd_signal == 'SELL':
            tech_signals.append(-1)
            reasons.append("MACD bearish crossover")
        else:
            tech_signals.append(0)
        
        # EMA
        ema_signal = technical.get('ema_signal', 'NEUTRAL')
        if ema_signal == 'BUY':
            tech_signals.append(1)
            reasons.append("EMA alignment bullish")
        elif ema_signal == 'SELL':
            tech_signals.append(-1)
            reasons.append("EMA alignment bearish")
        else:
            tech_signals.append(0)
        
        # Bollinger Bands
        bb_signal = technical.get('bb_signal', 'NEUTRAL')
        if bb_signal == 'BUY':
            tech_signals.append(1)
            reasons.append("Price below lower Bollinger Band")
        elif bb_signal == 'SELL':
            tech_signals.append(-1)
            reasons.append("Price above upper Bollinger Band")
        else:
            tech_signals.append(0)
        
        # Volume
        volume_signal = technical.get('volume_signal', 'NEUTRAL')
        if volume_signal == 'BUY':
            tech_signals.append(1)
            reasons.append("High volume with price increase")
        elif volume_signal == 'SELL':
            tech_signals.append(-1)
            reasons.append("High volume with price decrease")
        else:
            tech_signals.append(0)
        
        # Calculate technical score (-1 to 1)
        if len(tech_signals) > 0:
            tech_score = sum(tech_signals) / len(tech_signals)
        else:
            tech_score = 0
        
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
        final_score = (tech_score * 0.7) + (sentiment_score * 0.3)
        
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
    
    def _calculate_risk_management(self, price: float, action: str) -> Dict:
        """
        Calculate risk management parameters
        
        Args:
            price: Current price
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
            }
        
        # Default risk parameters
        stop_loss_percent = 0.02  # 2%
        take_profit_percent = 0.05  # 5%
        position_size_percent = 0.10  # 10% of portfolio
        
        if action == 'BUY':
            stop_loss = price * (1 - stop_loss_percent)
            take_profit = price * (1 + take_profit_percent)
        else:  # SELL
            stop_loss = price * (1 + stop_loss_percent)
            take_profit = price * (1 - take_profit_percent)
        
        # Calculate risk/reward ratio
        risk = abs(price - stop_loss)
        reward = abs(take_profit - price)
        risk_reward_ratio = reward / risk if risk > 0 else 0
        
        return {
            'stop_loss': round(stop_loss, 2),
            'take_profit': round(take_profit, 2),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'position_size_percent': position_size_percent * 100,
        }
    
    def _empty_signal(self, symbol: str, timeframe: str) -> Dict:
        """Return empty signal dictionary"""
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'action': 'HOLD',
            'confidence': 0,
            'price': 0.0,
            'reasons': ['Error generating signal'],
            'technical': {},
            'sentiment': {},
            'risk_management': {
                'stop_loss': 0.0,
                'take_profit': 0.0,
                'risk_reward_ratio': 0.0,
                'position_size_percent': 0.0,
            },
        }
