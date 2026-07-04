with open(r"c:\Users\SRUTHI\Desktop\petland oman\style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "@media (max-width: 768px)" in line or "background: rgba(0, 0, 0, 0.95);" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print 5 lines before and after
        start = max(0, idx - 5)
        end = min(len(lines), idx + 10)
        for i in range(start, end):
            print(f"  [{i+1}] {lines[i].strip()}")
