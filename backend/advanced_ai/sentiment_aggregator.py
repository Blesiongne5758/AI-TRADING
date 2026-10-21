"""
Sentiment Aggregator
Menggabungkan semua sumber sentimen menjadi satu skor final
"""
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger

from .finbert_analyzer import FinBERTAnalyzer
from .news_api_client import NewsAPIClient
from .twitter_analyzer import SocialMediaAnalyzer
from .pump_dump_detector import PumpDumpDetector
from .cache_manager import cache


class SentimentAggregator:
    """
    Menggabungkan sentimen dari multiple sources dengan weighted scoring
    """

    # Bobot setiap sumber (total = 1.0)
    SOURCE_WEIGHTS = {
        "news_professional": 0.30,  # CryptoPanic, NewsAPI
        "social_influencers": 0.25,  # Twitter influencers
        "social_reddit": 0.15,  # Reddit posts
        "community_votes": 0.15,  # CryptoPanic community votes
        "on_chain": 0.15,  # Whale movements (future)
    }

    def __init__(self):
        self.finbert = FinBERTAnalyzer()
        self.news_client = NewsAPIClient()
        self.social_analyzer = SocialMediaAnalyzer()
        self.pump_detector = PumpDumpDetector()

    async def analyze_symbol(
        self,
        symbol: str,
        currency_code: str = None,
        include_pump_detection: bool = True,
    ) -> Dict:
        """
        Analisis sentimen lengkap untuk satu simbol
        
        Args:
            symbol: Trading pair (misal: "BTC/USDT")
            currency_code: Kode mata uang (misal: "BTC")
            include_pump_detection: Aktifkan deteksi pump/dump
            
        Returns:
            Dict dengan aggregated sentiment + breakdown
        """
        if currency_code is None:
            currency_code = symbol.split("/")[0]

        logger.info(f"🎯 Analyzing sentiment for {symbol}")

        # === 1. Fetch semua data secara paralel ===
        news_task = self.news_client.fetch_all_news(
            currencies=[currency_code], limit_per_source=30
        )
        social_task = self.social_analyzer.fetch_all_social(
            crypto_query=currency_code.lower(),
            monitor_influencers=True,
        )

        news_articles, social_data = await asyncio.gather(
            news_task, social_task
        )

        # === 2. Analisis sentimen dengan FinBERT ===
        all_texts = []
        source_map = {}  # Track source untuk setiap text

        # News texts
        for article in news_articles:
            text = f"{article.get('title', '')}. {article.get('summary', '')}"
            all_texts.append(text)
            source_map[len(all_texts)-1] = article.get("source", "unknown")

        # Social texts
        for source_name, posts in social_data.items():
            for post in posts:
                text = f"{post.get('title', '')}. {post.get('text', '')}"
                all_texts.append(text)
                source_map[len(all_texts)-1] = f"social/{source_name}"

        # Batch analyze dengan FinBERT
        if all_texts:
            sentiment_results = await self.finbert.analyze_batch(all_texts)
        else:
            sentiment_results = []

        # === 3. Aggregate by source ===
        source_scores = {
            "news_professional": [],
            "social_influencers": [],
            "social_reddit": [],
            "community_votes": [],
        }

        for i, sentiment in enumerate(sentiment_results):
            source = source_map.get(i, "unknown")
            score = sentiment["score"]

            if source.startswith("cryptopanic"):
                source_scores["news_professional"].append(score)
            elif source.startswith("newsapi") or source.startswith("gnews"):
                source_scores["news_professional"].append(score)
            elif source.startswith("twitter") or source.startswith("social/influencers"):
                source_scores["social_influencers"].append(score)
            elif source.startswith("reddit") or source.startswith("social/reddit"):
                source_scores["social_reddit"].append(score)

        # Tambahkan community votes dari CryptoPanic
        for article in news_articles:
            if article.get("source") == "cryptopanic":
                votes = article.get("community_votes", {})
                pos = votes.get("positive", 0)
                neg = votes.get("negative", 0)
                total = pos + neg
                if total > 0:
                    community_score = (pos - neg) / total  # -1 to +1
                    source_scores["community_votes"].append(community_score)

        # === 4. Hitung weighted final score ===
        weighted_scores = []
        source_breakdown = {}

        for source_name, scores in source_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                weight = self.SOURCE_WEIGHTS.get(source_name, 0)
                weighted_scores.append(avg_score * weight)
                source_breakdown[source_name] = {
                    "score": round(avg_score, 3),
                    "weight": weight,
                    "weighted_contribution": round(avg_score * weight, 3),
                    "sample_size": len(scores),
                }
            else:
                source_breakdown[source_name] = {
                    "score": 0.0,
                    "weight": self.SOURCE_WEIGHTS.get(source_name, 0),
                    "weighted_contribution": 0.0,
                    "sample_size": 0,
                }

        final_score = sum(weighted_scores) if weighted_scores else 0.0

        # Normalize ke -1 sampai +1
        total_weight = sum(self.SOURCE_WEIGHTS.values())
        if total_weight > 0:
            final_score = final_score / total_weight

        # === 5. Tentukan label ===
        if final_score > 0.2:
            label = "BULLISH"
        elif final_score < -0.2:
            label = "BEARISH"
        else:
            label = "NEUTRAL"

        # === 6. Confidence score ===
        total_samples = sum(s["sample_size"] for s in source_breakdown.values())
        if total_samples > 100:
            confidence = 90
        elif total_samples > 50:
            confidence = 75
        elif total_samples > 20:
            confidence = 60
        elif total_samples > 5:
            confidence = 40
        else:
            confidence = 20

        # === 7. Pump & dump detection ===
        pump_dump_analysis = None
        if include_pump_detection:
            # Note: butuh price_data dan volume_data dari external source
            # Di sini kita skip jika tidak ada data
            pump_dump_analysis = {
                "status": "requires_price_data",
                "message": "Pump detection membutuhkan price & volume data",
            }

        # === 8. Top articles/posts ===
        top_positive = sorted(
            [
                {**sentiment_results[i], "text": all_texts[i][:200], "source": source_map.get(i)}
                for i in range(len(sentiment_results))
                if sentiment_results[i]["score"] > 0.5
            ],
            key=lambda x: x["score"],
            reverse=True,
        )[:5]

        top_negative = sorted(
            [
                {**sentiment_results[i], "text": all_texts[i][:200], "source": source_map.get(i)}
                for i in range(len(sentiment_results))
                if sentiment_results[i]["score"] < -0.5
            ],
            key=lambda x: x["score"],
        )[:5]

        result = {
            "symbol": symbol,
            "currency": currency_code,
            "timestamp": datetime.now().isoformat(),
            "final_score": round(final_score, 3),
            "label": label,
            "confidence": confidence,
            "total_samples": total_samples,
            "source_breakdown": source_breakdown,
            "top_positive": top_positive,
            "top_negative": top_negative,
            "pump_dump_analysis": pump_dump_analysis,
            "raw_counts": {
                "news_articles": len(news_articles),
                "social_posts": sum(len(v) for v in social_data.values()),
                "total_analyzed": len(sentiment_results),
            },
        }

        logger.info(
            f"✅ {symbol} sentiment: {label} ({final_score:+.3f}) "
            f"with {confidence}% confidence from {total_samples} samples"
        )

        return result

    async def analyze_all_symbols(
        self, symbols: List[str]
    ) -> List[Dict]:
        """Analisis sentiment untuk multiple symbols"""
        tasks = [self.analyze_symbol(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results = []
        for r in results:
            if isinstance(r, Dict):
                valid_results.append(r)
            elif isinstance(r, Exception):
                logger.error(f"Analysis error: {r}")

        return valid_results

    async def close(self):
        """Cleanup"""
        await self.news_client.close()
        await self.social_analyzer.close()

    def get_source_weights(self) -> Dict:
        """Info bobot setiap sumber"""
        return self.SOURCE_WEIGHTS
