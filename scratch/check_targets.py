import json
import sys

filepath = r'D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\.agents\IntelligenceCurator\temp_prioritize.json'
outpath = r'D:\Boss\3) Hobby\3.13) AI\AI Agent\Second Brain\My Second Brain Sync\scratch\targets_output.txt'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

targets = ['yt_sNz4k5BQg30', 'yt_L7xvwsg7WA8', 'yt_J82zFDyYck0', 'yt_zpCWFhEv_EI', 'yt_A5oYUQ-pmQQ', 'yt_XImly72tLw0', 'yt_jikOaczZxTY', 'yt_1egwM88T3C0', 'yt__y7siiS-V5A', 'yt_RMmEB9ajmdo', 'yt_4L4x67B8N-M', 'yt_CTHFBXULU7o']

lines = []
for item in data:
    if item['id'] in targets:
        lines.append(f"ID: {item['id']} | Source: {item['source']} | Title: {item['title']}")

with open(outpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print("Wrote targets successfully")
