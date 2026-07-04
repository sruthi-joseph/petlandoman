with open(r"c:\Users\SRUTHI\Desktop\petland oman\style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(2210, len(lines)):
    line = lines[idx]
    if "color" in line:
        print(f"Line {idx+1}: {line.strip()}")
