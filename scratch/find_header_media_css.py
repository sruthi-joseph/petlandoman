with open(r"c:\Users\SRUTHI\Desktop\petland oman\style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_media_query = False
for idx, line in enumerate(lines):
    if "@media" in line:
        in_media_query = True
    if in_media_query and "header" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print 10 lines
        for i in range(idx, min(len(lines), idx + 15)):
            print(f"  {i+1}: {lines[i].rstrip()}")
