import os
import re

TARGET_DIR = r"C:\Users\ibrah\.gemini\antigravity\scratch\ipo_analyzer\src"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match st.markdown("""...<style>...</style>...""", unsafe_allow_html=True)
    pattern = re.compile(r'st\.markdown\(\s*(?:f?)[\'"]{3}\s*<style>.*?</style>\s*[\'"]{3},\s*unsafe_allow_html=True\)', re.DOTALL)
    
    if not pattern.search(content):
        return False
        
    # The import logic: if it's in pages/, we still import from src.theme because we run the app from ipo_analyzer dir!
    # Wait, when running `streamlit run src/app.py`, `src` is in the path. `from src.theme` works.
    replacement = "from src.theme import CSS_STYLE\nst.markdown(CSS_STYLE, unsafe_allow_html=True)"
    new_content = pattern.sub(replacement, content)
    
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
