@echo off
setlocal enabledelayedexpansion

:: ============================================
:: AI Trading Agent - Start Website Script
:: ============================================
:: Script ini akan menjalankan:
:: 1. Backend API (FastAPI) di port 8000
:: 2. Frontend (Vite) di port 5173
:: 3. Auto-open browser
:: ============================================

:: Warna untuk output
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "RESET=[0m"

echo.
echo %CYAN%========================================%RESET%
echo %CYAN%  AI Trading Agent - Starting Servers   %RESET%
echo %CYAN%========================================%RESET%
echo.

:: Check Python
echo %BLUE%[1/5] Checking Python installation...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR] Python not found! Please install Python 3.11+%RESET%
    echo %YELLOW%Download from: https://www.python.org/downloads/%RESET%
    pause
    exit /b 1
)
echo %GREEN%[OK] Python found%RESET%

:: Check Node.js
echo %BLUE%[2/5] Checking Node.js installation...%RESET%
node --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR] Node.js not found! Please install Node.js 18+%RESET%
    echo %YELLOW%Download from: https://nodejs.org/%RESET%
    pause
    exit /b 1
)
echo %GREEN%[OK] Node.js found%RESET%

:: Check backend dependencies
echo %BLUE%[3/5] Checking backend dependencies...%RESET%
cd backend
if not exist "venv" (
    echo %YELLOW%[INFO] Creating virtual environment...%RESET%
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install backend dependencies
echo %YELLOW%[INFO] Installing backend dependencies...%RESET%
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR] Failed to install backend dependencies%RESET%
    pause
    exit /b 1
)
echo %GREEN%[OK] Backend dependencies installed%RESET%

:: Check frontend dependencies
echo %BLUE%[4/5] Checking frontend dependencies...%RESET%
cd ..\frontend
if not exist "node_modules" (
    echo %YELLOW%[INFO] Installing frontend dependencies...%RESET%
    call npm install
    if errorlevel 1 (
        echo %RED%[ERROR] Failed to install frontend dependencies%RESET%
        pause
        exit /b 1
    )
)
echo %GREEN%[OK] Frontend dependencies ready%RESET%

:: Start servers
echo %BLUE%[5/5] Starting servers...%RESET%
echo.
echo %CYAN%========================================%RESET%
echo %CYAN%  Starting Backend API (port 8000)      %RESET%
echo %CYAN%  Starting Frontend (port 5173)         %RESET%
echo %CYAN%========================================%RESET%
echo.

:: Start backend in background
cd ..\backend
start "AI Trading Agent - Backend" cmd /k "call venv\Scripts\activate.bat && python -m api.main"

:: Wait for backend to start
echo %YELLOW%[INFO] Waiting for backend to start...%RESET%
timeout /t 3 /nobreak >nul

:: Start frontend in background
cd ..\frontend
start "AI Trading Agent - Frontend" cmd /k "npm run dev"

:: Wait for frontend to start
echo %YELLOW%[INFO] Waiting for frontend to start...%RESET%
timeout /t 3 /nobreak >nul

:: Open browser
echo %GREEN%[OK] Opening browser...%RESET%
start http://localhost:5173

echo.
echo %CYAN%========================================%RESET%
echo %GREEN%  Servers are running!                %RESET%
echo %CYAN%========================================%RESET%
echo.
echo %BLUE%Backend API:%RESET%  http://localhost:8000
echo %BLUE%API Docs:%RESET%     http://localhost:8000/docs
echo %BLUE%Frontend:%RESET%     http://localhost:5173
echo.
echo %YELLOW%Press any key to stop all servers...%RESET%
pause >nul

:: Stop servers
echo.
echo %YELLOW%[INFO] Stopping servers...%RESET%
taskkill /FI "WINDOWTITLE eq AI Trading Agent - Backend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq AI Trading Agent - Frontend*" /T /F >nul 2>&1
echo %GREEN%[OK] Servers stopped%RESET%
echo.
echo %CYAN%========================================%RESET%
echo %GREEN%  Thank you for using AI Trading Agent%RESET%
echo %CYAN%========================================%RESET%
echo.

pause
