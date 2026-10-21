"""
Cache Manager
Cache system untuk menghemat API calls dan meningkatkan performa
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
from loguru import logger
import asyncio
from .config import AdvancedAIConfig


class CacheManager:
    """
    Cache manager untuk Advanced AI module
    
    Features:
    - File-based caching
    - TTL (Time To Live) support
    - Hash-based keys
    - Async operations
    - Automatic cleanup
    """
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory for cache files (default: ./cache)
        """
        self.cache_dir = cache_dir or AdvancedAIConfig.CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            "hits": 0,
            "misses": 0,
            "writes": 0
        }
        
        logger.info(f"💾 Cache manager initialized: {self.cache_dir}")
    
    def _generate_key(self, prefix: str, data: Any) -> str:
        """
        Generate cache key from data
        
        Args:
            prefix: Cache category prefix
            data: Data to hash
            
        Returns:
            Hash-based cache key
        """
        data_str = json.dumps(data, sort_keys=True, default=str)
        hash_obj = hashlib.md5(data_str.encode())
        return f"{prefix}_{hash_obj.hexdigest()}"
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path"""
        return self.cache_dir / f"{key}.json"
    
    async def get(self, prefix: str, data: Any, ttl_seconds: int) -> Optional[Any]:
        """
        Get cached data
        
        Args:
            prefix: Cache category
            data: Data to generate key
            ttl_seconds: Time to live in seconds
            
        Returns:
            Cached data or None if not found/expired
        """
        if not AdvancedAIConfig.ENABLE_CACHE:
            return None
        
        key = self._generate_key(prefix, data)
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            self.stats["misses"] += 1
            logger.debug(f"Cache miss: {key}")
            return None
        
        try:
            # Read cache file
            loop = asyncio.get_event_loop()
            cache_data = await loop.run_in_executor(
                None,
                lambda: json.loads(cache_path.read_text())
            )
            
            # Check TTL
            cached_time = datetime.fromisoformat(cache_data["timestamp"])
            if datetime.now() - cached_time > timedelta(seconds=ttl_seconds):
                self.stats["misses"] += 1
                logger.debug(f"Cache expired: {key}")
                # Delete expired cache
                await loop.run_in_executor(None, cache_path.unlink)
                return None
            
            self.stats["hits"] += 1
            logger.debug(f"Cache hit: {key}")
            return cache_data["data"]
            
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            self.stats["misses"] += 1
            return None
    
    async def set(self, prefix: str, data: Any, value: Any) -> None:
        """
        Set cache data
        
        Args:
            prefix: Cache category
            data: Data to generate key
            value: Value to cache
        """
        if not AdvancedAIConfig.ENABLE_CACHE:
            return
        
        key = self._generate_key(prefix, data)
        cache_path = self._get_cache_path(key)
        
        cache_data = {
            "key": key,
            "timestamp": datetime.now().isoformat(),
            "data": value
        }
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: cache_path.write_text(json.dumps(cache_data, default=str))
            )
            
            self.stats["writes"] += 1
            logger.debug(f"Cache write: {key}")
            
        except Exception as e:
            logger.error(f"Error writing cache: {e}")
    
    async def clear(self, prefix: Optional[str] = None) -> int:
        """
        Clear cache
        
        Args:
            prefix: Clear only specific prefix (None = clear all)
            
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        
        try:
            loop = asyncio.get_event_loop()
            
            for cache_file in self.cache_dir.glob("*.json"):
                if prefix is None or cache_file.stem.startswith(prefix):
                    await loop.run_in_executor(None, cache_file.unlink)
                    deleted_count += 1
            
            logger.info(f"🗑️  Cleared {deleted_count} cache files")
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
        
        return deleted_count
    
    async def cleanup_expired(self) -> int:
        """
        Cleanup expired cache files
        
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        
        try:
            loop = asyncio.get_event_loop()
            
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    cache_data = await loop.run_in_executor(
                        None,
                        lambda: json.loads(cache_file.read_text())
                    )
                    
                    cached_time = datetime.fromisoformat(cache_data["timestamp"])
                    
                    # Default TTL: 1 hour
                    if datetime.now() - cached_time > timedelta(hours=1):
                        await loop.run_in_executor(None, cache_file.unlink)
                        deleted_count += 1
                        
                except Exception:
                    # Delete corrupted cache files
                    await loop.run_in_executor(None, cache_file.unlink)
                    deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"🧹 Cleaned up {deleted_count} expired cache files")
            
        except Exception as e:
            logger.error(f"Error cleaning up cache: {e}")
        
        return deleted_count
    
    def get_stats(self) -> Dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total * 100) if total > 0 else 0
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "writes": self.stats["writes"],
            "hit_rate": f"{hit_rate:.1f}%",
            "cache_dir": str(self.cache_dir),
            "cache_files": len(list(self.cache_dir.glob("*.json")))
        }
    
    def print_stats(self):
        """Print cache statistics"""
        stats = self.get_stats()
        
        logger.info("\n" + "=" * 70)
        logger.info("💾 CACHE STATISTICS")
        logger.info("=" * 70)
        logger.info(f"   Hits: {stats['hits']}")
        logger.info(f"   Misses: {stats['misses']}")
        logger.info(f"   Hit Rate: {stats['hit_rate']}")
        logger.info(f"   Writes: {stats['writes']}")
        logger.info(f"   Cache Files: {stats['cache_files']}")
        logger.info("=" * 70 + "\n")


# Global cache instance
cache = CacheManager()
