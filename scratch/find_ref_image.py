import os

# Let's search the workspace for any images that might be related to "reference", "ref", "canin", etc.
for root, dirs, files in os.walk(r"c:\Users\SRUTHI\Desktop\petland oman"):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".webp"]:
            p = os.path.join(root, f)
            if "ref" in f.lower() or "canin" in f.lower() or "bag" in f.lower():
                print(f"Match: {p}, Size: {os.path.getsize(p)}")
