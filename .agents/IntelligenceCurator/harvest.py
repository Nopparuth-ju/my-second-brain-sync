import os
import sys
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import re
import subprocess
import html

# Reconfigure standard output to support UTF-8 (emojis and Thai characters) in Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass # Support Python versions without reconfigure

# Directory configuration
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.dirname(os.path.dirname(CUR_DIR))
SOURCES_CONFIG_PATH = os.path.join(CUR_DIR, "intelligence_sources.json")
STATE_PATH = os.path.join(CUR_DIR, "processed_sources.json")

# Standard HTTP headers to prevent 403 Forbidden
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_url_content(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read()
    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}", file=sys.stderr)
        return None

def clean_html_text(html_bytes):
    try:
        html_str = html_bytes.decode('utf-8', errors='ignore')
    except Exception:
        return ""
    
    # Remove script and style elements
    html_str = re.sub(r'<script.*?>.*?</script>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
    html_str = re.sub(r'<style.*?>.*?</style>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
    
    # Find all paragraph tags
    paragraphs = re.findall(r'<p.*?>(.*?)</p>', html_str, flags=re.DOTALL | re.IGNORECASE)
    if paragraphs:
        # Strip internal tags and unescape HTML entities
        text_list = []
        for p in paragraphs:
            cleaned = re.sub(r'<.*?>', '', p)
            cleaned = html.unescape(cleaned).strip()
            if cleaned:
                text_list.append(cleaned)
        text = "\n\n".join(text_list)
    else:
        # Fallback: remove all HTML tags and unescape
        cleaned = re.sub(r'<.*?>', '', html_str)
        text = html.unescape(cleaned).strip()
        # Compress blank lines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
    return text

def parse_youtube_feed(channel_name, channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    print(f"📺 Scanning YouTube Channel: {channel_name}...")
    xml_data = fetch_url_content(url)
    if not xml_data:
        return []
    
    entries = []
    try:
        root = ET.fromstring(xml_data)
        # XML Namespaces
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'yt': 'http://www.youtube.com/xml/schemas/2015'
        }
        
        # YouTube feeds use Atom standard
        for entry in root.findall('atom:entry', ns):
            video_id_elem = entry.find('yt:videoId', ns)
            title_elem = entry.find('atom:title', ns)
            link_elem = entry.find('atom:link', ns)
            
            if video_id_elem is not None and title_elem is not None:
                video_id = video_id_elem.text
                title = title_elem.text
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                entries.append({
                    'type': 'youtube',
                    'id': f"yt_{video_id}",
                    'title': title,
                    'url': video_url,
                    'source': channel_name
                })
    except Exception as e:
        print(f"⚠️ XML Parse Error for YouTube channel {channel_name}: {e}", file=sys.stderr)
        
    return entries

def parse_rss_feed(feed_name, feed_url):
    print(f"📰 Scanning RSS Feed: {feed_name}...")
    xml_data = fetch_url_content(feed_url)
    if not xml_data:
        return []
    
    entries = []
    try:
        root = ET.fromstring(xml_data)
        # Support RSS 2.0 structure
        channel = root.find('channel')
        if channel is not None:
            for item in channel.findall('item'):
                title_elem = item.find('title')
                link_elem = item.find('link')
                guid_elem = item.find('guid')
                
                if title_elem is not None and link_elem is not None:
                    title = title_elem.text
                    link = link_elem.text
                    # Use GUID if present, otherwise fallback to URL
                    item_id = guid_elem.text if guid_elem is not None else link
                    # Clean ID to prevent special char problems
                    clean_id = re.sub(r'[^a-zA-Z0-9]', '_', item_id)
                    
                    entries.append({
                        'type': 'rss',
                        'id': f"rss_{clean_id[:50]}",
                        'title': title,
                        'url': link,
                        'source': feed_name
                    })
    except Exception as e:
        print(f"⚠️ XML Parse Error for RSS {feed_name}: {e}", file=sys.stderr)
        
    return entries

def process_youtube_entry(entry):
    print(f"\n🎥 [NEW VIDEO FOUND]: {entry['title']} ({entry['source']})")
    print(f"🔗 URL: {entry['url']}")
    
    # 1. Fetch transcript using get_youtube_transcript.py
    yt_manager_dir = os.path.join(VAULT_ROOT, ".agents", "YouTubeManager")
    script_path = os.path.join(yt_manager_dir, "get_youtube_transcript.py")
    temp_transcript = os.path.join(yt_manager_dir, "temp_transcript.txt")
    
    # Clean up existing temp transcript if any
    if os.path.exists(temp_transcript):
        os.remove(temp_transcript)
        
    print("⏳ Step 1: Downloading transcript...")
    res = subprocess.run([sys.executable, script_path, entry['url']], capture_output=True, text=True, cwd=yt_manager_dir)
    
    if not os.path.exists(temp_transcript):
        print(f"❌ Failed to get transcript for {entry['title']}. Error:\n{res.stderr}")
        return False
        
    # 2. Invoke agy AI Agent to distill the video content
    print("⏳ Step 2: Running YouTube Multi-Agent Pipeline via AI Agent...")
    prompt = (
        "ให้อ่านกฎและทักษะจากไฟล์ .agents/YouTubeManager/skill.md และ .agents/YouTubeManager/instruction.md ก่อน "
        "รวมถึงวิเคราะห์ตามหน้าที่ของลูกทีมย่อยจาก .agents/YouTubeManager/Summarizer.md, .agents/YouTubeManager/Contrarian.md "
        f"และ .agents/YouTubeManager/Verifier.md จากนั้นอ่านบทถอดความจากวิดีโอ (Transcript) ในไฟล์ .agents/YouTubeManager/temp_transcript.txt "
        f"อ้างอิงลิงก์ YouTube {entry['url']} ช่วยประมวลผลสร้างเฉพาะโน้ตสรุปภาพรวมความเห็นต่างและข้อเท็จจริง 1 ไฟล์เซฟลงใน 02_SOURCE/CURATED_FEEDS เท่านั้น "
        "(ไม่ต้องสร้างไฟล์ใน 03_ZETTEL) โดยระบุที่มาอย่างถูกต้องและตั้งชื่อไฟล์ตามแก่นของเนื้อหา"
    )
    
    # Run agy CLI tool
    res = subprocess.run(["agy", "-p", prompt], capture_output=True, text=True)
    if res.returncode == 0:
        print("✅ Success: Distilled summary generated and saved directly to 02_SOURCE/CURATED_FEEDS!")
        # Clean up
        if os.path.exists(temp_transcript):
            os.remove(temp_transcript)
        return True
    else:
        print(f"❌ Error invoking agy: {res.stderr}")
        return False

def process_rss_entry(entry):
    print(f"\n📰 [NEW ARTICLE FOUND]: {entry['title']} ({entry['source']})")
    print(f"🔗 URL: {entry['url']}")
    
    # 1. Fetch and clean HTML content
    print("⏳ Step 1: Downloading and cleaning article content...")
    raw_content = fetch_url_content(entry['url'])
    if not raw_content:
        print("❌ Failed to download article content.")
        return False
        
    cleaned_text = clean_html_text(raw_content)
    if not cleaned_text:
        print("❌ Article content is empty after cleaning HTML.")
        return False
        
    # Save to temp file
    temp_article_path = os.path.join(CUR_DIR, "temp_article.txt")
    with open(temp_article_path, "w", encoding="utf-8") as f:
        f.write(f"Title: {entry['title']}\nSource: {entry['source']}\nURL: {entry['url']}\n\n{cleaned_text}")
        
    # 2. Invoke agy AI Agent to distill the article content
    print("⏳ Step 2: Invoking AI Distiller Agent...")
    prompt = (
        "ให้อ่านกฎและทักษะจากไฟล์ .agents/Distiller/skill.md และ .agents/Distiller/instruction.md ก่อน "
        f"จากนั้นอ่านข้อมูลบทความเนื้อหาที่เซฟไว้ในไฟล์ .agents/IntelligenceCurator/temp_article.txt อ้างอิงแหล่งที่มาจาก URL {entry['url']} "
        "ช่วยประมวลผลสกัดความรู้อ่านแล้วเขียนสรุปภาพรวมทั้งหมด 1 ไฟล์เซฟไว้ที่ 02_SOURCE/CURATED_FEEDS อย่างเดียวเท่านั้น (ไม่ต้องสร้างไฟล์ใน 03_ZETTEL) "
        "และตั้งชื่อไฟล์สรุปตามแก่นเรื่องเป็นภาษาไทยอย่างสวยงามและน่าอ่านเป็นระบบ"
    )
    
    res = subprocess.run(["agy", "-p", prompt], capture_output=True, text=True)
    if res.returncode == 0:
        print("✅ Success: Distilled summary generated and saved directly to 02_SOURCE/CURATED_FEEDS!")
        # Clean up
        if os.path.exists(temp_article_path):
            os.remove(temp_article_path)
        return True
    else:
        print(f"❌ Error invoking agy: {res.stderr}")
        # Clean up
        if os.path.exists(temp_article_path):
            os.remove(temp_article_path)
        return False

def main():
    print("🚀 --- starting Personal AI Intelligence Curator Engine ---")
    
    # Ensure CURATED_FEEDS directory exists
    os.makedirs(os.path.join(VAULT_ROOT, "02_SOURCE", "CURATED_FEEDS"), exist_ok=True)
    
    # Load settings and processed state
    config = load_json(SOURCES_CONFIG_PATH)
    state = load_json(STATE_PATH)
    processed_ids = set(state.get("processed_ids", []))
    
    new_entries = []
    
    # 1. Parse YouTube feeds
    for ch in config.get("youtube_channels", []):
        try:
            entries = parse_youtube_feed(ch["name"], ch["channel_id"])
            for entry in entries:
                if entry["id"] not in processed_ids:
                    new_entries.append(entry)
        except Exception as e:
            print(f"⚠️ Failed to scan channel {ch.get('name')}: {e}", file=sys.stderr)
            
    # 2. Parse RSS feeds
    for f in config.get("rss_feeds", []):
        try:
            entries = parse_rss_feed(f["name"], f["url"])
            for entry in entries:
                if entry["id"] not in processed_ids:
                    new_entries.append(entry)
        except Exception as e:
            print(f"⚠️ Failed to scan feed {f.get('name')}: {e}", file=sys.stderr)
            
    print(f"\n📊 Total new items discovered: {len(new_entries)}")
    
    if not new_entries:
        print("✅ No new content. Your Second Brain is fully up-to-date!")
        sys.exit(0)
        
    # Process new entries (limit to 3 per run to prevent token/quota overload, can be adjusted)
    processed_count = 0
    max_process = 5
    
    for entry in new_entries:
        if processed_count >= max_process:
            print(f"\n⚠️ Reached limit of {max_process} processed items per run. Remaining items will be processed in the next run.")
            break
            
        success = False
        if entry["type"] == "youtube":
            success = process_youtube_entry(entry)
        elif entry["type"] == "rss":
            success = process_rss_entry(entry)
            
        if success:
            processed_ids.add(entry["id"])
            processed_count += 1
            # Save state incrementally to ensure progress is saved in case of failure
            state["processed_ids"] = list(processed_ids)
            save_json(STATE_PATH, state)
            
    print(f"\n🎉 Successfully processed and distilled {processed_count} new entries!")

if __name__ == "__main__":
    main()
