"""
News Scraper - Mengumpulkan berita dari berbagai RSS feed

File ini bertanggung jawab untuk:
1. Mengambil berita crypto dari RSS feeds (CoinDesk, CoinTelegraph, Decrypt)
2. Parse artikel berita (title, summary, link, published_date)
3. Menyimpan berita ke database

Untuk pemula:
- RSS (Really Simple Syndication) = format untuk distribute berita
- feedparser = library untuk parse RSS feeds
- Kita fetch berita setiap 15 menit (configurable)
- Berita disimpan ke database untuk analisis sentimen di Fase 2

Alur kerja:
1. Parse RSS feed dari setiap source
2. Extract artikel (title, link, summary, date)
3. Save ke database (hindari duplikasi)
4. Loop setiap 15 menit
"""

import asyncio
import feedparser
from datetime import datetime
from typing import List, Dict
from loguru import logger
from data_collector.config import NEWS_FEEDS, NEWS_FETCH_INTERVAL
from data_collector.database import DatabaseManager


class NewsScraper:
    """
    Mengumpulkan berita crypto dari RSS feeds.
    
    Class ini menangani:
    - Parse RSS feeds dari multiple sources
    - Extract artikel berita
    - Save ke database (dengan deduplication)
    - Periodic fetching (setiap 15 menit)
    
    Attributes:
        db: DatabaseManager instance untuk save data
        running: Boolean flag untuk kontrol loop
    """

    def __init__(self, db: DatabaseManager):
        """
        Initialize NewsScraper.
        
        Args:
            db: DatabaseManager instance untuk save data
        """
        self.db = db
        self.running = False

    def parse_feed(self, feed_config: Dict) -> List[Dict]:
        """
        Mengparse satu RSS feed menjadi list artikel.
        
        Args:
            feed_config: Dictionary dengan info feed (name, url, category)
        
        Returns:
            List of article dictionaries
        
        Contoh feed_config:
            {
                "name": "CoinDesk",
                "url": "https://www.coindesk.com/arc/outboundfeeds/rss/",
                "category": "crypto"
            }
        
        Contoh return:
            [
                {
                    "source": "CoinDesk",
                    "title": "Bitcoin reaches new high",
                    "link": "https://coindesk.com/...",
                    "published_date": 1642684522000,
                    "summary": "Bitcoin price surged...",
                    "category": "crypto"
                },
                ...
            ]
        
        Note:
            - Ambil max 20 artikel terbaru per feed
            - Summary di-truncate ke 500 karakter
            - Error pada 1 feed tidak akan menghentikan feed lain
        """
        try:
            feed = feedparser.parse(feed_config["url"])
            articles = []

            for entry in feed.entries[:20]:  # Ambil 20 artikel terbaru
                # Parse tanggal publikasi
                published_date = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_date = int(
                        datetime(*entry.published_parsed[:6]).timestamp() * 1000
                    )

                # Bersihkan summary (hapus HTML tags sederhana)
                summary = entry.get("summary", "")
                if len(summary) > 500:
                    summary = summary[:500] + "..."

                articles.append(
                    {
                        "source": feed_config["name"],
                        "title": entry.get("title", "").strip(),
                        "link": entry.get("link", "").strip(),
                        "published_date": published_date,
                        "summary": summary,
                        "category": feed_config.get("category", "general"),
                    }
                )

            return articles

        except Exception as e:
            logger.error(f"❌ Error parsing {feed_config['name']}: {e}")
            return []

    async def fetch_all_news(self) -> List[Dict]:
        """
        Mengambil berita dari semua sumber.
        
        Returns:
            List of all articles from all sources
        
        Note:
            - Menggunakan asyncio.to_thread untuk parse feed (blocking operation)
            - Semua artikel di-save ke database
            - Database akan handle deduplication (berita dengan link sama di-skip)
        """
        logger.info("📰 Fetching news from all sources...")

        all_articles = []
        for feed_config in NEWS_FEEDS:
            # Parse feed di thread terpisah (karena feedparser blocking)
            articles = await asyncio.to_thread(self.parse_feed, feed_config)
            all_articles.extend(articles)
            logger.info(f"📰 {feed_config['name']}: {len(articles)} articles")

        # Simpan ke database
        await self.db.save_news(all_articles)
        return all_articles

    async def start(self) -> None:
        """
        Loop untuk mengambil berita secara periodik.
        
        Alur:
        1. Ambil berita sekali saat startup
        2. Loop setiap NEWS_FETCH_INTERVAL detik (default 900 = 15 menit)
        3. Stop jika self.running = False
        
        Note:
            - Error pada 1 cycle tidak akan menghentikan loop
            - Jika error, tunggu 30 detik sebelum retry
        """
        self.running = True
        logger.info(
            f"🔄 Starting news scraper (interval: {NEWS_FETCH_INTERVAL}s)"
        )

        # Ambil berita sekali saat startup
        await self.fetch_all_news()

        # Loop periodik
        while self.running:
            try:
                await asyncio.sleep(NEWS_FETCH_INTERVAL)
                await self.fetch_all_news()
            except asyncio.CancelledError:
                # Loop dibatalkan (shutdown)
                break
            except Exception as e:
                logger.error(f"❌ News scraper error: {e}")
                await asyncio.sleep(30)

    async def stop(self) -> None:
        """
        Menghentikan scraper.
        
        Set running = False untuk stop loop.
        """
        self.running = False
        logger.info("🛑 News scraper stopped")


# ============================================
# STANDALONE TESTING
# ============================================

async def test_scraper():
    """
    Test NewsScraper secara standalone.
    
    Cara menjalankan:
        python -m data_collector.news_scraper
    """
    logger.info("Testing NewsScraper...")
    
    # Initialize database
    db = DatabaseManager()
    await db.initialize()
    
    # Create scraper
    scraper = NewsScraper(db)
    
    try:
        # Fetch news once
        articles = await scraper.fetch_all_news()
        logger.info(f"✅ Fetched {len(articles)} total articles")
        
        # Show sample articles
        for i, article in enumerate(articles[:3]):
            logger.info(f"\n📰 Article {i+1}:")
            logger.info(f"   Source: {article['source']}")
            logger.info(f"   Title: {article['title']}")
            logger.info(f"   Link: {article['link']}")
            logger.info(f"   Category: {article['category']}")
        
        # Get news from database
        news = await db.get_latest_news(limit=10)
        logger.info(f"\n✅ Retrieved {len(news)} news from database")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
    
    logger.info("✅ Test completed")


if __name__ == "__main__":
    asyncio.run(test_scraper())
