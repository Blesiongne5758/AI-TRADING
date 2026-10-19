# 📦 Installation Guide - AI Trading Agent

Panduan lengkap instalasi AI Trading Agent dari awal sampai siap digunakan.

## 📋 Prerequisites

Sebelum instalasi, pastikan Anda memiliki:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** - Biasanya sudah termasuk dengan Python

### Cek Versi Python

```bash
python --version
# Output: Python 3.11.x atau lebih baru
```

Jika versi Python < 3.11, download dan install versi terbaru dari [python.org](https://www.python.org/downloads/).

---

## 🚀 Quick Start (5 Menit)

### 1. Clone atau Download Project

```bash
# Jika menggunakan git
git clone <repository-url>
cd ai-trading-agent

# Atau download ZIP dan extract
```

### 2. Buat Virtual Environment (Recommended)

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Anda akan melihat `(venv)` di awal command prompt.

### 3. Install Dependencies

**Opsi A: Menggunakan Script Otomatis (Recommended)**

**Linux/Mac:**
```bash
cd backend
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
cd backend
setup.bat
```

**Opsi B: Manual Installation**

```bash
cd backend

# Install semua dependencies
pip install -r requirements.txt

# Download TextBlob corpora
python -m textblob.download_corpora
```

### 4. Setup Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit file .env
nano .env  # Linux/Mac
notepad .env  # Windows
```

Isi dengan API keys Anda:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Dapatkan API keys dari:** https://testnet.binance.vision/

### 5. Jalankan Aplikasi

**Terminal 1 - Data Collector:**
```bash
cd backend
python -m data_collector.main_collector
```

**Terminal 2 - Analysis Engine:**
```bash
cd backend
python -m analysis.main_analysis
```

---

## 📦 Dependencies Detail

### Fase 1: Data Collection

| Package | Version | Size | Purpose |
|---------|---------|------|---------|
| ccxt | 4.2.25 | ~15MB | Binance API |
| websockets | 12.0 | ~2MB | WebSocket client |
| aiohttp | 3.9.1 | ~10MB | Async HTTP |
| pandas | 2.1.4 | ~40MB | Data processing |
| numpy | 1.26.2 | ~30MB | Numerical computing |
| feedparser | 6.0.11 | ~1MB | RSS parser |
| aiosqlite | 0.19.0 | ~1MB | Async SQLite |
| python-dotenv | 1.0.0 | ~0.5MB | Environment variables |
| loguru | 0.7.2 | ~2MB | Logging |

**Total Fase 1: ~100MB**

### Fase 2: Analysis Engine

| Package | Version | Size | Purpose |
|---------|---------|------|---------|
| pandas-ta | 0.3.14b | ~5MB | Technical analysis |
| textblob | 0.17.1 | ~1MB | Sentiment analysis |

**Total Fase 2: ~6MB**

### Optional: FinBERT (ML-based Sentiment)

| Package | Version | Size | Purpose |
|---------|---------|------|---------|
| transformers | 4.36.2 | ~100MB | Hugging Face models |
| torch | 2.1.2 | ~400MB | PyTorch |

**Total Optional: ~500MB**

**Grand Total: ~106MB (tanpa FinBERT) atau ~606MB (dengan FinBERT)**

---

## 🔧 Troubleshooting

### Error: "python: command not found"

**Solusi:**
- Install Python dari [python.org](https://www.python.org/downloads/)
- Atau gunakan `python3` instead of `python`
- Pastikan Python ada di PATH

**Windows:**
```bash
py --version  # Gunakan py launcher
```

### Error: "pip: command not found"

**Solusi:**
```bash
# Linux/Mac
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# Windows
py -m ensurepip --upgrade
py -m pip install --upgrade pip
```

### Error: "Permission denied" saat install

**Solusi:**
```bash
# Gunakan --user flag
pip install --user -r requirements.txt

# Atau gunakan virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Error: "ModuleNotFoundError: No module named 'pandas_ta'"

**Solusi:**
```bash
# Install pandas-ta
pip install pandas-ta==0.3.14b

# Verify installation
python -c "import pandas_ta; print(pandas_ta.version)"
```

### Error: "ModuleNotFoundError: No module named 'textblob'"

**Solusi:**
```bash
# Install textblob
pip install textblob==0.17.1

# Download corpora
python -m textblob.download_corpora

# Verify installation
python -c "from textblob import TextBlob; print('TextBlob OK')"
```

### Error: "TextBlob corpora not found"

**Solusi:**
```bash
# Download corpora manually
python -m textblob.download_corpora

# Jika masih error, download manual
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### Error: "Database locked"

**Solusi:**
```bash
# Hapus database lama
rm database/trading_data.db  # Linux/Mac
del database\trading_data.db  # Windows

# Jalankan ulang aplikasi
python -m data_collector.main_collector
```

### Error: "BINANCE_API_KEY required"

**Solusi:**
```bash
# Copy .env.example ke .env
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Edit .env dan isi API keys
nano .env  # atau text editor lainnya
```

### Error: "Connection refused" atau "Timeout"

**Solusi:**
- Cek koneksi internet
- Cek firewall/antivirus
- Coba gunakan VPN jika ada restriksi
- Verify API keys valid

### Error: "Rate limit exceeded"

**Solusi:**
- Tunggu beberapa menit
- Binance rate limit: 1200 requests/menit
- Aplikasi sudah handle rate limiting otomatis

---

## 🐧 Platform-Specific Instructions

### Linux (Ubuntu/Debian)

```bash
# Update system
sudo apt update
sudo apt upgrade

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Clone project
git clone <repository-url>
cd ai-trading-agent

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
./setup.sh
```

### macOS

```bash
# Install Homebrew (jika belum ada)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Clone project
git clone <repository-url>
cd ai-trading-agent

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
./setup.sh
```

### Windows

```bash
# Download Python 3.11 dari python.org
# Saat install, centang "Add Python to PATH"

# Clone atau download project
# Extract ke folder yang diinginkan

# Open Command Prompt atau PowerShell
cd ai-trading-agent

# Setup virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
cd backend
setup.bat
```

---

## 🧪 Verify Installation

### Test 1: Check Python Version
```bash
python --version
# Expected: Python 3.11.x
```

### Test 2: Check Dependencies
```bash
pip list | grep -E "pandas-ta|textblob"
# Expected:
# pandas-ta    0.3.14b
# textblob     0.17.1
```

### Test 3: Test Import
```bash
python -c "import pandas_ta; import textblob; print('✅ All imports OK')"
```

### Test 4: Test TextBlob
```bash
python -c "from textblob import TextBlob; blob = TextBlob('Hello world'); print(f'✅ TextBlob OK: {blob.sentiment}')"
```

### Test 5: Run Analysis
```bash
# Pastikan data collector sudah berjalan di terminal lain
python -m analysis.main_analysis
# Expected: Output dengan signals
```

---

## 🔄 Upgrade Dependencies

### Upgrade All Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Upgrade Specific Package
```bash
pip install --upgrade pandas-ta
pip install --upgrade textblob
```

### Upgrade to FinBERT (Optional)
```bash
pip install transformers==4.36.2 torch==2.1.2
```

---

## 🗑️ Uninstall

### Uninstall All Dependencies
```bash
pip freeze | xargs pip uninstall -y  # Linux/Mac
pip freeze | %{pip uninstall -y}     # Windows PowerShell
```

### Remove Virtual Environment
```bash
# Linux/Mac
deactivate
rm -rf venv

# Windows
deactivate
rmdir /s /q venv
```

### Remove Database
```bash
# Linux/Mac
rm -rf database/

# Windows
rmdir /s /q database
```

---

## 📚 Additional Resources

### Python
- [Python Documentation](https://docs.python.org/3/)
- [Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/)

### Libraries
- [pandas-ta Documentation](https://github.com/twopirllc/pandas-ta)
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [CCXT Documentation](https://docs.ccxt.com/)

### Troubleshooting
- [Stack Overflow](https://stackoverflow.com/)
- [GitHub Issues](https://github.com/<your-repo>/issues)

---

## ✅ Installation Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] TextBlob corpora downloaded (`python -m textblob.download_corpora`)
- [ ] `.env` file created and configured
- [ ] Binance API keys obtained
- [ ] Data collector running successfully
- [ ] Analysis engine running successfully
- [ ] All tests passed

---

## 🆘 Need Help?

Jika Anda mengalami masalah:

1. **Check logs** - Lihat file di `logs/` folder
2. **Check documentation** - Baca README.md dan analysis/README.md
3. **Search issues** - Cek GitHub issues
4. **Ask community** - Post di Stack Overflow atau forum terkait

---

**Happy Trading! 🚀📈**
