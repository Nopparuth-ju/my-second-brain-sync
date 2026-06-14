import json
import os

filepath = r'D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\.agents\IntelligenceCurator\temp_prioritize.json'
outpath = r'D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\scratch\filter_output.txt'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

lines = []
for x in data:
    title = x['title'].lower()
    source = x['source'].lower()
    
    keywords_rule1 = ['business', 'wealth', 'leverage', 'entrepreneur', 'system', 'money', 'financ', 'รวย', 'เงิน', 'ธุรกิจ', 'ลงทุน', 'หุ้นกู้', 'ประหยัด', 'หนี้', 'ภาษี', 'เกษียณ']
    keywords_rule2 = ['mental model', 'system thinking', 'first principles', 'psychology', 'philosophy', 'mindset', 'คิด', 'ปัญญา', 'จิตวิทยา', 'ปรัชญา']
    keywords_rule3 = ['ai', 'agent', 'stablecoin', 'robot', 'devtool', 'coding', 'automation', 'automate', 'tech']
    
    match1 = any(kw in title or kw in source for kw in keywords_rule1)
    match2 = any(kw in title or kw in source for kw in keywords_rule2)
    match3 = any(kw in title or kw in source for kw in keywords_rule3)
    
    if match1 or match2 or match3:
        lines.append(f"{x['id']} | {x['source']} | {x['title']}")

with open(outpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"Successfully wrote {len(lines)} lines to {outpath}")
