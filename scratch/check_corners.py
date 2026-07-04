from PIL import Image
import os

products = [
    "pet food.jpeg",
    "toys & fun.jpeg",
    "groomin products.jpeg",
    "accessories.jpeg"
]

for name in products:
    if not os.path.exists(name):
        continue
    img = Image.open(name).convert("RGB")
    w, h = img.size
    print(f"\n{name}:")
    print(f"  Corner TL (0,0): {img.getpixel((0,0))}")
    print(f"  Corner TR (w-1,0): {img.getpixel((w-1,0))}")
    print(f"  Corner BL (0,h-1): {img.getpixel((0,h-1))}")
    print(f"  Corner BR (w-1,h-1): {img.getpixel((w-1,h-1))}")
    print(f"  Top Middle (w//2, 10): {img.getpixel((w//2, 10))}")
    print(f"  Bottom Middle (w//2, h-10): {img.getpixel((w//2, h-10))}")
    print(f"  Left Middle (10, h//2): {img.getpixel((10, h//2))}")
    print(f"  Right Middle (w-10, h//2): {img.getpixel((w-10, h//2))}")
