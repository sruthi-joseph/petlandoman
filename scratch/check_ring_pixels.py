import numpy as np
from PIL import Image

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
img = Image.open(img_path).convert("RGB")
w, h = img.size
arr = np.array(img)

cx, cy = 1200.5, 906.5

# Let's check pixel colors along different radii at angles: 0, 45, 90, 135, 180, 225, 270, 315
angles = [0, 45, 90, 135, 180, 225, 270, 315]

for r_test in [755, 760, 765, 770, 775, 780]:
    print(f"\nTesting radius R = {r_test}:")
    for angle_deg in angles:
        angle = np.radians(angle_deg)
        x = int(cx + r_test * np.cos(angle))
        y = int(cy + r_test * np.sin(angle))
        if 0 <= x < w and 0 <= y < h:
            color = arr[y, x]
            print(f"  Angle {angle_deg:3d}° (x={x}, y={y}): RGB = {color}")
