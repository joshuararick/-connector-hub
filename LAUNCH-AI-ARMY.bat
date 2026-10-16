@echo off
title Josh's AI Army Command Center
echo.
echo  ================================
echo   Josh's AI Army Command Center
echo  ================================
echo.
cd /d "%USERPROFILE%\OneDrive\Documents\Ai Army\agent-maker-starter"
if errorlevel 1 (
    echo ERROR: Could not find Ai Army folder
    pause
    exit /b 1
)
if not exist .venv (
    echo Creating Python environment...
    python -m venv .venv
)
call .venv\Scripts\activate
echo Installing dependencies...
pip install -e . -q
echo.
echo  Starting AI Army at http://localhost:7777
timeout /t 2 /nobreak >nul
start "" "http://localhost:7777"
python -m agent_maker.web.app
pause
