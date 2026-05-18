# Package pinyin-game-api -> dist\yyyyMMddHHmmss.zip
$ErrorActionPreference = 'Stop'

$Root = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$timestamp = Get-Date -Format 'yyyyMMddHHmmss'
$distDir = Join-Path $Root 'dist'
$staging = Join-Path $distDir ('staging_' + $timestamp)
$zipFile = Join-Path $distDir ($timestamp + '.zip')

Write-Host '========================================'
Write-Host '  Pinyin Game API build'
Write-Host '========================================'
Write-Host ''

if (-not (Test-Path -LiteralPath $distDir)) {
    New-Item -ItemType Directory -Path $distDir | Out-Null
}
if (Test-Path -LiteralPath $staging) {
    Remove-Item -LiteralPath $staging -Recurse -Force
}
New-Item -ItemType Directory -Path $staging | Out-Null

function Invoke-RobocopySafe {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Dest
    )
    if (-not (Test-Path -LiteralPath $Source)) {
        return
    }
    $null = robocopy $Source $Dest /E /XD __pycache__ .pytest_cache .mypy_cache .ruff_cache /XF *.pyc *.pyo /NFL /NDL /NJH /NJS /NC /NS /NP
    if ($LASTEXITCODE -ge 8) {
        throw ('robocopy failed: ' + $Source + ' -> ' + $Dest + ' (exit ' + $LASTEXITCODE + ')')
    }
}

Write-Host '[1/4] copy app ...'
Invoke-RobocopySafe -Source (Join-Path $Root 'app') -Dest (Join-Path $staging 'app')

Write-Host '[2/4] copy scripts, requirements, .env.example ...'
Invoke-RobocopySafe -Source (Join-Path $Root 'scripts') -Dest (Join-Path $staging 'scripts')

$req = Join-Path $Root 'requirements.txt'
if (-not (Test-Path -LiteralPath $req)) {
    throw 'requirements.txt not found'
}
Copy-Item -LiteralPath $req -Destination $staging -Force

$envExample = Join-Path $Root '.env.example'
if (Test-Path -LiteralPath $envExample) {
    Copy-Item -LiteralPath $envExample -Destination $staging -Force
}

$readme = Join-Path $Root 'README.md'
if (Test-Path -LiteralPath $readme) {
    Copy-Item -LiteralPath $readme -Destination $staging -Force
}

Write-Host ('[3/4] create zip: dist\' + $timestamp + '.zip ...')
if (Test-Path -LiteralPath $zipFile) {
    Remove-Item -LiteralPath $zipFile -Force
}

$items = @(Get-ChildItem -LiteralPath $staging)
if ($items.Count -eq 0) {
    throw 'staging folder is empty'
}

$paths = @($items | ForEach-Object { $_.FullName })
Compress-Archive -Path $paths -DestinationPath $zipFile -CompressionLevel Optimal -Force

if (-not (Test-Path -LiteralPath $zipFile)) {
    throw 'zip file was not created'
}

$lenKB = [math]::Round((Get-Item -LiteralPath $zipFile).Length / 1KB, 1)
Write-Host ('zip size: ' + $lenKB + ' KB')

Write-Host '[4/4] remove staging ...'
Remove-Item -LiteralPath $staging -Recurse -Force

Write-Host ''
Write-Host ('done: ' + $zipFile)
Write-Host ''
Get-Item -LiteralPath $zipFile | Format-Table Name, Length, LastWriteTime -AutoSize

Write-Host 'deploy:'
Write-Host '  1. copy .env.example to .env'
Write-Host '  2. python -m venv .venv'
Write-Host '  3. .venv\Scripts\activate'
Write-Host '  4. pip install -r requirements.txt'
Write-Host '  5. python -m app.scripts.init_admin'
Write-Host '  6. uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2'
Write-Host ''
