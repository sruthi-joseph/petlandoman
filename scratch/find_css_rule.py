with open(r"c:\Users\SRUTHI\Desktop\petland oman\style.css", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "hero-logo-overlay" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print 10 lines before and after
        start = max(0, idx - 5)
        end = min(len(lines), idx + 10)
        for i in range(start, end):
            print(f"  {i+1}: {lines[i].rstrip()}")
