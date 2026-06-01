import os
import re
import sys

# Reconfigure standard output to support UTF-8 (emojis and Thai characters) in Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Directories
VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_DIR = os.path.join(VAULT_ROOT, "02_SOURCE", "WORK_KNOWLEDGE")
SUMMARY_DIR = os.path.join(VAULT_ROOT, "02_SOURCE - WORK_KNOWLEDGE_SUMMARY")

# Domain categorization criteria (maps domain title to list of keyword matches in filepath)
DOMAINS = {
    "1_Business_Analytics_&_Accounting": {
        "title": "📊 1. Business Analytics & Cost Accounting (วิชาการวิเคราะห์ธุรกิจและการบัญชีต้นทุน)",
        "keywords": ["business", "cost accounting", "accounting"]
    },
    "2_Cloud_DevOps_&_Infrastructure": {
        "title": "☁️ 2. Cloud Computing, DevOps & Infrastructure (วิชาระบบคลาวด์และโครงสร้างพื้นฐาน)",
        "keywords": ["aws", "azure", "docker", "splunk", "airflow", "command prompt", "unix", "linux"]
    },
    "3_Databases_&_Data_Engineering": {
        "title": "🛢️ 3. Databases, SQL & Data Engineering (วิชาฐานข้อมูลและการวิศวกรรมข้อมูล)",
        "keywords": ["sql", "database", "mongodb", "pyspark", "snowflake", "bigquery"]
    },
    "4_Business_Intelligence_&_Visualization": {
        "title": "📉 4. Business Intelligence & Data Visualization (วิชา BI และการแสดงข้อมูล)",
        "keywords": ["tableau", "powerbi", "power bi", "alteryx", "excel", "spreadsheet"]
    },
    "5_Programming_&_Hacking": {
        "title": "💻 5. Programming Languages & Technical Skills (วิชาเขียนโปรแกรมและทักษะเทคนิค)",
        "keywords": ["python", "java", "/r/", "hacking", "claude", "ethical hacking"]
    },
    "6_Data_Science_&_Core_Concepts": {
        "title": "📚 6. General Data Science & Statistical Readings (วิชาวิทยาศาสตร์ข้อมูลและแนวคิดสถิติ)",
        "keywords": ["data science", "data literacy", "naked statistics", "analytics for beginners", "marketing", "statistics", "read about data", "อ่านเกี่ยวกับ data"]
    }
}

# Fallback domain for files that don't match any keyword
FALLBACK_DOMAIN = "6_Data_Science_&_Core_Concepts"

def get_domain_key(file_path):
    """Categorize file path into a domain."""
    normalized_path = file_path.lower().replace("\\", "/")
    
    for key, config in DOMAINS.items():
        for kw in config["keywords"]:
            if kw in normalized_path:
                return key
    return FALLBACK_DOMAIN

def parse_and_summarize_note(file_path, obsidian_link_name):
    """Parses a markdown note, extracts headings and bold terms to build a dense executive summary."""
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
    except Exception:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return f"❌ *ไม่สามารถอ่านโน้ตได้เนื่องจากข้อผิดพลาด: {e}*"

    lines = content.split("\n")
    summary_lines = []
    
    # Extract Title from first # heading or use file name
    title = os.path.basename(file_path).replace(".md", "")
    for line in lines:
        if line.startswith("# ") and not line.startswith("#type") and not line.startswith("#status") and not line.startswith("#domain"):
            title = line.replace("# ", "").strip()
            break

    summary_lines.append(f"### 📖 [[{obsidian_link_name}|{title}]]")
    summary_lines.append(f"*📁 ลิงก์โน้ตวิชาตัวเต็ม: [[{obsidian_link_name}|คลิกเปิดอ่านตัวเต็มพร้อมรูปประกอบ WebP]]*")
    summary_lines.append("")

    headings_and_definitions = []
    current_heading = None
    
    # Simple semantic extractor
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        # 1. Capture headings (## or ###)
        if stripped.startswith("## ") or stripped.startswith("### "):
            h_level = "##" if stripped.startswith("## ") else "###"
            h_text = stripped.replace("## ", "").replace("### ", "").strip()
            
            # Skip metadata headings
            if h_text.lower() in ["type", "status", "domain", "creator"]:
                continue
                
            current_heading = h_text
            headings_and_definitions.append(f"  * **หัวข้อ: {h_text}**")
            
        # 2. Capture bullet points with bold definitions
        elif stripped.startswith("-") or stripped.startswith("*") or (stripped[0].isdigit() and stripped[1] == '.'):
            # Clean list prefix
            clean_line = re.sub(r'^[-*]\s*', '', stripped)
            clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
            
            # Check for bold terms like **Term** = or **Term** คือ or **Term** : or **Term** (Details)
            bold_matches = re.findall(r'\*\*([^*]+)\*\*', clean_line)
            if bold_matches:
                # Limit size to prevent summary blow-up
                if len(headings_and_definitions) < 25: # Max 25 key takeaways per file
                    # Highlight bold terms inside summary
                    headings_and_definitions.append(f"    - {clean_line}")

    if headings_and_definitions:
        summary_lines.extend(headings_and_definitions)
    else:
        # Fallback if no specific structured bullets exist
        preview = []
        for line in lines:
            stripped = line.strip()
            # Grab first few normal bullet points or paragraphs
            if stripped and not stripped.startswith("#") and len(preview) < 5:
                preview.append(f"    - {stripped}")
        if preview:
            summary_lines.append("  * **แก่นเนื้อหาสรุปย่อ:**")
            summary_lines.extend(preview)
        else:
            summary_lines.append("  * *โน้ตเล่มนี้ว่างเปล่าหรือเป็นโครงสร้างรูปภาพอย่างเดียว*")
            
    summary_lines.append("\n" + "---" + "\n")
    return "\n".join(summary_lines)

def run_distillation():
    print("🚀 Starting Knowledge Distillation Pipeline...", flush=True)
    
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: SOURCE directory {SOURCE_DIR} does not exist.")
        return
        
    os.makedirs(SUMMARY_DIR, exist_ok=True)
    
    # Store summaries categorized by domain key
    domain_contents = {key: [] for key in DOMAINS.keys()}
    domain_files_count = {key: 0 for key in DOMAINS.keys()}
    
    # Walk through SOURCE_DIR recursively to find all .md files
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if not file.endswith(".md") or file.lower() == "readme.md":
                continue
                
            full_path = os.path.join(root, file)
            
            # Get Obsidian relative link path
            rel_path = os.path.relpath(full_path, VAULT_ROOT).replace("\\", "/")
            obsidian_link_name = rel_path.replace(".md", "")
            
            domain_key = get_domain_key(full_path)
            
            print(f"   - Processing: {file} -> Domain: {domain_key}")
            
            course_summary = parse_and_summarize_note(full_path, obsidian_link_name)
            domain_contents[domain_key].append(course_summary)
            domain_files_count[domain_key] += 1

    # Write summary files for each domain
    print("\n✍️ Writing distilled domain summaries to folder 02_SOURCE - WORK_KNOWLEDGE_SUMMARY...", flush=True)
    
    for key, config in DOMAINS.items():
        summary_file_name = f"{config['title']}.md".replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "-").replace("?", "-").replace("\"", "-").replace("<", "-").replace(">", "-").replace("|", "-")
        summary_file_path = os.path.join(SUMMARY_DIR, summary_file_name)
        
        file_count = domain_files_count[key]
        
        markdown_header = f"#type/source-summary\n#status/processed\n#domain/work-knowledge\n#creator/ai\n\n"
        markdown_header += f"# {config['title']}\n\n"
        markdown_header += f"> [!NOTE] สรุปรวบยอดความคิดประจำเป็นโดเมนความรู้\n"
        markdown_header += f"> - 📚 **จำนวนคอร์สเรียนในหมวดนี้:** {file_count} โน้ตวิชาเรียน\n"
        markdown_header += f"> - 🎯 **จุดประสงค์:** โน้ตนี้รวบรวมแก่นนิยาม หัวข้อ และคีย์เวิร์ดสำคัญของโน้ตทุกเล่มในหมวดนี้มาสรุปรวมในหน้าเดียว เพื่อการทบทวนด่วนบนมือถือ หากต้องการอ่านลึกพร้อมรูปภาพ WebP สามารถคลิกที่ชื่อโน้ตเพื่อเปิดดูวิชาตัวเต็มได้ทันที\n\n"
        
        markdown_header += "## 📌 สารบัญวิชาเรียนย่อยทั้งหมดในหมวดนี้ (Table of Contents)\n\n"
        
        # Add index list
        for root, dirs, files in os.walk(SOURCE_DIR):
            for file in files:
                if not file.endswith(".md") or file.lower() == "readme.md":
                    continue
                full_path = os.path.join(root, file)
                if get_domain_key(full_path) == key:
                    rel_path = os.path.relpath(full_path, VAULT_ROOT).replace("\\", "/")
                    obsidian_link_name = rel_path.replace(".md", "")
                    title = file.replace(".md", "")
                    markdown_header += f"- [[{obsidian_link_name}|📖 {title}]]\n"
                    
        markdown_header += "\n\n" + "---" + "\n\n"
        markdown_header += "## 🎯 แก่นสรุปใจความสำคัญแยกรายวิชา (Executive Domain Takeaways)\n\n"
        
        if domain_contents[key]:
            markdown_body = "\n\n".join(domain_contents[key])
        else:
            markdown_body = "*ยังไม่มีข้อมูลวิชาในหมวดหมู่การเรียนรู้นี้*"
            
        full_markdown = markdown_header + markdown_body
        
        with open(summary_file_path, "w", encoding="utf-8-sig") as f:
            f.write(full_markdown)
            
        print(f"   - Generated Summary File: {summary_file_name} ({file_count} files distilled)")
        
    print("\n🎉 All domain summaries have been successfully distilled and saved! Enjoy offline reading!")

if __name__ == "__main__":
    run_distillation()
