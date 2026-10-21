"""
News API Integration
Integrasi dengan news API profesional (CryptoPanic, NewsAPI)
"""
import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger


class NewsAPIIntegration:
    """
    Professional news API integration
    
    Supported APIs:
    - CryptoPanic (crypto-specific)
    - NewsAPI (general news)
    - CoinGecko News (crypto news)
    """
    
    def __init__(
        self,
        cryptopanic_api_key: Optional[str] = None,
        newsapi_api_key: Optional[str] = None
    ):
        """
        Initialize news API integration
        
        Args:
            cryptopanic_api_key: CryptoPanic API key (https://cryptopanic.com/developers/api/)
            newsapi_api_key: NewsAPI key (https://newsapi.org/)
        """
        self.cryptopanic_api_key = cryptopanic_api_key
        self.newsapi_api_key = newsapi_api_key
        
        self.session = None
        
        logger.info("📰 News API Integration initialized")
        if cryptopanic_api_key:
            logger.info("   ✅ CryptoPanic API configured")
        if newsapi_api_key:
            logger.info("   ✅ NewsAPI configured")
    
    async def initialize(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close session"""
        if self.session:
            await self.session.close()
    
    async def fetch_cryptopanic_news(
        self,
        currencies: List[str] = ["BTC", "ETH"],
        limit: int = 50,
        filter_type: str = "hot"  # hot, rising, important
    ) -> List[Dict]:
        """
        Fetch news from CryptoPanic API
        
        Args:
            currencies: List of currency codes (BTC, ETH, etc)
            limit: Max number of articles
            filter_type: Filter type (hot, rising, important)
            
        Returns:
            List of news articles
        """
        if not self.cryptopanic_api_key:
            logger.warning("⚠️  CryptoPanic API key not configured")
            return []
        
        try:
            url = "https://cryptopanic.com/api/v1/posts/"
            
            params = {
                "auth_token": self.cryptopanic_api_key,
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
                        "source": item.get("source", {}).get("title", "Unknown"),
                        "link": item.get("url", ""),
                        "published_date": item.get("published_at", ""),
                        "category": "crypto",
                        "votes": {
                            "positive": item.get("votes", {}).get("positive", 0),
                            "negative": item.get("votes", {}).get("negative", 0)
                        }
                    })
                
                logger.info(f"✅ Fetched {len(articles)} articles from CryptoPanic")
                return articles
                
        except Exception as e:
            logger.error(f"❌ Error fetching CryptoPanic news: {e}")
            return []
    
    async def fetch_newsapi_news(
        self,
        query: str = "cryptocurrency OR bitcoin OR ethereum",
        limit: int = 50,
        days_back: int = 1
    ) -> List[Dict]:
        """
        Fetch news from NewsAPI
        
        Args:
            query: Search query
            limit: Max number of articles
            days_back: How many days back to fetch
            
        Returns:
            List of news articles
        """
        if not self.newsapi_api_key:
            logger.warning("⚠️  NewsAPI key not configured")
            return []
        
        try:
            url = "https://newsapi.org/v2/everything"
            
            from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            params = {
                "q": query,
                "from": from_date,
                "sortBy": "relevancy",
                "pageSize": limit,
                "apiKey": self.newsapi_api_key,
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
                        "source": item.get("source", {}).get("name", "Unknown"),
                        "link": item.get("url", ""),
                        "published_date": item.get("publishedAt", ""),
                        "category": "crypto"
                    })
                
                logger.info(f"✅ Fetched {len(articles)} articles from NewsAPI")
                return articles
                
        except Exception as e:
            logger.error(f"❌ Error fetching NewsAPI news: {e}")
            return []
    
    async def fetch_all_news(
        self,
        currencies: List[str] = ["BTC", "ETH"],
        limit_per_source: int = 30
    ) -> List[Dict]:
        """
        Fetch news from all configured sources
        
        Args:
            currencies: List of currency codes
            limit_per_source: Max articles per source
            
        Returns:
            Combined list of news articles
        """
        all_articles = []
        
        # Fetch from CryptoPanic
        cryptopanic_news = await self.fetch_cryptopanic_news(
            currencies=currencies,
            limit=limit_per_source
        )
        all_articles.extend(cryptopanic_news)
        
        # Fetch from NewsAPI
        newsapi_news = await self.fetch_newsapi_news(
            query=" OR ".join(currencies),
            limit=limit_per_source
        )
        all_articles.extend(newsapi_news)
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_articles = []
        
        for article in all_articles:
            title = article.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        logger.info(f"✅ Total unique articles: {len(unique_articles)}")
        return unique_articles
    
    async def save_to_database(self, articles: List[Dict], db):
        """
        Save fetched articles to database
        
        Args:
            articles: List of news articles
            db: DatabaseManager instance
        """
        try:
            saved_count = await db.save_news(articles)
            logger.info(f"✅ Saved {saved_count} articles to database")
        except Exception as e:
            logger.error(f"❌ Error saving articles to database: {e}")


# === USAGE EXAMPLE ===

async def example_usage():
    """Example how to use NewsAPIIntegration"""
    
    # Initialize (with API keys from environment or config)
    news_api = NewsAPIIntegration(
        cryptopanic_api_key="your_cryptopanic_key",
        newsapi_api_key="your_newsapi_key"
    )
    
    await news_api.initialize()
    
    try:
        # Fetch from CryptoPanic
        crypto_news = await news_api.fetch_cryptopanic_news(
            currencies=["BTC", "ETH"],
            limit=20,
            filter_type="hot"
        )
        
        print(f"\n📰 CryptoPanic News ({len(crypto_news)} articles):")
        for article in crypto_news[:3]:
            print(f"  • [{article['source']}] {article['title'][:60]}...")
        
        # Fetch from NewsAPI
        general_news = await news_api.fetch_newsapi_news(
            query="bitcoin",
            limit=20
        )
        
        print(f"\n📰 NewsAPI News ({len(general_news)} articles):")
        for article in general_news[:3]:
            print(f"  • [{article['source']}] {article['title'][:60]}...")
        
        # Fetch from all sources
        all_news = await news_api.fetch_all_news(
            currencies=["BTC", "ETH", "SOL"],
            limit_per_source=15
        )
        
        print(f"\n📰 All News ({len(all_news)} articles)")
        
    finally:
        await news_api.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
