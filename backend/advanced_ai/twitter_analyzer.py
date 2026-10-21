"""
Twitter/X Analyzer
Multi-platform social media sentiment analysis (Twitter, Reddit, Telegram)
"""
import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
import re
from .config import AdvancedAIConfig
from .cache_manager import cache


class TwitterAnalyzer:
    """
    Multi-platform social media analyzer
    
    Features:
    - Twitter/X sentiment analysis
    - Reddit crypto sentiment
    - Telegram group monitoring
    - Hype/FUD detection
    - Engagement scoring
    - Coordinated activity detection
    """
    
    def __init__(self, finbert_analyzer=None):
        """
        Initialize Twitter analyzer
        
        Args:
            finbert_analyzer: FinBERT analyzer instance
        """
        self.finbert = finbert_analyzer
        self.session = None
        
        logger.info("📱 Twitter Analyzer initialized")
        logger.info(f"   Twitter: {'✅' if AdvancedAIConfig.ENABLE_TWITTER else '❌'}")
        logger.info(f"   Reddit: {'✅' if AdvancedAIConfig.ENABLE_REDDIT else '❌'}")
        logger.info(f"   Telegram: {'✅' if AdvancedAIConfig.ENABLE_TELEGRAM else '❌'}")
    
    async def initialize(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession()
        logger.info("✅ Twitter analyzer session initialized")
    
    async def close(self):
        """Close session"""
        if self.session:
            await self.session.close()
            logger.info("🔒 Twitter analyzer session closed")
    
    # ============================================
    # Twitter/X Integration
    # ============================================
    
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
            max_results: Max tweets
            start_time: Start time for search
            
        Returns:
            List of tweets
        """
        if not AdvancedAIConfig.ENABLE_TWITTER:
            logger.warning("⚠️  Twitter API not enabled")
            return []
        
        if not AdvancedAIConfig.TWITTER_BEARER_TOKEN:
            logger.warning("⚠️  Twitter API key not configured")
            return []
        
        # Check cache
        cache_key = {
            "platform": "twitter",
            "query": query,
            "max_results": max_results
        }
        
        cached = await cache.get("tweets", cache_key, AdvancedAIConfig.CACHE_TTL_TWEETS)
        if cached:
            logger.info(f"✅ Twitter cache hit: {len(cached)} tweets")
            return cached
        
        try:
            url = "https://api.twitter.com/2/tweets/search/recent"
            
            if start_time is None:
                start_time = datetime.now() - timedelta(hours=24)
            
            params = {
                "query": query,
                "max_results": min(max_results, 100),
                "start_time": start_time.isoformat() + "Z",
                "tweet.fields": "created_at,author_id,public_metrics",
                "expansions": "author_id"
            }
            
            headers = {
                "Authorization": f"Bearer {AdvancedAIConfig.TWITTER_BEARER_TOKEN}"
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
                        "author_id": tweet.get("author_id"),
                        "platform": "twitter"
                    })
                
                # Cache results
                await cache.set("tweets", cache_key, tweets)
                
                logger.info(f"✅ Fetched {len(tweets)} tweets from Twitter")
                return tweets
                
        except Exception as e:
            logger.error(f"❌ Error fetching Twitter tweets: {e}")
            return []
    
    # ============================================
    # Reddit Integration
    # ============================================
    
    async def fetch_reddit_posts(
        self,
        subreddit: str = "cryptocurrency",
        limit: int = 50,
        time_filter: str = "day"
    ) -> List[Dict]:
        """
        Fetch Reddit posts from crypto subreddits
        
        Args:
            subreddit: Subreddit name
            limit: Max posts
            time_filter: Time filter (hour, day, week, month, year, all)
            
        Returns:
            List of Reddit posts
        """
        if not AdvancedAIConfig.ENABLE_REDDIT:
            logger.warning("⚠️  Reddit API not enabled")
            return []
        
        # Check cache
        cache_key = {
            "platform": "reddit",
            "subreddit": subreddit,
            "limit": limit,
            "time": time_filter
        }
        
        cached = await cache.get("tweets", cache_key, AdvancedAIConfig.CACHE_TTL_TWEETS)
        if cached:
            logger.info(f"✅ Reddit cache hit: {len(cached)} posts")
            return cached
        
        try:
            # Reddit public API (no auth needed for read-only)
            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            
            params = {
                "limit": limit,
                "t": time_filter
            }
            
            headers = {
                "User-Agent": "AI-Trading-Agent/1.0"
            }
            
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"❌ Reddit API error: {response.status}")
                    return []
                
                data = await response.json()
                posts = []
                
                for post in data.get("data", {}).get("children", []):
                    post_data = post.get("data", {})
                    
                    posts.append({
                        "id": post_data.get("id"),
                        "text": post_data.get("title", "") + " " + post_data.get("selftext", ""),
                        "created_at": datetime.fromtimestamp(post_data.get("created_utc", 0)).isoformat(),
                        "metrics": {
                            "upvotes": post_data.get("ups", 0),
                            "downvotes": post_data.get("downs", 0),
                            "comments": post_data.get("num_comments", 0)
                        },
                        "author": post_data.get("author"),
                        "subreddit": subreddit,
                        "platform": "reddit"
                    })
                
                # Cache results
                await cache.set("tweets", cache_key, posts)
                
                logger.info(f"✅ Fetched {len(posts)} posts from r/{subreddit}")
                return posts
                
        except Exception as e:
            logger.error(f"❌ Error fetching Reddit posts: {e}")
            return []
    
    # ============================================
    # Telegram Integration
    # ============================================
    
    async def fetch_telegram_messages(
        self,
        channel: str = "crypto",
        limit: int = 50
    ) -> List[Dict]:
        """
        Fetch messages from Telegram channels
        
        Note: Requires Telegram Bot API setup
        
        Args:
            channel: Channel username
            limit: Max messages
            
        Returns:
            List of messages
        """
        if not AdvancedAIConfig.ENABLE_TELEGRAM:
            logger.warning("⚠️  Telegram API not enabled")
            return []
        
        if not AdvancedAIConfig.TELEGRAM_BOT_TOKEN:
            logger.warning("⚠️  Telegram bot token not configured")
            return []
        
        # Check cache
        cache_key = {
            "platform": "telegram",
            "channel": channel,
            "limit": limit
        }
        
        cached = await cache.get("tweets", cache_key, AdvancedAIConfig.CACHE_TTL_TWEETS)
        if cached:
            logger.info(f"✅ Telegram cache hit: {len(cached)} messages")
            return cached
        
        try:
            # Telegram Bot API
            url = f"https://api.telegram.org/bot{AdvancedAIConfig.TELEGRAM_BOT_TOKEN}/getUpdates"
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"❌ Telegram API error: {response.status}")
                    return []
                
                data = await response.json()
                messages = []
                
                for update in data.get("result", [])[:limit]:
                    message = update.get("message", {})
                    
                    messages.append({
                        "id": message.get("message_id"),
                        "text": message.get("text", ""),
                        "created_at": datetime.fromtimestamp(message.get("date", 0)).isoformat(),
                        "metrics": {},
                        "author": message.get("from", {}).get("username"),
                        "channel": channel,
                        "platform": "telegram"
                    })
                
                # Cache results
                await cache.set("tweets", cache_key, messages)
                
                logger.info(f"✅ Fetched {len(messages)} messages from Telegram")
                return messages
                
        except Exception as e:
            logger.error(f"❌ Error fetching Telegram messages: {e}")
            return []
    
    # ============================================
    # Sentiment Analysis
    # ============================================
    
    async def analyze_sentiment(
        self,
        posts: List[Dict]
    ) -> Dict:
        """
        Analyze sentiment of social media posts
        
        Args:
            posts: List of posts from any platform
            
        Returns:
            Sentiment analysis results
        """
        if not self.finbert:
            logger.warning("⚠️  FinBERT analyzer not configured")
            return {
                "overall_score": 0.0,
                "overall_label": "NEUTRAL",
                "total_posts": 0,
                "posts": []
            }
        
        if not posts:
            return {
                "overall_score": 0.0,
                "overall_label": "NENEUTRAL",
                "total_posts": 0,
                "posts": []
            }
        
        # Extract text from posts
        texts = [post.get("text", "") for post in posts]
        
        # Analyze with FinBERT
        sentiments = self.finbert.analyze_batch(texts)
        
        # Build results
        post_results = []
        scores = []
        
        for post, sentiment in zip(posts, sentiments):
            post_results.append({
                "id": post.get("id"),
                "text": post.get("text"),
                "platform": post.get("platform"),
                "metrics": post.get("metrics", {}),
                "sentiment": sentiment
            })
            scores.append(sentiment["sentiment_score"])
        
        # Calculate overall metrics
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        positive_count = sum(1 for s in scores if s > 0.1)
        negative_count = sum(1 for s in scores if s < -0.1)
        neutral_count = len(scores) - positive_count - negative_count
        
        if avg_score > AdvancedAIConfig.SENTIMENT_POSITIVE_THRESHOLD:
            overall_label = "POSITIVE"
        elif avg_score < AdvancedAIConfig.SENTIMENT_NEGATIVE_THRESHOLD:
            overall_label = "NEGATIVE"
        else:
            overall_label = "NEUTRAL"
        
        return {
            "overall_score": avg_score,
            "overall_label": overall_label,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "total_posts": len(posts),
            "posts": post_results
        }
    
    # ============================================
    # Hype & FUD Detection
    # ============================================
    
    def detect_hype_keywords(self, text: str) -> List[str]:
        """Detect hype/pump keywords"""
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
        return [kw for kw in hype_keywords if kw in text_lower]
    
    def detect_fud_keywords(self, text: str) -> List[str]:
        """Detect FUD keywords"""
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
        return [kw for kw in fud_keywords if kw in text_lower]
    
    def calculate_engagement_score(self, metrics: Dict, platform: str) -> float:
        """
        Calculate engagement score from metrics
        
        Args:
            metrics: Platform-specific metrics
            platform: Platform name
            
        Returns:
            Engagement score (0-100)
        """
        if platform == "twitter":
            likes = metrics.get("like_count", 0)
            retweets = metrics.get("retweet_count", 0)
            replies = metrics.get("reply_count", 0)
            quotes = metrics.get("quote_count", 0)
            
            score = (
                likes * 1 +
                retweets * 3 +
                replies * 2 +
                quotes * 2
            )
            
        elif platform == "reddit":
            upvotes = metrics.get("upvotes", 0)
            comments = metrics.get("comments", 0)
            
            score = upvotes * 1 + comments * 5
            
        else:
            score = 0
        
        return min(score / 100, 100)  # Normalize to 0-100
    
    # ============================================
    # Multi-Platform Fetching
    # ============================================
    
    async def fetch_all_social_media(
        self,
        query: str = "bitcoin OR BTC",
        limit_per_platform: int = 30
    ) -> List[Dict]:
        """
        Fetch from all social media platforms
        
        Args:
            query: Search query
            limit_per_platform: Max posts per platform
            
        Returns:
            Combined list of posts
        """
        logger.info(f"📱 Fetching social media for: {query}")
        
        tasks = []
        
        # Twitter
        if AdvancedAIConfig.ENABLE_TWITTER:
            tasks.append(self.fetch_twitter_mentions(query, limit_per_platform))
        
        # Reddit
        if AdvancedAIConfig.ENABLE_REDDIT:
            tasks.append(self.fetch_reddit_posts("cryptocurrency", limit_per_platform))
            tasks.append(self.fetch_reddit_posts("bitcoin", limit_per_platform))
        
        # Telegram
        if AdvancedAIConfig.ENABLE_TELEGRAM:
            tasks.append(self.fetch_telegram_messages("crypto", limit_per_platform))
        
        if not tasks:
            logger.warning("⚠️  No social media platforms enabled")
            return []
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_posts = []
        for result in results:
            if isinstance(result, list):
                all_posts.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Error in social media fetch: {result}")
        
        logger.info(f"✅ Total posts: {len(all_posts)}")
        
        return all_posts


# Global instance
twitter_analyzer = TwitterAnalyzer()
