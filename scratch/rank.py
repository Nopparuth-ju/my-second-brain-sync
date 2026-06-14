import json

filepath = r'D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\.agents\IntelligenceCurator\temp_prioritize.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Let's write a scoring function based on:
# Rule 1: Business Systems & Leverage (Highest Priority)
# Rule 2: Timeless Knowledge (High Priority)
# Rule 3: High-Signal Tech/AI (High Priority)
# Deprioritize: Daily news, vlogs, politics, transient stuff.

def get_score(item):
    title = item['title'].lower()
    source = item['source'].lower()
    
    score = 0
    
    # Rule 1: Business, Wealth, Leverage, Entrepreneur, System Builder
    r1_keywords = [
        'business', 'wealth', 'leverage', 'entrepreneur', 'system builder',
        'passive income', 'financial free', 'financially free', 'creator rules',
        'sponsorships', 'brand deals', 'monetize', 'automate my finances',
        'ธุรกิจ', 'สร้างตัว', 'การเงิน', 'ลงทุน', 'ใช้แรงทำเงินให้เงินทำงาน',
        'สร้างระบบ', 'ระบบธุรกิจ'
    ]
    for kw in r1_keywords:
        if kw in title or kw in source:
            score += 15
            
    # Rule 2: Timeless Knowledge, Mental Models, System Thinking, First Principles, Psychology, Philosophy
    r2_keywords = [
        'mental model', 'system thinking', 'first principles', 'psychology', 'philosophy',
        'die with zero', 'procrastination', 'self control', 'cognitive money',
        'คิด', 'ปัญญา', 'จิตวิทยา', 'ปรัชญา', 'หลักการ', 'แบบจำลองความคิด'
    ]
    for kw in r2_keywords:
        if kw in title or kw in source:
            score += 10
            
    # Rule 3: High-Signal Tech/AI shifts & new business opportunities
    r3_keywords = [
        'ai', 'agent', 'stablecoin', 'devtool', 'coding era', 'robot economy', 'automating'
    ]
    for kw in r3_keywords:
        if kw in title or kw in source:
            score += 12
            
    # Deprioritize/Penalize (Rule 4)
    # vlogs, daily news, transient politics, standard news, etc.
    deprio_keywords = [
        'vlog', 'reels', 'shorts', 'duckybhai', 'rain', 'cricket', 'village', 'match',
        'นิวเคลียร์', 'พระศพ', 'เจ้าฟ้า', 'สวนสัตว์', 'passport', 'พรรคประชาชน', 'ทองคำ',
        'เงินเฟ้อสหรัฐ', 'irpc', 'mercedes-benz', 'ทองดิ่ง', 'ราคาทอง', 'ผู้ไม่หวังดี',
        'พี่มิจ', 'ญาติ', 'ไรเดอร์', ' LGBTQ+'
    ]
    for kw in deprio_keywords:
        if kw in title or kw in source:
            score -= 20
            
    # Specific source adjustments
    if 'y combinator' in source:
        # YC is generally high-signal for business systems, entrepreneurship, and tech shifts.
        score += 5
    if 'the school of life' in source:
        # School of life has some psychology/philosophy, but sometimes relationship advice. Let's keep it moderate.
        score += 2
    if 'huberman lab' in source:
        # Practical science but deprioritize deeply academic ones.
        score += 2
        
    return score

scored_items = []
for item in data:
    score = get_score(item)
    scored_items.append((score, item))

scored_items.sort(key=lambda x: x[0], reverse=True)

outpath = r'D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\scratch\ranked_output.txt'
with open(outpath, 'w', encoding='utf-8') as f:
    for score, item in scored_items[:30]:
        f.write(f"Score: {score} | ID: {item['id']} | Source: {item['source']} | Title: {item['title']}\n")

print("Scored and ranked successfully")
