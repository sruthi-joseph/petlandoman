with open(r"c:\Users\SRUTHI\Desktop\petland oman\style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "toggle" in line or "header" in line or "nav" in line:
        # print line and line number (1-based)
        print(f"Line {idx+1}: {line.strip()}")
