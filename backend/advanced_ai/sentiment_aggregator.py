"""
Sentiment Aggregator
Gabungkan sentiment dari semua sumber (news, social media, FinBERT)
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from .finbert_analyzer import FinBERTAnalyzer
from .news_api_client import NewsAPIClient
from .twitter_analyzer import TwitterAnalyzer
from .pump_dump_detector import PumpDumpDetector
from .cache_manager import cache


class SentimentAggregator:
    """
    Aggregate sentiment from multiple sources
    
    Features:
    - Combine news sentiment
    - Combine social media sentiment
    - Weighted scoring
    - Source reliability scoring
    - Conflict detection
    - Final sentiment recommendation
    """
    
    def __init__(self):
        """Initialize sentiment aggregator"""
        self.finbert = FinBERTAnalyzer()
        self.news_client = NewsAPIClient()
        self.twitter_analyzer = TwitterAnalyzer(self.finbert)
        self.pump_detector = PumpDumpDetector()
        
        # Source weights (can be adjusted)
        self.source_weights = {
            "news": 0.4,           # 40% weight
            "twitter": 0.3,        # 30% weight
            "reddit": 0.2,         # 20% weight
            "telegram": 0.1        # 10% weight
        }
        
        logger.info("🔄 Sentiment Aggregator initialized")
    
    async def initialize(self):
        """Initialize all components"""
        await self.finbert.initialize()
        await self.news_client.initialize()
        await self.twitter_analyzer.initialize()
        
        logger.info("✅ Sentiment aggregator initialized")
    
    async def close(self):
        """Close all components"""
        await self.news_client.close()
        await self.twitter_analyzer.close()
        
        logger.info("🔒 Sentiment aggregator closed")
    
    async def aggregate_sentiment(
        self,
        currencies: List[str] = ["BTC", "ETH"],
        include_news: bool = True,
        include_social: bool = True,
        include_pump_detection: bool = True
    ) -> Dict:
        """
        Aggregate sentiment from all sources
        
        Args:
            currencies: List of currency codes
            include_news: Include news sentiment
            include_social: Include social media sentiment
            include_pump_detection: Include pump & dump detection
            
        Returns:
            Aggregated sentiment results
        """
        logger.info(f"🔄 Aggregating sentiment for {currencies}...")
        
        # Check cache
        cache_key = {
            "currencies": currencies,
            "include_news": include_news,
            "include_social": include_social
        }
        
        cached = await cache.get("sentiment", cache_key)
        if cached:
            logger.info("✅ Sentiment cache hit")
            return cached
        
        results = {
            "currencies": currencies,
            "timestamp": datetime.now().isoformat(),
            "sources": {},
            "overall_score": 0.0,
            "overall_label": "NEUTRAL",
            "confidence": 0.0,
            "conflicts": [],
            "pump_dump_warning": False
        }
        
        weighted_scores = []
        
        # ============================================
        # 1. News Sentiment
        # ============================================
        if include_news:
            logger.info("📰 Analyzing news sentiment...")
            
            news_articles = await self.news_client.fetch_all(
                currencies=currencies,
                limit_per_source=20
            )
            
            if news_articles:
                news_sentiment = self.finbert.analyze_news_batch(news_articles)
                
                results["sources"]["news"] = {
                    "score": news_sentiment["overall_score"],
                    "label": news_sentiment["overall_label"],
                    "article_count": news_sentiment["total_articles"],
                    "weight": self.source_weights["news"]
                }
                
                weighted_scores.append(
                    news_sentiment["overall_score"] * self.source_weights["news"]
                )
                
                logger.info(f"   News: {news_sentiment['overall_label']} ({news_sentiment['overall_score']:+.3f})")
        
        # ============================================
        # 2. Social Media Sentiment
        # ============================================
        if include_social:
            logger.info("📱 Analyzing social media sentiment...")
            
            query = " OR ".join(currencies)
            social_posts = await self.twitter_analyzer.fetch_all_social_media(
                query=query,
                limit_per_platform=20
            )
            
            if social_posts:
                # Group by platform
                platform_posts = {}
                for post in social_posts:
                    platform = post.get("platform", "unknown")
                    if platform not in platform_posts:
                        platform_posts[platform] = []
                    platform_posts[platform].append(post)
                
                # Analyze each platform
                for platform, posts in platform_posts.items():
                    sentiment = await self.twitter_analyzer.analyze_sentiment(posts)
                    
                    weight = self.source_weights.get(platform, 0.1)
                    
                    results["sources"][platform] = {
                        "score": sentiment["overall_score"],
                        "label": sentiment["overall_label"],
                        "post_count": sentiment["total_posts"],
                        "weight": weight
                    }
                    
                    weighted_scores.append(sentiment["overall_score"] * weight)
                    
                    logger.info(f"   {platform.capitalize()}: {sentiment['overall_label']} ({sentiment['overall_score']:+.3f})")
        
        # ============================================
        # 3. Pump & Dump Detection
        # ============================================
        if include_pump_detection:
            logger.info("🚨 Checking for pump & dump patterns...")
            
            # Get hype analysis from social media
            if social_posts:
                hype_analysis = self.pump_detector.analyze_social_media_hype(
                    social_posts,
                    time_window_minutes=60
                )
                
                results["pump_dump_warning"] = hype_analysis["risk"] in ["HIGH", "VERY_HIGH"]
                results["hype_analysis"] = hype_analysis
                
                if results["pump_dump_warning"]:
                    logger.warning(f"   🚨 PUMP & DUMP WARNING: {hype_analysis['risk']} risk detected!")
        
        # ============================================
        # 4. Calculate Overall Sentiment
        # ============================================
        if weighted_scores:
            overall_score = sum(weighted_scores) / sum(self.source_weights.values())
            
            # Determine label
            if overall_score > 0.15:
                overall_label = "POSITIVE"
            elif overall_score < -0.15:
                overall_label = "NEGATIVE"
            else:
                overall_label = "NEUTRAL"
            
            # Calculate confidence (based on agreement between sources)
            if len(weighted_scores) > 1:
                # Check if sources agree
                all_positive = all(s > 0 for s in weighted_scores)
                all_negative = all(s < 0 for s in weighted_scores)
                
                if all_positive or all_negative:
                    confidence = 90.0  # High confidence
                elif len(set(s > 0 for s in weighted_scores)) == 2:
                    confidence = 50.0  # Mixed signals
                else:
                    confidence = 70.0  # Moderate confidence
            else:
                confidence = 60.0  # Single source
            
            results["overall_score"] = overall_score
            results["overall_label"] = overall_label
            results["confidence"] = confidence
            
            # Detect conflicts
            if len(weighted_scores) > 1:
                positive_sources = [name for name, data in results["sources"].items() if data["score"] > 0.1]
                negative_sources = [name for name, data in results["sources"].items() if data["score"] < -0.1]
                
                if positive_sources and negative_sources:
                    results["conflicts"].append({
                        "type": "SOURCE_CONFLICT",
                        "positive_sources": positive_sources,
                        "negative_sources": negative_sources,
                        "message": f"Conflicting signals: {', '.join(positive_sources)} vs {', '.join(negative_sources)}"
                    })
        
        # Cache results
        await cache.set("sentiment", results, 300, cache_key)  # 5 min cache
        
        logger.info(f"\n✅ Sentiment aggregation complete:")
        logger.info(f"   Overall: {results['overall_label']} ({results['overall_score']:+.3f})")
        logger.info(f"   Confidence: {results['confidence']:.1f}%")
        logger.info(f"   Sources: {len(results['sources'])}")
        
        if results["conflicts"]:
            logger.warning(f"   ⚠️  Conflicts detected: {len(results['conflicts'])}")
        
        if results["pump_dump_warning"]:
            logger.warning(f"   🚨 Pump & dump warning!")
        
        return results
    
    def get_sentiment_impact(self, sentiment_score: float) -> Dict:
        """
        Determine impact level of sentiment
        
        Args:
            sentiment_score: Score from -1 to +1
            
        Returns:
            Impact analysis
        """
        abs_score = abs(sentiment_score)
        
        if abs_score < 0.15:
            return {
                "impact": "LOW",
                "weight": 0.1,
                "reason": "Sentimen netral, tidak mempengaruhi keputusan"
            }
        elif abs_score < 0.4:
            return {
                "impact": "MODERATE",
                "weight": 0.25,
                "reason": "Sentimen cukup kuat, jadi pertimbangan tambahan"
            }
        elif abs_score < 0.7:
            return {
                "impact": "HIGH",
                "weight": 0.4,
                "reason": "Sentimen kuat, bobot signifikan dalam keputusan"
            }
        else:
            return {
                "impact": "VERY_HIGH",
                "weight": 0.5,
                "reason": "Sentimen sangat kuat (breaking news?), bobot maksimal"
            }
    
    def format_summary(self, results: Dict) -> str:
        """
        Format sentiment results as summary string
        
        Args:
            results: Aggregated sentiment results
            
        Returns:
            Formatted summary
        """
        lines = []
        
        lines.append("=" * 70)
        lines.append("📊 SENTIMENT ANALYSIS SUMMARY")
        lines.append("=" * 70)
        lines.append(f"Currencies: {', '.join(results['currencies'])}")
        lines.append(f"Timestamp: {results['timestamp']}")
        lines.append("")
        
        # Overall sentiment
        emoji = "🟢" if results["overall_label"] == "POSITIVE" else "🔴" if results["overall_label"] == "NEGATIVE" else "⚪"
        lines.append(f"{emoji} OVERALL SENTIMENT: {results['overall_label']}")
        lines.append(f"   Score: {results['overall_score']:+.3f}")
        lines.append(f"   Confidence: {results['confidence']:.1f}%")
        lines.append("")
        
        # Source breakdown
        lines.append("📰 SOURCE BREAKDOWN:")
        for source, data in results["sources"].items():
            source_emoji = "🟢" if data["label"] == "POSITIVE" else "🔴" if data["label"] == "NEGATIVE" else "⚪"
            lines.append(f"   {source_emoji} {source.capitalize()}: {data['label']} ({data['score']:+.3f})")
            lines.append(f"      Articles/Posts: {data['post_count' if 'post_count' in data else 'article_count']}")
            lines.append(f"      Weight: {data['weight']:.0%}")
        lines.append("")
        
        # Conflicts
        if results["conflicts"]:
            lines.append("⚠️  CONFLICTS DETECTED:")
            for conflict in results["conflicts"]:
                lines.append(f"   • {conflict['message']}")
            lines.append("")
        
        # Pump & dump warning
        if results["pump_dump_warning"]:
            lines.append("🚨 PUMP & DUMP WARNING:")
            lines.append(f"   Risk Level: {results['hype_analysis']['risk']}")
            lines.append(f"   Hype Score: {results['hype_analysis']['hype_score']:.1f}")
            lines.append(f"   Recommendation: AVOID TRADING")
            lines.append("")
        
        # Impact
        impact = self.get_sentiment_impact(results["overall_score"])
        lines.append("💡 TRADING IMPACT:")
        lines.append(f"   Impact Level: {impact['impact']}")
        lines.append(f"   Weight in Decision: {impact['weight']:.0%}")
        lines.append(f"   Reason: {impact['reason']}")
        lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)


# Global instance
sentiment_aggregator = SentimentAggregator()
