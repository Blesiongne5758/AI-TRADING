# 🎯 Sentiment Aggregator Documentation

## Overview

Sentiment Aggregator adalah sistem canggih yang menggabungkan analisis sentimen dari **multiple sources** menjadi satu skor final dengan **weighted scoring**.

**Key Features:**
- ✅ **Multi-source aggregation** - Gabungkan news, social media, community votes
- ✅ **Weighted scoring** - Setiap sumber punya bobot berbeda
- ✅ **Confidence calculation** - Berdasarkan sample size
- ✅ **Source breakdown** - Detail kontribusi setiap sumber
- ✅ **Top articles/posts** - Identify most impactful content
- ✅ **Pump & dump integration** - Deteksi manipulasi pasar
- ✅ **Batch analysis** - Analisis multiple symbols sekaligus
- ✅ **Async processing** - Parallel fetching untuk performa optimal

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Sentiment Aggregator                           │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ News API     │  │ Social Media │  │ Community    │     │
│  │ Client       │  │ Analyzer     │  │ Votes        │     │
│  │              │  │              │  │              │     │
│  │ - CryptoPanic│  │ - Twitter    │  │ - CryptoPanic│     │
│  │ - NewsAPI    │  │ - Reddit     │  │   votes      │     │
│  │ - GNews      │  │ - Influencers│  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │             │
│         └─────────────────┼─────────────────┘             │
│                           ↓                               │
│              ┌────────────────────────┐                   │
│              │   FinBERT Analyzer     │                   │
│              │   (Batch Processing)   │                   │
│              └────────────┬───────────┘                   │
│                           ↓                               │
│              ┌────────────────────────┐                   │
│              │  Source Classification │                   │
│              │  & Score Aggregation   │                   │
│              └────────────┬───────────┘                   │
│                           ↓                               │
│              ┌────────────────────────┐                   │
│              │  Weighted Scoring      │                   │
│              │  (Source Weights)      │                   │
│              └────────────┬───────────┘                   │
│                           ↓                               │
│              ┌────────────────────────┐                   │
│              │  Confidence Calculation│                   │
│              │  (Sample Size Based)   │                   │
│              └────────────┬───────────┘                   │
│                           ↓                               │
│              ┌────────────────────────┐                   │
│              │  Final Sentiment Score │                   │
│              │  + Source Breakdown    │                   │
│              └────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## Weighted Scoring System

### **Source Weights**

| Source | Weight | Rationale |
|--------|--------|-----------|
| **News Professional** | 30% | CryptoPanic, NewsAPI, GNews - reliable sources |
| **Social Influencers** | 25% | Twitter whales & analysts - market movers |
| **Social Reddit** | 15% | Reddit communities - crowd sentiment |
| **Community Votes** | 15% | CryptoPanic votes - crowd validation |
| **On-Chain** | 15% | Whale movements - smart money (future) |
| **Total** | **100%** | - |

### **Score Calculation**

```python
# Step 1: Calculate average score per source
news_avg = sum(news_scores) / len(news_scores)
influencer_avg = sum(influencer_scores) / len(influencer_scores)
reddit_avg = sum(reddit_scores) / len(reddit_scores)
community_avg = sum(community_scores) / len(community_scores)

# Step 2: Apply weights
weighted_score = (
    news_avg * 0.30 +
    influencer_avg * 0.25 +
    reddit_avg * 0.15 +
    community_avg * 0.15
)

# Step 3: Normalize to -1 to +1
final_score = weighted_score / total_weight
```

### **Score Interpretation**

| Score Range | Label | Meaning |
|-------------|-------|---------|
| **+0.2 to +1.0** | BULLISH | Positive sentiment, potential uptrend |
| **-0.2 to +0.2** | NEUTRAL | Mixed sentiment, no clear direction |
| **-1.0 to -0.2** | BEARISH | Negative sentiment, potential downtrend |

## Confidence Calculation

Confidence score berdasarkan **sample size** (jumlah data yang dianalisis):

| Sample Size | Confidence | Reliability |
|-------------|------------|-------------|
| **> 100** | 90% | Very High |
| **50-100** | 75% | High |
| **20-50** | 60% | Medium |
| **5-20** | 40% | Low |
| **< 5** | 20% | Very Low |

**Rationale:**
- More samples = more reliable sentiment
- Small sample size = high variance
- Confidence helps users decide how much to trust the score

## Usage

### **Basic Usage**

```python
from advanced_ai.sentiment_aggregator import SentimentAggregator

# Initialize aggregator
aggregator = SentimentAggregator()

# Analyze single symbol
result = await aggregator.analyze_symbol(
    symbol="BTC/USDT",
    currency_code="BTC",
    include_pump_detection=True
)

# Print results
print(f"Symbol: {result['symbol']}")
print(f"Sentiment: {result['label']} ({result['final_score']:+.3f})")
print(f"Confidence: {result['confidence']}%")
print(f"Total Samples: {result['total_samples']}")

# Source breakdown
print("\nSource Breakdown:")
for source, data in result['source_breakdown'].items():
    print(f"  {source}: {data['score']:+.3f} (weight: {data['weight']:.0%})")

# Top articles
print("\nTop Positive Articles:")
for article in result['top_positive'][:3]:
    print(f"  [{article['source']}] {article['text'][:100]}...")
    print(f"    Score: {article['score']:+.3f}")

# Cleanup
await aggregator.close()
```

### **Batch Analysis**

```python
# Analyze multiple symbols
symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
results = await aggregator.analyze_all_symbols(symbols)

# Sort by sentiment score
results.sort(key=lambda x: x['final_score'], reverse=True)

for result in results:
    print(f"{result['symbol']}: {result['label']} ({result['final_score']:+.3f})")
```

### **Integration dengan Trading Bot**

```python
from advanced_ai.sentiment_aggregator import SentimentAggregator

aggregator = SentimentAggregator()

async def should_trade(symbol: str) -> bool:
    """Determine if should trade based on sentiment"""
    result = await aggregator.analyze_symbol(symbol)
    
    # Only trade if sentiment is strong and confidence is high
    if result['label'] == 'BULLISH' and result['confidence'] >= 75:
        print(f"✅ {symbol}: Strong bullish sentiment, consider LONG")
        return True
    elif result['label'] == 'BEARISH' and result['confidence'] >= 75:
        print(f"✅ {symbol}: Strong bearish sentiment, consider SHORT")
        return True
    else:
        print(f"⚠️ {symbol}: Weak or neutral sentiment, skip trade")
        return False

# Usage
if await should_trade("BTC/USDT"):
    # Execute trade
    pass
```

### **Integration dengan Pump Detector**

```python
from advanced_ai.sentiment_aggregator import SentimentAggregator
from advanced_ai.pump_dump_detector import PumpDumpDetector

aggregator = SentimentAggregator()
pump_detector = PumpDumpDetector()

async def analyze_with_pump_detection(symbol: str, price_data: Dict, volume_data: List):
    """Analyze sentiment + pump detection"""
    
    # Sentiment analysis
    sentiment = await aggregator.analyze_symbol(
        symbol=symbol,
        include_pump_detection=False  # We'll do it separately
    )
    
    # Pump detection
    pump_result = pump_detector.analyze_symbol(
        symbol=symbol,
        price_data=price_data,
        volume_data=volume_data,
        social_mentions=[]  # Optional
    )
    
    # Combine results
    if pump_result['risk_level'] in ['CRITICAL', 'HIGH']:
        print(f"🚨 {symbol}: Pump detected! Sentiment may be manipulated")
        return {
            'sentiment': sentiment,
            'pump_warning': True,
            'recommendation': 'AVOID TRADE'
        }
    else:
        print(f"✅ {symbol}: No pump detected, sentiment is reliable")
        return {
            'sentiment': sentiment,
            'pump_warning': False,
            'recommendation': 'TRADE OK'
        }
```

## API Reference

### `SentimentAggregator()`

Initialize sentiment aggregator.

**Example:**
```python
aggregator = SentimentAggregator()
```

---

### `async analyze_symbol(symbol, currency_code, include_pump_detection) -> Dict`

Analyze sentiment for single symbol.

**Parameters:**
- `symbol` (str): Trading pair (e.g., "BTC/USDT")
- `currency_code` (str, optional): Currency code (default: extracted from symbol)
- `include_pump_detection` (bool): Enable pump detection (default: True)

**Returns:**
```python
{
    "symbol": "BTC/USDT",
    "currency": "BTC",
    "timestamp": "2024-01-15T10:00:00",
    "final_score": 0.456,
    "label": "BULLISH",
    "confidence": 85,
    "total_samples": 150,
    "source_breakdown": {
        "news_professional": {
            "score": 0.523,
            "weight": 0.30,
            "weighted_contribution": 0.157,
            "sample_size": 45
        },
        "social_influencers": {
            "score": 0.412,
            "weight": 0.25,
            "weighted_contribution": 0.103,
            "sample_size": 38
        },
        "social_reddit": {
            "score": 0.389,
            "weight": 0.15,
            "weighted_contribution": 0.058,
            "sample_size": 52
        },
        "community_votes": {
            "score": 0.478,
            "weight": 0.15,
            "weighted_contribution": 0.072,
            "sample_size": 15
        }
    },
    "top_positive": [
        {
            "score": 0.95,
            "label": "POSITIVE",
            "text": "Bitcoin reaches new all-time high...",
            "source": "cryptopanic"
        },
        # ... more articles
    ],
    "top_negative": [
        {
            "score": -0.87,
            "label": "NEGATIVE",
            "text": "Regulatory concerns spark fear...",
            "source": "newsapi"
        },
        # ... more articles
    ],
    "pump_dump_analysis": {
        "status": "requires_price_data",
        "message": "Pump detection membutuhkan price & volume data"
    },
    "raw_counts": {
        "news_articles": 45,
        "social_posts": 105,
        "total_analyzed": 150
    }
}
```

---

### `async analyze_all_symbols(symbols) -> List[Dict]`

Analyze sentiment for multiple symbols.

**Parameters:**
- `symbols` (List[str]): List of trading pairs

**Returns:**
List of analysis results (same format as `analyze_symbol`)

**Example:**
```python
results = await aggregator.analyze_all_symbols([
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT"
])
```

---

### `async close()`

Cleanup resources (close HTTP sessions).

**Example:**
```python
await aggregator.close()
```

---

### `get_source_weights() -> Dict`

Get source weight configuration.

**Returns:**
```python
{
    "news_professional": 0.30,
    "social_influencers": 0.25,
    "social_reddit": 0.15,
    "community_votes": 0.15,
    "on_chain": 0.15
}
```

---

## Configuration

### **Custom Source Weights**

```python
class CustomSentimentAggregator(SentimentAggregator):
    SOURCE_WEIGHTS = {
        "news_professional": 0.40,  # Increase news weight
        "social_influencers": 0.30,  # Increase influencer weight
        "social_reddit": 0.10,  # Decrease reddit weight
        "community_votes": 0.10,  # Decrease community weight
        "on_chain": 0.10,  # Decrease on-chain weight
    }
```

### **Custom Confidence Thresholds**

```python
class CustomSentimentAggregator(SentimentAggregator):
    async def analyze_symbol(self, symbol, currency_code=None, include_pump_detection=True):
        # ... existing code ...
        
        # Custom confidence calculation
        total_samples = sum(s["sample_size"] for s in source_breakdown.values())
        if total_samples > 200:
            confidence = 95  # Higher threshold
        elif total_samples > 100:
            confidence = 80
        elif total_samples > 50:
            confidence = 65
        else:
            confidence = 40
        
        # ... rest of code ...
```

### **Custom Sentiment Labels**

```python
class CustomSentimentAggregator(SentimentAggregator):
    async def analyze_symbol(self, symbol, currency_code=None, include_pump_detection=True):
        # ... existing code ...
        
        # Custom label thresholds
        if final_score > 0.3:  # Stricter threshold
            label = "VERY_BULLISH"
        elif final_score > 0.1:
            label = "BULLISH"
        elif final_score < -0.3:
            label = "VERY_BEARISH"
        elif final_score < -0.1:
            label = "BEARISH"
        else:
            label = "NEUTRAL"
        
        # ... rest of code ...
```

## Performance

### **Processing Speed**

| Operation | Time | Notes |
|-----------|------|-------|
| **Single Symbol** | ~5-10s | Depends on API response time |
| **Batch (5 symbols)** | ~15-30s | Parallel processing |
| **Batch (10 symbols)** | ~25-50s | Parallel processing |

### **API Calls**

| Source | Calls per Symbol | Rate Limit |
|--------|------------------|------------|
| **CryptoPanic** | 1 | 30 req/min |
| **NewsAPI** | 1 | 100 req/day |
| **GNews** | 1 | 100 req/day |
| **Twitter (Nitter)** | 10-20 | Unlimited |
| **Reddit** | 1 | 60 req/min |
| **Total** | ~15-25 | - |

### **Cache Performance**

| Metric | Without Cache | With Cache | Improvement |
|--------|---------------|------------|-------------|
| **API Calls** | 15-25 per symbol | ~5 per symbol | **-70%** ✅ |
| **Response Time** | 5-10s | 0.5-1s | **-90%** ✅ |
| **Cost** | High (API limits) | Low | **Significant** ✅ |

## Best Practices

### **1. Use Appropriate Sample Size**

```python
# ✅ Good: Large sample size
result = await aggregator.analyze_symbol("BTC/USDT")
if result['total_samples'] > 50:
    print(f"Reliable sentiment: {result['label']}")

# ❌ Bad: Small sample size
if result['total_samples'] < 10:
    print("Unreliable sentiment, need more data")
```

### **2. Check Confidence Score**

```python
# ✅ Good: High confidence
if result['confidence'] >= 75:
    print(f"High confidence: {result['label']}")
    # Consider trading

# ⚠️ Warning: Low confidence
elif result['confidence'] < 50:
    print(f"Low confidence, skip trade")
    # Skip trading
```

### **3. Review Source Breakdown**

```python
# Check if sources agree
scores = [data['score'] for data in result['source_breakdown'].values()]
if all(s > 0 for s in scores):
    print("✅ All sources bullish")
elif all(s < 0 for s in scores):
    print("✅ All sources bearish")
else:
    print("⚠️ Mixed signals from sources")
```

### **4. Combine dengan Pump Detection**

```python
# Always check for pump before trading
if result['pump_dump_analysis']:
    if result['pump_dump_analysis'].get('risk_level') in ['CRITICAL', 'HIGH']:
        print("🚨 Pump detected! Avoid trade")
        return False
```

### **5. Monitor Top Articles**

```python
# Review top positive/negative articles
print("Top Positive:")
for article in result['top_positive'][:3]:
    print(f"  {article['text'][:100]}...")

print("\nTop Negative:")
for article in result['top_negative'][:3]:
    print(f"  {article['text'][:100]}...")
```

## Integration Examples

### **Dashboard Integration**

```python
from advanced_ai.sentiment_aggregator import SentimentAggregator

aggregator = SentimentAggregator()

async def get_dashboard_data(symbols):
    """Get sentiment data for dashboard"""
    results = await aggregator.analyze_all_symbols(symbols)
    
    dashboard_data = {
        "bullish": [],
        "neutral": [],
        "bearish": []
    }
    
    for result in results:
        category = result['label'].lower()
        dashboard_data[category].append({
            "symbol": result['symbol'],
            "score": result['final_score'],
            "confidence": result['confidence'],
            "samples": result['total_samples']
        })
    
    return dashboard_data
```

### **Alert System**

```python
async def monitor_sentiment_alerts(symbols):
    """Monitor for sentiment changes"""
    previous_results = {}
    
    while True:
        results = await aggregator.analyze_all_symbols(symbols)
        
        for result in results:
            symbol = result['symbol']
            prev = previous_results.get(symbol)
            
            # Check for significant change
            if prev and abs(result['final_score'] - prev['final_score']) > 0.3:
                await send_alert(
                    f"🚨 {symbol} sentiment changed significantly!",
                    f"From {prev['label']} ({prev['final_score']:+.3f}) "
                    f"to {result['label']} ({result['final_score']:+.3f})"
                )
            
            previous_results[symbol] = result
        
        await asyncio.sleep(300)  # Check every 5 minutes
```

### **Trading Strategy**

```python
async def sentiment_based_strategy(symbol: str):
    """Trading strategy based on sentiment"""
    result = await aggregator.analyze_symbol(symbol)
    
    # Entry conditions
    if (result['label'] == 'BULLISH' and 
        result['confidence'] >= 75 and
        result['total_samples'] >= 50):
        
        print(f"✅ {symbol}: Strong bullish sentiment")
        print(f"   Score: {result['final_score']:+.3f}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Action: OPEN LONG")
        
        return {
            "action": "OPEN_LONG",
            "position_size": 0.10,  # 10% of portfolio
            "stop_loss": 0.02,      # 2% below entry
            "take_profit": 0.05     # 5% above entry
        }
    
    elif (result['label'] == 'BEARISH' and 
          result['confidence'] >= 75 and
          result['total_samples'] >= 50):
        
        print(f"✅ {symbol}: Strong bearish sentiment")
        print(f"   Score: {result['final_score']:+.3f}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Action: OPEN SHORT")
        
        return {
            "action": "OPEN_SHORT",
            "position_size": 0.10,
            "stop_loss": 0.02,
            "take_profit": 0.05
        }
    
    else:
        print(f"⚠️ {symbol}: Weak or neutral sentiment")
        print(f"   Score: {result['final_score']:+.3f}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Action: SKIP")
        
        return {"action": "SKIP"}
```

## Troubleshooting

### **Issue: Low Confidence Score**

**Symptoms:**
- Confidence < 50%
- Total samples < 20

**Solutions:**
1. **Increase sample size**
   ```python
   # Fetch more data
   news_articles = await news_client.fetch_all_news(
       currencies=[currency_code],
       limit_per_source=50  # Increase from 30
   )
   ```

2. **Enable more sources**
   ```python
   # Enable Reddit and Twitter
   social_data = await social_analyzer.fetch_all_social(
       crypto_query=currency_code.lower(),
       monitor_influencers=True
   )
   ```

3. **Check API keys**
   ```python
   # Verify all API keys are configured
   sources = news_client.get_enabled_sources()
   print(f"Enabled sources: {sources}")
   ```

---

### **Issue: Mixed Signals from Sources**

**Symptoms:**
- Some sources bullish, others bearish
- Final score close to 0

**Solutions:**
1. **Review source breakdown**
   ```python
   for source, data in result['source_breakdown'].items():
       print(f"{source}: {data['score']:+.3f} (weight: {data['weight']:.0%})")
   ```

2. **Adjust source weights**
   ```python
   # Increase weight for reliable sources
   SOURCE_WEIGHTS = {
       "news_professional": 0.40,  # Increase
       "social_influencers": 0.30,  # Increase
       "social_reddit": 0.10,  # Decrease
       "community_votes": 0.10,  # Decrease
       "on_chain": 0.10,
   }
   ```

3. **Require higher confidence**
   ```python
   # Only trade if confidence >= 80%
   if result['confidence'] >= 80:
       # Proceed with trade
   ```

---

### **Issue: Slow Performance**

**Symptoms:**
- Analysis takes > 10 seconds
- API timeouts

**Solutions:**
1. **Enable caching**
   ```python
   # Cache is enabled by default
   # Check cache stats
   stats = cache.get_stats()
   print(f"Cache hit rate: {stats['hit_rate']}")
   ```

2. **Reduce sample size**
   ```python
   # Fetch less data
   news_articles = await news_client.fetch_all_news(
       currencies=[currency_code],
       limit_per_source=20  # Reduce from 30
   )
   ```

3. **Use batch analysis**
   ```python
   # ✅ Good: Batch analysis
   results = await aggregator.analyze_all_symbols(symbols)
   
   # ❌ Bad: Sequential analysis
   for symbol in symbols:
       result = await aggregator.analyze_symbol(symbol)
   ```

---

### **Issue: Pump Detection Not Working**

**Symptoms:**
- `pump_dump_analysis` shows "requires_price_data"
- No pump detection

**Solutions:**
1. **Provide price and volume data**
   ```python
   # Get price data from your data source
   price_data = {
       "current": 67500.0,
       "1h_ago": 60000.0,
       "24h_ago": 55000.0,
       "high_24h": 68000.0,
       "low_24h": 54000.0,
   }
   
   volume_data = [1000, 1100, 1050, ..., 5000, 6000, 7000]
   
   # Run pump detection separately
   pump_result = pump_detector.analyze_symbol(
       symbol="BTC/USDT",
       price_data=price_data,
       volume_data=volume_data
   )
   ```

2. **Integrate dengan data collector**
   ```python
   # In your main application
   price_data = await data_collector.get_price_data(symbol)
   volume_data = await data_collector.get_volume_data(symbol)
   
   result = await aggregator.analyze_symbol(
       symbol=symbol,
       include_pump_detection=False  # We'll do it separately
   )
   
   pump_result = pump_detector.analyze_symbol(
       symbol=symbol,
       price_data=price_data,
       volume_data=volume_data
   )
   ```

## Conclusion

Sentiment Aggregator adalah sistem canggih untuk menggabungkan analisis sentimen dari multiple sources dengan:

✅ **Multi-source aggregation** - News, social media, community votes  
✅ **Weighted scoring** - Each source has different weight  
✅ **Confidence calculation** - Based on sample size  
✅ **Source breakdown** - Detailed contribution analysis  
✅ **Top articles/posts** - Identify impactful content  
✅ **Pump detection integration** - Avoid manipulated sentiment  
✅ **Batch analysis** - Analyze multiple symbols  
✅ **Async processing** - Optimal performance  

**Your sentiment analysis is now enterprise-grade! 🎯🚀**

---

**Last Updated:** 2024  
**Version:** 1.0.0  
**License:** MIT
