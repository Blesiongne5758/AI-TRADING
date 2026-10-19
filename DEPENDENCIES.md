# 📚 Penjelasan Dependencies

Panduan lengkap untuk memahami setiap dependency yang digunakan di AI Trading Agent.

---

## 🎯 Overview

AI Trading Agent menggunakan dependencies yang dipilih dengan hati-hati untuk:
- **Performance** - Cepat dan efisien
- **Reliability** - Stabil dan well-maintained
- **Simplicity** - Mudah dipahami pemula
- **Modularity** - Bisa diinstall/dihapus sesuai kebutuhan

---

## 📦 Phase 1 Dependencies (Wajib)

### 1. **ccxt==4.2.25** - Crypto Exchange Library

**Fungsi:** Koneksi ke Binance API dan exchange lainnya

**Mengapa digunakan:**
- Support 100+ exchanges
- Unified API untuk semua exchange
- Well-maintained dan active development
- Support WebSocket untuk real-time data

**Cara digunakan:**
```python
import ccxt.async_support as ccxt

exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
})

# Fetch OHLCV data
ohlcv = await exchange.fetch_ohlcv('BTC/USDT', '1h')
```

**Untuk pemula:**
- CCXT adalah "universal remote" untuk crypto exchanges
- Satu library untuk semua exchange (Binance, Coinbase, Kraken, dll)
- Handle semua kompleksitas API exchange

**Documentation:** https://docs.ccxt.com/

---

### 2. **websockets==12.0** - WebSocket Client

**Fungsi:** Koneksi real-time ke Binance WebSocket

**Mengapa digunakan:**
- Async/await support
- Lightweight dan fast
- Reliable untuk real-time data

**Cara digunakan:**
```python
import websockets

async with websockets.connect('wss://stream.binance.com:9443/ws') as ws:
    await ws.send('{"method": "SUBSCRIBE", "params": ["btcusdt@trade"]}')
    async for message in ws:
        print(message)
```

**Untuk pemula:**
- WebSocket = koneksi dua arah yang tetap terbuka
- Berbeda dengan HTTP yang request-response
- Cocok untuk data real-time seperti harga crypto

**Documentation:** https://websockets.readthedocs.io/

---

### 3. **aiohttp==3.9.1** - Async HTTP Client

**Fungsi:** HTTP requests secara async

**Mengapa digunakan:**
- Async/await support
- Bisa handle banyak request bersamaan
- Fast dan efficient

**Cara digunakan:**
```python
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get('https://api.binance.com/api/v3/ticker/price') as resp:
        data = await resp.json()
```

**Untuk pemula:**
- Async HTTP = tidak blocking saat menunggu response
- Bisa fetch banyak data sekaligus tanpa menunggu satu per satu
- Penting untuk performance

**Documentation:** https://docs.aiohttp.org/

---

### 4. **pandas==2.1.4** - Data Processing

**Fungsi:** Manipulasi dan analisis data

**Mengapa digunakan:**
- Standard untuk data science di Python
- Mudah digunakan untuk time series data
- Banyak fungsi built-in untuk analisis

**Cara digunakan:**
```python
import pandas as pd

# Create DataFrame dari OHLCV data
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Calculate moving average
df['ma_20'] = df['close'].rolling(window=20).mean()
```

**Untuk pemula:**
- Pandas = "Excel untuk Python"
- Mudah untuk manipulasi data
- Penting untuk analisis teknikal

**Documentation:** https://pandas.pydata.org/docs/

---

### 5. **numpy==1.26.2** - Numerical Computing

**Fungsi:** Komputasi numerik dan array operations

**Mengapa digunakan:**
- Fast untuk numerical operations
- Foundation untuk pandas dan library data science lainnya
- Efficient untuk large datasets

**Cara digunakan:**
```python
import numpy as np

# Calculate returns
prices = np.array([100, 102, 101, 105, 103])
returns = np.diff(prices) / prices[:-1]

# Calculate standard deviation
std = np.std(returns)
```

**Untuk pemula:**
- NumPy = foundation untuk data science di Python
- Lebih cepat dari Python lists untuk numerical operations
- Pandas built on top of NumPy

**Documentation:** https://numpy.org/doc/

---

### 6. **feedparser==6.0.11** - RSS Feed Parser

**Fungsi:** Parse RSS feeds dari news sources

**Mengapa digunakan:**
- Simple dan mudah digunakan
- Support banyak format RSS/Atom
- Reliable untuk news scraping

**Cara digunakan:**
```python
import feedparser

feed = feedparser.parse('https://cointelegraph.com/rss')

for entry in feed.entries:
    print(entry.title)
    print(entry.summary)
    print(entry.published)
```

**Untuk pemula:**
- RSS = format untuk distribute berita
- Feedparser = parser untuk RSS feeds
- Mudah untuk ambil berita dari website

**Documentation:** https://feedparser.readthedocs.io/

---

### 7. **aiosqlite==0.19.0** - Async SQLite

**Fungsi:** Async database operations untuk SQLite

**Mengapa digunakan:**
- Async/await support
- Lightweight (tidak perlu server database)
- Perfect untuk MVP dan development

**Cara digunakan:**
```python
import aiosqlite

async with aiosqlite.connect('database.db') as db:
    await db.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER, name TEXT)')
    await db.execute('INSERT INTO test VALUES (?, ?)', (1, 'test'))
    await db.commit()
```

**Untuk pemula:**
- SQLite = database file-based (tidak perlu server)
- Async = tidak blocking saat query database
- Perfect untuk development dan small-scale applications

**Documentation:** https://aiosqlite.omnilib.dev/

---

### 8. **sqlalchemy==2.0.25** - Database ORM

**Fungsi:** Object-Relational Mapping untuk database

**Mengapa digunakan:**
- Work dengan Python objects, bukan SQL queries
- Support async operations
- Migration dan schema management
- Well-documented dan widely used

**Cara digunakan:**
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine

# Define model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create engine
engine = create_async_engine('sqlite+aiosqlite:///database.db')

# Query
async with async_session() as session:
    result = await session.execute(select(User))
    users = result.scalars().all()
```

**Untuk pemula:**
- ORM = Object-Relational Mapping
- Work dengan Python objects, bukan SQL
- Lebih mudah dan safer daripada raw SQL
- Auto-handle data types dan relationships

**Documentation:** https://docs.sqlalchemy.org/

---

### 9. **python-dotenv==1.0.0** - Environment Variables

**Fungsi:** Load environment variables dari file .env

**Mengapa digunakan:**
- Secure untuk API keys dan secrets
- Mudah untuk switch between environments
- Standard practice untuk configuration

**Cara digunakan:**
```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get environment variable
api_key = os.getenv('BINANCE_API_KEY')
```

**Untuk pemula:**
- .env file = tempat simpan secrets (API keys, dll)
- Jangan commit .env ke Git!
- Mudah untuk switch antara development/production

**Documentation:** https://saurabh-kumar.com/python-dotenv/

---

### 10. **loguru==0.7.2** - Logging

**Fungsi:** Structured logging untuk debugging dan monitoring

**Mengapa digunakan:**
- Lebih mudah dari logging bawaan Python
- Beautiful output dengan colors
- File rotation dan retention
- Flexible formatting

**Cara digunakan:**
```python
from loguru import logger

# Add file handler
logger.add("file.log", rotation="10 MB")

# Log messages
logger.info("Application started")
logger.error("Something went wrong")
logger.debug("Debug information")
```

**Untuk pemula:**
- Logging = catatan untuk debugging
- Penting untuk tahu apa yang terjadi di aplikasi
- Loguru lebih mudah dari logging bawaan Python

**Documentation:** https://loguru.readthedocs.io/

---

### 11. **pydantic==2.5.3** - Data Validation

**Fungsi:** Data validation dan parsing

**Mengapa digunakan:**
- Type hints untuk validation
- Auto-convert data types
- Clear error messages
- Fast performance

**Cara digunakan:**
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# Validate data
user = User(id=1, name="John", email="john@example.com")
```

**Untuk pemula:**
- Pydantic = validation untuk data
- Pastikan data yang masuk sesuai format
- Auto-convert types (string ke int, dll)
- Clear error messages jika data invalid

**Documentation:** https://docs.pydantic.dev/

---

### 12. **pydantic-settings==2.1.0** - Settings Management

**Fungsi:** Configuration management dengan environment variables

**Mengapa digunakan:**
- Load config dari .env file
- Type hints untuk validation
- Default values
- Easy to use

**Cara digunakan:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BINANCE_API_KEY: str
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
print(settings.BINANCE_API_KEY)
```

**Untuk pemula:**
- Settings = konfigurasi aplikasi
- Load dari .env file atau environment variables
- Type hints untuk validation
- Default values untuk optional settings

**Documentation:** https://docs.pydantic.dev/latest/concepts/pydantic_settings/

---

## 🔮 Phase 2 Dependencies (Opsional)

### 1. **transformers==4.36.2** - Hugging Face Transformers

**Fungsi:** Load dan gunakan AI models (FinBERT untuk sentiment analysis)

**Mengapa digunakan:**
- State-of-the-art NLP models
- Easy to use pre-trained models
- Well-documented

**Size:** ~440MB (untuk FinBERT)

**Cara digunakan:**
```python
from transformers import pipeline

# Load FinBERT model
classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert")

# Analyze sentiment
result = classifier("Bitcoin price surges to new all-time high")
print(result)  # [{'label': 'positive', 'score': 0.95}]
```

**Untuk pemula:**
- Transformers = library untuk AI/NLP models
- FinBERT = model AI untuk financial text
- Analyze sentiment berita otomatis

**Documentation:** https://huggingface.co/docs/transformers

---

### 2. **torch==2.1.2** - PyTorch

**Fungsi:** Deep learning framework (dependency untuk transformers)

**Mengapa digunakan:**
- Required untuk transformers
- Industry standard untuk deep learning
- Well-maintained

**Size:** ~2GB

**Note:** Tidak digunakan langsung, hanya dependency untuk transformers

**Documentation:** https://pytorch.org/docs

---

## 📊 Dependency Size

### Phase 1 (Wajib)
```
Total: ~150MB
- ccxt: ~15MB
- pandas: ~40MB
- numpy: ~30MB
- sqlalchemy: ~20MB
- Lainnya: ~45MB
```

### Phase 2 (Opsional)
```
Total: ~2.5GB
- torch: ~2GB
- transformers: ~500MB
```

---

## 🎯 Rekomendasi Instalasi

### Untuk Development (Phase 1)
```bash
pip install -r requirements.txt
```

### Untuk Production (Phase 1 + Phase 2)
```bash
pip install -r requirements.txt
pip install transformers==4.36.2 torch==2.1.2
```

### Untuk Testing (Minimal)
```bash
pip install ccxt pandas numpy aiosqlite sqlalchemy loguru
```

---

## ✅ Checklist Pemahaman

Setelah membaca dokumen ini, Anda harus bisa menjawab:

- [ ] Apa fungsi ccxt?
- [ ] Mengapa menggunakan websockets?
- [ ] Apa perbedaan pandas dan numpy?
- [ ] Mengapa menggunakan SQLAlchemy?
- [ ] Apa fungsi .env file?
- [ ] Mengapa menggunakan loguru?
- [ ] Apa itu Pydantic?
- [ ] Kapan install transformers?

---

## 📚 Resources

### Official Documentation
- [CCXT](https://docs.ccxt.com/)
- [Pandas](https://pandas.pydata.org/docs/)
- [NumPy](https://numpy.org/doc/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Loguru](https://loguru.readthedocs.io/)

### Tutorials
- [Python Asyncio](https://realpython.com/async-io-python/)
- [Pandas Tutorial](https://pandas.pydata.org/docs/getting_started/tutorials.html)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)

---

**Happy Learning! 📚🚀**
