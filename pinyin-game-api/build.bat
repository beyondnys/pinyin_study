@echo off
REM Package pinyin-game-api -> dist\yyyyMMddHHmmss.zip (logic in build.ps1)
chcp 65001 >nul
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"
set "EXITCODE=%ERRORLEVEL%"

if not "%EXITCODE%"=="0" (
    echo.
    echo [ERROR] Build failed, exit code: %EXITCODE%
    exit /b %EXITCODE%
)

exit /b 0
