@echo off
REM ========================================
REM Auto-Update Setup - Windows
REM ========================================

echo.
echo ========================================
echo  Auto-Update Setup
echo ========================================
echo.

REM Get current directory
set REPO_PATH=%~dp0
set REPO_PATH=%REPO_PATH:~0,-1%

echo Repository: %REPO_PATH%
echo.

REM Create update script
echo Creating update script...

(
echo @echo off
echo cd /d "%REPO_PATH%"
echo.
echo REM Check for local changes
echo git status --porcelain ^| find /v "" ^>nul
echo if %%errorlevel%% equ 0 ^(
echo     echo [SKIP] Lokale Aenderungen gefunden, ueberspringe Update
echo     exit /b 0
echo ^)
echo.
echo REM Fetch and pull
echo git fetch origin ^>nul 2^>^&1
echo git pull origin main ^>nul 2^>^&1 ^|^| git pull origin master ^>nul 2^>^&1
echo.
echo if %%errorlevel%% equ 0 ^(
echo     echo [OK] Update erfolgreich: %%date%% %%time%%
echo ^) else ^(
echo     echo [ERROR] Update fehlgeschlagen: %%date%% %%time%%
echo ^)
) > "%REPO_PATH%\auto-update.bat"

echo [OK] Update script erstellt!
echo.

REM Create Task Scheduler task
echo ========================================
echo  Erstelle geplante Aufgabe...
echo ========================================
echo.

schtasks /create /tn "AgentBattleAutoUpdate" /tr "\"%REPO_PATH%\auto-update.bat\"" /sc minute /mo 10 /f

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  Auto-Update aktiviert!
    echo ========================================
    echo.
    echo Das Repository wird jetzt automatisch
    echo alle 10 Minuten aktualisiert!
    echo.
    echo Zum Deaktivieren:
    echo   schtasks /delete /tn "AgentBattleAutoUpdate" /f
    echo.
    echo Zum Testen:
    echo   auto-update.bat
    echo.
) else (
    echo.
    echo [ERROR] Konnte geplante Aufgabe nicht erstellen!
    echo.
    echo Bitte als Administrator ausfuehren!
    echo.
)

echo ========================================
pause
