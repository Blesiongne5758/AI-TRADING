"""
Sentiment Analysis Module
Menganalisis sentimen berita crypto menggunakan keyword-based approach

Phase 2a: Rule-based sentiment (simple, no ML dependencies)
Phase 2b: ML-based sentiment (transformers + FinBERT) - optional upgrade

Dependencies:
    - re: Regular expressions
    - Optional: transformers, torch (untuk ML-based)
"""

import re
from typing import Dict, List, Tuple
from loguru import logger


class SentimentAnalyzer:
    """
    Menganalisis sentimen berita crypto
    
    Menggunakan keyword-based approach untuk Phase 2
    Bisa di-upgrade ke ML-based (FinBERT) di masa depan
    
    Contoh penggunaan:
        analyzer = SentimentAnalyzer()
        sentiment = analyzer.analyze("Bitcoin reaches new all-time high")
        print(sentiment['score'])  # 0.75
        print(sentiment['label'])  # 'BULLISH'
    """
    
    def __init__(self, use_ml: bool = False):
        """
        Initialize sentiment analyzer
        
        Args:
            use_ml: Gunakan ML-based analysis (butuh transformers + torch)
                   Default False untuk Phase 2a (rule-based)
        """
        self.use_ml = use_ml
        self.model = None
        
        # Keyword dictionaries untuk sentiment analysis
        self.bullish_keywords = self._get_bullish_keywords()
        self.bearish_keywords = self._get_bearish_keywords()
        
        if use_ml:
            self._load_ml_model()
    
    def _get_bullish_keywords(self) -> Dict[str, float]:
        """
        Daftar keyword bullish dengan weight
        
        Returns:
            Dictionary {keyword: weight}
        """
        return {
            # Strong bullish
            'bull': 1.0,
            'bullish': 1.0,
            'rally': 0.9,
            'surge': 0.9,
            'soar': 0.9,
            'pump': 0.8,
            'moon': 0.8,
            'breakout': 0.8,
            'all-time high': 1.0,
            'ath': 0.9,
            'record high': 1.0,
            
            # Medium bullish
            'rise': 0.7,
            'gain': 0.7,
            'up': 0.5,
            'increase': 0.6,
            'grow': 0.6,
            'adoption': 0.7,
            'institutional': 0.6,
            'etf approved': 0.9,
            'etf approval': 0.9,
            'buy': 0.6,
            'accumulate': 0.7,
            'support': 0.5,
            'recovery': 0.6,
            'rebound': 0.6,
            'positive': 0.6,
            'optimistic': 0.7,
            'upgrade': 0.6,
            'partnership': 0.5,
            'launch': 0.5,
            'success': 0.6,
            
            # Weak bullish
            'hope': 0.4,
            'potential': 0.4,
            'opportunity': 0.4,
            'promising': 0.5,
        }
    
    def _get_bearish_keywords(self) -> Dict[str, float]:
        """
        Daftar keyword bearish dengan weight
        
        Returns:
            Dictionary {keyword: weight}
        """
        return {
            # Strong bearish
            'bear': 1.0,
            'bearish': 1.0,
            'crash': 1.0,
            'plunge': 0.9,
            'dump': 0.9,
            'collapse': 1.0,
            'bubble': 0.8,
            'scam': 0.9,
            'hack': 0.8,
            'ban': 0.9,
            'regulation': 0.6,
            'crackdown': 0.8,
            
            # Medium bearish
            'fall': 0.7,
            'drop': 0.7,
            'down': 0.5,
            'decrease': 0.6,
            'decline': 0.7,
            'sell': 0.6,
            'sell-off': 0.8,
            'correction': 0.5,
            'resistance': 0.4,
            'overbought': 0.6,
            'negative': 0.6,
            'pessimistic': 0.7,
            'fear': 0.6,
            'risk': 0.5,
            'warning': 0.6,
            'concern': 0.5,
            'lawsuit': 0.7,
            'investigation': 0.6,
            'fraud': 0.9,
            
            # Weak bearish
            'uncertain': 0.4,
            'volatile': 0.4,
            'risk': 0.4,
            'threat': 0.5,
        }
    
    def _load_ml_model(self):
        """
        Load ML model (FinBERT) untuk sentiment analysis
        
        Note: Butuh transformers dan torch
        """
        try:
            from transformers import pipeline
            
            logger.info("Loading FinBERT model untuk sentiment analysis...")
            self.model = pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert",
                tokenizer="ProsusAI/finbert"
            )
            logger.info("✅ FinBERT model loaded successfully")
            
        except ImportError:
            logger.warning("⚠️  transformers/torch not installed, using rule-based only")
            self.use_ml = False
        except Exception as e:
            logger.error(f"❌ Error loading ML model: {e}")
            self.use_ml = False
    
    def analyze(self, text: str) -> Dict:
        """
        Analisis sentimen dari text
        
        Args:
            text: Text yang akan dianalisis (judul berita, summary, dll)
        
        Returns:
            Dictionary dengan sentiment analysis results
        
        Example:
            {
                'score': 0.75,  # -1.0 to 1.0
                'label': 'BULLISH',  # BULLISH, BEARISH, NEUTRAL
                'confidence': 85,  # 0-100
                'bullish_count': 5,
                'bearish_count': 1,
                'method': 'rule-based'  # atau 'ml-based'
            }
        """
        if not text or len(text.strip()) == 0:
            return self._neutral_sentiment()
        
        # Clean text
        text = self._clean_text(text)
        
        if self.use_ml and self.model:
            return self._analyze_ml(text)
        else:
            return self._analyze_rule_based(text)
    
    def _analyze_rule_based(self, text: str) -> Dict:
        """
        Analisis sentimen menggunakan rule-based approach
        
        Args:
            text: Cleaned text
        
        Returns:
            Sentiment analysis results
        """
        text_lower = text.lower()
        
        # Hitung bullish dan bearish scores
        bullish_score = 0.0
        bearish_score = 0.0
        bullish_count = 0
        bearish_count = 0
        
        # Check bullish keywords
        for keyword, weight in self.bullish_keywords.items():
            if keyword in text_lower:
                bullish_score += weight
                bullish_count += 1
        
        # Check bearish keywords
        for keyword, weight in self.bearish_keywords.items():
            if keyword in text_lower:
                bearish_score += weight
                bearish_count += 1
        
        # Calculate final score (-1.0 to 1.0)
        total_score = bullish_score - bearish_score
        max_possible = max(bullish_score + bearish_score, 1.0)
        
        # Normalize to -1.0 to 1.0
        score = total_score / max_possible
        score = max(-1.0, min(1.0, score))  # Clamp
        
        # Determine label
        if score > 0.2:
            label = 'BULLISH'
        elif score < -0.2:
            label = 'BEARISH'
        else:
            label = 'NEUTRAL'
        
        # Calculate confidence
        total_keywords = bullish_count + bearish_count
        confidence = min(100, int(total_keywords * 15))
        
        return {
            'score': round(score, 3),
            'label': label,
            'confidence': confidence,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count,
            'method': 'rule-based',
        }
    
    def _analyze_ml(self, text: str) -> Dict:
        """
        Analisis sentimen menggunakan ML model (FinBERT)
        
        Args:
            text: Cleaned text
        
        Returns:
            Sentiment analysis results
        """
        try:
            # Truncate text if too long
            text_truncated = text[:512]
            
            # Analyze with model
            result = self.model(text_truncated)[0]
            
            # Map labels
            label_map = {
                'positive': 'BULLISH',
                'negative': 'BEARISH',
                'neutral': 'NEUTRAL',
            }
            
            label = label_map.get(result['label'].lower(), 'NEUTRAL')
            score = result['score']
            
            # Convert to -1.0 to 1.0 range
            if label == 'BULLISH':
                final_score = score
            elif label == 'BEARISH':
                final_score = -score
            else:
                final_score = 0.0
            
            return {
                'score': round(final_score, 3),
                'label': label,
                'confidence': int(score * 100),
                'bullish_count': 0,
                'bearish_count': 0,
                'method': 'ml-based',
            }
            
        except Exception as e:
            logger.error(f"Error in ML analysis: {e}")
            return self._neutral_sentiment()
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text untuk analisis
        
        Args:
            text: Raw text
        
        Returns:
            Cleaned text
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove special characters (keep letters, numbers, spaces)
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _neutral_sentiment(self) -> Dict:
        """Return neutral sentiment"""
        return {
            'score': 0.0,
            'label': 'NEUTRAL',
            'confidence': 0,
            'bullish_count': 0,
            'bearish_count': 0,
            'method': 'rule-based',
        }
    
    def analyze_multiple(self, texts: List[str]) -> Dict:
        """
        Analisis sentimen dari multiple texts dan aggregate
        
        Args:
            texts: List of texts
        
        Returns:
            Aggregated sentiment analysis
        """
        if not texts:
            return self._neutral_sentiment()
        
        # Analyze each text
        sentiments = [self.analyze(text) for text in texts]
        
        # Aggregate scores
        avg_score = sum(s['score'] for s in sentiments) / len(sentiments)
        total_bullish = sum(s['bullish_count'] for s in sentiments)
        total_bearish = sum(s['bearish_count'] for s in sentiments)
        
        # Determine label
        if avg_score > 0.2:
            label = 'BULLISH'
        elif avg_score < -0.2:
            label = 'BEARISH'
        else:
            label = 'NEUTRAL'
        
        # Calculate confidence
        avg_confidence = sum(s['confidence'] for s in sentiments) / len(sentiments)
        
        return {
            'score': round(avg_score, 3),
            'label': label,
            'confidence': int(avg_confidence),
            'bullish_count': total_bullish,
            'bearish_count': total_bearish,
            'method': 'aggregated',
            'count': len(sentiments),
        }
