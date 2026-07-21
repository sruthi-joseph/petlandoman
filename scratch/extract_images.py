import pypdf
import os

pdf_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\docs\logo.pdf"
out_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images"
os.makedirs(out_dir, exist_ok=True)

reader = pypdf.PdfReader(pdf_path)
page = reader.pages[0]

for idx, img in enumerate(page.images):
    name = img.name
    # Clean the name to avoid issues
    name = "".join(c for c in name if c.isalnum() or c in "._-")
    # If name doesn't have extension, add it based on content or metadata
    if not name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        # Check the format or just default to png/jpg
        # Let's save as png or jpg based on name/type
        pass
    
    out_path = os.path.join(out_dir, f"img_{idx}_{name}")
    with open(out_path, "wb") as f:
        f.write(img.data)
    print(f"Saved {out_path} ({len(img.data)} bytes)")
