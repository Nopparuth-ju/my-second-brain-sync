# Personal AI Intelligence Curator Runner
# Root of Project: run-intelligence.ps1

$curatorScript = ".agents\IntelligenceCurator\harvest.py"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "🛰️  Personal AI Intelligence Curator Engine Starting..." -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Cyan

if (-not (Test-Path $curatorScript)) {
    Write-Host "❌ Error: Cannot find harvest.py at $curatorScript" -ForegroundColor Red
    exit 1
}

# Ensure Python is installed
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCheck -eq $null) {
    Write-Host "❌ Error: Python is not installed or not in system PATH." -ForegroundColor Red
    exit 1
}

Write-Host "⏳ Fetching new updates from subscribed sources & running AI distillers..." -ForegroundColor Yellow
Write-Host "This might take a couple of minutes depending on the new content found.`n" -ForegroundColor DarkGray

# Execute the python script
python $curatorScript

Write-Host "`n=========================================================" -ForegroundColor Cyan
Write-Host "🎉 Personal AI Intelligence Update Complete!" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Cyan
