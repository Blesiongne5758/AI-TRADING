"""
News Scraper & Sentiment Analysis

Modul ini bertanggung jawab untuk:
1. Mengambil berita crypto dari RSS feeds (CoinDesk, CoinTelegraph, dll)
2. Menganalisis sentimen berita menggunakan FinBERT (AI model)
3. Menyimpan berita dan sentimen ke database

Untuk pemula:
- RSS (Really Simple Syndication) adalah format untuk distribute berita
- FinBERT adalah AI model yang dilatih khusus untuk financial text
- Sentimen score: -1.0 (sangat negatif/bearish) sampai +1.0 (sangat positif/bullish)
- Kita fetch berita setiap 15 menit untuk analisis real-time

Alur kerja:
1. Fetch RSS feed dari multiple sources
2. Parse berita (title, summary, published date)
3. Analisis sentimen dengan FinBERT
4. Simpan ke database dengan sentiment score
"""

import asyncio
import feedparser
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
import re

from data_collector.config import (
    NEWS_FEEDS,
    NEWS_FETCH_INTERVAL,
    SENTIMENT_MODEL,
)
from data_collector.database import DatabaseManager


class SentimentAnalyzer:
    """
    Sentiment analyzer menggunakan FinBERT model.
    
    FinBERT adalah model AI yang dilatih khusus untuk financial text.
    Model ini bisa menganalisis apakah berita bersifat:
    - Bullish (positif untuk harga)
    - Bearish (negatif untuk harga)
    - Neutral (tidak ada dampak signifikan)
    
    Attributes:
        model: Hugging Face transformers pipeline
        initialized: Boolean flag untuk status initialization
    """
    
    def __init__(self):
        """Initialize sentiment analyzer."""
        self.pipeline = None
        self.initialized = False
        
        logger.info("SentimentAnalyzer created (lazy initialization)")
    
    async def initialize(self) -> None:
        """
        Initialize FinBERT model.
        
        Ini akan download model dari Hugging Face jika belum ada.
        Model size: ~440MB, pertama kali butuh beberapa menit.
        
        Note: Initialization dilakukan async karena model loading blocking.
        """
        if self.initialized:
            return
        
        try:
            logger.info(f"Loading sentiment model: {SENTIMENT_MODEL}")
            
            # Import transformers (lazy import untuk speed up startup)
            from transformers import pipeline
            
            # Load model in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            self.pipeline = await loop.run_in_executor(
                None,
                lambda: pipeline(
                    "sentiment-analysis",
                    model=SENTIMENT_MODEL,
                    tokenizer=SENTIMENT_MODEL,
                    max_length=512,
                    truncation=True
                )
            )
            
            self.initialized = True
            logger.info("Sentiment model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            logger.warning("Sentiment analysis will be disabled")
            raise
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a text.
        
        Args:
            text: Text to analyze (news title + summary)
        
        Returns:
            Dictionary with sentiment analysis results:
            {
                "score": float,  # -1.0 to 1.0
                "label": str,    # "bullish", "bearish", "neutral"
                "confidence": float  # 0.0 to 1.0
            }
        
        Contoh:
            >>> await analyzer.analyze_sentiment("Bitcoin price surges to new all-time high")
            {
                "score": 0.85,
                "label": "bullish",
                "confidence": 0.92
            }
        """
        if not self.initialized:
            await self.initialize()
        
        if not self.pipeline:
            # Return neutral if model not available
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0
            }
        
        try:
            # Clean text
            text = self._clean_text(text)
            
            if not text:
                return {
                    "score": 0.0,
                    "label": "neutral",
                    "confidence": 0.0
                }
            
            # Analyze with FinBERT
            # Run in thread pool to avoid blocking async loop
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.pipeline(text[:512])  # Limit text length
            )
            
            # Parse result
            # FinBERT returns: [{"label": "positive", "score": 0.95}]
            # or: [{"label": "negative", "score": 0.87}]
            # or: [{"label": "neutral", "score": 0.72}]
            
            label = result[0]['label'].lower()
            confidence = result[0]['score']
            
            # Convert to our format
            if label == 'positive':
                sentiment_label = 'bullish'
                sentiment_score = confidence  # 0.0 to 1.0
            elif label == 'negative':
                sentiment_label = 'bearish'
                sentiment_score = -confidence  # -1.0 to 0.0
            else:  # neutral
                sentiment_label = 'neutral'
                sentiment_score = 0.0
            
            return {
                "score": sentiment_score,
                "label": sentiment_label,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0
            }
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text for sentiment analysis.
        
        Args:
            text: Raw text
        
        Returns:
            Cleaned text
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()


class NewsScraper:
    """
    News scraper untuk mengambil berita dari RSS feeds.
    
    Class ini menangani:
    - Fetch RSS feeds dari multiple sources
    - Parse news articles
    - Deduplication (hindari berita duplikat)
    - Sentiment analysis integration
    
    Attributes:
        sources: List of RSS feed URLs
        analyzer: SentimentAnalyzer instance
        running: Boolean flag untuk kontrol loop
    """
    
    def __init__(self, sources: Optional[List[str]] = None, db: Optional[DatabaseManager] = None):
        """
        Initialize NewsScraper.
        
        Args:
            sources: List of RSS feed URLs. Default dari config.
            db: DatabaseManager instance. Default akan dibuat baru.
        """
        # Extract URLs dari NEWS_FEEDS (list of dicts)
        default_urls = [feed["url"] for feed in NEWS_FEEDS]
        self.sources = sources or default_urls
        self.db = db or DatabaseManager()
        self.analyzer = SentimentAnalyzer()
        self.running = False
        
        # Statistics
        self.news_fetched = 0
        self.news_saved = 0
        self.last_fetch_time: Optional[datetime] = None
        
        logger.info(f"NewsScraper initialized with {len(self.sources)} sources")
    
    async def initialize(self) -> None:
        """
        Initialize sentiment analyzer.
        """
        await self.analyzer.initialize()
    
    async def fetch_rss_feed(self, url: str) -> List[Dict[str, Any]]:
        """
        Fetch and parse RSS feed.
        
        Args:
            url: RSS feed URL
        
        Returns:
            List of news dictionaries
        
        Contoh return:
            [
                {
                    "title": "Bitcoin reaches $50,000",
                    "source": "CoinDesk",
                    "url": "https://coindesk.com/...",
                    "published_at": datetime(2024, 1, 15, 10, 30),
                    "summary": "Bitcoin price surged today..."
                },
                ...
            ]
        """
        try:
            logger.debug(f"Fetching RSS feed: {url}")
            
            # Parse RSS feed
            # Note: feedparser is synchronous, run in thread pool
            loop = asyncio.get_event_loop()
            feed = await loop.run_in_executor(
                None,
                lambda: feedparser.parse(url)
            )
            
            news_items = []
            
            for entry in feed.entries:
                try:
                    # Extract published date
                    published_at = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_at = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published_at = datetime(*entry.updated_parsed[:6])
                    else:
                        published_at = datetime.utcnow()
                    
                    # Extract summary
                    summary = None
                    if hasattr(entry, 'summary'):
                        summary = entry.summary
                    elif hasattr(entry, 'description'):
                        summary = entry.description
                    
                    # Clean summary (remove HTML)
                    if summary:
                        summary = re.sub(r'<[^>]+>', '', summary)
                        summary = summary.strip()[:500]  # Limit length
                    
                    news_item = {
                        "title": entry.title,
                        "source": feed.feed.get('title', url),
                        "url": entry.get('link', ''),
                        "published_at": published_at,
                        "summary": summary
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    logger.warning(f"Failed to parse news entry: {e}")
                    continue
            
            logger.info(f"Fetched {len(news_items)} news from {url}")
            return news_items
            
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed {url}: {e}")
            return []
    
    async def fetch_all_news(self) -> List[Dict[str, Any]]:
        """
        Fetch news from all sources.
        
        Returns:
            List of all news items from all sources
        """
        all_news = []
        
        # Fetch from all sources concurrently
        tasks = [self.fetch_rss_feed(url) for url in self.sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error fetching news: {result}")
            else:
                all_news.extend(result)
        
        # Sort by published date (newest first)
        all_news.sort(key=lambda x: x['published_at'], reverse=True)
        
        self.last_fetch_time = datetime.utcnow()
        self.news_fetched += len(all_news)
        
        logger.info(f"Fetched {len(all_news)} total news from {len(self.sources)} sources")
        return all_news
    
    async def process_news_with_sentiment(
        self,
        news_items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process news items with sentiment analysis.
        
        Args:
            news_items: List of news dictionaries
        
        Returns:
            List of news with sentiment analysis results
        """
        processed_news = []
        
        for news in news_items:
            try:
                # Combine title and summary for analysis
                text_to_analyze = news['title']
                if news.get('summary'):
                    text_to_analyze += " " + news['summary']
                
                # Analyze sentiment
                sentiment = await self.analyzer.analyze_sentiment(text_to_analyze)
                
                # Add sentiment to news item
                news_with_sentiment = {
                    **news,
                    "sentiment_score": sentiment['score'],
                    "sentiment_label": sentiment['label'],
                    "sentiment_confidence": sentiment['confidence']
                }
                
                processed_news.append(news_with_sentiment)
                
                logger.debug(
                    f"Analyzed: {news['title'][:50]}... "
                    f"-> {sentiment['label']} ({sentiment['score']:.2f})"
                )
                
            except Exception as e:
                logger.error(f"Failed to process news: {e}")
                # Add news without sentiment
                news_with_sentiment = {
                    **news,
                    "sentiment_score": 0.0,
                    "sentiment_label": "neutral",
                    "sentiment_confidence": 0.0
                }
                processed_news.append(news_with_sentiment)
        
        return processed_news
    
    async def save_news_to_db(self, news_items: List[Dict[str, Any]]) -> int:
        """
        Save news items to database.
        
        Args:
            news_items: List of news with sentiment
        
        Returns:
            Number of news saved
        """
        # Convert news_items ke format yang dibutuhkan DatabaseManager
        db_news_items = []
        for news in news_items:
            db_news_items.append({
                "source": news['source'],
                "title": news['title'],
                "link": news['url'],
                "published_date": int(news['published_at'].timestamp()) if isinstance(news['published_at'], datetime) else news['published_at'],
                "summary": news.get('summary'),
                "category": news.get('category', 'crypto'),
            })
        
        try:
            saved_count = await self.db.save_news(db_news_items)
            self.news_saved += saved_count
            logger.info(f"Saved {saved_count} news to database")
            return saved_count
        except Exception as e:
            logger.error(f"Failed to save news: {e}")
            return 0
    
    async def run_once(self) -> Dict[str, Any]:
        """
        Run one cycle of news fetching and processing.
        
        Returns:
            Dictionary with statistics
        """
        try:
            # Fetch all news
            news_items = await self.fetch_all_news()
            
            # Process with sentiment analysis
            processed_news = await self.process_news_with_sentiment(news_items)
            
            # Save to database
            saved_count = await self.save_news_to_db(processed_news)
            
            return {
                "fetched": len(news_items),
                "processed": len(processed_news),
                "saved": saved_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in news scraping cycle: {e}")
            raise
    
    async def start(self) -> None:
        """
        Start continuous news scraping.
        
        Ini akan fetch berita setiap NEWS_FETCH_INTERVAL detik.
        """
        self.running = True
        logger.info("Starting news scraper...")
        
        while self.running:
            try:
                # Run one cycle
                stats = await self.run_once()
                
                logger.info(
                    f"News cycle completed: "
                    f"fetched={stats['fetched']}, saved={stats['saved']}"
                )
                
                # Wait for next cycle
                await asyncio.sleep(NEWS_FETCH_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in news scraper loop: {e}")
                # Wait before retry
                await asyncio.sleep(60)
    
    async def stop(self) -> None:
        """
        Stop news scraper.
        """
        logger.info("Stopping news scraper...")
        self.running = False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get scraper statistics.
        """
        return {
            "running": self.running,
            "sources": self.sources,
            "news_fetched": self.news_fetched,
            "news_saved": self.news_saved,
            "last_fetch_time": self.last_fetch_time.isoformat() if self.last_fetch_time else None
        }


# ============================================
# STANDALONE RUNNER
# ============================================

async def main():
    """
    Main function untuk standalone testing.
    
    Cara menjalankan:
        python news_scraper.py
    """
    # Setup logging
    logger.add(
        "logs/news_scraper.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO"
    )
    
    # Create scraper
    scraper = NewsScraper()
    
    try:
        # Initialize
        await scraper.initialize()
        
        # Run once for testing
        logger.info("Running news scraper once...")
        stats = await scraper.run_once()
        
        logger.info(f"Stats: {stats}")
        
        # Uncomment to run continuously
        # await scraper.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        await scraper.stop()
        logger.info("News scraper stopped")


if __name__ == "__main__":
    asyncio.run(main())
