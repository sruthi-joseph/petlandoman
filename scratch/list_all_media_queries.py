with open("style.css", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Find all @media declarations
matches = re.finditer(r'(@media[^{]*\{)', content)
for m in matches:
    print(f"\nMedia Query Header: {m.group(1)}")
    # Find matching closing brace
    brace_count = 1
    i = m.end()
    block_content = ""
    while i < len(content) and brace_count > 0:
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
        block_content += content[i]
        i += 1
    
    # Check if there is any rule in the block content that applies to footer or main-card
    # We will search for footer or main-card or bottom-bar
    sub_rules = re.findall(r'([^{}]*\{[^{}]*\})', block_content, re.DOTALL)
    for rule in sub_rules:
        if "footer" in rule or "main-card" in rule:
            print(f"  Rule: {rule.strip()}")
