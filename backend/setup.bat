@echo off
REM Setup script untuk AI Trading Agent - Fase 2 (Windows)
REM Analysis Engine dependencies installation

echo ======================================================================
echo 🚀 AI Trading Agent - Fase 2 Setup
echo ======================================================================
echo.

REM Check if virtual environment is active
if "%VIRTUAL_ENV%"=="" (
    echo ⚠️  Warning: Virtual environment not detected!
    echo    Recommended: Create and activate virtual environment first
    echo    python -m venv venv
    echo    venv\Scripts\activate
    echo.
    set /p CONTINUE="Continue anyway? (y/n) "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

echo 📦 Installing dependencies...
echo.

REM Install main dependencies
pip install pandas-ta==0.3.14b textblob==0.17.1

if %errorlevel% neq 0 (
    echo ❌ Error installing dependencies
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.
echo 📥 Downloading TextBlob corpora...
echo.

REM Download TextBlob corpora
python -m textblob.download_corpora

if %errorlevel% neq 0 (
    echo ❌ Error downloading TextBlob corpora
    exit /b 1
)

echo ✅ TextBlob corpora downloaded successfully
echo.
echo ======================================================================
echo ✅ Setup completed successfully!
echo ======================================================================
echo.
echo 🎯 Next steps:
echo    1. Start data collector: python -m data_collector.main_collector
echo    2. Start analysis engine: python -m analysis.main_analysis
echo.
echo 📚 Documentation:
echo    - Main README: ..\README.md
echo    - Analysis README: analysis\README.md
echo.
echo 🚀 Ready to analyze!
echo.
pause
