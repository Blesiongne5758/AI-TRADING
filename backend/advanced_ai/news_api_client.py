"""
News API Client
Multi-source news aggregator dengan caching dan rate limiting
"""
import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
from .config import AdvancedAIConfig
from .cache_manager import cache


class NewsAPIClient:
    """
    Multi-source news aggregator
    
    Features:
    - CryptoPanic API (crypto-specific)
    - NewsAPI (general news)
    - CoinGecko News (crypto news)
    - Caching untuk hemat API calls
    - Rate limiting
    - Deduplication
    """
    
    def __init__(self):
        """Initialize news API client"""
        self.session = None
        
        # Rate limiting
        self.last_request_time = {
            "cryptopanic": datetime.min,
            "newsapi": datetime.min,
            "coingecko": datetime.min
        }
        
        logger.info("📰 News API Client initialized")
    
    async def initialize(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession()
        logger.info("✅ News API session initialized")
    
    async def close(self):
        """Close session"""
        if self.session:
            await self.session.close()
            logger.info("🔒 News API session closed")
    
    async def _check_rate_limit(self, source: str) -> bool:
        """
        Check if we can make request (rate limiting)
        
        Args:
            source: API source name
            
        Returns:
            True if can make request, False if rate limited
        """
        now = datetime.now()
        last_request = self.last_request_time[source]
        
        rate_limits = {
            "cryptopanic": timedelta(seconds=60 / AdvancedAIConfig.CRYPTOPANIC_RATE_LIMIT),
            "newsapi": timedelta(seconds=60 / AdvancedAIConfig.NEWSAPI_RATE_LIMIT),
            "coingecko": timedelta(seconds=2)  # CoinGecko: 30 req/min
        }
        
        min_interval = rate_limits.get(source, timedelta(seconds=2))
        
        if now - last_request < min_interval:
            wait_time = (min_interval - (now - last_request)).total_seconds()
            logger.debug(f"Rate limited for {source}, waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
        
        self.last_request_time[source] = datetime.now()
        return True
    
    async def fetch_cryptopanic(
        self,
        currencies: List[str] = ["BTC", "ETH"],
        limit: int = 50,
        filter_type: str = "hot"
    ) -> List[Dict]:
        """
        Fetch news from CryptoPanic API
        
        Args:
            currencies: List of currency codes
            limit: Max articles
            filter_type: Filter type (hot, rising, important)
            
        Returns:
            List of news articles
        """
        if not AdvancedAIConfig.CRYPTOPANIC_API_KEY:
            logger.warning("⚠️  CryptoPanic API key not configured")
            return []
        
        # Check cache first
        cache_key = {
            "source": "cryptopanic",
            "currencies": currencies,
            "limit": limit,
            "filter": filter_type
        }
        
        cached = await cache.get("news", cache_key, AdvancedAIConfig.CACHE_TTL_NEWS)
        if cached:
            logger.info(f"✅ CryptoPanic cache hit: {len(cached)} articles")
            return cached
        
        # Rate limiting
        await self._check_rate_limit("cryptopanic")
        
        try:
            url = "https://cryptopanic.com/api/v1/posts/"
            
            params = {
                "auth_token": AdvancedAIConfig.CRYPTOPANIC_API_KEY,
                "currencies": ",".join(currencies),
                "filter": filter_type,
                "kind": "news",
                "page": 1
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"❌ CryptoPanic API error: {response.status}")
                    return []
                
                data = await response.json()
                articles = []
                
                for item in data.get("results", [])[:limit]:
                    articles.append({
                        "title": item.get("title", ""),
                        "summary": item.get("body", "")[:500],
                        "source": item.get("source", {}).get("title", "CryptoPanic"),
                        "link": item.get("url", ""),
                        "published_date": item.get("published_at", ""),
                        "category": "crypto",
                        "votes": {
                            "positive": item.get("votes", {}).get("positive", 0),
                            "negative": item.get("votes", {}).get("negative", 0)
                        },
                        "api_source": "cryptopanic"
                    })
                
                # Cache results
                await cache.set("news", cache_key, articles)
                
                logger.info(f"✅ Fetched {len(articles)} articles from CryptoPanic")
                return articles
                
        except Exception as e:
            logger.error(f"❌ Error fetching CryptoPanic news: {e}")
            return []
    
    async def fetch_newsapi(
        self,
        query: str = "cryptocurrency OR bitcoin OR ethereum",
        limit: int = 50,
        days_back: int = 1
    ) -> List[Dict]:
        """
        Fetch news from NewsAPI
        
        Args:
            query: Search query
            limit: Max articles
            days_back: How many days back
            
        Returns:
            List of news articles
        """
        if not AdvancedAIConfig.NEWSAPI_API_KEY:
            logger.warning("⚠️  NewsAPI key not configured")
            return []
        
        # Check cache
        cache_key = {
            "source": "newsapi",
            "query": query,
            "limit": limit,
            "days": days_back
        }
        
        cached = await cache.get("news", cache_key, AdvancedAIConfig.CACHE_TTL_NEWS)
        if cached:
            logger.info(f"✅ NewsAPI cache hit: {len(cached)} articles")
            return cached
        
        # Rate limiting
        await self._check_rate_limit("newsapi")
        
        try:
            url = "https://newsapi.org/v2/everything"
            
            from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            params = {
                "q": query,
                "from": from_date,
                "sortBy": "relevancy",
                "pageSize": min(limit, 100),  # API limit
                "apiKey": AdvancedAIConfig.NEWSAPI_API_KEY,
                "language": "en"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"❌ NewsAPI error: {response.status}")
                    return []
                
                data = await response.json()
                articles = []
                
                for item in data.get("articles", []):
                    articles.append({
                        "title": item.get("title", ""),
                        "summary": item.get("description", "") or "",
                        "source": item.get("source", {}).get("name", "NewsAPI"),
                        "link": item.get("url", ""),
                        "published_date": item.get("publishedAt", ""),
                        "category": "crypto",
                        "api_source": "newsapi"
                    })
                
                # Cache results
                await cache.set("news", cache_key, articles)
                
                logger.info(f"✅ Fetched {len(articles)} articles from NewsAPI")
                return articles
                
        except Exception as e:
            logger.error(f"❌ Error fetching NewsAPI news: {e}")
            return []
    
    async def fetch_coingecko_news(
        self,
        coin_id: str = "bitcoin",
        limit: int = 30
    ) -> List[Dict]:
        """
        Fetch news from CoinGecko (free, no API key needed)
        
        Args:
            coin_id: CoinGecko coin ID
            limit: Max articles
            
        Returns:
            List of news articles
        """
        # Check cache
        cache_key = {
            "source": "coingecko",
            "coin_id": coin_id,
            "limit": limit
        }
        
        cached = await cache.get("news", cache_key, AdvancedAIConfig.CACHE_TTL_NEWS)
        if cached:
            logger.info(f"✅ CoinGecko cache hit: {len(cached)} articles")
            return cached
        
        # Rate limiting
        await self._check_rate_limit("coingecko")
        
        try:
            url = f"https://api.coingecko.com/api/v3/news"
            
            params = {
                "per_page": limit
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"❌ CoinGecko API error: {response.status}")
                    return []
                
                data = await response.json()
                articles = []
                
                for item in data.get("data", [])[:limit]:
                    # Filter by coin if needed
                    title = item.get("title", "").lower()
                    if coin_id.lower() in title or coin_id.upper() in title:
                        articles.append({
                            "title": item.get("title", ""),
                            "summary": item.get("description", "")[:500],
                            "source": item.get("author", "CoinGecko"),
                            "link": item.get("url", ""),
                            "published_date": item.get("updated_at", ""),
                            "category": "crypto",
                            "api_source": "coingecko"
                        })
                
                # Cache results
                await cache.set("news", cache_key, articles)
                
                logger.info(f"✅ Fetched {len(articles)} articles from CoinGecko")
                return articles
                
        except Exception as e:
            logger.error(f"❌ Error fetching CoinGecko news: {e}")
            return []
    
    async def fetch_all(
        self,
        currencies: List[str] = ["BTC", "ETH"],
        limit_per_source: int = 30
    ) -> List[Dict]:
        """
        Fetch news from all sources
        
        Args:
            currencies: List of currency codes
            limit_per_source: Max articles per source
            
        Returns:
            Combined list of news articles (deduplicated)
        """
        logger.info(f"📰 Fetching news from all sources for {currencies}...")
        
        # Fetch from all sources concurrently
        tasks = [
            self.fetch_cryptopanic(currencies, limit_per_source),
            self.fetch_newsapi(" OR ".join(currencies), limit_per_source),
        ]
        
        # Add CoinGecko for major coins
        if "BTC" in currencies:
            tasks.append(self.fetch_coingecko_news("bitcoin", limit_per_source))
        if "ETH" in currencies:
            tasks.append(self.fetch_coingecko_news("ethereum", limit_per_source))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine all articles
        all_articles = []
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Error in news fetch: {result}")
        
        # Deduplicate by title
        seen_titles = set()
        unique_articles = []
        
        for article in all_articles:
            title = article.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        logger.info(f"✅ Total unique articles: {len(unique_articles)} (from {len(all_articles)} total)")
        
        return unique_articles
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return cache.get_stats()


# Global instance
news_client = NewsAPIClient()
