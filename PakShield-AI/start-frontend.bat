@echo off
cd /d "%~dp0frontend"
echo ========================================
echo   PakShield AI - Starting Frontend
echo ========================================
echo.
echo [1/2] Installing npm dependencies...
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] npm install failed
    pause
    exit /b 1
)
echo.
echo [2/2] Starting Next.js on http://localhost:3000
echo.
npm run dev
pause
