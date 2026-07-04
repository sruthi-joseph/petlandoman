from PIL import Image
import os

screenshot_path = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\22fa6263-8c42-49d6-9c65-fef095efda85\footer_screenshot_1782473802557.png"

if not os.path.exists(screenshot_path):
    print("Screenshot not found")
    exit()

img = Image.open(screenshot_path).convert("RGB")
w, h = img.size
print(f"Screenshot size: {w}x{h}")

# Let's inspect horizontal lines in the footer area
# The footer main card is black/dark gray, and the bottom bar is yellow.
# Let's check a line through the main card (e.g. h - 100) and a line through the bottom bar (e.g. h - 20)
mid_y_card = h - 100
mid_y_bar = h - 20

print(f"\nRow at y={mid_y_card} (footer card):")
card_colors = [img.getpixel((x, mid_y_card)) for x in range(w)]
# Find range of black/dark colors (e.g. R,G,B all < 30)
dark_pixels = [x for x, rgb in enumerate(card_colors) if rgb[0] < 30 and rgb[1] < 30 and rgb[2] < 30]
if dark_pixels:
    print(f"  Dark card region: x={dark_pixels[0]} to x={dark_pixels[-1]}")
    print(f"  Color at x=0: {card_colors[0]}")
    print(f"  Color at x=w-1: {card_colors[-1]}")
else:
    print("  No dark card region found!")

print(f"\nRow at y={mid_y_bar} (footer bottom bar):")
bar_colors = [img.getpixel((x, mid_y_bar)) for x in range(w)]
# Find range of yellow colors (e.g. R > 200, G > 160, B < 50)
yellow_pixels = [x for x, rgb in enumerate(bar_colors) if rgb[0] > 200 and rgb[1] > 160 and rgb[2] < 50]
if yellow_pixels:
    print(f"  Yellow bar region: x={yellow_pixels[0]} to x={yellow_pixels[-1]}")
    print(f"  Color at x=0: {bar_colors[0]}")
    print(f"  Color at x=w-1: {bar_colors[-1]}")
else:
    print("  No yellow bar region found!")
