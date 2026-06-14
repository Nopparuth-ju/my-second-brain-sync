import json
import os

filepath = r"D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\.agents\IntelligenceCurator\temp_prioritize.json"
outpath = r"D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\scratch\candidates.txt"

with open(filepath, "r", encoding="utf-8") as f:
    items = json.load(f)

# Keywords for:
# 1. Business Systems & Leverage, Wealth Creation, Transitioning, etc.
# 2. Timeless Knowledge (Mental Models, System Thinking, Philosophy, Psychology)
# 3. High-Signal Tech/AI (major technology shifts, AI agents, stablecoins, startup leverage)
keywords = [
    "wealth", "leverage", "freedom", "quit", "business", "entrepreneur", 
    "system", "automate", "finance", "passive", "income", "profit", 
    "money", "career", "creator", "agent", "startup", "invest",
    "model", "psychology", "philosophy", "think", "standard wealth"
]

# Let's search Thai translation keywords as well
thai_keywords = [
    "ธุรกิจ", "รวย", "เงิน", "เกษียณ", "อิสรภาพ", "สร้างชีวิต", 
    "ลงทุน", "เวลา", "งาน", "ทุน", "ระบบ", "หนังสือ", "พัฒนา"
]

with open(outpath, "w", encoding="utf-8") as out:
    out.write(f"Total items loaded: {len(items)}\n\n")
    for item in items:
        title_lower = item["title"].lower()
        source_lower = item["source"].lower()
        
        matched_en = [kw for kw in keywords if kw in title_lower or kw in source_lower]
        matched_th = [kw for kw in thai_keywords if kw in title_lower]
        
        if matched_en or matched_th:
            out.write(f"ID: {item['id']}\n")
            out.write(f"Title: {item['title']}\n")
            out.write(f"Source: {item['source']}\n")
            out.write(f"Matched EN: {matched_en}\n")
            out.write(f"Matched TH: {matched_th}\n")
            out.write("-" * 40 + "\n")

print("Finished writing candidates to file.")
