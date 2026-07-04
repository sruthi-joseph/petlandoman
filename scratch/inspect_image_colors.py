import os
from PIL import Image
import numpy as np

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
        img = Image.open(path).convert("RGB")
        w, h = img.size
        data = np.array(img)
        
        # Corner values
        tl = data[0, 0]
        tr = data[0, w-1]
        bl = data[h-1, 0]
        br = data[h-1, w-1]
        
        # Center top edge
        ct = data[0, w//2]
        # Center right edge
        cr = data[h//2, w-1]
        
        print(f"File: {f}")
        print(f"  Corners RGB: TL={tl}, TR={tr}, BL={bl}, BR={br}")
        print(f"  Edges RGB: TopCenter={ct}, RightCenter={cr}")
    else:
        print("Not found:", path)
