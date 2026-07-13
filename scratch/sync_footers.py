import os
import re

workspace_dir = r"c:\Users\SRUTHI\Desktop\petland oman"
index_path = os.path.join(workspace_dir, "index.html")

# Read the correct footer from index.html
with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Find the footer content
# We will match from <footer> to </footer>
footer_match = re.search(r"<footer>.*?</footer>", index_content, re.DOTALL)
if not footer_match:
    print("Error: Could not find footer in index.html")
    exit()

correct_footer = footer_match.group(0)
print("Correct footer extracted successfully from index.html.")

# Now scan and replace in all other html files
html_files = [f for f in os.listdir(workspace_dir) if f.endswith(".html")]

for filename in html_files:
    if filename == "index.html":
        continue
        
    file_path = os.path.join(workspace_dir, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace the footer block
    new_content, count = re.subn(r"<footer>.*?</footer>", correct_footer, content, flags=re.DOTALL)
    
    if count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated footer in: {filename}")
    else:
        print(f"No footer block found or could not replace in: {filename}")
