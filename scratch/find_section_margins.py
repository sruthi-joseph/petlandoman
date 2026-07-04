with open("style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line_num, line in enumerate(lines, 1):
    # Search for selectors that match footer or section or main or body
    if "margin" in line or "max-width" in line or "width" in line:
        # Print lines that define dimensions, margins, or widths for structural tags
        cleaned = line.strip()
        # look back 3 lines to see the selector
        selector = ""
        for i in range(max(0, line_num-4), line_num-1):
            selector += lines[i].strip() + " "
        print(f"Line {line_num}: Selector Context: {selector} => Code: {cleaned}")
