import os

for root, dirs, files in os.walk(r"c:\Users\SRUTHI\Desktop\petland oman"):
    for f in files:
        if "chatgpt" in f.lower() or "jun24" in f.lower():
            print(f"Found: {os.path.join(root, f)}")
