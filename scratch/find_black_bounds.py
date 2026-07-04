from PIL import Image
import os

screenshot_path = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\22fa6263-8c42-49d6-9c65-fef095efda85\footer_screenshot_1782473802557.png"

if not os.path.exists(screenshot_path):
    print("Screenshot not found")
    exit()

img = Image.open(screenshot_path).convert("RGB")
w, h = img.size

# Let's inspect row y=500
y = 500
black_pixels = []
for x in range(w):
    r, g, b = img.getpixel((x, y))
    # If it matches the footer background #111111 (allowing small tollerance)
    if abs(r - 17) < 3 and abs(g - 17) < 3 and abs(b - 17) < 3:
        black_pixels.append(x)

if black_pixels:
    start_x = black_pixels[0]
    end_x = black_pixels[-1]
    print(f"Footer black starts at x={start_x}, ends at x={end_x}")
    print(f"Left gap width: {start_x}px")
    print(f"Right gap width: {w - 1 - end_x}px")
else:
    print("No footer black pixels found at y=500")
