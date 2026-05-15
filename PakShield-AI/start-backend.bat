@echo off
cd /d "%~dp0backend"
echo ========================================
echo   PakShield AI - Starting Backend
echo ========================================
echo.
echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed
    pause
    exit /b 1
)
echo.
echo [2/3] Initializing database and seeding...
python run.py
echo.
echo [3/3] Starting FastAPI server on http://localhost:8000
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
