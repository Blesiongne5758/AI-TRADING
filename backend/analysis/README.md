# 📊 Analysis Engine - Fase 2

Analysis Engine adalah modul yang menganalisis data dari Data Collector dan menghasilkan trading signals.

## 🎯 Fitur

- ✅ **Technical Indicators** - RSI, MACD, EMA, Bollinger Bands, Volume, ATR (menggunakan **pandas-ta**)
- ✅ **Interpretation System** - Scoring system (-100 to +100) dengan reason untuk setiap indikator
- ✅ **Sentiment Analysis** - TextBlob (Phase 2a, simple & lightweight) dengan opsi FinBERT (Phase 2b, ML-based)
- ✅ **Signal Generation** - Menggabungkan technical + sentiment menjadi trading signal dengan weighted scoring
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
# Uncomment di requirements.txt
pip install transformers==4.36.2 torch==2.1.2

# Update code
generator = SignalGenerator(use_ml_sentiment=True)
```

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
📊 Loaded 500 candles dan 60 news articles

📈 SIGNAL: BUY
🎯 Confidence: 75%
💰 Current Price: $42,300.75

📋 Reasons:
   1. Strong buy signal (score: +0.65)
   2. RSI 28.5 < 30 → potensi rebound
   3. MACD histogram baru crossover ke positif → sinyal beli kuat
   4. Harga > EMA20 > EMA50 > EMA200 → uptrend kuat
   5. News sentiment bullish (+0.72)

🛡️  Risk Management (ATR-based):
   ATR: 425.50
   Stop Loss: $41,449.75 (2.02%)
   Take Profit: $44,413.50
   Risk/Reward Ratio: 2.50:1
   Position Size: 10.0% of portfolio

📊 Technical Indicators:
   RSI: 28.50
   MACD: 125.50 (Signal: 98.30)
   EMA 20/50/200: 42150.00 / 41800.00 / 40500.00
   Bollinger Bands: 41500.00 - 43000.00
   Volume Ratio: 1.85x

🔍 Interpretation:
   RSI: OVERSOLD (score: +80)
      → RSI 28.5 < 30 → potensi rebound
   MACD: BULLISH_CROSSOVER (score: +90)
      → MACD histogram baru crossover ke positif → sinyal beli kuat
   EMA: STRONG_UPTREND (score: +85)
      → Harga > EMA20 > EMA50 > EMA200 → uptrend kuat
   BOLLINGER: OVERSOLD (score: +70)
      → Harga (42300.75) menyentuh lower band → potensi bounce
   VOLUME: HIGH (score: +30)
      → Volume 1.85x rata-rata → aktivitas tinggi

📰 Sentiment Analysis:
   Score: +0.720
   Label: BULLISH
   Confidence: 85%
   Method: textblob
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

#### Phase 2a: TextBlob (Current)
- Menggunakan **TextBlob** library
- Pattern matching + lexicon-based approach
- Lightweight (~1MB)
- Polarity: -1.0 (bearish) sampai +1.0 (bullish)
- Subjectivity: 0.0 (objective) sampai 1.0 (subjective)
- Good untuk MVP dan quick testing

#### Phase 2b: FinBERT (Optional Upgrade)
- Menggunakan **FinBERT** model (transformers)
- ML-based, lebih akurat untuk financial text
- Butuh transformers + torch (~500MB)
- Startup lambat (30-60 detik pertama kali)
- Lebih baik untuk production

### 3. Signal Generator (`signal_generator.py`)

#### Weighted Scoring System
- **Technical Interpretation**: 70% weight (average of indicator scores)
- **Sentiment Analysis**: 30% weight
- **Final Score**: (tech_avg_score × 0.7) + (sentiment_score × 0.3)

#### Signal Thresholds
- **BUY**: final_score > 0.2
- **SELL**: final_score < -0.2
- **HOLD**: -0.2 ≤ final_score ≤ 0.2

#### Confidence Calculation
- Confidence = |final_score| × 100
- Range: 0-100%

#### ATR-based Risk Management
- **Stop Loss**: 2x ATR dari entry price
- **Take Profit**: 2.5x risk distance (R:R ratio 2.5:1)
- **Position Size**: 10% of portfolio (default)
- **ATR Multiplier**: 2.0 (configurable)

**Keuntungan ATR-based:**
- Adaptive terhadap volatilitas market
- Stop-loss lebih akurat daripada fixed percentage
- Risk/reward ratio konsisten

## 🧪 Testing

### Test Individual Components

```python
from analysis.technical_indicators import TechnicalAnalyzer
from analysis.sentiment_analysis import SentimentAnalyzer
from analysis.signal_generator import SignalGenerator

# Test Technical Analyzer
ta = TechnicalAnalyzer()
result = ta.calculate_all(candles_list)
print(f"Latest Price: {result['latest_price']}")
print(f"RSI: {result['indicators']['rsi']['value']}")
print(f"RSI Interpretation: {result['interpretation']['rsi']}")

# Test Sentiment Analysis
sa = SentimentAnalyzer()
sentiment = sa.analyze("Bitcoin reaches new all-time high")
print(f"Score: {sentiment['score']}")
print(f"Label: {sentiment['label']}")

# Test Signal Generator
sg = SignalGenerator()
signal = sg.generate(candles_list, news_texts, "BTC/USDT", "1h")
print(f"Action: {signal['action']}")
print(f"Confidence: {signal['confidence']}%")
print(f"Stop Loss: ${signal['risk_management']['stop_loss']}")
print(f"ATR: {signal['risk_management']['atr']}")
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
⚠️  textblob not installed, sentiment analysis will use fallback
```
**Solusi**: Install textblob dengan `pip install textblob==0.17.1`

### Error: "transformers not installed" (jika pakai FinBERT)
```
⚠️  transformers/torch not installed, using TextBlob only
```
**Solusi**: Ini normal untuk Phase 2a. Install transformers jika ingin upgrade ke FinBERT

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
- [FinBERT Model](https://huggingface.co/ProsusAI/finbert) (optional upgrade)

## ✅ Status

**Analysis Engine: COMPLETE ✅**

- ✅ Technical indicators (RSI, MACD, EMA, BB, Volume, ATR) - menggunakan **pandas-ta**
- ✅ Interpretation system dengan scoring (-100 to +100)
- ✅ Sentiment analysis - menggunakan **TextBlob** (simple & lightweight)
- ✅ Signal generation dengan weighted scoring
- ✅ ATR-based risk management
- ✅ Confidence scoring
- ✅ Testing entry point

---

**Ready for Phase 3: Paper Trading Engine! 🚀**
