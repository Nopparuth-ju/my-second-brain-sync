Write-Host "🔄 Word-to-Obsidian Sync System: โหมดอัปเดตเอกสารความรู้เรียนรู้" -ForegroundColor Cyan
Write-Host "-----------------------------------------------------------------------"

$inboxPath = "01_INBOX\WORK_KNOWLEDGE"
$targetPath = "02_SOURCE\WORK_KNOWLEDGE"

if (-not (Test-Path $inboxPath)) {
    Write-Host "❌ ไม่พบโฟลเดอร์ $inboxPath ใน Inbox คาดว่าประมวลผลไปหมดแล้ว" -ForegroundColor Red
    Write-Host "💡 วิธีใช้งาน: ก๊อปปี้โฟลเดอร์ WORK_KNOWLEDGE มาวางใน 01_INBOX แล้วกดรันใหม่อีกครั้งครับ" -ForegroundColor Yellow
    exit
}

Write-Host "⏳ ขั้นตอนที่ 1: ตรวจจับและกวาดซิงก์ประมวลผลไฟล์ Word (.docx) ทั้งหมด..." -ForegroundColor Cyan

# รัน Python script เพื่อกวาดซิงก์
python .agents\WordSync\sync_word_notes.py

Write-Host "`n🎉 จัดการแปลงและซิงก์เอกสารความรู้ลงโฟลเดอร์ $targetPath เรียบร้อยแล้ว!" -ForegroundColor Green
