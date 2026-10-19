"""
Sentiment Analysis Engine
Menganalisis sentimen berita crypto menggunakan TextBlob (MVP)
atau FinBERT (Advanced - opsional)
"""
from typing import List, Dict, Tuple
from loguru import logger

# Coba import FinBERT, fallback ke TextBlob jika tidak tersedia
try:
    from transformers import pipeline
    FINBERT_AVAILABLE = True
except ImportError:
    FINBERT_AVAILABLE = False

from textblob import TextBlob


class SentimentAnalyzer:
    """Menganalisis sentimen dari teks berita"""

    def __init__(self, use_finbert: bool = False):
        """
        Args:
            use_finbert: True untuk pakai FinBERT (lebih akurat, butuh GPU idealnya)
                        False untuk pakai TextBlob (cepat, ringan)
        """
        self.use_finbert = use_finbert and FINBERT_AVAILABLE
        self.finbert_pipeline = None

        if self.use_finbert:
            logger.info("🧠 Loading FinBERT model (first time may download ~500MB)...")
            try:
                self.finbert_pipeline = pipeline(
                    "sentiment-analysis",
                    model="yiyanghkust/finbert-tone",
                    tokenizer="yiyanghkust/finbert-tone",
                )
                logger.info("✅ FinBERT loaded successfully")
            except Exception as e:
                logger.warning(f"⚠️  FinBERT gagal dimuat: {e}. Fallback ke TextBlob")
                self.use_finbert = False

        if not self.use_finbert:
            logger.info("📝 Menggunakan TextBlob untuk sentiment analysis (MVP mode)")

    def analyze_text(self, text: str) -> Dict:
        """
        Analisis sentimen satu teks
        
        Returns:
            {
                "score": float (-1 sampai +1),
                "label": str ("POSITIVE", "NEGATIVE", "NEUTRAL"),
                "confidence": float (0-1),
                "method": str ("finbert" atau "textblob")
            }
        """
        if not text or len(text.strip()) < 10:
            return {
                "score": 0.0,
                "label": "NEUTRAL",
                "confidence": 0.0,
                "method": "empty",
            }

        if self.use_finbert and self.finbert_pipeline:
            return self._analyze_with_finbert(text)
        else:
            return self._analyze_with_textblob(text)

    def _analyze_with_finbert(self, text: str) -> Dict:
        """Analisis dengan FinBERT (akurasi tinggi untuk finansial)"""
        try:
            # Potong teks jika terlalu panjang (max 512 tokens)
            text_truncated = text[:500]
            result = self.finbert_pipeline(text_truncated)[0]

            label = result["label"].upper()
            confidence = result["score"]

            # Konversi ke skor -1 sampai +1
            if label == "POSITIVE":
                score = confidence
            elif label == "NEGATIVE":
                score = -confidence
            else:  # NEUTRAL
                score = 0.0

            return {
                "score": score,
                "label": label,
                "confidence": confidence,
                "method": "finbert",
            }
        except Exception as e:
            logger.error(f"❌ FinBERT error: {e}")
            return self._analyze_with_textblob(text)

    def _analyze_with_textblob(self, text: str) -> Dict:
        """Analisis dengan TextBlob (cepat dan ringan)"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 sampai +1
            subjectivity = blob.sentiment.subjectivity  # 0 sampai 1

            # Tentukan label
            if polarity > 0.1:
                label = "POSITIVE"
            elif polarity < -0.1:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"

            # Confidence berdasarkan kekuatan polarity
            confidence = abs(polarity)

            return {
                "score": polarity,
                "label": label,
                "confidence": confidence,
                "method": "textblob",
            }
        except Exception as e:
            logger.error(f"❌ TextBlob error: {e}")
            return {
                "score": 0.0,
                "label": "NEUTRAL",
                "confidence": 0.0,
                "method": "error",
            }

    def analyze_news_batch(self, news_items: List[Dict]) -> Dict:
        """
        Analisis sentimen dari batch berita
        
        Args:
            news_items: List of {"title": str, "summary": str, ...}
            
        Returns:
            {
                "overall_score": float (-1 sampai +1),
                "overall_label": str,
                "positive_count": int,
                "negative_count": int,
                "neutral_count": int,
                "articles": List[Dict] (detail per artikel)
            }
        """
        if not news_items:
            return {
                "overall_score": 0.0,
                "overall_label": "NEUTRAL",
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
                "articles": [],
            }

        articles_analysis = []
        scores = []

        for item in news_items:
            # Gabungkan title + summary untuk analisis lebih kaya
            text = f"{item.get('title', '')}. {item.get('summary', '')}"
            analysis = self.analyze_text(text)

            articles_analysis.append(
                {
                    "source": item.get("source"),
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "sentiment": analysis,
                }
            )
            scores.append(analysis["score"])

        # Hitung rata-rata skor
        avg_score = sum(scores) / len(scores) if scores else 0.0

        # Tentukan label overall
        if avg_score > 0.15:
            overall_label = "POSITIVE"
        elif avg_score < -0.15:
            overall_label = "NEGATIVE"
        else:
            overall_label = "NEUTRAL"

        # Hitung distribusi
        positive_count = sum(1 for s in scores if s > 0.1)
        negative_count = sum(1 for s in scores if s < -0.1)
        neutral_count = len(scores) - positive_count - negative_count

        return {
            "overall_score": avg_score,
            "overall_label": overall_label,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "total_articles": len(news_items),
            "articles": articles_analysis,
        }

    def get_sentiment_impact(self, sentiment_score: float) -> Dict:
        """
        Menginterpretasi dampak sentimen terhadap trading decision
        """
        abs_score = abs(sentiment_score)

        if abs_score < 0.15:
            return {
                "impact": "LOW",
                "weight": 0.1,  # Bobot rendah dalam keputusan final
                "reason": "Sentimen netral, tidak mempengaruhi keputusan",
            }
        elif abs_score < 0.4:
            return {
                "impact": "MODERATE",
                "weight": 0.25,
                "reason": "Sentimen cukup kuat, jadi pertimbangan tambahan",
            }
        elif abs_score < 0.7:
            return {
                "impact": "HIGH",
                "weight": 0.4,
                "reason": "Sentimen kuat, bobot signifikan dalam keputusan",
            }
        else:
            return {
                "impact": "VERY_HIGH",
                "weight": 0.5,
                "reason": "Sentimen sangat kuat (breaking news?), bobot maksimal",
            }
