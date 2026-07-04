from PIL import Image
import os

screenshot_path = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\22fa6263-8c42-49d6-9c65-fef095efda85\footer_screenshot_1782473802557.png"

if not os.path.exists(screenshot_path):
    print("Screenshot not found")
    exit()

img = Image.open(screenshot_path).convert("RGB")
w, h = img.size
print(f"Image size: {w}x{h}")

# Let's print every 100th pixel for y = 500, 700, 900, 1000
for target_y in [500, 700, 900, 1000]:
    print(f"\nRow at y={target_y}:")
    row_colors = [img.getpixel((x, target_y)) for x in range(0, w, 100)]
    for idx, color in enumerate(row_colors):
        x = idx * 100
        print(f"  x={x:04d}: {color}")
