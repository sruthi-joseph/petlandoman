with open("style.css", "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        if "calc(100%" in line:
            print(f"Line {line_num}: {line.strip()}")
