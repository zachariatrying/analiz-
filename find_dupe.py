lines = open('src/analyzer.py', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'def detect_flag_pattern' in line:
        print(f"Found at line {i+1}: {line.strip()}")

