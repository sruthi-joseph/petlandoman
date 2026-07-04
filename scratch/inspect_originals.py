from PIL import Image
import os

brain_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\d7344ec0-3c55-4d54-9497-0adca2bc614e"
files = [
    "grooming_shower_1782985193264.png",
    "grooming_haircut_1782985216768.png",
    "grooming_deshedding_1782985233345.png",
    "grooming_full_1782985251369.png",
    "grooming_medicated_1782985875259.png"
]

for f in files:
    path = os.path.join(brain_dir, f)
    if os.path.exists(path):
        img = Image.open(path)
        print(f"Original: {f} | Size: {img.size} | Mode: {img.mode}")
    else:
        print("Not found:", path)
