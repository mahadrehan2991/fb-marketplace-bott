@echo off
echo ========================================================
echo   Facebook Marketplace Auto-Poster Bot Setup & Run
echo ========================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to your PATH!
    echo Please install Python 3.8+ and check "Add Python to PATH" during installation.
    echo Exiting...
    pause
    exit /b
)

:: Install dependencies
echo [1/3] Installing/Updating required Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install requirements! Make sure internet connection is active.
    pause
    exit /b
)

:: Install Playwright Chromium browser
echo.
echo [2/3] Installing Playwright Chromium browser...
playwright install chromium
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install Playwright browser!
    pause
    exit /b
)

:: Start the bot GUI
echo.
echo [3/3] Starting the Facebook Marketplace Bot GUI...
python bot.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Bot exited with an error code.
    pause
)
