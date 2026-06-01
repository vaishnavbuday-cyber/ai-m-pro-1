@echo off
echo ============================================================
echo   Traffic Accident Analysis System — Starting Flask Backend
echo ============================================================
echo.

:: Ensure Python is in the PATH (bypassing Windows Store stubs)
set PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%

cd /d "%~dp0full_web_app\backend"

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

:: Start the Flask server
echo Starting Flask server on http://localhost:5000 ...
python app.py
pause
