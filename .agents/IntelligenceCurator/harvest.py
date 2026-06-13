import os
import sys
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import re
import subprocess
import html
import datetime

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
        
        items = []
        # Support RSS 2.0 structure
        channel = root.find('channel')
        if channel is not None:
            items = channel.findall('item')
        else:
            # Support Atom feeds (used by some blogs like Substack, LessWrong)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            items = root.findall('atom:entry', ns)
        
        for item in items:
            # RSS uses <title>, <link>, <guid>; Atom uses <title>, <link href="...">, <id>
            title_elem = item.find('title') or item.find('{http://www.w3.org/2005/Atom}title')
            link_elem = item.find('link') or item.find('{http://www.w3.org/2005/Atom}link')
            guid_elem = item.find('guid') or item.find('{http://www.w3.org/2005/Atom}id')
            
            if title_elem is not None and link_elem is not None:
                title = title_elem.text
                # Atom <link> stores URL in href attribute, RSS stores it as text
                link = link_elem.get('href') or link_elem.text
                if not title or not link:
                    continue
                # Use GUID if present, otherwise fallback to URL
                item_id = (guid_elem.text if guid_elem is not None and guid_elem.text else link)
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
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    prompt = (
        "Read the rules and skills from .agents/YouTubeManager/skill.md and .agents/YouTubeManager/instruction.md first. "
        "Also analyze based on the roles of sub-agents in .agents/YouTubeManager/Summarizer.md, .agents/YouTubeManager/Contrarian.md, "
        "and .agents/YouTubeManager/Verifier.md. Then read the video transcript in .agents/YouTubeManager/temp_transcript.txt. "
        f"Referencing the YouTube link {entry['url']}, process and generate exactly 1 summary note under 02_SOURCE/CURATED_FEEDS/{today_str}/ only "
        f"(do NOT create files in 03_ZETTEL). You MUST fill the 'Analysis Date' template field with '{today_str}' directly under the source link. "
        "Name the summary file beautifully in Thai based on the core thesis of the content."
    )
    
    # Run agy CLI tool
    res = subprocess.run(["agy", "--dangerously-skip-permissions", "-p", prompt], capture_output=True, text=True)
    if res.returncode == 0:
        print("✅ Success: Distilled summary generated and saved directly to 02_SOURCE/CURATED_FEEDS!")
        # Clean up
        if os.path.exists(temp_transcript):
            os.remove(temp_transcript)
        return True
    else:
        print(f"❌ Error invoking agy: {res.stderr}")
        # Clean up transcript on failure too
        if os.path.exists(temp_transcript):
            os.remove(temp_transcript)
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
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    prompt = (
        "Read the rules and skills from .agents/Distiller/skill.md and .agents/Distiller/instruction.md first. "
        f"Then read the article content stored in .agents/IntelligenceCurator/temp_article.txt referencing URL {entry['url']}. "
        f"Process and extract the core knowledge into exactly 1 summary note under 02_SOURCE/CURATED_FEEDS/{today_str}/ only "
        f"(do NOT create files in 03_ZETTEL). You MUST fill the 'Analysis Date' template field with '{today_str}' directly under the source link. "
        "Name the summary file beautifully in Thai based on the core thesis of the content."
    )
    
    res = subprocess.run(["agy", "--dangerously-skip-permissions", "-p", prompt], capture_output=True, text=True)
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

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-process', type=int, default=3, help='Maximum number of items to process')
    args = parser.parse_args()
    
    print("=========================================================")
    print("  🧠 Personal AI Intelligence Curator Engine 🧠")
    
    # Ensure CURATED_FEEDS directory and today's subfolder exists
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    curated_feeds_dir = os.path.join(VAULT_ROOT, "02_SOURCE", "CURATED_FEEDS")
    os.makedirs(os.path.join(curated_feeds_dir, today_str), exist_ok=True)
    
    # Extract all processed URLs from existing markdown files to prevent any duplicates
    processed_urls = set()
    for root_dir, _, files in os.walk(curated_feeds_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Find all URLs in the file
                        urls = re.findall(r'https?://[^\s)\]"\']+', content)
                        processed_urls.update(urls)
                except Exception:
                    pass
    
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
                if entry["id"] not in processed_ids and entry["url"] not in processed_urls:
                    new_entries.append(entry)
        except Exception as e:
            print(f"⚠️ Failed to scan channel {ch.get('name')}: {e}", file=sys.stderr)
            
    # 2. Parse RSS feeds
    for f in config.get("rss_feeds", []):
        try:
            entries = parse_rss_feed(f["name"], f["url"])
            for entry in entries:
                if entry["id"] not in processed_ids and entry["url"] not in processed_urls:
                    new_entries.append(entry)
        except Exception as e:
            print(f"⚠️ Failed to scan feed {f.get('name')}: {e}", file=sys.stderr)
            
    print(f"\n📊 Total new items discovered: {len(new_entries)}")
    
    if not new_entries:
        print("✅ No new content. Your Second Brain is fully up-to-date!")
        sys.exit(0)
        
    max_process = args.max_process
    
    # Prioritization Step via AI
    if len(new_entries) > max_process:
        print(f"⏳ Discovered {len(new_entries)} items, which exceeds the quota of {max_process}.")
        print("🧠 Invoking Prioritizer Agent to select the most Timeless & High-Signal content...")
        
        # Prepare data for AI
        prioritize_data = [{"id": e["id"], "title": e["title"], "source": e["source"]} for e in new_entries]
        temp_prioritize_path = os.path.join(CUR_DIR, "temp_prioritize.json")
        save_json(temp_prioritize_path, prioritize_data)
        
        prioritized_ids_path = os.path.join(CUR_DIR, "prioritized_ids.json")
        if os.path.exists(prioritized_ids_path):
            os.remove(prioritized_ids_path)
            
        prompt = (
            "Read the rules and skills from .agents/Prioritizer/skill.md and .agents/Prioritizer/instruction.md first. "
            f"Here is the list of items in .agents/IntelligenceCurator/temp_prioritize.json. "
            f"Select exactly the top {max_process} items. Save the final JSON array of their IDs to '.agents/IntelligenceCurator/prioritized_ids.json' using your file writing tool. Do not just print it."
        )
        
        res = subprocess.run(["agy", "--dangerously-skip-permissions", "-p", prompt], capture_output=False)
        if res.returncode == 0:
            try:
                if not os.path.exists(prioritized_ids_path):
                    raise ValueError("Prioritizer Agent failed to create prioritized_ids.json")
                    
                selected_ids = set(load_json(prioritized_ids_path))
                if not selected_ids:
                    raise ValueError("prioritized_ids.json is empty or invalid")
                    
                new_entries = [e for e in new_entries if e["id"] in selected_ids]
                print(f"✅ Prioritization complete! Selected {len(new_entries)} items.")
                os.remove(prioritized_ids_path)
            except Exception as e:
                print(f"⚠️ Failed to parse Prioritizer output. Falling back to standard slicing. Error: {e}")
                new_entries = new_entries[:max_process]
        else:
            print(f"⚠️ Prioritizer Agent failed. Falling back to standard slicing.")
            new_entries = new_entries[:max_process]
            
        if os.path.exists(temp_prioritize_path):
            os.remove(temp_prioritize_path)
    else:
        new_entries = new_entries[:max_process]
        
    processed_count = 0
    
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
            state["last_updated"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_json(STATE_PATH, state)
            
    print(f"\n🎉 Successfully processed and distilled {processed_count} new entries!")

if __name__ == "__main__":
    main()
