import os

folder = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
for f in os.listdir(folder):
    if os.path.isfile(os.path.join(folder, f)):
        print(f"File: {f}, Size: {os.path.getsize(os.path.join(folder, f))}")
