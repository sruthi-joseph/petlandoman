import os
import re

workspace_dir = r"c:\Users\SRUTHI\Desktop\petland oman"
pages_dir = os.path.join(workspace_dir, "pages")

target_files = [
    os.path.join(pages_dir, "toys.html"),
    os.path.join(pages_dir, "pet-food.html"),
    os.path.join(pages_dir, "hygiene.html"),
    os.path.join(pages_dir, "accessories.html")
]

# Pattern to search
pattern = re.compile(
    r'var\s+observer\s*=\s*new\s+IntersectionObserver\s*\(\s*function\s*\(\s*entries\s*\)\s*\{\s*'
    r'entries\.forEach\s*\(\s*function\s*\(\s*entry\s*\)\s*\{\s*'
    r'if\s*\(\s*entry\.isIntersecting\s*\)\s*\{\s*'
    r'var\s+idx\s*=\s*Array\.from\s*\(\s*cards\s*\)\.indexOf\s*\(\s*entry\.target\s*\);\s*'
    r'setTimeout\s*\(\s*function\s*\(\s*\)\s*\{\s*'
    r'entry\.target\.style\.opacity\s*=\s*\'1\';\s*'
    r'entry\.target\.style\.transform\s*=\s*\'translateY\(0\)\';\s*'
    r'\}\s*,\s*idx\s*\*\s*(\d+)\s*\);\s*'
    r'observer\.unobserve\s*\(\s*entry\.target\s*\);\s*'
    r'\}\s*\}\s*\);\s*\}\s*,\s*\{\s*threshold\s*:\s*0\.1\s*\}\s*\);\s*'
    r'\s*cards\.forEach\s*\(\s*function\s*\(\s*card\s*\)\s*\{\s*'
    r'card\.style\.opacity\s*=\s*\'0\';\s*'
    r'card\.style\.transform\s*=\s*\'translateY\(30px\)\';\s*'
    r'card\.style\.transition\s*=\s*\'[^\']+\';\s*'
    r'observer\.observe\s*\(\s*card\s*\);\s*'
    r'\}\s*\);',
    re.DOTALL | re.IGNORECASE
)

for file_path in target_files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    match = pattern.search(content)
    if match:
        delay_val = match.group(1)
        print(f"Found card animation script in: {os.path.basename(file_path)} with delay factor: {delay_val}")
        
        replacement = (
            f"var observer = new IntersectionObserver(function(entries) {{\n"
            f"                entries.forEach(function(entry) {{\n"
            f"                    if (entry.isIntersecting) {{\n"
            f"                        var idx = entry.target._cardIndex;\n"
            f"                        setTimeout(function() {{\n"
            f"                            entry.target.style.opacity = '1';\n"
            f"                            entry.target.style.transform = 'translateY(0)';\n"
            f"                        }}, idx * {delay_val});\n"
            f"                        observer.unobserve(entry.target);\n"
            f"                    }}\n"
            f"                }});\n"
            f"            }}, {{ threshold: 0.1 }});\n"
            f"\n"
            f"            cards.forEach(function(card, index) {{\n"
            f"                card._cardIndex = index;\n"
            f"                card.style.opacity = '0';\n"
            f"                card.style.transform = 'translateY(30px)';\n"
            f"                card.style.transition = 'opacity 0.55s ease, transform 0.55s cubic-bezier(0.16,1,0.3,1), box-shadow 0.35s ease';\n"
            f"                observer.observe(card);\n"
            f"            }});"
        )
        
        new_content = pattern.sub(replacement, content)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  Successfully optimized {os.path.basename(file_path)}!")
    else:
        print(f"  Pattern not matched in {os.path.basename(file_path)}")
