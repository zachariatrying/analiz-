import os
import re

TARGET_DIR = r"C:\Users\ibrah\.gemini\antigravity\scratch\ipo_analyzer\src"

safe_import = """import sys
import os
curr_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(curr_dir)
if curr_dir not in sys.path: sys.path.append(curr_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)
try:
    from src.theme import CSS_STYLE
except ImportError:
    from theme import CSS_STYLE

st.markdown(CSS_STYLE, unsafe_allow_html=True)"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = re.compile(r'from src\.theme import CSS_STYLE\s*st\.markdown\(CSS_STYLE, unsafe_allow_html=True\)', re.DOTALL)
    
    if not pattern.search(content):
        return False
        
    new_content = pattern.sub(safe_import, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

changed = 0
for root, _, files in os.walk(TARGET_DIR):
    for f in files:
        if f.endswith('.py') and f != "theme.py":
            filepath = os.path.join(root, f)
            if process_file(filepath):
                print(f"Updated {f}")
                changed += 1

print(f"Total files updated: {changed}")
