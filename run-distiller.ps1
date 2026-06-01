$inboxPath = "01_INBOX"
$files = Get-ChildItem -Path $inboxPath -Filter "*.md"

if ($files.Count -eq 0) {
    Write-Host "✅ Inbox Zero! ไม่มีไฟล์ค้างใน 01_INBOX ครับ" -ForegroundColor Green
    exit
}

Write-Host "🚀 พบไฟล์รอการประมวลผลใน INBOX จำนวน $($files.Count) ไฟล์" -ForegroundColor Cyan

foreach ($file in $files) {
    Write-Host "`n----------------------------------------"
    Write-Host "📄 ไฟล์ปัจจุบัน: $($file.Name)" -ForegroundColor Yellow
    
    $filePath = "$inboxPath\$($file.Name)"
    $fileContent = Get-Content -Path $filePath -Raw
    
    # ตรวจสอบลิงก์ YouTube
    $ytRegex = '(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)'
    $isYouTube = $fileContent -match $ytRegex
    
    if ($isYouTube) {
        $ytUrl = $Matches[1]
        Write-Host "📺 ตรวจพบลิงก์ YouTube: $ytUrl" -ForegroundColor Magenta
    }
    
    Write-Host "1. สกัดลง 03_ZETTEL อย่างเดียว (เหมาะกับไอเดียสั้นๆ / Concept)"
    Write-Host "2. สรุปลง 02_SOURCE + สกัดลง 03_ZETTEL (เหมาะกับเนื้อหาที่ต้องการวิเคราะห์ลึกซึ้งและเก็บเป็นความรู้คงทน)"
    Write-Host "3. สรุปเก็บเฉพาะ 02_SOURCE อย่างเดียว (เหมาะสำหรับการอัปเดต / ไม่ต้องการสกัดแก่นไอเดียย่อย)"
    Write-Host "4. ข้ามไฟล์นี้ไปก่อน (Skip)"
    
    $choice = Read-Host "เลือกตัวเลือก (1/2/3/4)"
    
    if ($choice -eq '4') {
        Write-Host "ข้ามไฟล์ $($file.Name)" -ForegroundColor DarkGray
        continue
    }
    
    if ($choice -ne '1' -and $choice -ne '2' -and $choice -ne '3') {
        Write-Host "ตัวเลือกไม่ถูกต้อง ข้ามไฟล์นี้" -ForegroundColor Red
        continue
    }
    
    if ($isYouTube) {
        Write-Host "⏳ ขั้นตอนที่ 1: กำลังรัน Python ดึง Transcript/Subtitle..." -ForegroundColor Cyan
        
        $scriptPath = ".agents\YouTubeManager\get_youtube_transcript.py"
        $tempTranscriptPath = ".agents\YouTubeManager\temp_transcript.txt"
        
        # รัน Python script เพื่อดึง Subtitle
        python $scriptPath "$ytUrl"
        
        if (-not (Test-Path $tempTranscriptPath)) {
            Write-Host "❌ เกิดข้อผิดพลาดในการดึง Transcript กรุณาตรวจสอบคลิปหรือเปิด Subtitle ด้วยตัวเอง" -ForegroundColor Red
            continue
        }
        
        Write-Host "⏳ ขั้นตอนที่ 2: รัน YouTube Multi-Agent Pipeline (Orchestrator, Summarizer, Contrarian, Verifier)..." -ForegroundColor Cyan
        
        # ฐานคำสั่งสำหรับ YouTube Orchestrator
        $basePrompt = "ให้อ่านกฎและทักษะจากไฟล์ .agents/YouTubeManager/skill.md และ .agents/YouTubeManager/instruction.md ก่อน รวมถึงวิเคราะห์ตามหน้าลูกทีมย่อยจาก .agents/YouTubeManager/Summarizer.md, .agents/YouTubeManager/Contrarian.md และ .agents/YouTubeManager/Verifier.md จากนั้นอ่านบทถอดความจากวิดีโอ (Transcript) ในไฟล์ .agents/YouTubeManager/temp_transcript.txt อ้างอิงลิงก์ YouTube $ytUrl"
        
        if ($choice -eq '1') {
            $prompt = "$basePrompt ช่วยตกผลึกเนื้อหารอบด้านและบันทึกเฉพาะโน้ตแบบ Atomic Note (Zettel) 1 ไฟล์เซฟลงใน 03_ZETTEL และเมื่อเสร็จแล้วให้ลบไฟล์ต้นทาง $filePath ทิ้ง"
        }
        elseif ($choice -eq '2') {
            $prompt = "$basePrompt ช่วยวิเคราะห์อย่างละเอียดและประมวลผล: 1. สร้างสรุปภาพรวมความเห็นต่างและข้อเท็จจริง 1 ไฟล์เซฟลงใน 02_SOURCE และ 2. แตกเฉพาะประเด็นย่อยที่น่าสนใจเป็น Atomic Notes (Zettel) เซฟลงใน 03_ZETTEL และเมื่อเสร็จแล้วให้ลบไฟล์ต้นทาง $filePath ทิ้ง"
        }
        elseif ($choice -eq '3') {
            $prompt = "$basePrompt ช่วยประมวลผลสร้างเฉพาะโน้ตสรุปภาพรวมความเห็นต่างและข้อเท็จจริง 1 ไฟล์เซฟลงใน 02_SOURCE เท่านั้น (ไม่ต้องสร้างหรือแตกไฟล์ใน 03_ZETTEL) และเมื่อเสร็จแล้วให้ลบไฟล์ต้นทาง $filePath ทิ้ง"
        }
        
        # สั่งรัน AI Agent
        agy -p "$prompt"
        
        # ลบไฟล์ชั่วคราวทิ้งหลังเสร็จงาน
        if (Test-Path $tempTranscriptPath) {
            Remove-Item -Path $tempTranscriptPath -Force
        }
        
    } else {
        # ประมวลผลไฟล์ข้อความปกติโดยใช้ Distiller เดิม
        Write-Host "📄 ประมวลผลด้วย Distiller (ข้อความปกติ)..." -ForegroundColor Cyan
        $basePrompt = "ให้อ่านกฎและทักษะจากไฟล์ .agents/Distiller/skill.md และ .agents/Distiller/instruction.md ก่อน จากนั้น"
        
        if ($choice -eq '1') {
            $prompt = "$basePrompt ช่วยอ่านข้อมูลในไฟล์ $filePath แล้วสกัดเป็น Atomic Notes เซฟไว้ใน 03_ZETTEL และเมื่อเสร็จแล้วให้ลบไฟล์ต้นทางทิ้ง"
        }
        elseif ($choice -eq '2') {
            $prompt = "$basePrompt ช่วยอ่านข้อมูลในไฟล์ $filePath ทำ 2 อย่าง: 1. เขียนสรุปภาพรวมทั้งหมด 1 ไฟล์เซฟไว้ที่ 02_SOURCE และ 2. ดึงเฉพาะแก่นที่สำคัญแตกเป็น Atomic Notes เซฟไว้ที่ 03_ZETTEL และเมื่อเสร็จแล้วให้ลบไฟล์ต้นทางทิ้ง"
        }
        elseif ($choice -eq '3') {
            $prompt = "$basePrompt ช่วยอ่านข้อมูลในไฟล์ $filePath เพื่อเขียนสรุปภาพรวมทั้งหมด 1 ไฟล์เซฟไว้ที่ 02_SOURCE อย่างเดียวเท่านั้น (ไม่ต้องสร้างไฟล์ใน 03_ZETTEL) และเมื่อเสร็จแล้วให้ลบไฟล์ต้นทางทิ้ง"
        }
        
        # สั่งรัน AI Agent
        agy -p "$prompt"
    }
}

Write-Host "`n🎉 เคลียร์ INBOX เรียบร้อยแล้ว!" -ForegroundColor Green
