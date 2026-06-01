import os
import sys

# Reconfigure standard output to support UTF-8 (emojis and Thai characters) in Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WRITING_DIR = os.path.join(VAULT_ROOT, "05_OUTPUT", "Writing", "Daily Writing")

# Mapping of daily writing files to custom tags
TAGS_MAPPING = {
    "Day1 - การใช้ภาพเปรียบเทียบ (Analogy).md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/analogy #domain/communication",
    "Day2 - การโต้แย้งความเชื่อกระแสหลัก (Contrarian).md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/contrarian #domain/critical-thinking",
    "Day3 - การโน้มน้าวใจ (Persuasion).md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/persuasion #domain/philosophy",
    "Day4 - การตกผลึก (Synthesis).md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/synthesis #domain/productivity",
    "Day6 - บทความยาว.md": "#type/output #creator/me #status/practice #writing/daily #writing/essay #concept/writing-structure #domain/writing",
    "Day7 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/writing-structure #domain/writing",
    "Day8 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/critique #domain/psychology",
    "Day9 - Book Summary.md": "#type/output #creator/me #status/practice #writing/daily #writing/essay #concept/book-summary #domain/productivity",
    "Day10 - Short form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/storytelling #domain/philosophy",
    "Day11 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/happiness #domain/psychology",
    "Day12 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/feedback #domain/business",
    "Day13 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/2-minute-rule #domain/productivity",
    "Day14 - Short Form.md": "#type/output #creator/me #status/idea #writing/daily",
    "Day15 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/rest #domain/health",
    "Day16 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/discipline #domain/productivity",
    "Day17 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/analogy #domain/data-engineering",
    "Day18 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/focus #domain/neuroscience",
    "Day19 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/paradox-of-choice #domain/psychology",
    "Day20 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/procrastination #domain/psychology",
    "Day21 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/analogy #domain/data-engineering",
    "Day22 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/spotlight-effect #domain/psychology",
    "Day23 - Short Form.md": "#type/output #creator/me #status/practice #writing/daily #writing/short-form #concept/sunk-cost #domain/psychology",
    "Day24 - Short Form.md": "#type/output #creator/me #status/idea #writing/daily"
}

def inject_tags():
    print("🏷️ Starting Auto-Tagging Daily Writing notes...")
    updated_count = 0
    
    for filename, tags in TAGS_MAPPING.items():
        filepath = os.path.join(WRITING_DIR, filename)
        if not os.path.exists(filepath):
            # Try with case variations
            alt_filename = filename.replace("Short Form", "Short form") if "Short Form" in filename else filename.replace("Short form", "Short Form")
            filepath = os.path.join(WRITING_DIR, alt_filename)
            if not os.path.exists(filepath):
                print(f"   ⚠️ File not found: {filename}")
                continue
        
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                content = f.read()
        except Exception:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
        lines = content.split('\n')
        # Check if first line already has tags
        if lines and lines[0].startswith('#type/'):
            lines[0] = tags
            new_content = '\n'.join(lines)
        else:
            new_content = tags + '\n\n' + content
            
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            f.write(new_content)
        print(f"   ✅ Tagged: {os.path.basename(filepath)}")
        updated_count += 1
        
    print(f"\n🎉 Successfully tagged {updated_count} daily writing practice files in UTF-8 with BOM format!")

if __name__ == '__main__':
    inject_tags()
