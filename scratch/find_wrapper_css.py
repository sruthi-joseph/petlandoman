with open(r"c:\Users\SRUTHI\Desktop\petland oman\style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "sticky-canvas-wrapper" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print 10 lines
        for i in range(idx, min(len(lines), idx + 10)):
            print(f"  {i+1}: {lines[i].rstrip()}")
