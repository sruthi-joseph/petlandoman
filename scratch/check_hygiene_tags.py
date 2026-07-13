import re

with open("hygiene.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

tags = ["div", "section", "header", "footer", "body", "html", "ul", "li", "nav", "a"]
counts = {t: {"open": 0, "close": 0} for t in tags}

for line_num, line in enumerate(lines, 1):
    for tag in tags:
        # Match opening tags, excluding self-closing or scripts/comments
        open_matches = re.findall(rf'<\s*{tag}\b[^>]*>', line, re.IGNORECASE)
        # Match closing tags
        close_matches = re.findall(rf'<\s*/\s*{tag}\b[^>]*>', line, re.IGNORECASE)
        
        counts[tag]["open"] += len(open_matches)
        counts[tag]["close"] += len(close_matches)

print("HTML Structural Tag Counts for hygiene.html:")
all_balanced = True
for tag, count in counts.items():
    diff = count["open"] - count["close"]
    status = "BALANCED" if diff == 0 else "MISMATCHED"
    print(f"  <{tag}>: open={count['open']}, close={count['close']} (diff={diff}) -> {status}")
    if diff != 0:
        all_balanced = False

if all_balanced:
    print("\nSUCCESS: All structural HTML tags are balanced!")
else:
    print("\nWARNING: Some structural HTML tags are mismatched. Please inspect.")
