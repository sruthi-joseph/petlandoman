from PIL import Image
import os

images = [
    "extracted_images/product_1.png",
    "extracted_images/product_2.png",
    "extracted_images/product_3.png",
    "extracted_images/product_4.png"
]

for path in images:
    if not os.path.exists(path):
        print(f"{path} not found")
        continue
    img = Image.open(path)
    w, h = img.size
    print(f"\nCropped Image: {path} (size: {w}x{h})")
    
    # We cropped to circular mask. Let's find any pixels with alpha > 0 (visible pixels)
    # and print their color near the left/right boundaries of the circle.
    # In a 500x500 image, the circle is centered at (250, 250) with radius 250.
    # Let's inspect along the horizontal midline (y = 250) at x coordinates near the edge of the circle (e.g. x = 5, 10, 15, 20)
    for x in [5, 10, 20, 30, 250]:
        rgba = img.getpixel((x, 250))
        print(f"  Pixel at x={x}, y=250: {rgba}")
