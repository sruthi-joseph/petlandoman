import os
import math
from PIL import Image

pet_food_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
if not os.path.exists(pet_food_path):
    print("pet food.jpeg not found!")
    exit(1)

img = Image.open(pet_food_path).convert("RGB")
w, h = img.size

# We know the image is 2400x1792.
# Let's find the circle center and radius.
# Usually, the circle has a distinct border or inner background that is light,
# and outside the circle it is also a light cream color, but there is a border line.
# Let's scan along multiple lines to find the circular border.
# Let's sample a grid of pixels or search from the center (1200, 896) radially.
center_x = w // 2
center_y = h // 2

# Let's inspect pixel colors on a horizontal line through the center
print("Horizontal line scan:")
for x in range(0, w, 100):
    r, g, b = img.getpixel((x, center_y))
    print(f"x={x}: R={r}, G={g}, B={b}")

# Let's find the border. The border is a golden-beige ring.
# Let's find where the ring is.
# Let's scan with 1px step from 1200 down to 200 (left) and 1200 to 2200 (right).
left_x = None
for x in range(1200, 100, -1):
    r, g, b = img.getpixel((x, center_y))
    # Let's see if we see a change indicating the golden border.
    # Golden border has some darker yellow/brown color.
    # Let's print the pixels from x=300 to 500 to see the exact border.
    if x >= 300 and x <= 500:
        pass

# Let's print pixel values around the border region to find the ring.
print("\nPixels from x=350 to 450 (left of center):")
for x in range(350, 451, 5):
    r, g, b = img.getpixel((x, center_y))
    print(f"x={x}: R={r}, G={g}, B={b}")
