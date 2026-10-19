# 📊 Analysis Engine - Fase 2

Analysis Engine adalah modul yang menganalisis data dari Data Collector dan menghasilkan trading signals.

## 🎯 Fitur

- ✅ **Technical Indicators** - RSI, MACD, EMA, Bollinger Bands, Volume
- ✅ **Sentiment Analysis** - Rule-based (Phase 2a) dengan opsi ML-based (Phase 2b)
- ✅ **Signal Generation** - Menggabungkan semua analisis menjadi trading signal
- ✅ **Risk Management** - Stop-loss, take-profit, position sizing
- ✅ **Confidence Scoring** - Weighted voting system

## 📁 Struktur File

```
analysis/
├── __init__.py                    # Module exports
├── technical_indicators.py        # RSI, MACD, EMA, BB, Volume
├── sentiment_analysis.py          # Sentiment analysis
├── signal_generator.py            # Generate trading signals
└── main_analysis.py               # Entry point untuk testing
```

## 🚀 Cara Menjalankan

### 1. Pastikan Data Collector sudah berjalan
```bash
# Terminal 1: Data Collector
python -m data_collector.main_collector
```

### 2. Jalankan Analysis Engine
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
   2. RSI oversold (28.5)
   3. MACD bullish crossover
   4. EMA alignment bullish
   5. News sentiment bullish (+0.72)

🛡️  Risk Management:
   Stop Loss: $41,454.74
   Take Profit: $44,415.79
   Risk/Reward Ratio: 2.50
   Position Size: 10.0% of portfolio

📊 Technical Indicators:
   RSI: 28.50 (BUY)
   MACD: 125.50 (BUY)
   EMA 20/50/200: 42150.00 / 41800.00 / 40500.00
   Bollinger Bands: 41500.00 - 43000.00
   Volume Ratio: 1.85x

📰 Sentiment Analysis:
   Score: +0.720
   Label: BULLISH
   Confidence: 85%
   Method: rule-based
```

## 🔍 Penjelasan Komponen

### 1. Technical Indicators (`technical_indicators.py`)

#### RSI (Relative Strength Index)
- **Range**: 0-100
- **Overbought**: > 70 (potensi turun)
- **Oversold**: < 30 (potensi naik)
- **Signal**: BUY jika < 30, SELL jika > 70

#### MACD (Moving Average Convergence Divergence)
- **Components**: MACD line, Signal line, Histogram
- **Bullish**: MACD > Signal line
- **Bearish**: MACD < Signal line
- **Signal**: BUY jika MACD crossover ke atas

#### EMA (Exponential Moving Average)
- **Periods**: 20, 50, 200
- **Uptrend**: Price > EMA20 > EMA50 > EMA200
- **Downtrend**: Price < EMA20 < EMA50 < EMA200
- **Signal**: BUY jika alignment bullish

#### Bollinger Bands
- **Components**: Upper, Middle (SMA), Lower bands
- **Overbought**: Price > Upper band
- **Oversold**: Price < Lower band
- **Signal**: BUY jika price < lower band

#### Volume Analysis
- **Volume Ratio**: Current volume / Average volume
- **High Volume**: > 1.5x average
- **Signal**: BUY jika high volume + price up

### 2. Sentiment Analysis (`sentiment_analysis.py`)

#### Phase 2a: Rule-based (Current)
- Menggunakan keyword matching
- Bullish keywords: "bull", "rally", "surge", "adoption", dll
- Bearish keywords: "bear", "crash", "plunge", "ban", dll
- Score: -1.0 (bearish) sampai +1.0 (bullish)

#### Phase 2b: ML-based (Optional Upgrade)
- Menggunakan FinBERT model
- Butuh transformers + torch (~2.5GB)
- Lebih akurat tapi lebih berat

### 3. Signal Generator (`signal_generator.py`)

#### Weighted Voting System
- **Technical**: 70% weight
- **Sentiment**: 30% weight
- **Final Score**: (tech_score × 0.7) + (sentiment_score × 0.3)

#### Signal Thresholds
- **BUY**: score > 0.2
- **SELL**: score < -0.2
- **HOLD**: -0.2 ≤ score ≤ 0.2

#### Confidence Calculation
- Confidence = |final_score| × 100
- Range: 0-100%

#### Risk Management
- **Stop Loss**: 2% dari entry price
- **Take Profit**: 5% dari entry price
- **Risk/Reward Ratio**: 2.5:1
- **Position Size**: 10% of portfolio

## 🧪 Testing

### Test Individual Components

```python
from analysis.technical_indicators import TechnicalIndicators
from analysis.sentiment_analysis import SentimentAnalyzer
from analysis.signal_generator import SignalGenerator
import pandas as pd

# Test Technical Indicators
ti = TechnicalIndicators()
indicators = ti.calculate_all(df)
print(f"RSI: {indicators['rsi']}")
print(f"Signal: {indicators['signal']}")

# Test Sentiment Analysis
sa = SentimentAnalyzer()
sentiment = sa.analyze("Bitcoin reaches new all-time high")
print(f"Score: {sentiment['score']}")
print(f"Label: {sentiment['label']}")

# Test Signal Generator
sg = SignalGenerator()
signal = sg.generate(df, news_texts, "BTC/USDT", "1h")
print(f"Action: {signal['action']}")
print(f"Confidence: {signal['confidence']}%")
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

### Error: "transformers not installed"
```
⚠️  transformers/torch not installed, using rule-based only
```
**Solusi**: Ini normal untuk Phase 2a. Install transformers jika ingin ML-based

### Signal selalu HOLD
**Penyebab**: Data belum cukup atau market sideways
**Solusi**: 
- Tunggu data lebih banyak
- Coba timeframe berbeda (4h, 1d)
- Check apakah market memang sideways

## 📚 Resources

- [RSI Explanation](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD Tutorial](https://www.investopedia.com/terms/m/macd.asp)
- [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)
- [FinBERT Model](https://huggingface.co/ProsusAI/finbert)

## ✅ Status

**Analysis Engine: COMPLETE ✅**

- ✅ Technical indicators (RSI, MACD, EMA, BB, Volume)
- ✅ Sentiment analysis (rule-based)
- ✅ Signal generation
- ✅ Risk management
- ✅ Confidence scoring
- ✅ Testing entry point

---

**Ready for Phase 3: Paper Trading Engine! 🚀**
