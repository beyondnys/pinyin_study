@echo off
REM 打包 pinyin-game-api 发布压缩包到 dist\年月日时分秒.zip
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

for /f "delims=" %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TIMESTAMP=%%T"

set "DIST_DIR=%~dp0dist"
set "STAGING=%DIST_DIR%\staging_%TIMESTAMP%"
set "ZIPFILE=%DIST_DIR%\%TIMESTAMP%.zip"

echo ========================================
echo   Pinyin Game API 发布包构建
echo ========================================
echo.

if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"
if exist "%STAGING%" rmdir /s /q "%STAGING%"
mkdir "%STAGING%"

echo [1/4] 复制 app ...
robocopy "%~dp0app" "%STAGING%\app" /E /XD __pycache__ .pytest_cache .mypy_cache .ruff_cache /XF *.pyc *.pyo /NFL /NDL /NJH /NJS /NC /NS /NP
if %ERRORLEVEL% GEQ 8 (
    echo [错误] 复制 app 失败，错误码: %ERRORLEVEL%
    exit /b 1
)

echo [2/4] 复制 scripts、requirements、.env.example ...
if exist "%~dp0scripts" (
    robocopy "%~dp0scripts" "%STAGING%\scripts" /E /XD __pycache__ /NFL /NDL /NJH /NJS /NC /NS /NP
)
if not exist "%~dp0requirements.txt" (
    echo [错误] 缺少 requirements.txt
    exit /b 1
)
copy /Y "%~dp0requirements.txt" "%STAGING%\" >nul
if exist "%~dp0.env.example" copy /Y "%~dp0.env.example" "%STAGING%\" >nul
if exist "%~dp0README.md" copy /Y "%~dp0README.md" "%STAGING%\" >nul

echo [3/4] 生成 ZIP: dist\%TIMESTAMP%.zip ...
if exist "%ZIPFILE%" del /f /q "%ZIPFILE%"

REM 注意：必须用 -Path 不能用 -LiteralPath，否则 *\ 不会展开，zip 不会生成
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop';" ^
  "$staging='%STAGING%';" ^
  "$zip='%ZIPFILE%';" ^
  "$items=Get-ChildItem -LiteralPath $staging;" ^
  "if ($items.Count -eq 0) { Write-Error 'staging 目录为空'; exit 1 };" ^
  "Compress-Archive -Path ($items | ForEach-Object { $_.FullName }) -DestinationPath $zip -CompressionLevel Optimal -Force;" ^
  "if (-not (Test-Path -LiteralPath $zip)) { Write-Error 'ZIP 未生成'; exit 1 };" ^
  "$len=(Get-Item -LiteralPath $zip).Length;" ^
  "Write-Host ('已生成 ZIP，大小 ' + [math]::Round($len/1KB, 1) + ' KB')"

if errorlevel 1 (
    echo [错误] 压缩失败，请检查 dist 目录权限或磁盘空间
    if exist "%STAGING%" rmdir /s /q "%STAGING%"
    exit /b 1
)

echo [4/4] 清理临时目录 ...
if exist "%STAGING%" rmdir /s /q "%STAGING%"

echo.
echo [完成] 发布包: %ZIPFILE%
echo        dist 目录下为 zip 压缩包，解压后部署（不是解压后的文件夹）
echo.
dir /b "%ZIPFILE%" 2>nul
echo.
echo 部署提示:
echo   1. 解压后复制 .env.example 为 .env 并填写生产配置
echo   2. python -m venv .venv ^&^& .venv\Scripts\activate
echo   3. pip install -r requirements.txt
echo   4. python -m app.scripts.init_admin
echo   5. uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
echo.
endlocal
exit /b 0
