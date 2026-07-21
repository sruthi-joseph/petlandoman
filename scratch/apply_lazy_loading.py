import os
import re

workspace_dir = r"c:\Users\SRUTHI\Desktop\petland oman"
pages_dir = os.path.join(workspace_dir, "pages")

html_files = [os.path.join(workspace_dir, "index.html")]
if os.path.exists(pages_dir):
    for f in os.listdir(pages_dir):
        if f.endswith(".html"):
            html_files.append(os.path.join(pages_dir, f))

# Classes of images we definitely want to lazy load (below the fold)
lazy_classes = {
    "aboutus-pet-img",
    "banner-img",
    "svc-pet-img",
    "branch-storefront-img",
    "footer-pets-img",
    "boarding-card-img",
    "grooming-card-img",
    "svc-card-main-img"
}

# Image sources or parts we want to lazy load
lazy_src_keywords = {
    "extracted_images/product_",
    "extracted_images/service_",
    "extracted_images/branch_storefront_",
    "branches/petland",
    "branches/pethouse"
}

def should_lazy_load(tag):
    # Already has loading="lazy"
    if "loading=" in tag.lower():
        return False
        
    # Check class
    class_match = re.search(r'class="([^"]+)"', tag, re.IGNORECASE)
    if class_match:
        classes = set(class_match.group(1).split())
        if classes.intersection(lazy_classes):
            return True
            
    # Check src
    src_match = re.search(r'src="([^"]+)"', tag, re.IGNORECASE)
    if src_match:
        src = src_match.group(1)
        for keyword in lazy_src_keywords:
            if keyword in src.lower():
                return True
                
    # Also check if it's the footer pets image by src name
    if src_match and "footer_pets.png" in src_match.group(1):
        return True
        
    return False

print("Updating HTML files with lazy loading...")
for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Use list to bypass module-level scope issue in re.sub replacer function
    state = {"modified": False}
    
    def replacer(match):
        tag = match.group(0)
        if should_lazy_load(tag):
            # Insert loading="lazy" before the closing bracket
            new_tag = tag[:-1].rstrip() + ' loading="lazy">'
            print(f"  [{rel_path}] Updated: {tag} -> {new_tag}")
            state["modified"] = True
            return new_tag
        return tag

    new_content = re.sub(r'<img\b[^>]*>', replacer, content, flags=re.IGNORECASE)
    
    if state["modified"]:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Saved: {rel_path}")
