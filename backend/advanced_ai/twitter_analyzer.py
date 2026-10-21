"""
Twitter/X + Reddit + Telegram Analyzer
Mengumpulkan sentimen dari social media
"""
import asyncio
import re
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import (
    TWITTER_BEARER_TOKEN,
    NITTER_INSTANCES,
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    REDDIT_SUBREDDITS,
    INFLUENTIAL_ACCOUNTS,
)
from .cache_manager import cache


class SocialMediaAnalyzer:
    """Analyzer untuk Twitter/X, Reddit, dan Telegram"""

    def __init__(self):
        self.session = None
        self.reddit_token = None
        self.reddit_token_expiry = 0

    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    # ============================================
    # TWITTER/X via NITTER (GRATIS)
    # ============================================
    async def fetch_twitter_nitter(
        self,
        username: str,
        limit: int = 20,
    ) -> List[Dict]:
        """
        Fetch tweets via Nitter (gratis, tanpa API key)
        """
        await self._ensure_session()

        cache_key = f"twitter:{username}:{limit}"
        cached = await cache.get("twitter", cache_key)
        if cached:
            return cached

        tweets = []

        # Coba beberapa instance Nitter
        for instance in NITTER_INSTANCES:
            try:
                url = f"{instance}/{username}/rss"
                async with self.session.get(url) as response:
                    if response.status != 200:
                        continue

                    content = await response.text()

                    # Parse RSS XML sederhana
                    import xml.etree.ElementTree as ET
                    try:
                        root = ET.fromstring(content)
                        items = root.findall(".//item")

                        for item in items[:limit]:
                            title = item.find("title").text if item.find("title") is not None else ""
                            description = item.find("description").text if item.find("description") is not None else ""
                            pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                            link = item.find("link").text if item.find("link") is not None else ""

                            # Bersihkan HTML dari description
                            clean_desc = re.sub(r"<[^>]+>", "", description)

                            tweets.append({
                                "source": f"twitter/{username}",
                                "text": clean_desc[:500],
                                "title": title,
                                "url": link,
                                "published_at": pub_date,
                                "author": username,
                                "is_influential": username in INFLUENTIAL_ACCOUNTS["whales"] + INFLUENTIAL_ACCOUNTS["analysts"],
                            })

                        if tweets:
                            logger.info(f"🐦 Twitter/{username}: {len(tweets)} tweets via {instance}")
                            await cache.set("twitter", tweets, 60, cache_key)
                            return tweets

                    except ET.ParseError as e:
                        logger.debug(f"XML parse error: {e}")
                        continue

            except Exception as e:
                logger.debug(f"Nitter instance {instance} failed: {e}")
                continue

        logger.warning(f"⚠️  Could not fetch tweets for {username} from any Nitter instance")
        return []

    # ============================================
    # TWITTER/X via API v2 (BERBAYAR)
    # ============================================
    async def fetch_twitter_api(
        self,
        query: str,
        limit: int = 100,
    ) -> List[Dict]:
        """
        Fetch tweets via Twitter API v2 (butuh Bearer Token berbayar)
        """
        if not TWITTER_BEARER_TOKEN:
            return []

        await self._ensure_session()

        cache_key = f"twitter_api:{query}:{limit}"
        cached = await cache.get("twitter", cache_key)
        if cached:
            return cached

        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
        params = {
            "query": query,
            "max_results": min(limit, 100),
            "tweet.fields": "created_at,author_id,public_metrics,lang",
        }

        try:
            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    logger.warning(f"Twitter API error: {response.status}")
                    return []

                data = await response.json()
                tweets = []

                for tweet in data.get("data", []):
                    metrics = tweet.get("public_metrics", {})
                    tweets.append({
                        "source": "twitter_api",
                        "text": tweet.get("text", ""),
                        "id": tweet.get("id"),
                        "author_id": tweet.get("author_id"),
                        "published_at": tweet.get("created_at"),
                        "language": tweet.get("lang"),
                        "metrics": metrics,
                        "engagement_score": (
                            metrics.get("like_count", 0) +
                            metrics.get("retweet_count", 0) * 2 +
                            metrics.get("reply_count", 0)
                        ),
                    })

                await cache.set("twitter", tweets, 60, cache_key)
                logger.info(f"🐦 Twitter API: {len(tweets)} tweets for '{query}'")
                return tweets

        except Exception as e:
            logger.error(f"Twitter API error: {e}")
            return []

    # ============================================
    # REDDIT (GRATIS)
    # ============================================
    async def _get_reddit_token(self) -> Optional[str]:
        """Dapatkan Reddit OAuth token"""
        if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
            return None

        if self.reddit_token and datetime.now().timestamp() < self.reddit_token_expiry:
            return self.reddit_token

        await self._ensure_session()

        url = "https://www.reddit.com/api/v1/access_token"
        auth = aiohttp.BasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
        data = {"grant_type": "client_credentials"}
        headers = {"User-Agent": REDDIT_USER_AGENT}

        try:
            async with self.session.post(url, auth=auth, data=data, headers=headers) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                self.reddit_token = data["access_token"]
                self.reddit_token_expiry = datetime.now().timestamp() + data["expires_in"] - 60
                return self.reddit_token

        except Exception as e:
            logger.error(f"Reddit auth error: {e}")
            return None

    async def fetch_reddit(
        self,
        query: str = "bitcoin OR ethereum OR crypto",
        limit: int = 50,
        subreddits: List[str] = None,
    ) -> List[Dict]:
        """Ambil posts dari Reddit"""
        token = await self._get_reddit_token()
        if not token:
            # Fallback ke JSON endpoint (tanpa auth, terbatas)
            return await self._fetch_reddit_public(query, limit, subreddits)

        await self._ensure_session()

        cache_key = f"reddit:{query}:{limit}"
        cached = await cache.get("reddit", cache_key)
        if cached:
            return cached

        subs = subreddits or REDDIT_SUBREDDITS
        subreddit_query = "+".join([f"subreddit:{s}" for s in subs])
        full_query = f"({query}) {subreddit_query}"

        url = "https://oauth.reddit.com/search"
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": REDDIT_USER_AGENT,
        }
        params = {
            "q": full_query,
            "limit": limit,
            "sort": "relevance",
            "t": "day",
            "type": "link",
        }

        try:
            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    return []

                data = await response.json()
                posts = []

                for child in data.get("data", {}).get("children", []):
                    post_data = child.get("data", {})
                    posts.append({
                        "source": f"reddit/r/{post_data.get('subreddit', 'unknown')}",
                        "title": post_data.get("title", ""),
                        "text": (post_data.get("selftext") or "")[:500],
                        "url": f"https://reddit.com{post_data.get('permalink', '')}",
                        "published_at": datetime.fromtimestamp(
                            post_data.get("created_utc", 0)
                        ).isoformat(),
                        "score": post_data.get("score", 0),
                        "num_comments": post_data.get("num_comments", 0),
                        "upvote_ratio": post_data.get("upvote_ratio", 0),
                        "engagement_score": (
                            post_data.get("score", 0) +
                            post_data.get("num_comments", 0) * 2
                        ),
                    })

                await cache.set("reddit", posts, 300, cache_key)
                logger.info(f"🔴 Reddit: {len(posts)} posts fetched")
                return posts

        except Exception as e:
            logger.error(f"Reddit error: {e}")
            return []

    async def _fetch_reddit_public(
        self, query: str, limit: int, subreddits: List[str]
    ) -> List[Dict]:
        """Fallback: fetch dari public JSON endpoint"""
        await self._ensure_session()
        posts = []

        for sub in (subreddits or REDDIT_SUBREDDITS)[:3]:
            try:
                url = f"https://www.reddit.com/r/{sub}/search.json"
                params = {"q": query, "limit": limit // 3, "sort": "relevance", "t": "day"}
                headers = {"User-Agent": REDDIT_USER_AGENT}

                async with self.session.get(url, params=params, headers=headers) as response:
                    if response.status != 200:
                        continue

                    data = await response.json()
                    for child in data.get("data", {}).get("children", []):
                        post_data = child.get("data", {})
                        posts.append({
                            "source": f"reddit/r/{sub}",
                            "title": post_data.get("title", ""),
                            "text": (post_data.get("selftext") or "")[:500],
                            "url": f"https://reddit.com{post_data.get('permalink', '')}",
                            "published_at": datetime.fromtimestamp(
                                post_data.get("created_utc", 0)
                            ).isoformat(),
                            "score": post_data.get("score", 0),
                            "engagement_score": post_data.get("score", 0),
                        })

                await asyncio.sleep(2)  # Rate limit
            except Exception as e:
                logger.debug(f"Reddit public fetch error for {sub}: {e}")

        logger.info(f"🔴 Reddit (public): {len(posts)} posts")
        return posts

    # ============================================
    # INFLUENTIAL ACCOUNTS MONITORING
    # ============================================
    async def monitor_influential_accounts(
        self,
        categories: List[str] = None,
    ) -> List[Dict]:
        """
        Monitor tweet dari akun-akun berpengaruh
        """
        if categories is None:
            categories = ["whales", "analysts", "news"]

        all_accounts = []
        for cat in categories:
            all_accounts.extend(INFLUENTIAL_ACCOUNTS.get(cat, []))

        logger.info(f"👀 Monitoring {len(all_accounts)} influential accounts")

        tasks = [self.fetch_twitter_nitter(acc, limit=10) for acc in all_accounts]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_tweets = []
        for result in results:
            if isinstance(result, list):
                all_tweets.extend(result)

        return all_tweets

    # ============================================
    # AGGREGATOR
    # ============================================
    async def fetch_all_social(
        self,
        crypto_query: str = "bitcoin OR ethereum OR crypto",
        monitor_influencers: bool = True,
    ) -> Dict[str, List[Dict]]:
        """Ambil data dari semua social media secara paralel"""
        logger.info("📱 Fetching social media data...")

        tasks = {
            "reddit": self.fetch_reddit(query=crypto_query, limit=30),
        }

        if monitor_influencers:
            tasks["influencers"] = self.monitor_influential_accounts()

        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        output = {}
        for key, result in zip(tasks.keys(), results):
            if isinstance(result, list):
                output[key] = result
            else:
                output[key] = []
                logger.error(f"Social source {key} error: {result}")

        total = sum(len(v) for v in output.values())
        logger.info(f"✅ Total social posts: {total}")
        return output
