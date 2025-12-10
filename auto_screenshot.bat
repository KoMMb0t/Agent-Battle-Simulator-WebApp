@echo off
REM Automatic Screenshot Generator for Windows
REM Agent Battle Simulator - Hackathon Submission

echo ============================================================
echo Agent Battle Simulator - Auto Screenshot Generator
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo [1/4] Installing Selenium...
pip install selenium >nul 2>&1
if errorlevel 1 (
    echo WARNING: Could not install Selenium
    echo Trying to continue anyway...
)

echo [2/4] Checking ChromeDriver...
echo.
echo NOTE: You need ChromeDriver installed!
echo Download from: https://chromedriver.chromium.org/
echo Or install via: pip install webdriver-manager
echo.

echo [3/4] Starting screenshot automation...
python auto_screenshot.py

echo.
echo [4/4] Done!
echo.
echo Screenshots saved in: screenshots\
echo.
pause
