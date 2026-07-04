from PIL import Image
import os

screenshot_path = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\22fa6263-8c42-49d6-9c65-fef095efda85\footer_gap_1782474053526.png"

if not os.path.exists(screenshot_path):
    print("Screenshot not found")
    exit()

img = Image.open(screenshot_path).convert("RGB")
w, h = img.size
print(f"Screenshot size: {w}x{h}")

# Let's check a horizontal line inside the footer main card (e.g. y = 700)
# We want to see where the dark background ends on the right, and what colors follow it.
y = 700
row_colors = [img.getpixel((x, y)) for x in range(w)]

# Find start and end of black region (RGB ~ (17,17,17) or sum < 60)
black_indices = [x for x, rgb in enumerate(row_colors) if sum(rgb) < 60]

if black_indices:
    start_x = black_indices[0]
    end_x = black_indices[-1]
    print(f"Black region: x={start_x} to x={end_x}")
    print(f"Pixels right of black region:")
    # print up to 50 pixels to the right of end_x
    for x in range(end_x + 1, min(w, end_x + 50)):
        print(f"  x={x}: {row_colors[x]}")
else:
    print("No black pixels found!")
