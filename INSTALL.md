# 📦 Panduan Instalasi Dependencies

Panduan lengkap untuk menginstall semua dependencies AI Trading Agent.

---

## 🎯 Overview

### Phase 1 Dependencies (Wajib)
```
ccxt==4.2.25          # Binance API
websockets==12.0      # WebSocket client
aiohttp==3.9.1        # Async HTTP
pandas==2.1.4         # Data processing
numpy==1.26.2         # Numerical computing
feedparser==6.0.11    # RSS parser
aiosqlite==0.19.0     # Async SQLite
sqlalchemy==2.0.25    # Database ORM
python-dotenv==1.0.0  # Environment variables
loguru==0.7.2         # Logging
pydantic==2.5.3       # Data validation
pydantic-settings==2.1.0  # Settings management
```

### Phase 2 Dependencies (Opsional - Install Nanti)
```
transformers==4.36.2  # FinBERT model
torch==2.1.2          # PyTorch
```

---

## 🚀 Instalasi Cepat

### 1. Buat Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Verifikasi Instalasi

```bash
python -c "import ccxt; import pandas; import sqlalchemy; print('✅ All dependencies installed!')"
```

---

## 🔧 Troubleshooting Instalasi

### Error: "Could not find a version that satisfies the requirement"

**Solusi:**
```bash
# Update pip
python -m pip install --upgrade pip

# Retry install
pip install -r requirements.txt
```

### Error: "Microsoft Visual C++ 14.0 is required" (Windows)

**Solusi:**
1. Download Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Restart terminal dan retry install

### Error: "Failed building wheel for aiohttp"

**Solusi:**
```bash
# Install pre-compiled wheels
pip install --only-binary :all: -r requirements.txt
```

### Error: "No module named 'setuptools'"

**Solusi:**
```bash
pip install setuptools wheel
pip install -r requirements.txt
```

### Error: "Permission denied"

**Solusi:**
```bash
# Gunakan --user flag
pip install --user -r requirements.txt

# Atau gunakan virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Error: "Could not find a version that satisfies the requirement ccxt"

**Solusi:**
```bash
# Check Python version (harus 3.11+)
python --version

# Jika versi lama, download Python 3.11+ dari:
# https://www.python.org/downloads/
```

---

## 📊 Verifikasi Dependencies

### Check Semua Dependencies

```bash
pip list
```

### Check Versi Spesifik

```bash
python -c "import ccxt; print(f'ccxt: {ccxt.__version__}')"
python -c "import pandas; print(f'pandas: {pandas.__version__}')"
python -c "import sqlalchemy; print(f'sqlalchemy: {sqlalchemy.__version__}')"
```

### Test Import

```bash
python -c "
import ccxt
import websockets
import aiohttp
import pandas
import numpy
import feedparser
import aiosqlite
import sqlalchemy
import dotenv
from loguru import logger
from pydantic import BaseModel
from pydantic_settings import BaseSettings
print('✅ All imports successful!')
"
```

---

## 🔄 Update Dependencies

### Update Semua Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Update Spesifik Package

```bash
pip install --upgrade ccxt
pip install --upgrade pandas
```

---

## 🗑️ Uninstall Dependencies

### Uninstall Semua

```bash
pip freeze | xargs pip uninstall -y
```

### Uninstall Spesifik Package

```bash
pip uninstall ccxt
pip uninstall pandas
```

---

## 📝 Catatan Penting

### Python Version
- **Minimum:** Python 3.11
- **Recommended:** Python 3.11+
- Check versi: `python --version`

### Virtual Environment
- **WAJIB** menggunakan virtual environment
- Mencegah konflik dependencies
- Memudahkan management

### Internet Connection
- Beberapa packages perlu download dari internet
- Pastikan koneksi stabil saat install
- Jika gagal, retry dengan `--timeout 100`

### Disk Space
- Total size: ~500MB
- Pastikan ada cukup disk space
- Check dengan: `df -h` (Linux/macOS) atau `dir` (Windows)

---

## 🆘 Bantuan Lebih Lanjut

### Jika Masih Error

1. **Check Python version**
   ```bash
   python --version
   ```

2. **Check pip version**
   ```bash
   pip --version
   ```

3. **Clear pip cache**
   ```bash
   pip cache purge
   ```

4. **Reinstall dari scratch**
   ```bash
   # Hapus virtual environment lama
   rm -rf venv  # Linux/macOS
   rmdir /s /q venv  # Windows
   
   # Buat baru
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   
   # Reinstall
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Resources

- [Python Downloads](https://www.python.org/downloads/)
- [pip Documentation](https://pip.pypa.io/)
- [Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## ✅ Checklist Instalasi

- [ ] Python 3.11+ terinstall
- [ ] Virtual environment dibuat
- [ ] Virtual environment activated
- [ ] pip diupgrade
- [ ] Dependencies terinstall
- [ ] Verifikasi import berhasil
- [ ] Test run aplikasi

---

**Happy Coding! 🚀**
