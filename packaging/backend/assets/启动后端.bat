@echo off
cd /d "%~dp0"
title PersonaWeaver Backend
echo ============================================================
echo   PersonaWeaver Backend Service
echo ============================================================
if not exist ".env" goto noenv
echo Health check: http://127.0.0.1:8000/health
echo Press Ctrl+C or close window to stop.
echo.
personaweaver-backend.exe --port 8000
pause
exit /b 0
:noenv
echo [WARNING] .env not found!
echo Please copy .env.example to .env and fill in your API keys.
echo (See the Chinese guide: shiyongshuoming.txt)
echo.
pause
exit /b 1