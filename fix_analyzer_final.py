import os

file_path = 'src/analyzer.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_mode = False
skip_call_block = False

for i, line in enumerate(lines):
    # 1. Detect Legacy Method Start
    if "def detect_rsi_divergence(self, df, window=5):" in line:
        skip_mode = True
        print(f"Started removing legacy method at line {i+1}")
        continue
    
    # 2. Detect Legacy Method End (Start of next method)
    if skip_mode:
        if "def get_detailed_signals(self, df):" in line:
            skip_mode = False
            print(f"Ended removing legacy method at line {i+1}")
            new_lines.append(line) # Add the next method definition
        continue

    # 3. Detect Legacy Call Block in detect_patterns
    # We want to remove the comment block and the call
    stripped = line.strip()
    if stripped == "# RSI DIVERGENCE":
        # Check surrounding lines to be sure it's the block we want
        # The block usually has dashes above/below
        skip_call_block = True 
        continue
    
    if skip_call_block:
        if "divergences = self.detect_rsi_divergence(df)" in line:
            continue
        if "patterns.extend(divergences)" in line:
            skip_call_block = False # End of block
            print(f"Removed legacy call block around line {i+1}")
            continue
        # Also remove dashed lines or empty lines in this immediate block
        if "---" in line or stripped == "":
            continue
            
    # Safety: If we are not skipping, append
    if not skip_call_block:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Finished cleaning analyzer.py")

