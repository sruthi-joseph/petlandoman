with open("style.css", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Let's find all media query blocks: @media ... { ... }
# Note: media queries can have nested curly braces, so we need to parse them carefully
# Let's print any lines within @media blocks that mention body, footer, main-card, or container
matches = re.finditer(r'@media[^{]*\{', content)
for m in matches:
    start_idx = m.start()
    # Find matching closing brace
    brace_count = 1
    i = m.end()
    while i < len(content) and brace_count > 0:
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
        i += 1
    media_block = content[start_idx:i]
    
    # Check if this media block contains body, footer, or main-card
    if any(k in media_block for k in ["body", "footer", "main-card"]):
        print(f"\n=================== Media Query: {content[start_idx:m.end()].strip()} ===================")
        # print lines in the block that match
        for line in media_block.split('\n'):
            if any(k in line for k in ["body", "footer", "main-card", "margin", "padding"]):
                print("  " + line.strip())
