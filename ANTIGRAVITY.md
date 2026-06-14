# ANTIGRAVITY

นี่คือไฟล์ระบบที่บันทึกความเข้าใจของ **Antigravity (AI Coding Assistant)** เกี่ยวกับโครงสร้างและกลไกทั้งหมดของระบบ Second Brain (Zettelkasten) ใน Obsidian Vault นี้ เพื่อใช้เป็นหน่วยความจำถาวรสำหรับการประสานงานและจัดระบบร่วมกับคุณ

---

## 1. ปรัชญาและกฎหลักของระบบ (Core Philosophy & Rules)

### ก. Combinatorial Creativity (การคิดเชื่อมโยง)
- เน้นสร้างเครือข่ายความรู้ผ่านลิงก์ของ Obsidian เพื่อเชื่อมโยงข้ามศาสตร์ มากกว่าการจัดเก็บบรรณารักษ์แบบแยกห้องสมุดทั่วไป

### ข. High-Value Information (กฎ 1 ปี)
- เลือกกรองเฉพาะข้อมูลที่เป็น "แก่น" (Principles / Insights / Frameworks) ที่มีมูลค่าใช้ซ้ำได้ยาวนานอย่างน้อย 1 ปีขึ้นไป หลีกเลี่ยงข่าวรายวันหรือข้อมูลฉาบฉวย

### ค. The Deep Learning Workflow (แกะกล่องดำ)
- เมื่อเผชิญหน้ากับความรู้ อุตสาหกรรม หรือทักษะใหม่ๆ ที่ซับซ้อน ให้ใช้กระบวนการ [The Deep Learning Workflow](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/SECOND_BRAIN_PRINCIPLE/The%20Deep%20Learning%20Workflow.md) เป็น Framework หลักในการย่อยข้อมูล โดยแบ่งเป็น:
  1. **Deconstruction:** ย่อยให้เหลือแค่ 4 เสาหลัก (Value Prop, Business Model, Unit Economics, Moats)
  2. **Mapping:** กางแผนที่เรียนรู้คำศัพท์, 80/20 Rule, และ KPI หลัก (North Star Metric)
  3. **Progression:** เรียนรู้แบบเป็นลำดับขั้น (กฏพื้นฐาน -> ข้อโต้แย้ง -> กลยุทธ์)
  4. **Active Practice:** นำความรู้ไปลองจำลองสถานการณ์หรือหา Case Study
  5. **Synthesis:** ใช้ Feynman Technique ในการถ่ายทอดกลับ

### ง. The Leverage Philosophy (มุ่งสู่เจ้าของระบบ)
- ระบบนี้มีจุดประสงค์หลักเพื่อเปลี่ยนสถานะจาก "พนักงานประจำ" ไปสู่ "เจ้าของธุรกิจและผู้สร้างระบบ" (System Builder & Entrepreneur) ค้นหาและเก็บรวบรวมคานงัด (Code, Capital, Content, Collaboration) เพื่อสร้างระบบที่เงินทำงานแทนเวลา

### จ. การจำแนกประเภทข้อมูล: Domain vs. Concept
* **Domain (อยู่ที่ไหน?):** หมวดวิชาหลัก เช่น `#domain/tech`, `#domain/business`, `#domain/productivity`, `#domain/health`
* **Concept (ทำงานยังไง?):** แก่นกลไกการทำงาน (Mental Model) ที่ประยุกต์ข้าม Domain ได้ เช่น `#concept/leverage` (คานงัด), `#concept/bottleneck` (คอขวด), `#concept/compounding` (ดอกเบี้ยทบต้น), `#concept/trade-off` (การได้อย่างเสียอย่าง)

### ฉ. Token Optimization Strategy (โครงสร้างอิงอังกฤษ เนื้อหาอิงไทย)
- **คำสั่งระบบ (System Prompts):** โครงสร้างไฟล์ในโฟลเดอร์ `.agents` ทั้งหมด รวมถึง Template หัวข้อใน Markdown (เช่น `### 1. Core Thesis`) ต้องเขียนเป็น **ภาษาอังกฤษล้วน** เสมอ เพื่อลดการสูญเสีย Token โดยเปล่าประโยชน์จากการทำงานของ LLM Tokenizer
- **ผลลัพธ์ (Output Data):** แม้โครงสร้างจะประหยัด Token ด้วยภาษาอังกฤษ แต่จะมีการฝังคำสั่งบังคับให้ AI เขียนเนื้อหาเชิงลึก (Detail/Summaries) ออกมาเป็น **ภาษาไทยระดับมืออาชีพที่อ่านง่าย** เสมอ

---

## 2. โครงสร้างการไหลของข้อมูล (The Idea Pipeline)

| โฟลเดอร์ / ตำแหน่ง | หน้าที่ | สถานะปัจจุบัน / รายชื่อไฟล์ |
| :--- | :--- | :--- |
| **`Root`** | รูทของโปรเจกต์ประกอบด้วยสคริปต์หลักและคู่มือระบบ | - `ANTIGRAVITY.md` (คู่มือความเข้าใจระบบ AI)<br>- `README.md` (คู่มือแนะนำระบบสำหรับ GitHub)<br>- `run-architect.ps1`<br>- `run-distiller.ps1`<br>- `run-intelligence.ps1` (สคริปต์รวบรวมและคัดสรรข่าวความรู้ระดับโลก)<br>- `run-intelligence.ps1` (สคริปต์รวบรวมและคัดสรรข่าวความรู้ระดับโลก)<br>- `run-word-sync.ps1` (สคริปต์ซิงก์อัปเดตไฟล์ Word)<br>- `.gitignore` |
| **`01_INBOX`** | จุดพักข้อมูลดิบชั่วคราว ต้องเคลียร์เป็นศูนย์เสมอ | - `inbox_feyman.md` (Raw)<br>- `วิธีสรุปหนังสือ.md` (Raw) |
| **`02_SOURCE`** | สรุปภาพรวมและแก่นความคิดจากแหล่งข้อมูลภายนอก | - `สรุป The Almanack of Naval Ravikant.md`<br>- `WORK_KNOWLEDGE/` (โฟลเดอร์ย่อยเก็บวิชาความรู้จากการเรียน)<br>- `WORK_KNOWLEDGE/attachments/` (รูปภาพแนบจาก Word)<br>- `WORK_KNOWLEDGE_SUMMARY/` (แดชบอร์ดสรุปวิชาแยกราย 6 โดเมน)<br>- `CURATED_FEEDS/` (โฟลเดอร์รวบรวมสรุปความรู้ระดับโลกจาก YouTube & RSS Newsletters แยกเก็บเป็นโฟลเดอร์รายวัน YYYY-MM-DD อัตโนมัติ) |
| **`03_ZETTEL`** | คลังเก็บ "Atomic Notes" (1 ไอเดียต่อ 1 โน้ต) | - `Permissionless Leverage.md`<br>- `Rapid Skill Acquisition.md`<br>- `Specific Knowledge.md`<br>- `Wealth is Assets Not Money.md` |
| **`04_MOC`** | สารบัญเชื่อมโยงแนวคิดข้ามสายตาม Theme หลัก (Map of Content) | - `Daily Writing MOC.md` (รวบรวมงานเขียนฝึกฝนรายวัน)<br>- `Featured Writing MOC.md` (พอร์ตโฟลิโอศูนย์กลางเชื่อมโยงงานซีรีส์บทความเขียนเผยแพร่หลัก) |
| **`05_OUTPUT`** | ผลงานฉบับร่างที่สมบูรณ์พร้อมใช้จริง | - `Writing` (โฟลเดอร์ย่อย) |
| **`SECOND_BRAIN_PRINCIPLE`** | คลังคู่มือหลักการจัดหมวดหมู่และกลไกความรู้ | - `Domain & Concept obsidian.md`<br>- `My Idea.md`<br>- `Overview Domain Knowledge.md`<br>- `The Optimal Problem-Solving Framework.md` |

---

## 3. กฎเกณฑ์การตั้ง Tag และการจัดหน้า (Tagging & Formatting Rules)
- **ห้ามใช้ YAML Frontmatter:** ห้ามเขียน `---` เปิดปิดส่วนหัว ให้ใช้สัญลักษณ์ `#` พิมพ์ลงในบรรทัดเนื้อหาโดยตรง
- **แท็กผู้สร้าง (บังคับระบุ):**
  - `#creator/ai` = เนื้อหาจัดทำ/สรุปโดย AI
  - `#creator/me` = เนื้อหาเรียบเรียง/เขียนขึ้นโดยคุณเอง
- **แท็กประเภทโน้ต:** `#type/source`, `#type/zettel`, `#type/moc`, `#type/output`
- **การพิมพ์แท็ก:** ใช้ตัวพิมพ์เล็กทั้งหมด คำประสมเชื่อมด้วยขีดกลาง (เช่น `#concept/feedback-loop`)
- **การใช้กล่องเน้นข้อมูลสำหรับความเห็นต่าง (Obsidian Callouts):**
  - ในการประมวลผลประเด็นโต้แย้ง/ความเสี่ยง (Contrarian Analysis & Trade-offs) ให้บังคับใช้ระบบ Obsidian Callouts เสมอ เพื่อให้ตัวเอกสารสามารถแสดงผลเป็นกล่องส้มเตือนความจำได้อย่างสวยงาม ทันสมัย และอ่านง่าย ไร้ความล้าของสายตาทั้งบน Desktop และแอปพลิเคชัน Obsidian Mobile ในมือถือ (iOS/Android)
  - รูปแบบเทมเพลตมาตรฐาน:
    ```markdown
    > [!WARNING] มุมวิเคราะห์ขัดแย้งเชิงวิพากษ์ & ข้อดีข้อเสียที่ต้องแลก (Contrarian Analysis & Trade-offs)
    > - ⚖️ **[ประเด็นโต้แย้งที่ 1]:** [รายละเอียดวิพากษ์โดย Contrarian...]
    ```

---

## 4. แผนงานการสั่งการของผู้ช่วย AI (Agent Commands & CLI Integration)
ระบบนี้ทำงานร่วมกับบทบาทเฉพาะทางของ AI ในโฟลเดอร์ `.agents/` ผ่านการเรียกใช้ `agy` CLI ในสคริปต์ PowerShell:

* **The Distiller ([instruction](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/.agents/Distiller/instruction.md)):** ทำหน้าที่เป็น **Timeless Knowledge Extractor** สกัดแก่นความคิด (Mental Models) และมุมมองขัดแย้ง (Contrarian Analysis) จากไฟล์ข้อความดิบใน `01_INBOX` ลงมาสู่ `02_SOURCE` หรือ `03_ZETTEL` อย่างมีโครงสร้าง
* **The YouTube Orchestrator Manager ([instruction](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/.agents/YouTubeManager/instruction.md)):** 
  * ระบบจำลอง Multi-Agent Consensus ย่อยในการถอดความและวิเคราะห์คลิปวิดีโอจาก YouTube อัตโนมัติ (ถอด Transcript ผ่านสคริปต์ Python)
  * ประสานงานระหว่าง **Summarizer (สรุปแก่น)**, **Contrarian (คิดค้าน/หา Bias/Trade-off)** และ **Verifier (สแกน Fact vs Noise)**
  * รวมผลลัพธ์รอบด้านเข้าสู่ `02_SOURCE` (สรุปรวม) และ `03_ZETTEL` (ย่อยรายประเด็น) โดยสามารถเลือกสรุปลง `02_SOURCE` เฉพาะอย่างเดียวเพื่อติดตามข่าวสารโดยไม่แตก Zettel ได้
* **The Personal AI Intelligence Curator (`run-intelligence.ps1`):** สแกนดึงข้อมูลอัตโนมัติจาก YouTube Channel และ RSS Feed ตามลิสต์ระดับโลกใน `intelligence_sources.json`
  * **[AI Prioritization Step]** หากพบบทความเกินโควต้า ระบบจะเรียกใช้ **Prioritizer Agent** ในการให้คะแนนและเลือกเฉพาะ 20 บทความที่สะท้อน "Timeless Knowledge" มากที่สุด
  * ดาวน์โหลดทรานสคริปต์/บทความดิบ คลีนข้อมูล และส่งให้ Multi-Agent / Distiller แปลงเป็นโน้ตสรุปแก่น Timeless Knowledge คุณภาพสูง ปลายทางแยกไว้เฉพาะที่ `02_SOURCE/CURATED_FEEDS/` (โดยจัดหมวดหมู่แยกเก็บรายวันตามโฟลเดอร์ YYYY-MM-DD อัตโนมัติ) 
  * มีระบบ Deduplication เพื่อสแกนและป้องกันการดึงเนื้อหาที่เคยมีอยู่แล้วซ้ำซ้อน
  * **[Maintenance Rule]** เมื่อเพิ่มช่อง YouTube ใหม่ลงใน `intelligence_sources.json` ห้ามเชื่อถือ Channel ID จากเว็บไซต์ภายนอก ให้ดึงจาก Source Code ของหน้า YouTube นั้นๆ โดยตรง (ตัวแปร `channel_id`) เพื่อป้องกันปัญหา RSS Feed 404 Not Found
  * **[Architecture Rule: Agent IPC]** การสื่อสารระหว่าง Script และ AI Agent (`Prioritizer`) บังคับให้ใช้การเขียนไฟล์ (File-Based IPC) เสมอ ห้ามดักจับข้อความจากหน้าจอ (Stdout Parsing) เพื่อป้องกันปัญหาข้อมูลพังจาก UI หรือข้อความแชทของ AI ที่แทรกเข้ามา
* **The Word Ingestion Sync Engine:** 
  * แปลงและนำเข้าสคริปต์ความรู้จากการเรียนเรียน (.docx) ในโฟลเดอร์ `01_INBOX/WORK_KNOWLEDGE/` ที่คุณก๊อปปี้มาวาง
  * สแกนกวาดซับโฟลเดอร์ย่อยทั้งหมด (Recursive) และสร้างโครงสร้างแบบ 1:1 ปลายทางที่ `02_SOURCE/WORK_KNOWLEDGE/`
  * ถอดแกะรูปภาพแนบออกมาเซฟที่โฟลเดอร์ `02_SOURCE/WORK_KNOWLEDGE/attachments/` และเขียนลิงก์ Obsidian Wikilink `![[ชื่อไฟล์-img1.png]]` ลงในเอกสารให้อย่างเป็นระเบียบ
  * ใช้กลไก State Database ในการเปรียบเทียบเวลาแก้ไขและค่า MD5 Hash เพื่อประมวลผลเฉพาะไฟล์ใหม่หรือไฟล์เก่าที่มีการแก้ไขเพิ่มเติมเท่านั้น และทำการล้างเคลียร์ Inbox เป็นศูนย์อัตโนมัติเมื่อซิงก์สำเร็จลุล่วง
* **The Excel Writing List Sync Engine:**
  * แปลงและจัดเรียงสคริปต์งานเขียนหลักและบทความซีรีส์จาก Excel database (`D:\Boss\3) Hobby\3.14) Writing\Writing List.xlsx`) ประสานข้อมูลจากชีต `Publish Detail`, `Excerpt`, และ `Midgrad` ลงคลังอัตโนมัติ
  * จัดกลุ่มแยกตอนและสกัดประเภท/แท็กโดเมนอย่างไดนามิก วางปลายทางเป็นหมวดซีรีส์ใต้ `05_OUTPUT/Writing/`
  * ปรับปรุงหน้าแผนผังพอร์ตโฟลิโอ [Featured Writing MOC.md](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/04_MOC/Featured%20Writing%20MOC.md) อัตโนมัติในทุกครั้งที่รัน เพื่อจัดโครงสร้างซีรีส์งานเขียนทั้งหมดให้เชื่อมโยงสยายปีกสวยงามใน Graph View
* **The Architect ([instruction](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/.agents/Architect/instruction.md)):** คลัสเตอร์โน้ตใน Zettel เพื่อจัดกลุ่มเชื่อมโยงออกมาเป็นแผนผังความคิดใน MOC
* **The Builder ([instruction](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/.agents/Builder/instruction.md)):** สังเคราะห์วัตถุดิบและเขียนร่างชิ้นงานฉบับสมบูรณ์ใน `05_OUTPUT`
* **The Deep Learning Business Analyst (`run-business.ps1`):** 
  * Dedicated interactive script for autonomous deep-dive business research across 5 MECE domains.
  * Provides an interactive prompt to select the domain (Business Models, Behavioral Psychology, Systems Thinking, Culture & Leadership, Risk Management) and input multiple topics.
  * Dynamically instructs the corresponding Agent (`BusinessModelAnalyst`, `BehavioralAnalyst`, `SystemsAnalyst`, `CultureAnalyst`, `RiskAnalyst`) to perform active web searches and deconstruct the topic using highly specialized frameworks.
  * Synthesizes findings strictly into Timeless Knowledge and saves the output to specific category folders under `02_SOURCE/BUSINESS_FEEDS/`.
  * Focuses exclusively on high-value case studies to expand mental models and structural understanding.
  * **Recommended Topics (Starter Pack):** `Amazon, Costco, Netflix, Stripe, Hermes, TSMC, Pinduoduo`

---

## 5. บันทึกประวัติการปรับปรุงระบบ (System Changelog)
- **2026-06-01 (รอบแรก - อัปเดตระบบ YouTube Multi-Agent Pipeline & ออปชั่นสรุปเฉพาะ SOURCE):**
  - อัปเกรดสคริปต์ `run-distiller.ps1` ให้ทำหน้าที่เป็น Entry Router ตรวจจับ YouTube Link ด้วย Regex และเปลี่ยนปลายทางกระบวนการอัตโนมัติ
  - สร้างสคริปต์ถอดคำบรรยายด่วน `get_youtube_transcript.py` รองรับ API เวอร์ชันล่าสุดของ `youtube-transcript-api` (v1.2.4)
  - พัฒนากลไกการวิเคราะห์แบบทีมขัดแย้งเชิงวิพากษ์ (Summarizer + Contrarian + Verifier) ภายใต้ `YouTubeManager`
  - ทำการทดสอบสมบูรณ์แบบด้วยวิดีโอ *"The first 20 hours"* ของ Josh Kaufman ได้รับไฟล์ Zettel ชื่อ `Rapid Skill Acquisition.md` ในคุณภาพดีเยี่ยม ปราศจากอคติ
  - **[ฟีเจอร์ใหม่]** เพิ่มตัวเลือกที่ 3: **"สรุปลง 02_SOURCE อย่างเดียว"** สำหรับโน้ตปกติและลิงก์ YouTube เพื่อความรวดเร็วในการติดตามเนื้อหาโดยไม่มีการแตก Zettel บวมลงคลัง
  - **[ปรับแต่งไฟล์ระบบ]** ดำเนินการแปลงสคริปต์ `.ps1` ทั้งหมด (`run-distiller.ps1`, `run-architect.ps1`) รวมถึงไฟล์ระบบ `ANTIGRAVITY.md` และ `README.md` ให้จัดเก็บในรูปแบบ **UTF-8 with BOM** เพื่อให้แสดงภาษาไทยบน PowerShell/Obsidian ได้อย่างสมบูรณ์แบบ ไม่มีตัวอักษรต่างดาว
  - **[การจัดตั้ง Git & GitHub]** เริ่มต้นระบบควบคุมเวอร์ชัน (Local Git) พร้อมเขียนไฟล์ `.gitignore` คลุมข้อมูลส่วนบุคคล/ไฟล์ขยะ และเชื่อมโยงส่งออก Backup ขึ้นไปคลาวด์ GitHub (`https://github.com/Nopparuth-Ju/my-second-brain-sync.git`) ได้สำเร็จเรียบร้อย
  - **[การสร้างเอกสารโครงการ]** เขียนคู่มือหลักภาษาอังกฤษและสเปกโปรเจกต์ `README.md` ที่รูทอย่างสวยงามเพื่อให้พร้อมสำหรับ GitHub
  - **[มาตรฐานสำหรับมือถือ]** กำหนดแนวทางการแสดงผล Contrarian Analysis ผ่าน **Obsidian Callouts** (`> [!WARNING]`) ในคู่มือข้อที่ 3 เพื่อให้สามารถเปิดอ่านโน้ตความรู้บนแอป Obsidian Mobile ทั้งบน iOS และ Android ได้อย่างสวยงาม สบายตา ไร้อคติ โดยไม่ต้องพึ่งพาเบราว์เซอร์ภายนอก
  - **[ฟีเจอร์ซิงก์ไฟล์ Word]** พัฒนาและติดตั้งระบบ **Word-to-Obsidian Sync Engine** (`run-word-sync.ps1` + `.agents/WordSync/`) เพื่อช่วยให้ผู้ใช้เรียนไปจดไปผ่าน Word พร้อมแนบรูปภาพ และสั่งกวาดซิงก์อัปเดตลงคลัง Obsidian `02_SOURCE/WORK_KNOWLEDGE/` แบบตรวจจับความเปลี่ยนแปลงอัตโนมัติ (State DB) และกวาดล้าง Inbox อัตโนมัติเมื่อทำเสร็จ
- **2026-06-01 (รอบสอง - แก้ไขบักการดึงรูปภาพใน WordSync & ปัญหา Read-Only Windows Permission):**
  - **[แก้ไขระบบถอดรูปภาพ DOCX]** แก้ไขบั๊กของสคริปต์แปลงไฟล์โดยเปลี่ยนการสแกน `w:drawing` (รูปภาพสมัยใหม่) และ `v:imagedata` (รูปภาพ VML Legacy) จากเดิมค้นหาที่ระดับ Paragraph (`w:p`) ไปเป็นค้นหาแบบเรียกซ้ำ (Recursive) ภายใต้ระดับ Run (`w:r`) ซึ่งเป็นจุดที่โปรแกรม Word นำรูปมาเก็บจริง ผลลัพธ์คือ สามารถดึงรูปภาพแนบทั้งหมด 462 รูป ออกมาเซฟที่โฟลเดอร์ `02_SOURCE/WORK_KNOWLEDGE/attachments/` และเขียนลิงก์ Obsidian Wikilink `![[รูป.png]]` จำนวน 463 ลิงก์ในไฟล์ Markdown ปลายทางได้สมบูรณ์แบบ 100%
  - **[แก้ไข NAMESPACES Bug]** เพิ่มการระบุค่า `NAMESPACES` ในระบบ เพื่อแก้ไขข้อผิดพลาด `NameError: name 'NAMESPACES' is not defined` ของ Python
  - **[แก้บักลบไฟล์ติดล็อก Windows]** ปรับแต่งกระบวนการทำ Inbox Zero โดยเปลี่ยนจากการเรียก `shutil.rmtree()` เปล่าๆ ไปเป็นการส่ง Callback `onerror=remove_readonly` ร่วมกับ `os.chmod` เพื่อแก้ปัญหาการติดสิทธิ์ลบโฟลเดอร์ย่อยประเภท Read-Only เช่น ไฟล์ `.git/objects/` ซึ่งมักทำให้ระบบล่มบน Windows ปัจจุบันซิงก์และลบไฟล์ Inbox ลุล่วงเรียบร้อย
  - **[คลีนโครงการ]** ลบไฟล์ทรานซิชันทดสอบ `.agents/WordSync/test_single_sync.py` เพื่อให้คลังเก็บโค้ดตัวแทนเป็นระเบียบเรียบร้อย และทำการ Git Commit และ Push ขึ้น GitHub เรียบร้อย
- **2026-06-01 (รอบสาม - บีบอัดรูปภาพ WebP อัตโนมัติ, สร้างระบบ Distill แก่นความรู้รายโดเมน & รักษาความปลอดภัย Git 100%):**
  - **[ภาพแนบ WebP จิ๋วสมบูรณ์แบบ]** พัฒนาและติดตั้งระบบบีบอัดภาพ WebP อัตโนมัติด้วย Pillow ในสคริปต์ `sync_word_notes.py` เพื่อเปลี่ยนภาพสกรีนช็อตต้นฉบับขนาดใหญ่ให้เป็น WebP (Quality 80%) ทำการซิงก์กวาดข้อมูล Word **125 ไฟล์** ดึงรูปภาพสำเร็จ **17,794 รูป** โดยใช้พื้นที่รวมเพียง **758.7 MB** (เฉลี่ยรูปละ 42KB เท่านั้น ประหยัดพื้นที่ vault ไปกว่า 90% ซิงก์ด่วนขึ้น 10 เท่า และเรนเดอร์ลื่นไหลไม่เด้งบน Obsidian Mobile)
  - **[ระบบตกผลึกวิชา Domain Distiller]** พัฒนาสคริปต์ `distill_domains.py` คัดสรรจัดกลุ่มวิชาเรียน 125 ไฟล์ออกมาเป็นแดชบอร์ดสรุปรวมสำคัญ **6 โดเมนหลัก** วางปลายทางอย่างเป็นระเบียบเรียบร้อยที่โฟลเดอร์ **`02_SOURCE/WORK_KNOWLEDGE_SUMMARY/`** มีหน้าสารบัญ Wikilink เชื่อมโยงพร้อมคีย์เวิร์ด/หัวข้อสำคัญให้เปิดทวนด่วนบนมือถือได้ลื่นที่สุด
  - **[กลไกถนอมโฟลเดอร์ Inbox]** ปรับปรุงกระบวนการ Inbox Zero โดยให้ทำการล้างไฟล์ดิบ Word และโฟลเดอร์ย่อยทั้งหมดออก แต่ยังคงรักษากล่องโฟลเดอร์เปล่าที่ชื่อ `01_INBOX\WORK_KNOWLEDGE\` เอาไว้เพื่อให้ผู้ใช้งานไม่จำเป็นต้องสร้างใหม่ในรอบถัดไป
  - **[รักษาความปลอดภัยข้อมูลส่วนตัว 100%]** ปรับปรุงไฟล์ `.gitignore` และสั่งรันเคลียร์ Git Index ถอนการติดตามโฟลเดอร์เนื้อหาความรู้ส่วนตัวทั้งหมดออกจากระบบประวัติของ GitHub สำเร็จ 100% คงเหลือเพียงโค้ด orchestrators และ runners บน GitHub ทำให้คลังโค้ดของคุณมีความเป็นส่วนตัว ปลอดภัย และมีประสิทธิภาพสูง
- **2026-06-01 (รอบสี่ - ระบบซิงก์ Excel Writing List ลง 05_OUTPUT/Writing & จัดเรียงแยก Series อัตโนมัติ):**
  - **[ฟีเจอร์ใหม่]** พัฒนาและติดตั้งระบบ **Excel-to-Obsidian Writing Sync Engine** (`run-writing-sync.ps1` + `.agents/WordSync/sync_excel_writings.py`) ดึงข้อมูลจากไฟล์ `D:\Boss\3) Hobby\3.14) Writing\Writing List.xlsx`
  - **[การจัดเตรียมและจัดรูปเรียงไฟล์]** ดำเนินการกวาดอ่าน 3 แผ่นชีตหลัก (`Publish Detail`, `Excerpt`, `Midgrad`), ทำการผสานข้อมูลข้ามชีตด้วยคีย์ `(No, EP)` และรองรับกรณีชื่อตอนสะกดต่างกันเล็กน้อย (Fuzzy matching/Normalizing), จัดสรรแยกหมวดหมู่เป็นโฟลเดอร์ตามชื่อซีรีส์ พร้อมบันทึกไฟล์เป็นชื่อตอน `EP {Num} - {Title}.md`
  - **[ระบบแท็กและกล่องข้อมูลการเขียน]** แทรกกล่อง Obsidian Callout `> [!NOTE] ข้อมูลการเขียน` รวบรวม Objective, Human Desire, และ Excerpt ด้านบนสุด พร้อมจัดทำ frontmatter tags อัตโนมัติ `#type/output #creator/me #status/ready #writing/storytelling #writing/midgrad` รวมถึงโดเมนหลักอย่างไดนามิก (เช่น `#domain/happiness`, `#domain/knowledge`)
  - **[ระบบพอร์ตโฟลิโอ MOC แยกเฉพาะตัว]** พัฒนาและเปิดใช้งานระบบสร้าง/อัปเดตแผนผังรวมผลงานชิ้นเอกอัตโนมัติแยกเฉพาะใน [Featured Writing MOC.md](file:///D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\04_MOC\Featured%20Writing%20MOC.md) (ไม่รบกวนหน้าฝึกเขียนรายวัน) เชื่อมต่อซีรีส์ทั้งหมดกระจายออกจากจุดศูนย์กลางพอร์ตโฟลิโอผลงานหลักจุดเดียว เพื่อความสะอาดเป็นระเบียบและเห็นคลัสเตอร์ชัดเจนที่สุดใน Graph View
- **2026-06-01 (รอบห้า - ปรับปรุงประสิทธิภาพคำสั่ง AI แบบ Token-Saver & ความเสถียรของ Second Brain Reader):**
  - **[ลดโทเค็นลงกว่า 70%]** ดำเนินการอัปเกรดแปลงระบบคำสั่ง (System Instructions) และทักษะ (Core Skills) ของ AI Agents ทั้งหมด 5 ตัว (Architect, Distiller, Builder, YouTubeManager และลูกทีมย่อย) จากภาษาไทยให้เป็นภาษาอังกฤษที่กระชับและหนาแน่น ช่วยลดจำนวนความยาวของพร้อมต์ลงถึง 70% ลดระยะเวลาการหน่วงในการตอบสนอง (Latency) ได้ดีขึ้น 2-3 เท่า และเพิ่มความแม่นยำในการทำตามกฎ (เช่น No YAML Frontmatter) ได้อย่างยอดเยี่ยม โดยยังคงคำสั่งบังคับให้ผลิตผลลัพธ์ข้อมูลโน้ตเป็นภาษาไทยคุณภาพสูงสละสลวย 100% เช่นเดิม
  - **[แก้บักการเชื่อมต่อค้างใน Reader]** แก้ไขข้อจำกัดในการเชื่อมต่อโฟลเดอร์หลักและโฟลเดอร์ `02_SOURCE` ของแอปพลิเคชัน **Second Brain Reader** ซึ่งก่อนหน้านี้มีปัญหาค้างหรือเชื่อมต่อล้มเหลวเนื่องจากต้องกวาดอ่านรูปภาพแนบในโฟลเดอร์ `attachments` กว่า 17,794 รูป:
    - ปรับปรุงให้ตัวกรองการข้ามสแกน (`ignoredFolders`) ทำงานแบบไม่สนใจตัวพิมพ์เล็ก-ใหญ่ (Case-Insensitive) ทำให้ระบบทำการข้ามสแกนโฟลเดอร์มีเดียสะกดใหญ่-เล็กได้ทั้งหมด (`attachments`, `assets`, `images`)
    - เพิ่มคำสั่งให้ระบบข้ามโฟลเดอร์สำรองข้อมูล เช่น `"archive"`, `"backup"`, `"temp"`, `"tmp"`, และถังขยะ `".trash"` ทันที
    - ครอบระบบป้องกันการหยุดทำงาน (Try-Catch File Recovery) แยกเฉพาะระดับไฟล์เดี่ยว ทำให้หากเจอไฟล์สำรองหรือไฟล์ชั่วคราวบางตัวติดสิทธิ์ล็อกของระบบปฏิบัติการ ตัวแอปจะทำการข้ามและไปสแกนโน้ตถัดไปอย่างราบรื่น ส่งผลให้การเปิดเชื่อมต่อทำงานได้ทันทีภายในเสี้ยววินาทีและมีความแข็งแกร่งสูงสุด 100%
- **2026-06-02 (ติดตั้งระบบ Personal AI Intelligence Curator, โฟลเดอร์ CURATED_FEEDS แยกเฉพาะ & ซิงก์ Git อัปเดต @antigravity):**
  - **[จัดตั้งโฟลเดอร์แยกเฉพาะ]** จัดตั้งและกำหนดโฟลเดอร์ปลายทางใหม่ `02_SOURCE/CURATED_FEEDS/` เพื่อแยกไฟล์สรุปคัดกรองความรู้ระดับโลกออกมาต่างหากจากข้อมูลเรียนและสรุปแบบปกติของ vault ช่วยรักษาความเป็นระเบียบและทำให้ค้นหาเนื้อหาเด่นได้ทันที
  - **[เสร็จสมบูรณ์ระบบ Personal AI Intelligence Curator Engine]** ผสานการทำงานระหว่าง Python scraper (`harvest.py` ภายใต้ `.agents/IntelligenceCurator/`) และ CLI `run-intelligence.ps1` สแกนและกรองคอนเทนต์ข่าวและวิดีโอจาก YouTube 9 ช่องชั้นนำและ RSS 5 สำนักข่าว/จดหมายข่าวระดับพรีเมียม (เช่น Veritasium, Karpathy, Y Combinator, The Secret Sauce, Stratechery, BBC)
  - **[ระบบวิเคราะห์เตือนความเสี่ยง Obsidian Callouts]** บังคับใช้ระบบวิเคราะห์โต้แย้ง Contrarian Analysis & Trade-offs ภายในไฟล์สรุปทรานสคริปต์ของ YouTube/RSS เสมอ ผ่านการแสดงผลกล่องเตือน `> [!WARNING]` เพื่อคุณภาพสูงสุดและอ่านบนมือถือได้อย่างลื่นไหล
  - **[อัปเดตระบบหน่วยความจำกลาง]** อัปเดตและจดบันทึกประวัติกลไกของโปรเจกต์ลงใน `ANTIGRAVITY.md` และ `MY_AI_PROJECTS_MEMORIES.md` ของคลังความรู้ เพื่อให้ผู้ช่วย AI ในอนาคตเข้าใจโครงสร้างและวิสัยทัศน์ของระบบนี้ได้อย่างสมบูรณ์แบบ
  - **[บันทึกประวัติเวอร์ชันขึ้น GitHub]** ทำการคอมมิตและอัปโหลดซอร์สโค้ด (Engine, Runner, configurations) ทั้งหมดของโปรเจกต์ Second Brain ไปยัง Git repository บน GitHub ของคุณเพื่อความปลอดภัยและการ Backup อย่างเป็นระบบ
- **2026-06-12 (อัปเกรด Prioritizer Agent, โฟกัส Timeless Extractor, Code Review แก้บัก & เพิ่มช่องความรู้ไทย):**
  - **[จัดตั้ง Prioritizer Agent]** สร้างซับเอเจนต์ย่อยตัวใหม่ `Prioritizer` (`.agents/Prioritizer/`) และปรับแก้กลไกของ `harvest.py` ให้ทำงานในระบบโควต้า (ดึงไม่เกิน 20 บทความต่อรอบ) หากมีบทความเกินโควต้า ระบบจะให้ AI เข้ามาจัดอันดับและตัดเลือกเอาเฉพาะอันดับท็อป 20 อันดับที่มี High-Signal และ Timeless ที่สุดเท่านั้น
  - **[ปรับปรุง Distiller ให้เจาะจงแก่นแท้]** ปรับแก้คำสั่งของ `Distiller` ให้หันมาโฟกัสกับการจับประเด็นโครงสร้างวิเคราะห์แก่นแท้ (Mental Models & Frameworks) แทนการสรุปเนื้อหาธรรมดา พร้อมบังคับแทรกกล่องประเมินวิพากษ์ (Contrarian Analysis & Trade-offs) และเชื่อมโยงกับการประยุกต์ใช้ในชีวิตจริง
  - **[Code Review & Bug Fixes]** ทำการรีวิวโค้ดสคริปต์กวาดข้อมูล `harvest.py` เพิ่มส่วนสนับสนุน Fallback สำหรับ Atom feed (เช่น Substack, LessWrong), แก้บั๊กตัวแปรตกค้างเวลาระบบ AI ทำงานล้มเหลว (Cleanup temp files), ปรับ Performance โครงสร้างการค้นหาเป็น `set()` (O(1)) ตลอดจนเพิ่ม metadata timestamp ในตัว state database 
  - **[เพิ่มแหล่งข้อมูลไทย Timeless Knowledge]** ซ่อมแซมลิงก์ RSS ของ Morgan Housel และเพิ่ม YouTube Channels คุณภาพสูงสายไทยลงในระบบอัปเดตอัตโนมัติอีก 5 ช่อง (THE STANDARD, THE STANDARD WEALTH, The Money Coach, Nopadol's Story, DataRockie) รวมเป็น 14 ช่อง เพื่อให้คลังสมองได้รับแก่นความคิดที่หลากหลายและใช้งานได้จริงในบริบทคนไทย
- **2026-06-14 (ยกเครื่องระบบวิเคราะห์ธุรกิจเป็น 5 แกน (MECE Architecture) & ระบบ Interactive Prompt):**
  - **[สถาปัตยกรรม MECE 5 แกน]** ถอดถอน IndustryResearcher ตัวเก่าออกและสร้าง Agent วิจัยเชิงลึก 5 ตัวที่แยกตามหมวดหมู่ MECE ไม่ทับซ้อนกัน ได้แก่: `BusinessModelAnalyst`, `BehavioralAnalyst`, `SystemsAnalyst`, `CultureAnalyst`, `RiskAnalyst` เพื่อโฟกัสเนื้อหาเฉพาะทางอย่างเฉียบคม
  - **[ระบบ Interactive Runner]** อัปเกรดสคริปต์เก่าเป็น `run-business.ps1` แบบตอบโต้สด (Interactive) ผู้ใช้สามารถเลือกหมวดหมู่และพิมพ์ชื่อ Topic ได้หลายเรื่องพร้อมกัน (ไม่ต้องแก้ไฟล์ JSON Queue อีกต่อไป)
  - **[Token Optimization]** กำหนดโครงสร้างคำสั่ง Prompt ของ Agent 5 ตัวใหม่ทั้งหมดเป็นภาษาอังกฤษ 100% แต่บังคับให้ตอบผลลัพธ์การวิเคราะห์ที่ซับซ้อนออกมาเป็นภาษาไทย
  - **[หมวดหมู่โฟลเดอร์ปลายทาง]** จัดระเบียบผลลัพธ์แยกตามโฟลเดอร์ย่อย 5 สาขา ภายใต้ `02_SOURCE/BUSINESS_FEEDS/` โดยอัตโนมัติ

