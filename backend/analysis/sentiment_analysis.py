"""
Sentiment Analysis Module
Menganalisis sentimen berita crypto menggunakan TextBlob

Dependencies:
    - textblob: Simple NLP library untuk sentiment analysis
    - Optional: transformers, torch (untuk upgrade ke FinBERT)

Usage:
    analyzer = SentimentAnalyzer()
    sentiment = analyzer.analyze("Bitcoin reaches new all-time high")
    print(sentiment['score'])  # 0.75
    print(sentiment['label'])  # 'BULLISH'
"""

from typing import Dict, List
from loguru import logger

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    logger.warning("⚠️  textblob not installed, sentiment analysis will use fallback")


class SentimentAnalyzer:
    """
    Menganalisis sentimen berita crypto menggunakan TextBlob
    
    TextBlob menggunakan pattern matching dan lexicon-based approach.
    Lebih simple dan ringan dibandingkan ML-based approach.
    
    Score range: -1.0 (very bearish) to +1.0 (very bullish)
    """
    
    def __init__(self, use_ml: bool = False):
        """
        Initialize sentiment analyzer
        
        Args:
            use_ml: Gunakan ML-based analysis (butuh transformers + torch)
                   Default False untuk Phase 2a (TextBlob)
        """
        self.use_ml = use_ml
        self.model = None
        
        if use_ml:
            self._load_ml_model()
        elif not TEXTBLOB_AVAILABLE:
            logger.warning("⚠️  TextBlob not available, using fallback method")
    
    def _load_ml_model(self):
        """
        Load ML model (FinBERT) untuk sentiment analysis
        
        Note: Butuh transformers dan torch (~500MB)
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
            logger.warning("⚠️  transformers/torch not installed, using TextBlob only")
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
                'method': 'textblob'  # atau 'ml-based'
            }
        """
        if not text or len(text.strip()) == 0:
            return self._neutral_sentiment()
        
        if self.use_ml and self.model:
            return self._analyze_ml(text)
        elif TEXTBLOB_AVAILABLE:
            return self._analyze_textblob(text)
        else:
            return self._analyze_fallback(text)
    
    def _analyze_textblob(self, text: str) -> Dict:
        """
        Analisis sentimen menggunakan TextBlob
        
        TextBlob polarity:
        - -1.0 to 0.0: Negative (bearish)
        - 0.0: Neutral
        - 0.0 to 1.0: Positive (bullish)
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1.0 to 1.0
            subjectivity = blob.sentiment.subjectivity  # 0.0 to 1.0
            
            # Determine label based on polarity
            if polarity > 0.1:
                label = 'BULLISH'
            elif polarity < -0.1:
                label = 'BEARISH'
            else:
                label = 'NEUTRAL'
            
            # Calculate confidence based on polarity strength and subjectivity
            confidence = int(abs(polarity) * 100 * (0.5 + subjectivity * 0.5))
            confidence = min(100, max(0, confidence))
            
            return {
                'score': round(polarity, 3),
                'label': label,
                'confidence': confidence,
                'subjectivity': round(subjectivity, 3),
                'method': 'textblob',
            }
            
        except Exception as e:
            logger.error(f"Error in TextBlob analysis: {e}")
            return self._neutral_sentiment()
    
    def _analyze_ml(self, text: str) -> Dict:
        """
        Analisis sentimen menggunakan ML model (FinBERT)
        
        Note: Lebih akurat tapi butuh ~500MB dan startup lambat
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
                'method': 'ml-based',
            }
            
        except Exception as e:
            logger.error(f"Error in ML analysis: {e}")
            return self._neutral_sentiment()
    
    def _analyze_fallback(self, text: str) -> Dict:
        """
        Fallback method jika TextBlob tidak tersedia
        
        Simple keyword-based approach
        """
        text_lower = text.lower()
        
        # Simple keyword lists
        bullish_words = ['bull', 'rise', 'gain', 'up', 'grow', 'buy', 'positive', 'success']
        bearish_words = ['bear', 'fall', 'drop', 'down', 'decline', 'sell', 'negative', 'crash']
        
        bullish_count = sum(1 for word in bullish_words if word in text_lower)
        bearish_count = sum(1 for word in bearish_words if word in text_lower)
        
        total = bullish_count + bearish_count
        if total == 0:
            return self._neutral_sentiment()
        
        score = (bullish_count - bearish_count) / total
        
        if score > 0.1:
            label = 'BULLISH'
        elif score < -0.1:
            label = 'BEARISH'
        else:
            label = 'NEUTRAL'
        
        return {
            'score': round(score, 3),
            'label': label,
            'confidence': min(100, int(total * 20)),
            'method': 'fallback',
        }
    
    def _neutral_sentiment(self) -> Dict:
        """Return neutral sentiment"""
        return {
            'score': 0.0,
            'label': 'NEUTRAL',
            'confidence': 0,
            'method': 'none',
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
        avg_confidence = sum(s['confidence'] for s in sentiments) / len(sentiments)
        
        # Determine label
        if avg_score > 0.1:
            label = 'BULLISH'
        elif avg_score < -0.1:
            label = 'BEARISH'
        else:
            label = 'NEUTRAL'
        
        return {
            'score': round(avg_score, 3),
            'label': label,
            'confidence': int(avg_confidence),
            'method': 'aggregated',
            'count': len(sentiments),
        }
