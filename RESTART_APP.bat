@echo off
cls
echo ========================================
echo   RESTARTING MEDICAL SYSTEM
echo ========================================
echo.
echo Stopping any running Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul
echo.
echo Starting Fresh Flask Application...
echo.
echo Application will be available at:
echo http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
