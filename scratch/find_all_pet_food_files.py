import os

for root, dirs, files in os.walk(r"c:\Users\SRUTHI\Desktop\petland oman"):
    for f in files:
        if "pet food" in f.lower() or "pet_food" in f.lower():
            p = os.path.join(root, f)
            print(f"Path: {p}, Size: {os.path.getsize(p)}")
