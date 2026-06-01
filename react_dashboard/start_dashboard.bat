@echo off
echo ==========================================
echo   Traffic Accident Analysis System
echo   React Dashboard - Local Server
echo ==========================================
echo.
echo Starting local server at http://localhost:8080
echo Press Ctrl+C to stop the server
echo.
start http://localhost:8080
C:\Users\Akash\anaconda3\python.exe -m http.server 8080
