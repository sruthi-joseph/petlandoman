import re

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Let's count opening and closing tags for main structural elements: div, section, header, footer, body, html
tags = ["div", "section", "header", "footer", "body", "html", "ul", "li", "nav"]

counts = {t: {"open": 0, "close": 0} for t in tags}

for line_num, line in enumerate(lines, 1):
    # Find all opening tags like <div ...> (excluding self-closing or comments)
    # We will use simple regexes
    for tag in tags:
        # Opening tags: <tag or <tag> (but not </tag>)
        open_matches = re.findall(rf'<\s*{tag}\b[^>]*>', line, re.IGNORECASE)
        # Closing tags: </tag>
        close_matches = re.findall(rf'<\s*/\s*{tag}\b[^>]*>', line, re.IGNORECASE)
        
        counts[tag]["open"] += len(open_matches)
        counts[tag]["close"] += len(close_matches)
        
        if len(open_matches) != len(close_matches):
            # Print lines with tag mismatches to help inspect
            pass

print("HTML Structural Tag Counts:")
for tag, count in counts.items():
    diff = count["open"] - count["close"]
    print(f"  <{tag}>: open={count['open']}, close={count['close']} (diff={diff})")
