# 🤖 XAI (Explainable AI) Module

Modul XAI bertanggung jawab untuk menjelaskan keputusan trading bot dalam bahasa manusia yang mudah dipahami pemula.

## 📁 Struktur File

```
xai/
├── __init__.py                    # Module exports
├── explanation_generator.py       # Generate narasi penjelasan dari signal
├── trading_dictionary.py          # Kamus 50+ istilah trading
├── context_builder.py             # Bangun konteks dari database
├── chat_agent.py                  # Chat interface dengan pattern matching
└── main_xai.py                    # Entry point untuk testing & demo
```

## 🎯 Fitur Utama

### 1. **Explanation Generator**
Mengubah data teknis menjadi narasi penjelasan yang mudah dipahami:
- Penjelasan detail dari signal trading
- Breakdown indikator teknikal
- Analisis sentimen berita
- Risk management explanation
- Catatan edukasi untuk pemula

### 2. **Trading Dictionary**
Kamus 50+ istilah trading dengan:
- Definisi dalam bahasa Indonesia
- Contoh penggunaan
- Interpretasi nilai
- Kategori (technical, trading, risk, sentiment, dll)

**Contoh istilah:**
- RSI, MACD, EMA, Bollinger Bands, ATR
- Long, Short, Entry, Exit, Stop Loss, Take Profit
- Bullish, Bearish, Overbought, Oversold
- Win Rate, Profit Factor, Drawdown
- Dan banyak lagi!

### 3. **Context Builder**
Membangun konteks dari database untuk penjelasan yang lebih kaya:
- Current price dan ticker data
- Recent candles (24 jam terakhir)
- Recent news
- Open positions
- Portfolio statistics
- Trade history

### 4. **Chat Agent** (Intent-Based System)
Chat interface canggih dengan **intent detection** menggunakan regex pattern matching:

**Intent yang Didukung:**
- `greeting` - Salam dan perkenalan
- `explain_indicator` - Penjelasan indikator teknikal (RSI, MACD, EMA, dll)
- `explain_concept` - Penjelasan konsep trading (long, short, stop-loss, dll)
- `why_trade` - Penjelasan keputusan bot ("kenapa bot beli BTC?")
- `portfolio_status` - Status portfolio dan P&L
- `market_condition` - Kondisi market dan harga terbaru
- `recent_trades` - Riwayat trade terakhir
- `help` - Panduan penggunaan
- `thanks` - Ucapan terima kasih

**Fitur Canggih:**
- Natural language understanding dengan regex patterns
- Fuzzy matching untuk variasi pertanyaan
- Context-aware responses dari database
- Fallback ke dictionary search untuk pertanyaan tidak dikenal
- Integrasi penuh dengan TradingDictionary dan ContextBuilder

**Contoh Pertanyaan:**
```
👤 "halo"
🤖 → Greeting response

👤 "apa itu RSI?"
🤖 → Full explanation dari dictionary

👤 "kenapa bot beli BTC?"
🤖 → Signal context + explanation

👤 "status portfolio saya"
🤖 → Portfolio context dari database

👤 "bagaimana kondisi market?"
🤖 → Market context dengan harga & berita
```

## 🚀 Cara Menggunakan

### 1. Jalankan Demo
```bash
cd backend
python -m xai.main_xai
```

Output akan menampilkan:
- Demo explanation generator
- Demo trading dictionary
- Demo context builder
- Demo chat agent
- Interactive chat session (optional)

### 2. Interactive Chat
```bash
cd backend
python -m xai.main_xai
# Ketik 'y' saat ditanya untuk mulai interactive chat
```

**Contoh pertanyaan:**
```
👤 You: apa itu RSI?
🤖 Bot: 📖 RSI (Relative Strength Index)
   Indikator momentum yang mengukur kecepatan dan perubahan pergerakan harga...

👤 You: portfolio
🤖 Bot: 💼 PORTFOLIO STATUS:
   📊 Total Trades: 10
   🎯 Win Rate: 70.0%
   💰 Total P&L: $+1,234.56
   ...

👤 You: analisis BTC
🤖 Bot: 📈 ANALISIS BTC/USDT:
   💰 Current Price: $67,234.50
   🟢 24h Change: +2.34%
   ...
```

### 3. Gunakan di Code
```python
from xai import ExplanationGenerator, TradingDictionary, ChatAgent
from data_collector.database import DatabaseManager

# Initialize
db = DatabaseManager()
await db.initialize()

# Generate explanation dari signal
generator = ExplanationGenerator()
explanation = generator.generate_explanation(signal)
print(explanation)

# Search istilah di kamus
dictionary = TradingDictionary()
term = dictionary.get_term("rsi")
print(dictionary.format_term_explanation(term))

# Chat agent
chat = ChatAgent(db)
response = await chat.process_message("apa itu MACD?")
print(response)
```

## 📊 Contoh Output

### Explanation Generator
```
======================================================================
🤖 PENJELASAN KEPUTUSAN BOT
======================================================================

🟢 Bot MEREKOMENDASIKAN BELI BTC/USDT
   Confidence: 85.5% | Score: +78.45

📊 ANALISIS DETAIL:

   1️⃣  ANALISIS TEKNIKAL:
      🟢 RSI: OVERSOLD
         → RSI 28.5 < 30 → potensi rebound
      🟢 MACD: BULLISH_CROSSOVER
         → MACD histogram baru crossover ke positif → sinyal beli kuat
      🟢 EMA: STRONG_UPTREND
         → Harga > EMA20 > EMA50 > EMA200 → uptrend kuat

   2️⃣  ANALISIS SENTIMEN:
      🟢 Sentimen berita: positif (score: +0.450)
         → 12 berita positif, 3 berita negatif dari 20 artikel

🛡️  RISK MANAGEMENT:

   💰 Entry Price: $67,234.50
   🛑 Stop Loss: $65,834.50 (-2.08%)
      → Jika harga turun ke $65,834.50, posisi otomatis ditutup
      → Maksimal loss: 2.08% dari entry

   🎯 Take Profit: $70,034.50 (+4.16%)
      → Jika harga naik ke $70,034.50, posisi otomatis ditutup
      → Target profit: 4.16% dari entry

   📊 Risk/Reward Ratio: 1:2.0
      → Untuk setiap $1 risiko, target profit $2.0

   💼 Position Size: 10.0% dari portfolio
      → Max risk per trade: 2% dari portfolio

📚 CATATAN EDUKASI:

   💡 Mengapa bot merekomendasikan BELI?
      → Indikator teknikal menunjukkan kondisi bullish
      → Sentimen berita cenderung positif
      → Ada potensi harga naik dalam jangka pendek

   ⚠️  Penting untuk diingat:
      → Trading selalu memiliki risiko
      → Stop-loss WAJIB digunakan untuk membatasi kerugian
      → Jangan invest uang yang tidak siap Anda rugikan
      → DYOR (Do Your Own Research) sebelum trading

======================================================================
```

### Trading Dictionary
```
📖 RSI (Relative Strength Index)
   Indikator momentum yang mengukur kecepatan dan perubahan pergerakan harga. Nilainya 0-100.

   Interpretasi:
     • > 70: Overbought (jenuh beli) - potensi harga turun
     • < 30: Oversold (jenuh jual) - potensi harga naik
     • 30-70: Netral - tidak ada sinyal kuat

   💡 Contoh: RSI BTC = 28 → Market oversold, potensi rebound naik

   🏷️  Kategori: technical
```

### Chat Agent (Intent-Based System)
```
👤 User: halo
🤖 Bot:
👋 **Halo! Saya AI Trading Assistant**

Saya di sini untuk membantu Anda memahami trading dan keputusan yang diambil oleh bot.

💡 **Yang bisa saya bantu:**
• Jelaskan istilah trading (RSI, MACD, dll)
• Jelaskan kenapa bot melakukan trade tertentu
• Cek status portfolio Anda
• Analisis kondisi market
• Dan banyak lagi!

👤 User: apa itu RSI?
🤖 Bot:
📖 **RSI (Relative Strength Index)**

Indikator momentum yang mengukur kecepatan dan perubahan pergerakan harga. Nilainya 0-100.

**Interpretasi:**
• > 70: Overbought (potensi turun)
• < 30: Oversold (potensi naik)
• 30-70: Netral

💡 **Contoh:** RSI BTC = 28 → Market oversold, potensi rebound

👤 User: kenapa bot beli BTC?
🤖 Bot:
🤔 **Mengapa bot melakukan BUY pada BTC/USDT?**

📊 **Analisis BTC/USDT:**
💰 Harga: $67,234.50
🟢 RSI: OVERSOLD (score: +80)
🟢 MACD: BULLISH_CROSSOVER (score: +90)
🟢 EMA: STRONG_UPTREND (score: +85)

💡 **Kesimpulan**:
Bot menganalisis kombinasi indikator teknikal dan sentimen berita. Jika mayoritas indikator sejalan, bot akan memberikan sinyal BUY.

👤 User: status portfolio saya
🤖 Bot:
💼 **Status Portfolio Anda:**

📈 **Posisi Terbuka (1):**
💰 BTC/USDT (LONG)
   Entry: $67,234.50 → Current: $68,500.00
   PnL: +$1,885.00 | SL: $65,834.50 | TP: $70,034.50

📊 **Statistik Trading:**
• Total trades: 15
• Win rate: 73.3%
• Profit factor: 2.45
• Total PnL: +$1,234.56

👤 User: trade terakhir
🤖 Bot:
📜 **Riwayat Trade:**
💰 BTC/USDT (long)
   Entry: $67,234.50 → Exit: $70,034.50
   PnL: +$417.50 (+4.16%) - TAKE_PROFIT
💸 ETH/USDT (short)
   Entry: $3,450.00 → Exit: $3,520.00
   PnL: -$70.00 (-2.03%) - STOP_LOSS
```

## 🎓 Fitur Edukasi

### 1. **Penjelasan Bertahap**
- Summary singkat di awal
- Detail penjelasan di tengah
- Catatan edukasi di akhir

### 2. **Visual Indicators**
- Emoji untuk quick scanning (🟢 bullish, 🔴 bearish, ⚪ neutral)
- Aligned columns untuk readability
- Section headers yang jelas

### 3. **Kamus Interaktif**
- 50+ istilah trading
- Search functionality
- Category-based browsing
- Contoh penggunaan real

### 4. **Context-Aware**
- Informasi real-time dari database
- Portfolio statistics
- Trade history
- Market data

## 📚 Kategori Istilah

### Technical Analysis
- RSI, MACD, EMA, Bollinger Bands, ATR, Volume
- Support, Resistance, Golden Cross, Death Cross

### Trading Terms
- Long, Short, Entry, Exit, P&L
- Stop Loss, Take Profit, Position Size

### Risk Management
- Risk Management, Position Sizing, Daily Loss Limit
- Drawdown, Risk/Reward Ratio

### Sentiment Analysis
- Sentiment, Bullish, Bearish

### Market Conditions
- Overbought, Oversold, Breakout, Consolidation

### Performance Metrics
- Win Rate, Profit Factor, Sharpe Ratio

### General
- Paper Trading, DYOR, FOMO, HODL, Trading Fee

## 🔧 Configuration

### Custom Intents di Chat Agent
Edit `chat_agent.py` untuk menambah intent baru:

```python
def _build_intents(self) -> Dict:
    return {
        # Intent yang sudah ada...
        "greeting": {...},
        "explain_indicator": {...},
        
        # Tambah intent baru
        "custom_intent": {
            "patterns": [
                r"pattern1\s+(\w+)",
                r"pattern2\s+(\w+)",
            ],
            "response": self._handle_custom_intent,
        },
    }

async def _handle_custom_intent(self, match, message: str) -> str:
    """Handle custom intent"""
    param = match.group(1)
    return f"Custom response untuk {param}"
```

### Custom Terms di Dictionary
Edit `trading_dictionary.py` untuk menambah istilah:

```python
self.terms = {
    "custom_term": {
        "name": "Custom Term",
        "category": "custom",
        "simple": "Penjelasan sederhana",
        "detailed": "Penjelasan detail",
        "analogy": "Analogi untuk pemula",
        "example": "Contoh penggunaan"
    }
}
```

## 🎯 Best Practices

### 1. **Gunakan untuk Edukasi**
- Jelaskan keputusan bot ke user
- Bantu pemula memahami trading
- Build confidence melalui pemahaman

### 2. **Interactive Learning**
- Encourage questions
- Provide examples
- Link concepts together

### 3. **Transparency**
- Explain WHY bot made decision
- Show all factors considered
- Be honest about limitations

## 🚀 Next Steps

### Phase 5: Frontend Integration
- Integrate XAI ke React dashboard
- Add chat interface di UI
- Display explanations inline

### Phase 6: Advanced Features
- Voice interface
- Multi-language support
- Advanced NLP dengan transformers
- Personalized explanations

## ✅ Status

**XAI Module: COMPLETE ✅**

- ✅ Explanation Generator
- ✅ Trading Dictionary (50+ terms)
- ✅ Context Builder
- ✅ Chat Agent
- ✅ Interactive demo
- ✅ Build successful

---

**Your AI Trading Agent now speaks human language! 🤖💬**
