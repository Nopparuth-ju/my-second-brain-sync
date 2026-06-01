# ANTIGRAVITY

นี่คือไฟล์ระบบที่บันทึกความเข้าใจของ **Antigravity (AI Coding Assistant)** เกี่ยวกับโครงสร้างและกลไกทั้งหมดของระบบ Second Brain (Zettelkasten) ใน Obsidian Vault นี้ เพื่อใช้เป็นหน่วยความจำถาวรสำหรับการประสานงานและจัดระบบร่วมกับคุณ

---

## 1. ปรัชญาและกฎหลักของระบบ (Core Philosophy & Rules)

### ก. Combinatorial Creativity (การคิดเชื่อมโยง)
- เน้นสร้างเครือข่ายความรู้ผ่านลิงก์ของ Obsidian เพื่อเชื่อมโยงข้ามศาสตร์ มากกว่าการจัดเก็บบรรณารักษ์แบบแยกห้องสมุดทั่วไป

### ข. High-Value Information (กฎ 1 ปี)
- เลือกกรองเฉพาะข้อมูลที่เป็น "แก่น" (Principles / Insights / Frameworks) ที่มีมูลค่าใช้ซ้ำได้ยาวนานอย่างน้อย 1 ปีขึ้นไป หลีกเลี่ยงข่าวรายวันหรือข้อมูลฉาบฉวย

### ค. การจำแนกประเภทข้อมูล: Domain vs. Concept
* **Domain (อยู่ที่ไหน?):** หมวดวิชาหลัก เช่น `#domain/tech`, `#domain/business`, `#domain/productivity`, `#domain/health`
* **Concept (ทำงานยังไง?):** แก่นกลไกการทำงาน (Mental Model) ที่ประยุกต์ข้าม Domain ได้ เช่น `#concept/leverage` (คานงัด), `#concept/bottleneck` (คอขวด), `#concept/compounding` (ดอกเบี้ยทบต้น), `#concept/trade-off` (การได้อย่างเสียอย่าง)

---

## 2. โครงสร้างการไหลของข้อมูล (The Idea Pipeline)

| โฟลเดอร์ | หน้าที่ | สถานะปัจจุบัน / รายชื่อไฟล์ |
| :--- | :--- | :--- |
| **`01_INBOX`** | จุดพักข้อมูลดิบชั่วคราว ต้องเคลียร์เป็นศูนย์เสมอ | - `inbox_feyman.md` (Raw)<br>- `วิธีสรุปหนังสือ.md` (Raw) |
| **`02_SOURCE`** | สรุปภาพรวมและแก่นความคิดจากแหล่งข้อมูลภายนอก | - `สรุป The Almanack of Naval Ravikant.md` |
| **`03_ZETTEL`** | คลังเก็บ "Atomic Notes" (1 ไอเดียต่อ 1 โน้ต) | - `Permissionless Leverage.md`<br>- `Rapid Skill Acquisition.md`<br>- `Specific Knowledge.md`<br>- `Wealth is Assets Not Money.md` |
| **`04_MOC`** | สารบัญเชื่อมโยงแนวคิดข้ามสายตาม Theme หลัก (Map of Content) | *ว่าง (รอเริ่มสร้าง)* |
| **`05_OUTPUT`** | ผลงานฉบับร่างที่สมบูรณ์พร้อมใช้จริง | - `Writing` (โฟลเดอร์ย่อย) |
| **`SECOND_BRAIN_PRINCIPLE`** | คลังคู่มือหลักการจัดหมวดหมู่และกลไกความรู้ | - `Domain & Concept obsidian.md`<br>- `My Idea.md`<br>- `Overview Domain Knowledge.md`<br>- `The Optimal Problem-Solving Framework.md` |

---

## 3. กฎเกณฑ์การตั้ง Tag (Strict Tagging System)
- **ห้ามใช้ YAML Frontmatter:** ห้ามเขียน `---` เปิดปิดส่วนหัว ให้ใช้สัญลักษณ์ `#` พิมพ์ลงในบรรทัดเนื้อหาโดยตรง
- **แท็กผู้สร้าง (บังคับระบุ):**
  - `#creator/ai` = เนื้อหาจัดทำ/สรุปโดย AI
  - `#creator/me` = เนื้อหาเรียบเรียง/เขียนขึ้นโดยคุณเอง
- **แท็กประเภทโน้ต:** `#type/source`, `#type/zettel`, `#type/moc`, `#type/output`
- **การพิมพ์แท็ก:** ใช้ตัวพิมพ์เล็กทั้งหมด คำประสมเชื่อมด้วยขีดกลาง (เช่น `#concept/feedback-loop`)

---

## 4. แผนงานการสั่งการของผู้ช่วย AI (Agent Commands & CLI Integration)
ระบบนี้ทำงานร่วมกับบทบาทเฉพาะทางของ AI ในโฟลเดอร์ `.agents/` ผ่านการเรียกใช้ `agy` CLI ในสคริปต์ PowerShell:

* **The Distiller ([instruction](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/.agents/Distiller/instruction.md)):** สกัดไฟล์ข้อความปกติใน `01_INBOX` ลงมาสู่ `02_SOURCE` หรือ `03_ZETTEL` (สามารถเลือกเขียนเฉพาะไฟล์สรุปภาพรวมใน `02_SOURCE` อย่างเดียวได้)
* **The YouTube Orchestrator Manager ([instruction](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/.agents/YouTubeManager/instruction.md)):** 
  * ระบบจำลอง Multi-Agent Consensus ย่อยในการถอดความและวิเคราะห์คลิปวิดีโอจาก YouTube อัตโนมัติ (ถอด Transcript ผ่านสคริปต์ Python)
  * ประสานงานระหว่าง **Summarizer (สรุปแก่น)**, **Contrarian (คิดค้าน/หา Bias/Trade-off)** และ **Verifier (สแกน Fact vs Noise)**
  * รวมผลลัพธ์รอบด้านเข้าสู่ `02_SOURCE` (สรุปรวม) และ `03_ZETTEL` (ย่อยรายประเด็น) โดยสามารถเลือกสรุปลง `02_SOURCE` เฉพาะอย่างเดียวเพื่อติดตามข่าวสารโดยไม่แตก Zettel ได้
* **The Architect ([instruction](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/.agents/Architect/instruction.md)):** คลัสเตอร์โน้ตใน Zettel เพื่อจัดกลุ่มเชื่อมโยงออกมาเป็นแผนผังความคิดใน MOC
* **The Builder ([instruction](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/.agents/Builder/instruction.md)):** สังเคราะห์วัตถุดิบและเขียนร่างชิ้นงานฉบับสมบูรณ์ใน `05_OUTPUT`

---

## 5. บันทึกประวัติการปรับปรุงระบบ (System Changelog)
- **2026-06-01 (อัปเดตระบบ YouTube Multi-Agent Pipeline & ออปชั่นสรุปเฉพาะ SOURCE):**
  - อัปเกรดสคริปต์ `run-distiller.ps1` ให้ทำหน้าที่เป็น Entry Router ตรวจจับ YouTube Link ด้วย Regex และเปลี่ยนปลายทางกระบวนการอัตโนมัติ
  - สร้างสคริปต์ถอดคำบรรยายด่วน `get_youtube_transcript.py` รองรับ API เวอร์ชันล่าสุดของ `youtube-transcript-api` (v1.2.4)
  - พัฒนากลไกการวิเคราะห์แบบทีมขัดแย้งเชิงวิพากษ์ (Summarizer + Contrarian + Verifier) ภายใต้ `YouTubeManager`
  - ทำการทดสอบสมบูรณ์แบบด้วยวิดีโอ *"The first 20 hours"* ของ Josh Kaufman ได้รับไฟล์ Zettel ชื่อ `Rapid Skill Acquisition.md` ในคุณภาพดีเยี่ยม ปราศจากอคติ
  - **[ฟีเจอร์ใหม่]** เพิ่มตัวเลือกที่ 3: **"สรุปลง 02_SOURCE อย่างเดียว"** สำหรับโน้ตปกติและลิงก์ YouTube เพื่อความรวดเร็วในการติดตามเนื้อหาโดยไม่มีการแตก Zettel บวมลงคลัง
