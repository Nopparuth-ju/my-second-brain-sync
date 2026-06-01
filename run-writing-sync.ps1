Write-Host "🔄 Writing Sync System: Starting Import & Organization Process..." -ForegroundColor Cyan
Write-Host "-----------------------------------------------------------------------"

# Run Python script to sync Excel writing list
python .agents\WordSync\sync_excel_writings.py

Write-Host "🎉 Sync process completed!" -ForegroundColor Green
