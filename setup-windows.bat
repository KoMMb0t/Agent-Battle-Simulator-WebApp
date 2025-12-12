@echo off
REM ========================================
REM Agent Battle Simulator - Windows Setup
REM ========================================

echo.
echo ========================================
echo  Agent Battle Simulator - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python ist nicht installiert!
    echo.
    echo Bitte Python 3.11 oder neuer installieren von:
    echo https://www.python.org/downloads/
    echo.
    echo WICHTIG: Bei Installation "Add Python to PATH" ankreuzen!
    pause
    exit /b 1
)

echo [OK] Python gefunden!
python --version
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git ist nicht installiert!
    echo.
    echo Bitte Git installieren von:
    echo https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git gefunden!
git --version
echo.

REM Install dependencies
echo ========================================
echo  Installiere Abhaengigkeiten...
echo ========================================
echo.

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation fehlgeschlagen!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installation erfolgreich!
echo ========================================
echo.
echo Das Spiel ist jetzt bereit!
echo.
echo Zum Starten:
echo   1. Doppelklick auf: start-game.bat
echo.
echo Zum Auto-Update aktivieren:
echo   1. Doppelklick auf: setup-auto-update-windows.bat
echo.
echo ========================================
pause
