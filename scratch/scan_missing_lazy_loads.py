import os
import re

workspace_dir = r"c:\Users\SRUTHI\Desktop\petland oman"
pages_dir = os.path.join(workspace_dir, "pages")

html_files = [os.path.join(workspace_dir, "index.html")]
if os.path.exists(pages_dir):
    for f in os.listdir(pages_dir):
        if f.endswith(".html"):
            html_files.append(os.path.join(pages_dir, f))

img_tag_regex = re.compile(r'<img\s+[^>]*src="([^"]+)"[^>]*>', re.IGNORECASE)

print("Scanning HTML files for images without loading='lazy':")
for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    print(f"\nFile: {rel_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find all matches of <img> tags
    matches = re.finditer(r'<img\b[^>]*>', content, re.IGNORECASE)
    found_count = 0
    for match in matches:
        tag = match.group(0)
        if "loading=" not in tag.lower():
            # Check if it contains an image source
            src_match = re.search(r'src="([^"]+)"', tag, re.IGNORECASE)
            src = src_match.group(1) if src_match else "unknown"
            # Skip top-of-page elements like header logos
            if "logo" in src.lower() and found_count < 2 and "index.html" in rel_path:
                print(f"  [SKIP - Top Logo] {tag}")
            else:
                print(f"  [MISSING LAZY] {tag}")
            found_count += 1
