"""
News API Client
Mengumpulkan berita dari multiple sumber profesional
"""
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import (
    CRYPTOPANIC_API_KEY,
    NEWSAPI_API_KEY,
    GNEWS_API_KEY,
)
from .cache_manager import cache


class NewsAPIClient:
    """Multi-source news aggregator"""

    def __init__(self):
        self.session = None
        self.sources_enabled = self._check_sources()

    def _check_sources(self) -> Dict[str, bool]:
        """Cek API key mana yang tersedia"""
        return {
            "cryptopanic": bool(CRYPTOPANIC_API_KEY),
            "newsapi": bool(NEWSAPI_API_KEY),
            "gnews": bool(GNEWS_API_KEY),
        }

    async def _ensure_session(self):
        """Buat HTTP session jika belum ada"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)

    async def close(self):
        """Tutup session"""
        if self.session and not self.session.closed:
            await self.session.close()

    # ============================================
    # CRYPTOPANIC (KHUSUS CRYPTO - GRATIS)
    # ============================================
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def fetch_cryptopanic(
        self,
        currencies: List[str] = None,
        limit: int = 50,
        filter_type: str = "hot",  # hot, rising, important, bullish, bearish
    ) -> List[Dict]:
        """
        Ambil berita dari CryptoPanic (sumber terbaik untuk crypto)
        
        Args:
            currencies: Filter by currency (misal: ["BTC", "ETH"])
            limit: Jumlah berita
            filter_type: hot, rising, important, bullish, bearish, saved
        """
        if not self.sources_enabled["cryptopanic"]:
            return []

        await self._ensure_session()

        # Cek cache
        cache_key = f"cryptopanic:{','.join(currencies or ['all'])}:{filter_type}:{limit}"
        cached = await cache.get("news", cache_key)
        if cached:
            return cached

        url = "https://cryptopanic.com/api/v1/posts/"
        params = {
            "auth_token": CRYPTOPANIC_API_KEY,
            "kind": "news",
            "filter": filter_type,
            "page": 1,
        }

        if currencies:
            params["currencies"] = ",".join(currencies)

        try:
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.warning(f"CryptoPanic error: {response.status}")
                    return []

                data = await response.json()
                articles = []

                for item in data.get("results", [])[:limit]:
                    # Extract currencies mentioned
                    mentioned_currencies = [
                        c["code"] for c in item.get("currencies", [])
                    ]

                    # Extract votes (community sentiment)
                    votes = item.get("votes", {})
                    community_score = (
                        votes.get("positive", 0) - votes.get("negative", 0)
                    )

                    articles.append({
                        "source": "cryptopanic",
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "published_at": item.get("published_at"),
                        "summary": item.get("body", "")[:500],
                        "currencies": mentioned_currencies,
                        "community_votes": votes,
                        "community_score": community_score,
                        "importance": "high" if item.get("important") else "normal",
                        "kind": item.get("kind", "news"),
                    })

                # Cache 5 menit
                await cache.set("news", articles, 300, cache_key)
                logger.info(f"📰 CryptoPanic: {len(articles)} articles fetched")
                return articles

        except Exception as e:
            logger.error(f"CryptoPanic fetch error: {e}")
            return []

    # ============================================
    # NEWSAPI.ORG (UMUM - FREEMIUM)
    # ============================================
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def fetch_newsapi(
        self,
        query: str = "cryptocurrency OR bitcoin OR ethereum",
        limit: int = 30,
        days_back: int = 1,
    ) -> List[Dict]:
        """Ambil berita dari NewsAPI.org"""
        if not self.sources_enabled["newsapi"]:
            return []

        await self._ensure_session()

        cache_key = f"newsapi:{query}:{limit}:{days_back}"
        cached = await cache.get("news", cache_key)
        if cached:
            return cached

        url = "https://newsapi.org/v2/everything"
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        params = {
            "q": query,
            "from": from_date,
            "sortBy": "relevancy",
            "pageSize": limit,
            "language": "en",
            "apiKey": NEWSAPI_API_KEY,
        }

        try:
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.warning(f"NewsAPI error: {response.status}")
                    return []

                data = await response.json()
                articles = []

                for item in data.get("articles", []):
                    articles.append({
                        "source": f"newsapi/{item.get('source', {}).get('name', 'unknown')}",
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "published_at": item.get("publishedAt"),
                        "summary": (item.get("description") or "")[:500],
                        "content": (item.get("content") or "")[:1000],
                        "author": item.get("author"),
                    })

                await cache.set("news", articles, 300, cache_key)
                logger.info(f"📰 NewsAPI: {len(articles)} articles fetched")
                return articles

        except Exception as e:
            logger.error(f"NewsAPI fetch error: {e}")
            return []

    # ============================================
    # GNEWS (GRATIS ALTERNATIF)
    # ============================================
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def fetch_gnews(
        self,
        query: str = "cryptocurrency",
        limit: int = 30,
    ) -> List[Dict]:
        """Ambil berita dari GNews"""
        if not self.sources_enabled["gnews"]:
            return []

        await self._ensure_session()

        cache_key = f"gnews:{query}:{limit}"
        cached = await cache.get("news", cache_key)
        if cached:
            return cached

        url = "https://gnews.io/api/v4/search"
        params = {
            "q": query,
            "lang": "en",
            "max": limit,
            "apikey": GNEWS_API_KEY,
        }

        try:
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.warning(f"GNews error: {response.status}")
                    return []

                data = await response.json()
                articles = []

                for item in data.get("articles", []):
                    articles.append({
                        "source": f"gnews/{item.get('source', {}).get('name', 'unknown')}",
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "published_at": item.get("publishedAt"),
                        "summary": (item.get("description") or "")[:500],
                        "content": (item.get("content") or "")[:1000],
                    })

                await cache.set("news", articles, 300, cache_key)
                logger.info(f"📰 GNews: {len(articles)} articles fetched")
                return articles

        except Exception as e:
            logger.error(f"GNews fetch error: {e}")
            return []

    # ============================================
    # AGGREGATOR
    # ============================================
    async def fetch_all_news(
        self,
        currencies: List[str] = None,
        limit_per_source: int = 30,
    ) -> List[Dict]:
        """
        Ambil berita dari SEMUA sumber yang tersedia secara paralel
        """
        logger.info("📰 Fetching news from all sources...")

        tasks = []

        # CryptoPanic (paling penting untuk crypto)
        if self.sources_enabled["cryptopanic"]:
            tasks.append(self.fetch_cryptopanic(currencies=currencies, limit=limit_per_source))

        # NewsAPI
        if self.sources_enabled["newsapi"]:
            query = " OR ".join(currencies) if currencies else "cryptocurrency OR bitcoin"
            tasks.append(self.fetch_newsapi(query=query, limit=limit_per_source))

        # GNews
        if self.sources_enabled["gnews"]:
            query = " OR ".join(currencies) if currencies else "cryptocurrency"
            tasks.append(self.fetch_gnews(query=query, limit=limit_per_source))

        if not tasks:
            logger.warning("⚠️  No news sources enabled! Check API keys in .env")
            return []

        # Jalankan paralel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Gabungkan semua
        all_articles = []
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"News source error: {result}")

        # Sort by published date (terbaru dulu)
        all_articles.sort(
            key=lambda x: x.get("published_at") or "",
            reverse=True,
        )

        # Hapus duplikat berdasarkan title
        seen_titles = set()
        unique_articles = []
        for article in all_articles:
            title_key = article["title"].lower().strip()[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_articles.append(article)

        logger.info(f"✅ Total unique articles: {len(unique_articles)}")
        return unique_articles

    def get_enabled_sources(self) -> Dict[str, bool]:
        """Info sumber yang aktif"""
        return self.sources_enabled
