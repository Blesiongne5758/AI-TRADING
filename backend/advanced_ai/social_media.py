"""
Social Media Analyzer
Analisis sentimen dari Twitter/X dan social media lainnya
"""
import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
import re


class SocialMediaAnalyzer:
    """
    Social media sentiment analyzer
    
    Features:
    - Twitter/X sentiment analysis
    - Reddit crypto sentiment
    - Telegram group monitoring
    - Social media trend detection
    """
    
    def __init__(
        self,
        twitter_bearer_token: Optional[str] = None,
        finbert_analyzer=None
    ):
        """
        Initialize social media analyzer
        
        Args:
            twitter_bearer_token: Twitter API Bearer Token
            finbert_analyzer: FinBERT analyzer instance for sentiment
        """
        self.twitter_bearer_token = twitter_bearer_token
        self.finbert = finbert_analyzer
        self.session = None
        
        logger.info("📱 Social Media Analyzer initialized")
        if twitter_bearer_token:
            logger.info("   ✅ Twitter API configured")
    
    async def initialize(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close session"""
        if self.session:
            await self.session.close()
    
    async def fetch_twitter_mentions(
        self,
        query: str = "bitcoin OR BTC",
        max_results: int = 100,
        start_time: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Fetch tweets mentioning cryptocurrency
        
        Args:
            query: Search query
            max_results: Max number of tweets
            start_time: Start time for search
            
        Returns:
            List of tweets
        """
        if not self.twitter_bearer_token:
            logger.warning("⚠️  Twitter API not configured")
            return []
        
        try:
            url = "https://api.twitter.com/2/tweets/search/recent"
            
            if start_time is None:
                start_time = datetime.now() - timedelta(hours=24)
            
            params = {
                "query": query,
                "max_results": min(max_results, 100),  # API limit
                "start_time": start_time.isoformat() + "Z",
                "tweet.fields": "created_at,author_id,public_metrics",
                "expansions": "author_id"
            }
            
            headers = {
                "Authorization": f"Bearer {self.twitter_bearer_token}"
            }
            
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"❌ Twitter API error: {response.status}")
                    return []
                
                data = await response.json()
                tweets = []
                
                for tweet in data.get("data", []):
                    tweets.append({
                        "id": tweet.get("id"),
                        "text": tweet.get("text", ""),
                        "created_at": tweet.get("created_at"),
                        "metrics": tweet.get("public_metrics", {}),
                        "author_id": tweet.get("author_id")
                    })
                
                logger.info(f"✅ Fetched {len(tweets)} tweets from Twitter")
                return tweets
                
        except Exception as e:
            logger.error(f"❌ Error fetching Twitter tweets: {e}")
            return []
    
    async def analyze_twitter_sentiment(
        self,
        query: str = "bitcoin OR BTC",
        max_results: int = 50
    ) -> Dict:
        """
        Analyze sentiment of Twitter mentions
        
        Args:
            query: Search query
            max_results: Max tweets to analyze
            
        Returns:
            Sentiment analysis results
        """
        if not self.finbert:
            logger.warning("⚠️  FinBERT analyzer not configured")
            return {}
        
        # Fetch tweets
        tweets = await self.fetch_twitter_mentions(query, max_results)
        
        if not tweets:
            return {
                "overall_score": 0.0,
                "overall_label": "NEUTRAL",
                "total_tweets": 0,
                "tweets": []
            }
        
        # Analyze sentiment
        texts = [tweet["text"] for tweet in tweets]
        sentiments = self.finbert.analyze_batch(texts)
        
        # Build results
        tweet_results = []
        scores = []
        
        for tweet, sentiment in zip(tweets, sentiments):
            tweet_results.append({
                "id": tweet["id"],
                "text": tweet["text"],
                "created_at": tweet["created_at"],
                "metrics": tweet["metrics"],
                "sentiment": sentiment
            })
            scores.append(sentiment["sentiment_score"])
        
        # Calculate overall metrics
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        positive_count = sum(1 for s in scores if s > 0.1)
        negative_count = sum(1 for s in scores if s < -0.1)
        neutral_count = len(scores) - positive_count - negative_count
        
        if avg_score > 0.15:
            overall_label = "POSITIVE"
        elif avg_score < -0.15:
            overall_label = "NEGATIVE"
        else:
            overall_label = "NEUTRAL"
        
        return {
            "overall_score": avg_score,
            "overall_label": overall_label,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "total_tweets": len(tweets),
            "tweets": tweet_results
        }
    
    def detect_hype_keywords(self, text: str) -> List[str]:
        """
        Detect hype/pump keywords in text
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected hype keywords
        """
        hype_keywords = [
            "moon", "mooning", "pump", "pumping",
            "100x", "1000x", "10x",
            "gem", "gems",
            "buy now", "buying",
            "to the moon", "ttm",
            "rocket", "rockets",
            "bullish", "bullrun",
            "breakout", "breaking out",
            "skyrocket", "skyrocketing"
        ]
        
        text_lower = text.lower()
        detected = [kw for kw in hype_keywords if kw in text_lower]
        
        return detected
    
    def detect_fud_keywords(self, text: str) -> List[str]:
        """
        Detect FUD (Fear, Uncertainty, Doubt) keywords
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected FUD keywords
        """
        fud_keywords = [
            "crash", "crashing",
            "dump", "dumping",
            "scam", "rug pull", "rugpull",
            "bearish", "bear market",
            "sell", "selling",
            "panic", "panicking",
            "fear", "afraid",
            "bubble", "bursting",
            "ban", "banned", "regulation",
            "hack", "hacked",
            "exploit", "exploited"
        ]
        
        text_lower = text.lower()
        detected = [kw for kw in fud_keywords if kw in text_lower]
        
        return detected
    
    def calculate_engagement_score(self, metrics: Dict) -> float:
        """
        Calculate engagement score from Twitter metrics
        
        Args:
            metrics: Twitter public metrics
            
        Returns:
            Engagement score (0-100)
        """
        likes = metrics.get("like_count", 0)
        retweets = metrics.get("retweet_count", 0)
        replies = metrics.get("reply_count", 0)
        quotes = metrics.get("quote_count", 0)
        
        # Weighted score
        score = (
            likes * 1 +
            retweets * 3 +  # Retweets more valuable
            replies * 2 +   # Replies show engagement
            quotes * 2      # Quotes show discussion
        )
        
        # Normalize to 0-100
        normalized = min(score / 100, 100)
        
        return normalized


# === USAGE EXAMPLE ===

async def example_usage():
    """Example how to use SocialMediaAnalyzer"""
    
    # Initialize
    from .finbert_analyzer import FinBERTAnalyzer
    
    finbert = FinBERTAnalyzer()
    await finbert.initialize()
    
    analyzer = SocialMediaAnalyzer(
        twitter_bearer_token="your_twitter_token",
        finbert_analyzer=finbert
    )
    
    await analyzer.initialize()
    
    try:
        # Analyze Twitter sentiment
        result = await analyzer.analyze_twitter_sentiment(
            query="bitcoin OR BTC",
            max_results=50
        )
        
        print(f"\n📱 Twitter Sentiment Analysis:")
        print(f"   Overall: {result['overall_label']} ({result['overall_score']:+.3f})")
        print(f"   Total tweets: {result['total_tweets']}")
        print(f"   Positive: {result['positive_count']}")
        print(f"   Negative: {result['negative_count']}")
        print(f"   Neutral: {result['neutral_count']}")
        
        # Detect hype/FUD in sample tweet
        sample_tweet = "Bitcoin is going to the moon! 🚀 100x incoming!"
        hype_keywords = analyzer.detect_hype_keywords(sample_tweet)
        print(f"\n🔥 Hype keywords detected: {hype_keywords}")
        
        sample_fud = "Crypto market crashing, everyone selling in panic"
        fud_keywords = analyzer.detect_fud_keywords(sample_fud)
        print(f"😨 FUD keywords detected: {fud_keywords}")
        
    finally:
        await analyzer.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
