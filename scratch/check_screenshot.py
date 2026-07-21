from PIL import Image
import numpy as np
from collections import Counter

path = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\27e72719-adfb-4eaf-897f-894c3b5dc138\pdf_logo_page_1784617399323.png"
with Image.open(path) as img:
    arr = np.array(img.convert("RGB"))
    pixels = arr.reshape(-1, 3)
    counter = Counter(tuple(p) for p in pixels)
    most_common = counter.most_common(10)
    print("Dominant colors in screenshot:")
    for color, count in most_common:
        percent = count / len(pixels) * 100
        print(f"  RGB {color}: {count} pixels ({percent:.2f}%)")
