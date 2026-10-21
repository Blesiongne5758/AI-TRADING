"""
Cache Manager
Menghemat API calls dan mempercepat response
"""
import asyncio
import hashlib
import json
from datetime import datetime
from typing import Any, Optional, Callable
from pathlib import Path
from loguru import logger


class SimpleCache:
    """Simple in-memory + disk cache (tanpa dependency berat)"""

    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache = {}
        self.ttl_map = {}

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key dari args"""
        raw = f"{prefix}:{json.dumps(args, sort_keys=True)}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(raw.encode()).hexdigest()

    async def get(self, prefix: str, *args, **kwargs) -> Optional[Any]:
        """Ambil dari cache"""
        key = self._generate_key(prefix, *args, **kwargs)
        
        # Cek memory cache
        if key in self.memory_cache:
            if datetime.now().timestamp() < self.ttl_map.get(key, 0):
                logger.debug(f"💾 Cache HIT (memory): {prefix}")
                return self.memory_cache[key]
            else:
                del self.memory_cache[key]
                del self.ttl_map[key]

        # Cek disk cache
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                if datetime.now().timestamp() < data["expires_at"]:
                    logger.debug(f"💾 Cache HIT (disk): {prefix}")
                    # Load ke memory
                    self.memory_cache[key] = data["value"]
                    self.ttl_map[key] = data["expires_at"]
                    return data["value"]
                else:
                    cache_file.unlink()  # Hapus expired
            except Exception as e:
                logger.debug(f"Cache read error: {e}")

        return None

    async def set(self, prefix: str, value: Any, ttl: int, *args, **kwargs):
        """Simpan ke cache"""
        key = self._generate_key(prefix, *args, **kwargs)
        expires_at = datetime.now().timestamp() + ttl

        # Memory cache
        self.memory_cache[key] = value
        self.ttl_map[key] = expires_at

        # Disk cache (async)
        cache_file = self.cache_dir / f"{key}.json"
        try:
            data = {"value": value, "expires_at": expires_at}
            await asyncio.to_thread(cache_file.write_text, json.dumps(data))
        except Exception as e:
            logger.debug(f"Cache write error: {e}")

    async def clear(self, prefix: str = None):
        """Clear cache"""
        if prefix:
            keys_to_delete = [k for k in self.memory_cache if k.startswith(prefix)]
            for k in keys_to_delete:
                del self.memory_cache[k]
                if k in self.ttl_map:
                    del self.ttl_map[k]
        else:
            self.memory_cache.clear()
            self.ttl_map.clear()

        # Clear disk cache
        for f in self.cache_dir.glob("*.json"):
            f.unlink()

    def get_stats(self) -> dict:
        """Get cache statistics"""
        disk_files = len(list(self.cache_dir.glob("*.json")))
        return {
            "memory_entries": len(self.memory_cache),
            "disk_files": disk_files,
            "cache_dir": str(self.cache_dir)
        }


# Global cache instance
cache = SimpleCache()
