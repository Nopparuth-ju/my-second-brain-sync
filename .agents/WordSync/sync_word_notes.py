import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import shutil
import hashlib
import json
import re

# Reconfigure standard output to support UTF-8 (emojis and Thai characters) in Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass # Support Python versions without reconfigure

# Directories configuration - Resides in .agents/WordSync/ so we go 3 levels up to reach Vault Root
VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INBOX_DIR = os.path.join(VAULT_ROOT, "01_INBOX", "WORK_KNOWLEDGE")
TARGET_DIR = os.path.join(VAULT_ROOT, "02_SOURCE", "WORK_KNOWLEDGE")
ATTACHMENTS_DIR = os.path.join(TARGET_DIR, "attachments")
STATE_FILE = os.path.join(VAULT_ROOT, ".agents", "word_sync_state.json")

# Namespace mapping for Word XML documents
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'v': 'urn:schemas-microsoft-com:vml'
}

def get_md5(file_path):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_state():
    """Load sync state database."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read state database: {e}. Starting fresh.")
    return {}

def save_state(state):
    """Save sync state database."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

def extract_docx_media(docx_path, file_base_name):
    """Extract embedded images from docx and map relation IDs."""
    image_mapping = {}
    
    if not zipfile.is_zipfile(docx_path):
        return image_mapping

    with zipfile.ZipFile(docx_path) as z:
        # 1. Parse Relationships to map rId to media file names
        rels_xml = ""
        try:
            rels_xml = z.read("word/_rels/document.xml.rels")
        except KeyError:
            return image_mapping # No relationships found

        root = ET.fromstring(rels_xml)
        rId_to_target = {}
        for elem in root.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
            r_id = elem.get('Id')
            r_type = elem.get('Type')
            r_target = elem.get('Target')
            
            if "relationships/image" in r_type:
                rId_to_target[r_id] = r_target.split('/')[-1]

        # 2. Extract and rename the images
        os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
        img_counter = 1
        
        for r_id, media_name in rId_to_target.items():
            zip_image_path = f"word/media/{media_name}"
            try:
                img_data = z.read(zip_image_path)
                
                # Clean up filename for security and formatting
                safe_name = re.sub(r'[\s/\\?%*:|"<>#]', '_', file_base_name)
                
                # Attempt to convert to highly compressed WebP format using Pillow
                try:
                    from PIL import Image
                    import io
                    img = Image.open(io.BytesIO(img_data))
                    new_image_name = f"{safe_name}-img{img_counter}.webp"
                    target_image_path = os.path.join(ATTACHMENTS_DIR, new_image_name)
                    img.save(target_image_path, "WEBP", quality=80)
                except Exception as e:
                    # Fallback to saving original format if conversion fails
                    ext = media_name.split('.')[-1] if '.' in media_name else 'png'
                    new_image_name = f"{safe_name}-img{img_counter}.{ext}"
                    target_image_path = os.path.join(ATTACHMENTS_DIR, new_image_name)
                    with open(target_image_path, "wb") as img_file:
                        img_file.write(img_data)
                
                image_mapping[r_id] = new_image_name
                img_counter += 1
            except KeyError:
                print(f"Warning: Media file {zip_image_path} not found in zip package.")
                
    return image_mapping

def convert_docx_to_md(docx_path, output_md_path, file_base_name):
    """Converts a DOCX file to clean Markdown and links extracted images."""
    image_mapping = extract_docx_media(docx_path, file_base_name)
    
    if not zipfile.is_zipfile(docx_path):
        return False
        
    with zipfile.ZipFile(docx_path) as z:
        try:
            doc_xml = z.read("word/document.xml")
        except KeyError:
            print(f"Error: word/document.xml not found in {docx_path}")
            return False
            
        root = ET.fromstring(doc_xml)
        
        md_lines = []
        
        # Parse XML tags recursively to extract paragraphs, headings, lists, bold, italics, and drawings
        for paragraph in root.findall('.//w:p', NAMESPACES):
            # Check for Heading Style
            p_style = paragraph.find('.//w:pStyle', NAMESPACES)
            style_val = p_style.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if p_style is not None else ""
            
            prefix = ""
            if style_val:
                if "heading1" in style_val.lower(): prefix = "# "
                elif "heading2" in style_val.lower(): prefix = "## "
                elif "heading3" in style_val.lower(): prefix = "### "
                elif "heading4" in style_val.lower(): prefix = "#### "
                
            # Check for List Items
            num_pr = paragraph.find('.//w:numPr', NAMESPACES)
            if num_pr is not None and not prefix:
                prefix = "- "
            
            p_text_parts = []
            
            # Process all text runs inside paragraph
            for child in paragraph:
                # Runs contain both text and drawings/images
                if child.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r':
                    text_elem = child.find('w:t', NAMESPACES)
                    if text_elem is not None and text_elem.text:
                        text = text_elem.text
                        
                        # Style formatting (Bold / Italic)
                        r_pr = child.find('w:rPr', NAMESPACES)
                        if r_pr is not None:
                            is_bold = r_pr.find('w:b', NAMESPACES) is not None
                            is_italic = r_pr.find('w:i', NAMESPACES) is not None
                            if is_bold and is_italic:
                                text = f"***{text}***"
                            elif is_bold:
                                text = f"**{text}**"
                            elif is_italic:
                                text = f"*{text}*"
                        p_text_parts.append(text)
                    
                    # 1. Search for drawings nested INSIDE the run recursively!
                    drawings = child.findall('.//w:drawing', NAMESPACES)
                    for drawing in drawings:
                        for blip in drawing.findall('.//a:blip', NAMESPACES):
                            embed_id = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                            if embed_id and embed_id in image_mapping:
                                p_text_parts.append(f"\n\n![[{image_mapping[embed_id]}]]\n\n")
                                
                    # 2. Search for VML legacy images nested INSIDE the run recursively!
                    vml_images = child.findall('.//v:imagedata', NAMESPACES)
                    for img_data in vml_images:
                        r_id = img_data.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                        if r_id and r_id in image_mapping:
                            p_text_parts.append(f"\n\n![[{image_mapping[r_id]}]]\n\n")
                            
            full_p_text = "".join(p_text_parts).strip()
            if full_p_text:
                md_lines.append(f"{prefix}{full_p_text}")
            elif prefix == "- ":
                md_lines.append(prefix)
                
        # Format markdown body cleanly
        markdown_content = f"#type/source\n#status/processed\n#domain/work-knowledge\n#creator/me\n\n"
        markdown_content += "\n\n".join(md_lines)
        
        # Write to target file in UTF-8 with BOM format!
        os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
        with open(output_md_path, "w", encoding="utf-8-sig") as f:
            f.write(markdown_content)
            
    return True

def sync_pipeline():
    """Main execution pipeline."""
    if not os.path.exists(INBOX_DIR):
        print("Inbox folder 01_INBOX/WORK_KNOWLEDGE is empty. Nothing to sync.")
        return

    print("🚀 Scanning inbox for Word notes...", flush=True)
    state = load_state()
    files_processed = 0
    files_skipped = 0
    
    # Recursively scan INBOX_DIR for .docx files
    for root_dir, dirs, files in os.walk(INBOX_DIR):
        for file in files:
            if not file.endswith(".docx") or file.startswith("~$"):
                continue # Skip temp or non-word files
                
            docx_path = os.path.join(root_dir, file)
            
            # Find path relative to INBOX_DIR to preserve nested subfolder structure!
            rel_path = os.path.relpath(docx_path, INBOX_DIR)
            rel_dir = os.path.dirname(rel_path)
            
            file_base_name = file.replace(".docx", "")
            
            # Determine target markdown path
            output_md_name = f"{file_base_name}.md"
            output_md_path = os.path.join(TARGET_DIR, rel_dir, output_md_name)
            
            # Calculate file metadata for tracking changes
            mtime = os.path.getmtime(docx_path)
            file_hash = get_md5(docx_path)
            
            state_key = rel_path.replace("\\", "/")
            
            # Sync Decision making using State DB
            is_new = state_key not in state
            is_modified = not is_new and (state[state_key]["mtime"] != mtime or state[state_key]["hash"] != file_hash)
            
            if is_new or is_modified:
                status_str = "NEW" if is_new else "MODIFIED"
                print(f"📝 [{status_str}] Converting: {state_key} -> {rel_dir}/{output_md_name}...", flush=True)
                
                success = convert_docx_to_md(docx_path, output_md_path, file_base_name)
                
                if success:
                    # Update State Database
                    state[state_key] = {
                        "mtime": mtime,
                        "hash": file_hash,
                        "converted_path": os.path.relpath(output_md_path, VAULT_ROOT).replace("\\", "/")
                    }
                    files_processed += 1
                else:
                    print(f"❌ Failed to convert {file}")
            else:
                files_skipped += 1
                
    # Save the updated database state
    save_state(state)
    
    print(f"\n🎉 Sync completed successfully!")
    print(f"   - Converted/Updated: {files_processed} files")
    print(f"   - Skipped (Unchanged): {files_skipped} files")
    
    # Clean up 01_INBOX/WORK_KNOWLEDGE directory (Inbox Zero!)
    print("\n🧹 Cleaning up inbox landing pad...", flush=True)
    
    def remove_readonly(func, path, excinfo):
        import stat
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception:
            pass # Ignore failures to delete minor transient files
            
    try:
        # Clear contents of WORK_KNOWLEDGE instead of deleting the directory itself
        for item in os.listdir(INBOX_DIR):
            item_path = os.path.join(INBOX_DIR, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path, onerror=remove_readonly)
            else:
                try:
                    import stat
                    os.chmod(item_path, stat.S_IWRITE)
                    os.remove(item_path)
                except Exception:
                    pass
        print("   - Inbox cleared to Zero successfully (kept WORK_KNOWLEDGE folder).")
    except Exception as e:
        print(f"   - Warning: Could not clear inbox: {e}")

if __name__ == "__main__":
    sync_pipeline()
