@echo off
REM Andhra Pradesh Electricity Demand - Streamlit Dashboard
REM Run this file to start the dashboard

echo ================================
echo Streamlit Dashboard Launcher
echo ================================
echo.
echo Starting Streamlit app...
echo.

cd /d "%~dp0"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run Streamlit
streamlit run app.py

pause
