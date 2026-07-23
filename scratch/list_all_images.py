import os

# List all image files in the workspace with their sizes
for root, dirs, files in os.walk(r"c:\Users\SRUTHI\Desktop\petland oman"):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".webp"]:
            p = os.path.join(root, f)
            # Ignore scratch and .git directories to keep output clean
            if "scratch" not in p and ".git" not in p:
                print(f"Image: {p}, Size: {os.path.getsize(p)}")
