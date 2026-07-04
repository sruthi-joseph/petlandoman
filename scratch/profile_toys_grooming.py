from PIL import Image
import os

files = [
    ("toys & fun.jpeg", 1200, 894),
    ("groomin products.jpeg", 1200, 901)
]

for name, cx, cy in files:
    if not os.path.exists(name):
        continue
    img = Image.open(name).convert("RGB")
    print(f"\nProfile for {name} from center ({cx}, {cy}):")
    
    # We will print pixel colors horizontally to the left (cx - r, cy) for r in 650..820
    print("Horizontal left profile (radius, R, G, B):")
    for r in range(650, 820, 10):
        rgb = img.getpixel((cx - r, cy))
        print(f"  r={r}: {rgb} (sum: {sum(rgb)})")
        
    print("Vertical top profile (radius, R, G, B):")
    for r in range(650, 820, 10):
        rgb = img.getpixel((cx, cy - r))
        print(f"  r={r}: {rgb} (sum: {sum(rgb)})")
