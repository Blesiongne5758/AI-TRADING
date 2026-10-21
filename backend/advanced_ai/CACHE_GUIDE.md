# 💾 SimpleCache Documentation

## Overview

SimpleCache adalah sistem caching lightweight yang menggabungkan in-memory cache dan disk cache untuk menghemat API calls dan mempercepat response time.

**Keunggulan:**
- ✅ **Zero dependencies** - Tidak perlu install library external
- ✅ **Hybrid caching** - Memory + Disk untuk performa optimal
- ✅ **TTL support** - Time-to-live untuk setiap cache entry
- ✅ **Async support** - Fully asynchronous untuk performance
- ✅ **Auto-cleanup** - Expired entries automatically removed
- ✅ **Simple API** - Easy to use dan understand

## Architecture

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  (News API, Twitter, Sentiment, etc)    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         SimpleCache Layer               │
│                                         │
│  ┌──────────────┐  ┌────────────────┐  │
│  │ Memory Cache │  │  Disk Cache    │  │
│  │   (Fast)     │  │ (Persistent)   │  │
│  │              │  │                │  │
│  │ - Dict       │  │ - JSON files   │  │
│  │ - In-memory  │  │ - ./cache/     │  │
│  │ - Instant    │  │ - Persistent   │  │
│  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────┘
```

## Usage

### Basic Usage

```python
from advanced_ai.cache_manager import cache

# Set cache (dengan TTL dalam detik)
await cache.set("news", articles, 300, query="bitcoin")  # 5 minutes

# Get cache
result = await cache.get("news", query="bitcoin")
if result:
    print("Cache hit!")
else:
    print("Cache miss, fetch from API")
```

### API Reference

#### `cache.get(prefix, *args, **kwargs) -> Optional[Any]`

Ambil data dari cache.

**Parameters:**
- `prefix` (str): Cache category (e.g., "news", "tweets", "sentiment")
- `*args`: Positional arguments untuk generate cache key
- `**kwargs`: Keyword arguments untuk generate cache key

**Returns:**
- Cached value jika ada dan belum expired
- `None` jika cache miss atau expired

**Example:**
```python
# Get with simple key
data = await cache.get("news")

# Get with complex key
data = await cache.get("tweets", query="bitcoin", limit=50)
```

#### `cache.set(prefix, value, ttl, *args, **kwargs)`

Simpan data ke cache.

**Parameters:**
- `prefix` (str): Cache category
- `value` (Any): Data yang akan di-cache
- `ttl` (int): Time-to-live dalam detik
- `*args`: Positional arguments untuk generate cache key
- `**kwargs`: Keyword arguments untuk generate cache key

**Example:**
```python
# Set dengan TTL 5 menit
await cache.set("news", articles, 300)

# Set dengan complex key
await cache.set("tweets", tweets, 60, query="bitcoin", limit=50)
```

#### `cache.clear(prefix=None)`

Hapus cache.

**Parameters:**
- `prefix` (str, optional): Hapus hanya cache dengan prefix tertentu. Jika None, hapus semua cache.

**Example:**
```python
# Clear all cache
await cache.clear()

# Clear only news cache
await cache.clear("news")
```

#### `cache.get_stats() -> dict`

Dapatkan statistik cache.

**Returns:**
- Dictionary dengan statistik cache

**Example:**
```python
stats = cache.get_stats()
print(f"Memory entries: {stats['memory_entries']}")
print(f"Disk files: {stats['disk_files']}")
print(f"Cache directory: {stats['cache_dir']}")
```

## Cache Key Generation

Cache key di-generate menggunakan MD5 hash dari prefix + arguments:

```python
# Internal implementation
def _generate_key(prefix, *args, **kwargs):
    raw = f"{prefix}:{json.dumps(args)}:{json.dumps(kwargs)}"
    return hashlib.md5(raw.encode()).hexdigest()
```

**Example:**
```python
# These will generate different keys
await cache.get("news", query="bitcoin")
await cache.get("news", query="ethereum")
await cache.get("tweets", query="bitcoin")
```

## TTL (Time-to-Live)

Setiap cache entry memiliki TTL (Time-to-Live):

- **Memory cache**: Checked setiap kali `get()` dipanggil
- **Disk cache**: Checked saat load dari disk ke memory
- **Auto-cleanup**: Expired entries dihapus otomatis

**Recommended TTL values:**
- News data: 300 seconds (5 minutes)
- Twitter data: 60 seconds (1 minute)
- Sentiment data: 180 seconds (3 minutes)
- Reddit data: 300 seconds (5 minutes)

## Performance

### Memory vs Disk Cache

| Operation | Memory Cache | Disk Cache |
|-----------|--------------|------------|
| **Read** | ~0.001ms | ~1-5ms |
| **Write** | ~0.001ms | ~5-10ms |
| **Persistence** | ❌ No | ✅ Yes |
| **Size limit** | RAM | Disk space |

### Cache Hit Flow

```
1. Check memory cache
   ├─ Hit & not expired → Return immediately (fastest)
   └─ Miss or expired → Continue
   
2. Check disk cache
   ├─ Hit & not expired → Load to memory, return (fast)
   └─ Miss or expired → Continue
   
3. Return None (cache miss)
   → Fetch from API, then cache result
```

## Configuration

### Cache Directory

Default: `./cache`

Change via environment variable:
```bash
export CACHE_DIR=/path/to/cache
```

Or in Python:
```python
from advanced_ai.cache_manager import SimpleCache

cache = SimpleCache(cache_dir="/custom/path")
```

### Memory Limit

SimpleCache tidak memiliki memory limit. Untuk production, monitor memory usage:

```python
stats = cache.get_stats()
print(f"Memory entries: {stats['memory_entries']}")
```

## Best Practices

### 1. Use Appropriate TTL

```python
# Good: Short TTL for volatile data
await cache.set("tweets", tweets, 60)  # 1 minute

# Good: Longer TTL for stable data
await cache.set("config", config, 3600)  # 1 hour
```

### 2. Use Specific Prefixes

```python
# Good: Specific prefixes
await cache.set("news_cryptopanic", articles, 300)
await cache.set("news_newsapi", articles, 300)

# Bad: Generic prefixes
await cache.set("data", articles, 300)
```

### 3. Clear Cache Strategically

```python
# Clear specific category
await cache.clear("tweets")

# Clear all (use sparingly)
await cache.clear()
```

### 4. Monitor Cache Stats

```python
stats = cache.get_stats()
if stats['memory_entries'] > 10000:
    logger.warning("High memory cache usage")
```

## Integration Examples

### News API Client

```python
class NewsAPIClient:
    async def fetch_news(self, query: str):
        # Check cache first
        cached = await cache.get("news", query=query)
        if cached:
            return cached
        
        # Fetch from API
        articles = await self._fetch_from_api(query)
        
        # Cache for 5 minutes
        await cache.set("news", articles, 300, query=query)
        
        return articles
```

### Twitter Analyzer

```python
class TwitterAnalyzer:
    async def fetch_tweets(self, query: str, limit: int):
        # Check cache
        cached = await cache.get("tweets", query=query, limit=limit)
        if cached:
            return cached
        
        # Fetch from API
        tweets = await self._fetch_from_twitter(query, limit)
        
        # Cache for 1 minute
        await cache.set("tweets", tweets, 60, query=query, limit=limit)
        
        return tweets
```

### Sentiment Aggregator

```python
class SentimentAggregator:
    async def aggregate(self, currencies: list):
        # Check cache
        cached = await cache.get("sentiment", currencies=currencies)
        if cached:
            return cached
        
        # Aggregate sentiment
        result = await self._aggregate_sentiment(currencies)
        
        # Cache for 3 minutes
        await cache.set("sentiment", result, 180, currencies=currencies)
        
        return result
```

## Troubleshooting

### Cache Not Working

**Problem:** Cache selalu miss

**Solution:**
1. Check TTL value (mungkin terlalu pendek)
2. Check cache key generation (args/kwargs harus consistent)
3. Check disk permissions (cache directory harus writable)

### High Memory Usage

**Problem:** Memory usage terlalu tinggi

**Solution:**
1. Reduce TTL values
2. Clear cache periodically: `await cache.clear()`
3. Monitor with `cache.get_stats()`

### Disk Cache Not Persisting

**Problem:** Disk cache hilang setelah restart

**Solution:**
1. Check cache directory path
2. Check disk permissions
3. Check disk space

## Comparison with Other Cache Libraries

| Feature | SimpleCache | aiocache | Redis |
|---------|-------------|----------|-------|
| **Dependencies** | ✅ None | ❌ Heavy | ❌ External |
| **Memory + Disk** | ✅ Yes | ⚠️ Configurable | ❌ Memory only |
| **Async Support** | ✅ Yes | ✅ Yes | ✅ Yes |
| **TTL Support** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Cluster Support** | ❌ No | ⚠️ Limited | ✅ Yes |
| **Performance** | ✅ Fast | ✅ Fast | ✅ Fastest |
| **Setup Complexity** | ✅ Simple | ⚠️ Medium | ❌ Complex |

**Recommendation:** Use SimpleCache untuk development dan small-scale production. Use Redis untuk large-scale production dengan multiple instances.

## Migration from aiocache

Jika sebelumnya menggunakan aiocache, migration ke SimpleCache sangat mudah:

### Before (aiocache)

```python
from aiocache import Cache

cache = Cache(Cache.MEMORY)

# Set
await cache.set("key", value, ttl=300)

# Get
value = await cache.get("key")
```

### After (SimpleCache)

```python
from advanced_ai.cache_manager import cache

# Set
await cache.set("prefix", value, 300, "key")

# Get
value = await cache.get("prefix", "key")
```

**Key differences:**
- SimpleCache uses prefix + args/kwargs untuk key generation
- TTL adalah positional argument ke-3 (bukan keyword argument)
- No need to initialize cache instance (use global `cache`)

## Conclusion

SimpleCache adalah solusi caching yang simple, fast, dan dependency-free. Sangat cocok untuk:

- ✅ Development dan testing
- ✅ Small to medium scale applications
- ✅ Applications yang ingin minimize dependencies
- ✅ Quick prototyping

Untuk large-scale production dengan high traffic, pertimbangkan menggunakan Redis atau Memcached.

---

**Last Updated:** 2024  
**Version:** 1.0.0  
**License:** MIT
