Write-Host "📚 The Librarian: ผู้ช่วยจัดระเบียบ Tag (รองรับ 02_SOURCE และ 03_ZETTEL)" -ForegroundColor Cyan
Write-Host "-----------------------------------------------------------------------"

# 1. รับชื่อไฟล์
$targetFile = Read-Host "ใส่ชื่อไฟล์ที่ต้องการแก้ Tag (เช่น my_note.md หรือใส่แค่ my_note ก็ได้)"

# เติม .md ให้ถ้าผู้ใช้ลืมพิมพ์
if (-not $targetFile.EndsWith(".md")) {
    $targetFile += ".md"
}

# 2. ค้นหาไฟล์ในทั้ง 2 โฟลเดอร์
Write-Host "กำลังค้นหาไฟล์..." -ForegroundColor Yellow
$foundFiles = @(Get-ChildItem -Path "02_SOURCE", "03_ZETTEL" -Filter $targetFile -Recurse -ErrorAction SilentlyContinue)

if ($foundFiles.Count -eq 0) {
    Write-Host "❌ หาไฟล์ไม่เจอใน 02_SOURCE และ 03_ZETTEL กรุณาตรวจสอบชื่อไฟล์อีกครั้ง" -ForegroundColor Red
    exit
}

Write-Host "✅ พบไฟล์จำนวน $($foundFiles.Count) ไฟล์" -ForegroundColor Green

# 3. วนลูปแก้ไขทีละไฟล์ (เผื่อมีไฟล์ชื่อซ้ำกันใน 2 โฟลเดอร์)
foreach ($file in $foundFiles) {
    $filePath = $file.FullName
    Write-Host "`nกำลังจัดระเบียบไฟล์: $($file.Name) (ที่อยู่: $($file.Directory.Name))..." -ForegroundColor Cyan

    # 4. สร้าง Prompt เฉพาะกิจ (บังคับห้ามแก้เนื้อหา + ให้ฉลาดเรื่องการแยกโฟลเดอร์)
    $prompt = "หน้าที่ของคุณคือจัดระเบียบ Tag ให้ไฟล์นี้: $filePath `n"
    $prompt += "กฎเหล็กที่ต้องทำตามอย่างเคร่งครัด: `n"
    $prompt += "1. **ห้ามแก้ไข ตัดทอน เพิ่มเติม หรือสรุปเนื้อหาหลัก (Body) ของโน้ตเด็ดขาด** ให้คงเนื้อหาต้นฉบับไว้ 100% `n"
    $prompt += "2. ให้อ่าน Tag เดิมที่มีอยู่ แล้วปรับ Format ใหม่ให้เป็นมาตรฐาน (ตัวพิมพ์เล็กทั้งหมด, คำประสมใช้ขีดกลางคั่น เช่น #concept/combinatorial-creativity) `n"
    $prompt += "3. ต้องคงแท็กผู้สร้างเดิมไว้ (เช่น หากมีข้อความว่าผู้ใช้ทำเอง ให้ใส่ #creator/me ห้ามเปลี่ยนเป็น AI) `n"
    $prompt += "4. **พิจารณาจาก Path ของไฟล์:** หากไฟล์นี้อยู่ในโฟลเดอร์ '02_SOURCE' ให้บังคับใช้แท็ก #type/source และหากอยู่ใน '03_ZETTEL' ให้บังคับใช้แท็ก #type/zettel `n"
    $prompt += "5. ทำการเซฟเนื้อหาเดิมพร้อม Tag ที่จัด Format แล้ว ทับลงไปในไฟล์เดิมได้เลย"

    # สั่งรันแบบ One-Shot
    agy -p "$prompt"
}

Write-Host "`n🎉 จัด Format Tag เรียบร้อยแล้ว!" -ForegroundColor Green
