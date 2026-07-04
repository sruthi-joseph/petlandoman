with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's parse the HTML step by step and track active tags
# We will check if the footer starts while other divs or sections are still open
import re

# Simple HTML parser
tag_pattern = re.compile(r'<\s*(\/?)\s*([a-zA-Z0-9:-]+)\b[^>]*>', re.IGNORECASE)

open_tags = []

for match in tag_pattern.finditer(content):
    is_close = match.group(1) == '/'
    tag_name = match.group(2).lower()
    
    # Skip self-closing tags
    if tag_name in ['img', 'br', 'hr', 'input', 'link', 'meta', 'source']:
        continue
        
    if is_close:
        # Find matching open tag
        if open_tags and open_tags[-1][0] == tag_name:
            open_tags.pop()
        else:
            # tag mismatch, let's see
            # search for last open tag of this name
            found = False
            for idx in range(len(open_tags) - 1, -1, -1):
                if open_tags[idx][0] == tag_name:
                    open_tags = open_tags[:idx]
                    found = True
                    break
    else:
        open_tags.append((tag_name, match.start()))
        
    if tag_name == 'footer' and not is_close:
        print("Active tags when footer starts:")
        for t, pos in open_tags:
            # get line number
            line_num = content[:pos].count('\n') + 1
            print(f"  <{t}> opened at line {line_num}")
