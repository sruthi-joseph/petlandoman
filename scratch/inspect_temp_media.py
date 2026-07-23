from PIL import Image
import os

temp_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\5b0debc6-9cea-4d38-b726-b356ae133ac1\.tempmediaStorage"
if os.path.exists(temp_dir):
    for f in sorted(os.listdir(temp_dir)):
        p = os.path.join(temp_dir, f)
        if os.path.isfile(p) and (f.endswith(".png") or f.endswith(".jpeg")):
            try:
                with Image.open(p) as img:
                    print(f"File: {f}, Size: {img.size}, Mode: {img.mode}, Bytes: {os.path.getsize(p)}")
            except Exception as e:
                print(f"File: {f}, Error: {e}")
else:
    print("Temp media storage not found!")
