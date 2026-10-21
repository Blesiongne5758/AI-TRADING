"""
FinBERT Analyzer
Model AI khusus finansial untuk analisis sentimen
Menggantikan TextBlob dengan akurasi +30%
"""
import asyncio
from typing import Dict, List, Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import DEFAULT_FINBERT_MODEL, DEVICE, MODEL_CACHE_DIR
from .cache_manager import cache

# Lazy import untuk percepat startup
_model = None
_tokenizer = None
_pipeline = None


class FinBERTAnalyzer:
    """Analyzer sentimen finansial menggunakan FinBERT"""

    def __init__(self, model_name: str = DEFAULT_FINBERT_MODEL):
        self.model_name = model_name
        self.is_loaded = False
        self.fallback_to_textblob = False

    def _load_model(self):
        """Load model secara lazy (saat pertama kali dibutuhkan)"""
        global _model, _tokenizer, _pipeline

        if _pipeline is not None:
            self.is_loaded = True
            return

        try:
            from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
            import torch

            logger.info(f"🧠 Loading FinBERT model: {self.model_name}")
            logger.info(f"   Device: {DEVICE}")
            logger.info(f"   Cache dir: {MODEL_CACHE_DIR}")
            logger.info("   (First load may download ~400MB, please wait...)")

            # Load tokenizer dan model
            _tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=str(MODEL_CACHE_DIR),
            )
            _model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                cache_dir=str(MODEL_CACHE_DIR),
            )

            # Buat pipeline
            device_id = 0 if DEVICE == "cuda" else -1
            _pipeline = pipeline(
                "sentiment-analysis",
                model=_model,
                tokenizer=_tokenizer,
                device=device_id,
                truncation=True,
                max_length=512,
            )

            self.is_loaded = True
            logger.info("✅ FinBERT model loaded successfully")

        except Exception as e:
            logger.error(f"❌ Failed to load FinBERT: {e}")
            logger.warning("⚠️  Falling back to TextBlob (lower accuracy)")
            self.fallback_to_textblob = True

    def _preprocess_text(self, text: str) -> str:
        """Preprocess teks untuk FinBERT"""
        if not text:
            return ""

        # Bersihkan teks
        text = text.strip()

        # Hapus URL
        import re
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

        # Hapus mention (@user)
        text = re.sub(r"@\w+", "", text)

        # Hapus hashtag symbol tapi keep text
        text = re.sub(r"#(\w+)", r"\1", text)

        # Hapus extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Potong jika terlalu panjang (FinBERT max 512 tokens)
        words = text.split()
        if len(words) > 400:
            text = " ".join(words[:400])

        return text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _run_inference(self, text: str) -> Dict:
        """Jalankan inference dengan retry"""
        if _pipeline is None:
            raise RuntimeError("Model not loaded")

        result = _pipeline(text)[0]

        label = result["label"]
        score = result["score"]

        # Normalisasi label ke format standar
        label_map = {
            "Positive": "POSITIVE",
            "positive": "POSITIVE",
            "Negative": "NEGATIVE",
            "negative": "NEGATIVE",
            "Neutral": "NEUTRAL",
            "neutral": "NEUTRAL",
        }

        normalized_label = label_map.get(label, "NEUTRAL")

        # Konversi ke skor -1 sampai +1
        if normalized_label == "POSITIVE":
            numeric_score = score
        elif normalized_label == "NEGATIVE":
            numeric_score = -score
        else:
            numeric_score = 0.0

        return {
            "label": normalized_label,
            "confidence": score,
            "score": numeric_score,
            "method": "finbert",
        }

    def _analyze_with_textblob(self, text: str) -> Dict:
        """Fallback ke TextBlob jika FinBERT gagal"""
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity

            if polarity > 0.1:
                label = "POSITIVE"
            elif polarity < -0.1:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"

            return {
                "label": label,
                "confidence": abs(polarity),
                "score": polarity,
                "method": "textblob_fallback",
            }
        except Exception as e:
            logger.error(f"TextBlob fallback also failed: {e}")
            return {
                "label": "NEUTRAL",
                "confidence": 0.0,
                "score": 0.0,
                "method": "error",
            }

    async def analyze(self, text: str, use_cache: bool = True) -> Dict:
        """
        Analisis sentimen satu teks
        
        Args:
            text: Teks yang akan dianalisis
            use_cache: Gunakan cache untuk hemat resource
            
        Returns:
            Dict dengan label, confidence, score, method
        """
        if not text or len(text.strip()) < 5:
            return {
                "label": "NEUTRAL",
                "confidence": 0.0,
                "score": 0.0,
                "method": "empty",
            }

        # Preprocess
        processed_text = self._preprocess_text(text)

        # Cek cache
        if use_cache:
            cached = await cache.get("finbert", processed_text)
            if cached:
                return cached

        # Load model jika belum
        if not self.is_loaded and not self.fallback_to_textblob:
            await asyncio.to_thread(self._load_model)

        # Analisis
        try:
            if self.fallback_to_textblob:
                result = self._analyze_with_textblob(processed_text)
            else:
                result = await asyncio.to_thread(self._run_inference, processed_text)
        except Exception as e:
            logger.error(f"FinBERT inference error: {e}")
            result = self._analyze_with_textblob(processed_text)

        # Simpan ke cache
        if use_cache:
            await cache.set("finbert", result, 300, processed_text)

        return result

    async def analyze_batch(
        self, texts: List[str], batch_size: int = 16
    ) -> List[Dict]:
        """
        Analisis batch teks secara efisien
        
        Args:
            texts: List teks yang akan dianalisis
            batch_size: Ukuran batch untuk inference
            
        Returns:
            List hasil analisis
        """
        if not texts:
            return []

        # Load model jika belum
        if not self.is_loaded and not self.fallback_to_textblob:
            await asyncio.to_thread(self._load_model)

        results = []

        # Proses dalam batch
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            processed_batch = [self._preprocess_text(t) for t in batch]

            try:
                if self.fallback_to_textblob:
                    batch_results = [
                        self._analyze_with_textblob(t) for t in processed_batch
                    ]
                else:
                    # Batch inference (lebih cepat)
                    if _pipeline is not None:
                        raw_results = await asyncio.to_thread(
                            _pipeline, processed_batch
                        )
                        batch_results = []
                        for r in raw_results:
                            label = r["label"]
                            score = r["score"]
                            label_map = {
                                "Positive": "POSITIVE",
                                "positive": "POSITIVE",
                                "Negative": "NEGATIVE",
                                "negative": "NEGATIVE",
                                "Neutral": "NEUTRAL",
                                "neutral": "NEUTRAL",
                            }
                            normalized = label_map.get(label, "NEUTRAL")
                            numeric = (
                                score if normalized == "POSITIVE"
                                else -score if normalized == "NEGATIVE"
                                else 0.0
                            )
                            batch_results.append({
                                "label": normalized,
                                "confidence": score,
                                "score": numeric,
                                "method": "finbert_batch",
                            })
                    else:
                        batch_results = [
                            self._analyze_with_textblob(t) for t in processed_batch
                        ]

                results.extend(batch_results)

            except Exception as e:
                logger.error(f"Batch inference error: {e}")
                # Fallback per item
                for t in processed_batch:
                    results.append(self._analyze_with_textblob(t))

        return results

    def get_model_info(self) -> Dict:
        """Informasi model yang digunakan"""
        return {
            "model_name": self.model_name,
            "device": DEVICE,
            "is_loaded": self.is_loaded,
            "fallback_to_textblob": self.fallback_to_textblob,
            "cache_dir": str(MODEL_CACHE_DIR),
        }
