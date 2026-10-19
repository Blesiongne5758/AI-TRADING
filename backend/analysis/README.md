# 📊 Analysis Engine - Fase 2

Analysis Engine adalah modul yang menganalisis data dari Data Collector dan menghasilkan trading signals.

## 🎯 Fitur

- ✅ **Technical Indicators** - RSI, MACD, EMA, Bollinger Bands, Volume, ATR (menggunakan **pandas-ta**)
- ✅ **Interpretation System** - Scoring system (-100 to +100) dengan reason untuk setiap indikator
- ✅ **Sentiment Analysis** - Dual mode:
  - **TextBlob** (MVP, cepat, ringan ~1MB)
  - **FinBERT** (Advanced, akurat, ~500MB, optional upgrade)
- ✅ **Sentiment Impact Analysis** - Dynamic weighting berdasarkan kekuatan sentimen
- ✅ **Batch News Analysis** - Analisis multiple berita dengan distribusi positive/negative/neutral
- ✅ **Signal Generation** - Menggabungkan technical + sentiment dengan adaptive weighting
- ✅ **ATR-based Risk Management** - Stop-loss dan take-profit berdasarkan volatilitas (ATR)
- ✅ **Confidence Scoring** - Confidence level 0-100% berdasarkan signal strength

## 📦 Dependencies

### Technical Analysis
- **pandas-ta** - Comprehensive technical analysis library
  - Well-tested implementations
  - 100+ indicators available
  - Easy to use with pandas DataFrames

### Sentiment Analysis
- **TextBlob** (Phase 2a) - Simple NLP library
  - Lightweight (~1MB)
  - Pattern matching + lexicon-based
  - Good for MVP
  
- **FinBERT** (Phase 2b, optional) - ML-based
  - More accurate
  - Requires ~500MB
  - Slower startup (30-60s)

### Upgrade ke FinBERT
```bash
# Install dependencies
pip install transformers==4.36.2 torch==2.1.2

# Update code
generator = SignalGenerator(use_finbert=True)

# Atau langsung di SentimentAnalyzer
analyzer = SentimentAnalyzer(use_finbert=True)
```

**Note:** 
- Model yang digunakan: `yiyanghkust/finbert-tone`
- First time load akan download ~500MB
- Startup lambat (30-60 detik pertama kali)
- Lebih akurat untuk financial text

## 📁 Struktur File

```
analysis/
├── __init__.py                    # Module exports
├── technical_indicators.py        # RSI, MACD, EMA, BB, Volume
├── sentiment_analysis.py          # Sentiment analysis
├── signal_generator.py            # Generate trading signals
└── main_analysis.py               # Entry point untuk testing
```

## 🚀 Instalasi & Cara Menjalankan

### 1. Install Dependencies

**Opsi A: Menggunakan Script Otomatis (Recommended)**

```bash
cd backend

# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

**Opsi B: Manual Installation**

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Download TextBlob corpora (PENTING!)
python -m textblob.download_corpora
```

📚 **Panduan instalasi lengkap:** Lihat [INSTALL.md](../../INSTALL.md)

### 3. Verify Installation

Setelah instalasi, verifikasi semua dependencies terinstall dengan benar:

```bash
cd backend
python test_dependencies.py
```

Script ini akan test:
- ✅ Python version (3.11+)
- ✅ pandas-ta functionality
- ✅ TextBlob functionality
- ✅ Database connection
- ✅ Binance connection

Jika semua test passed, Anda siap menggunakan Analysis Engine!

### 4. Jalankan Data Collector
```bash
# Terminal 1: Data Collector
python -m data_collector.main_collector
```

### 5. Jalankan Analysis Engine
```bash
# Terminal 2: Analysis Engine
python -m analysis.main_analysis
```

## 📊 Output Contoh

```
======================================================================
🔍 Analyzing BTC/USDT [1h]
======================================================================
📊 Loaded 500 candles dan 20 news articles

📈 SIGNAL: STRONG_BUY
🎯 Confidence: 85.5%
💰 Current Price: $42,300.75
📊 Final Score: +72.35

📋 Reasons:
   1. [RSI] RSI 28.5 < 30 → potensi rebound
   2. [MACD] MACD histogram baru crossover ke positif → sinyal beli kuat
   3. [EMA] Harga > EMA20 > EMA50 > EMA200 → uptrend kuat
   4. [BOLLINGER] Harga (42300.75) menyentuh lower band → potensi bounce
   5. [SENTIMENT] POSITIVE → 12 positif, 3 negatif dari 20 artikel berita

🎯 Component Scores:
   RSI          | Score:  +80.0 | Signal: OVERSOLD           | Weight: 15%
   MACD         | Score:  +90.0 | Signal: BULLISH_CROSSOVER  | Weight: 25%
   EMA          | Score:  +85.0 | Signal: STRONG_UPTREND     | Weight: 25%
   BOLLINGER    | Score:  +70.0 | Signal: OVERSOLD           | Weight: 15%
   VOLUME       | Score:  +30.0 | Signal: HIGH               | Weight: 10%
   SENTIMENT    | Score:  +0.45 | Signal: POSITIVE           | Weight: 10%

🛡️  Suggested Actions:
   Action: OPEN_LONG
   Entry: $42,300.75
   Stop Loss: $41,450.75 (2.01%)
   Take Profit: $44,000.75 (4.02%)
   Risk/Reward Ratio: 2.0:1
   Position Size: 10.0% of portfolio
   Max Risk: 2.0% of portfolio

📰 Sentiment Analysis:
   Overall Score: +0.450
   Overall Label: POSITIVE
   Total Articles: 20
   Distribution: 12 positive, 3 negative, 5 neutral

⚠️  Risk Warning:
   Sinyal sangat kuat → pastikan bukan fake breakout/pump & dump | ⚠️  Ini adalah analisis otomatis, BUKAN saran keuangan. Selalu lakukan riset mandiri (DYOR).

📰 Top News Articles:
   1. [CoinDesk] Bitcoin reaches new all-time high as institutional...
      Sentiment: POSITIVE (score: +0.850)
   2. [CoinTelegraph] Ethereum 2.0 upgrade shows promising results...
      Sentiment: POSITIVE (score: +0.720)
   3. [Decrypt] Solana DeFi ecosystem continues to grow with new...
      Sentiment: POSITIVE (score: +0.680)

======================================================================
```

## 🔍 Penjelasan Komponen

### 1. Technical Analyzer (`technical_indicators.py`)

Class `TechnicalAnalyzer` menghitung dan menginterpretasi indikator teknikal dengan scoring system (-100 to +100).

#### Struktur Return
```python
{
    "indicators": {...},        # Nilai mentah indikator
    "interpretation": {...},    # Interpretasi dengan score & reason
    "latest_price": 42500.0,    # Harga terbaru
    "timestamp": "2024-01-15T10:00:00"
}
```

#### Indikator yang Dihitung

**1. RSI (Relative Strength Index)**
- **Range**: 0-100
- **Interpretation**:
  - `< 30`: OVERSOLD (score: +80) → potensi rebound
  - `> 70`: OVERBOUGHT (score: -80) → potensi koreksi
  - `30-45`: WEAK (score: +20) → momentum lemah
  - `55-70`: STRONG (score: -20) → rawan jenuh
  - `45-55`: NEUTRAL (score: 0)

**2. MACD (Moving Average Convergence Divergence)**
- **Components**: MACD line, Signal line, Histogram
- **Interpretation**:
  - Histogram crossover positif: BULLISH_CROSSOVER (score: +90)
  - Histogram crossover negatif: BEARISH_CROSSOVER (score: -90)
  - Histogram positif: BULLISH (score: +40)
  - Histogram negatif: BEARISH (score: -40)

**3. EMA (Exponential Moving Average)**
- **Periods**: 20, 50, 200
- **Interpretation**:
  - Price > EMA20 > EMA50 > EMA200: STRONG_UPTREND (score: +85)
  - Price < EMA20 < EMA50 < EMA200: STRONG_DOWNTREND (score: -85)
  - Price > EMA200: UPTREND (score: +40)
  - Price < EMA200: DOWNTREND (score: -40)

**4. Bollinger Bands**
- **Components**: Upper, Middle (SMA), Lower bands
- **Interpretation**:
  - Price ≤ Lower band: OVERSOLD (score: +70) → potensi bounce
  - Price ≥ Upper band: OVERBOUGHT (score: -70) → potensi pullback
  - Price < Middle: BEARISH (score: -20)
  - Price > Middle: BULLISH (score: +20)

**5. Volume Analysis**
- **Volume Ratio**: Current volume / 20-period SMA
- **Interpretation**:
  - `> 2.0x`: VERY_HIGH (score: +50) → konfirmasi kuat
  - `> 1.5x`: HIGH (score: +30) → aktivitas tinggi
  - `< 0.5x`: LOW (score: -30) → sinyal lemah
  - `0.5-2.0x`: NORMAL (score: 0)

**6. ATR (Average True Range)**
- **Purpose**: Volatility measurement untuk stop-loss calculation
- **Usage**: Stop-loss = 2x ATR dari entry price
- **Output**: ATR value dan ATR percentage

#### ATR-based Stop-Loss
```python
# Contoh perhitungan stop-loss
stop_loss = price - (ATR * 2.0)  # Untuk LONG
stop_loss = price + (ATR * 2.0)  # Untuk SHORT
```

**Keuntungan ATR-based:**
- Adaptive terhadap volatilitas market
- Tidak fixed percentage (lebih fleksibel)
- Berdasarkan actual price movement

### 2. Sentiment Analysis (`sentiment_analysis.py`)

Class `SentimentAnalyzer` menganalisis sentimen berita crypto dengan dua mode:

#### Mode 1: TextBlob (MVP - Default)
- **Library**: TextBlob (~1MB)
- **Kecepatan**: Cepat (<1 detik per artikel)
- **Akurasi**: Cukup baik untuk MVP
- **Method**: Pattern matching + lexicon-based
- **Return**: Polarity -1.0 sampai +1.0

#### Mode 2: FinBERT (Advanced - Optional)
- **Model**: `yiyanghkust/finbert-tone` (~500MB)
- **Kecepatan**: Lambat (30-60 detik pertama kali load)
- **Akurasi**: Tinggi untuk financial text
- **Method**: ML-based (transformers)
- **Requirements**: `pip install transformers torch`

#### API Methods

**1. `analyze_text(text: str) -> Dict`**
Analisis sentimen satu teks
```python
{
    "score": 0.75,           # -1 sampai +1
    "label": "POSITIVE",     # POSITIVE, NEGATIVE, NEUTRAL
    "confidence": 0.85,      # 0-1
    "method": "textblob"     # atau "finbert"
}
```

**2. `analyze_news_batch(news_items: List[Dict]) -> Dict`**
Analisis batch berita
```python
{
    "overall_score": 0.45,           # Rata-rata skor
    "overall_label": "POSITIVE",     # Label overall
    "positive_count": 12,            # Jumlah berita positif
    "negative_count": 3,             # Jumlah berita negatif
    "neutral_count": 5,              # Jumlah berita netral
    "total_articles": 20,            # Total artikel
    "articles": [...]                # Detail per artikel
}
```

**3. `get_sentiment_impact(sentiment_score: float) -> Dict`**
Interpretasi dampak sentimen terhadap trading decision
```python
{
    "impact": "HIGH",        # LOW, MODERATE, HIGH, VERY_HIGH
    "weight": 0.4,           # Bobot dalam keputusan final (0-1)
    "reason": "Sentimen kuat, bobot signifikan dalam keputusan"
}
```

#### Dynamic Weighting System
Bobot sentiment dalam keputusan final disesuaikan berdasarkan impact:
- **LOW** (|score| < 0.15): weight = 10%
- **MODERATE** (0.15 ≤ |score| < 0.4): weight = 25%
- **HIGH** (0.4 ≤ |score| < 0.7): weight = 40%
- **VERY_HIGH** (|score| ≥ 0.7): weight = 50%

Technical analysis weight = 100% - sentiment weight

### 3. Signal Generator (`signal_generator.py`)

Class `SignalGenerator` menggabungkan analisis teknikal dan sentimen menjadi trading signal yang actionable.

#### Architecture
```python
SignalGenerator
├── WEIGHTS (constants)
│   ├── rsi: 0.15
│   ├── macd: 0.25
│   ├── ema: 0.25
│   ├── bollinger: 0.15
│   ├── volume: 0.10
│   └── sentiment: 0.10
│
├── THRESHOLDS (constants)
│   ├── strong_buy: 75
│   ├── buy: 55
│   ├── neutral: 45
│   ├── sell: 55
│   └── strong_sell: 75
│
└── Methods
    ├── generate_signal()          # Main entry point
    ├── _score_to_signal()         # Convert score to signal
    ├── _get_sentiment_impact()    # Sentiment impact analysis
    ├── _collect_reasons()         # Collect reasons for signal
    ├── _calculate_suggested_actions()  # Entry/SL/TP calculation
    └── _generate_risk_warning()   # Risk warning generation
```

#### Main Method: `generate_signal()`

**Input:**
```python
signal_gen.generate_signal(
    symbol="BTC/USDT",
    timeframe="1h",
    technical_analysis=technical_result,  # From TechnicalAnalyzer
    sentiment_analysis=sentiment_result   # From SentimentAnalyzer
)
```

**Output Structure:**
```python
{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "timestamp": "2024-01-15T10:00:00",
    "signal": "STRONG_BUY",           # STRONG_BUY, BUY, NEUTRAL, SELL, STRONG_SELL
    "confidence": 85.5,               # 0-100
    "final_score": 72.35,             # -100 to +100
    "latest_price": 42300.75,
    "technical_score": 68.50,         # Weighted technical score
    "sentiment_score": 0.450,         # -1 to +1
    "sentiment_label": "POSITIVE",
    
    "component_scores": {             # Detailed breakdown
        "rsi": {"score": 80, "signal": "OVERSOLD", "weight": 0.15},
        "macd": {"score": 90, "signal": "BULLISH_CROSSOVER", "weight": 0.25},
        "ema": {"score": 85, "signal": "STRONG_UPTREND", "weight": 0.25},
        "bollinger": {"score": 70, "signal": "OVERSOLD", "weight": 0.15},
        "volume": {"score": 30, "signal": "HIGH", "weight": 0.10},
        "sentiment": {"score": 0.450, "label": "POSITIVE", "impact": "HIGH", "weight": 0.10}
    },
    
    "reasons": [                      # Top reasons (max 7)
        "[RSI] RSI 28.5 < 30 → potensi rebound",
        "[MACD] MACD histogram baru crossover ke positif → sinyal beli kuat",
        "[EMA] Harga > EMA20 > EMA50 > EMA200 → uptrend kuat",
        "[SENTIMENT] POSITIVE → 12 positif, 3 negatif dari 20 artikel berita"
    ],
    
    "suggested_actions": {            # Actionable trading plan
        "action": "OPEN_LONG",
        "entry": 42300.75,
        "stop_loss": 41450.75,        # 2x ATR
        "take_profit": 44000.75,      # 2x SL distance
        "risk_reward_ratio": 2.0,
        "position_size_percent": 10,  # Based on confidence
        "max_risk_percent": 2.0,
        "sl_distance_percent": 2.01,
        "tp_distance_percent": 4.02
    },
    
    "risk_warning": "⚠️  Ini adalah analisis otomatis, BUKAN saran keuangan. Selalu lakukan riset mandiri (DYOR)."
}
```

#### Signal Types & Thresholds

| Signal | Score Range | Confidence | Action |
|--------|-------------|------------|--------|
| **STRONG_BUY** | ≥ 60 | 60-100% | OPEN_LONG |
| **BUY** | 30 to 59 | 30-59% | OPEN_LONG |
| **NEUTRAL** | -29 to 29 | High (100-|score|) | HOLD |
| **SELL** | -59 to -30 | 30-59% | OPEN_SHORT |
| **STRONG_SELL** | ≤ -60 | 60-100% | OPEN_SHORT |

#### Scoring System

**1. Technical Score (90% weight)**
```python
weighted_tech_score = sum(
    tech_scores[k] * WEIGHTS[k]
    for k in ["rsi", "macd", "ema", "bollinger", "volume"]
)
```

**2. Sentiment Score (10% weight)**
```python
sentiment_impact = _get_sentiment_impact(sentiment_score)
sentiment_scaled = sentiment_score * 100 * sentiment_impact["weight"]
```

**3. Final Score**
```python
final_score = (weighted_tech_score * 0.9) + (sentiment_scaled * 0.1)
```

#### Position Sizing (Based on Confidence)

| Confidence | Position Size | Risk Level |
|------------|---------------|------------|
| ≥ 75% | 10% of portfolio | Aggressive |
| 60-74% | 5% of portfolio | Moderate |
| < 60% | 2% of portfolio | Conservative |

**Max Risk per Trade:** 2% of portfolio (industry standard)

#### ATR-based Risk Management

**Stop Loss Calculation:**
```python
sl_distance = atr * 2  # 2x ATR
stop_loss = price - sl_distance  # For LONG
```

**Take Profit Calculation:**
```python
tp_distance = sl_distance * 2.0  # Risk/Reward ratio 2:1
take_profit = price + tp_distance  # For LONG
```

**Keuntungan ATR-based:**
- ✅ Adaptive terhadap volatilitas market
- ✅ Stop-loss lebih akurat daripada fixed percentage
- ✅ Risk/reward ratio konsisten (2:1)
- ✅ Position sizing berdasarkan confidence

#### Risk Warning System

Automatic risk warnings based on conditions:
- **Low Confidence (< 60%)**: "Confidence rendah → pertimbangkan untuk tidak entry"
- **Strong Signal**: "Sinyal sangat kuat → pastikan bukan fake breakout/pump & dump"
- **Always**: "⚠️  Ini adalah analisis otomatis, BUKAN saran keuangan. Selalu lakukan riset mandiri (DYOR)."

## 🧪 Testing

### Test Individual Components

```python
from analysis.technical_indicators import TechnicalAnalyzer
from analysis.sentiment_analysis import SentimentAnalyzer
from analysis.signal_generator import SignalGenerator

# 1. Test Technical Analyzer
ta = TechnicalAnalyzer()
technical_result = ta.calculate_all(candles_list)
print(f"Latest Price: ${technical_result['latest_price']:,.2f}")
print(f"RSI: {technical_result['indicators']['rsi']['value']:.2f}")
print(f"RSI Interpretation: {technical_result['interpretation']['rsi']}")

# 2. Test Sentiment Analysis
sa = SentimentAnalyzer(use_finbert=False)
news_items = [
    {"title": "Bitcoin rises", "summary": "BTC up 5%", "source": "CoinDesk", "link": "..."},
    {"title": "Market crash", "summary": "Crypto down 10%", "source": "CoinTelegraph", "link": "..."},
]
sentiment_result = sa.analyze_news_batch(news_items)
print(f"Overall: {sentiment_result['overall_label']} ({sentiment_result['overall_score']:+.3f})")
print(f"Distribution: {sentiment_result['positive_count']} pos, {sentiment_result['negative_count']} neg")

# 3. Test Signal Generator
sg = SignalGenerator()
signal = sg.generate_signal(
    symbol="BTC/USDT",
    timeframe="1h",
    technical_analysis=technical_result,
    sentiment_analysis=sentiment_result
)

print(f"\n📈 Signal: {signal['signal']}")
print(f"🎯 Confidence: {signal['confidence']:.1f}%")
print(f"💰 Price: ${signal['latest_price']:,.2f}")
print(f"📊 Final Score: {signal['final_score']:+.2f}")

print(f"\n🛡️  Suggested Actions:")
actions = signal['suggested_actions']
print(f"   Action: {actions['action']}")
if actions['action'] != "HOLD":
    print(f"   Entry: ${actions['entry']:,.2f}")
    print(f"   Stop Loss: ${actions['stop_loss']:,.2f}")
    print(f"   Take Profit: ${actions['take_profit']:,.2f}")
    print(f"   Position Size: {actions['position_size_percent']:.1f}%")

print(f"\n⚠️  Risk Warning:")
print(f"   {signal['risk_warning']}")
```

### Run Full Analysis

```bash
# Pastikan data collector sudah berjalan
cd backend
python -m analysis.main_analysis
```

## 📈 Contoh Penggunaan

### Analisis Satu Symbol
```python
import asyncio
from analysis.main_analysis import analyze_symbol

async def main():
    await analyze_symbol("BTC/USDT", "1h")

asyncio.run(main())
```

### Analisis Semua Symbols
```python
import asyncio
from analysis.main_analysis import analyze_all_symbols

async def main():
    await analyze_all_symbols()

asyncio.run(main())
```

## 🎯 Upgrade ke ML-based Sentiment

Jika ingin menggunakan ML-based sentiment analysis:

### 1. Install dependencies
```bash
pip install transformers==4.36.2 torch==2.1.2
```

### 2. Update code
```python
# Di signal_generator.py atau main_analysis.py
generator = SignalGenerator(use_ml_sentiment=True)
```

### 3. Note
- Butuh download model ~440MB pertama kali
- Startup lebih lambat (30-60 detik)
- Lebih akurat tapi lebih berat

## 📊 Performance

### Resource Usage
- **CPU**: < 10%
- **RAM**: ~100-200MB
- **Analysis Time**: ~1-2 detik per symbol
- **Total Time**: ~10 detik untuk 5 symbols

### Data Requirements
- **Minimum candles**: 200 (untuk EMA 200)
- **Recommended**: 500 candles
- **News articles**: 20+ untuk sentiment yang reliable

## 🐛 Troubleshooting

### Error: "Data terlalu sedikit"
```
⚠️  Data terlalu sedikit (50 candles), butuh minimal 200
```
**Solusi**: Jalankan data collector lebih lama untuk mengumpulkan lebih banyak data

### Error: "textblob not installed"
```
❌ TextBlob error: ...
```
**Solusi**: Install textblob dengan `pip install textblob==0.17.1` dan download corpora: `python -m textblob.download_corpora`

### Error: "transformers not installed" (jika pakai FinBERT)
```
⚠️  FinBERT gagal dimuat: ... Fallback ke TextBlob
```
**Solusi**: Ini normal jika transformers belum diinstall. Install dengan `pip install transformers==4.36.2 torch==2.1.2`

### Error: "FinBERT download gagal"
```
🧠 Loading FinBERT model (first time may download ~500MB)...
⚠️  FinBERT gagal dimuat: ... Fallback ke TextBlob
```
**Solusi**: 
- Check koneksi internet
- Model akan otomatis fallback ke TextBlob
- Retry setelah koneksi stabil
- Atau gunakan TextBlob saja (sudah cukup baik untuk MVP)

### Signal selalu HOLD
**Penyebab**: Data belum cukup atau market sideways
**Solusi**: 
- Tunggu data lebih banyak
- Coba timeframe berbeda (4h, 1d)
- Check apakah market memang sideways

## 📚 Resources

### Technical Analysis
- [pandas-ta Documentation](https://github.com/twopirllc/pandas-ta)
- [RSI Explanation](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD Tutorial](https://www.investopedia.com/terms/m/macd.asp)
- [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)

### Sentiment Analysis
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [FinBERT Tone Model](https://huggingface.co/yiyanghkust/finbert-tone) (optional upgrade)
- [Original FinBERT](https://huggingface.co/ProsusAI/finbert) (alternative)

## ✅ Status

**Analysis Engine: COMPLETE ✅**

### Technical Analysis
- ✅ Technical indicators (RSI, MACD, EMA, BB, Volume, ATR) - menggunakan **pandas-ta**
- ✅ Interpretation system dengan scoring (-100 to +100)
- ✅ Detailed reason untuk setiap indikator

### Sentiment Analysis
- ✅ Dual mode:
  - **TextBlob** (MVP, cepat, ringan ~1MB)
  - **FinBERT** (Advanced, akurat, ~500MB, optional)
- ✅ Sentiment impact analysis dengan dynamic weighting
- ✅ Batch news analysis dengan distribusi positive/negative/neutral
- ✅ Top news articles dengan sentiment detail

### Signal Generation
- ✅ Weighted scoring system (technical 90% + sentiment 10%)
- ✅ Component scores breakdown (RSI, MACD, EMA, BB, Volume, Sentiment)
- ✅ 5 signal types: STRONG_BUY, BUY, NEUTRAL, SELL, STRONG_SELL
- ✅ Confidence scoring (0-100%)
- ✅ Max 7 reasons untuk clarity

### Risk Management
- ✅ ATR-based stop-loss (2x ATR)
- ✅ ATR-based take-profit (2:1 risk/reward ratio)
- ✅ Position sizing berdasarkan confidence:
  - ≥ 75% confidence → 10% position
  - 60-74% confidence → 5% position
  - < 60% confidence → 2% position
- ✅ Max 2% risk per trade (industry standard)
- ✅ Suggested entry, stop-loss, take-profit

### Safety Features
- ✅ Risk warning system
- ✅ Low confidence warning
- ✅ Strong signal warning (fake breakout detection)
- ✅ DYOR disclaimer (Not financial advice)

### Testing & Documentation
- ✅ Testing entry point (`main_analysis.py`)
- ✅ Comprehensive documentation
- ✅ Example output
- ✅ API reference

---

**Ready for Phase 3: Paper Trading Engine! 🚀**
