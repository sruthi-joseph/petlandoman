import os
from collections import Counter
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images"
img = Image.open(os.path.join(image_dir, "product_1.png")).convert("RGB")

# Sample pixels inside the letters
# Let's count colors of pixels in X: 211 to 349, Y: 141 to 170 where R < 100
colors = []
for y in range(141, 170):
    for x in range(211, 350):
        color = img.getpixel((x, y))
        if color[0] < 100 and color[1] < 80 and color[2] < 60:
            colors.append(color)

counter = Counter(colors)
print("Most common dark text colors:")
for color, count in counter.most_common(10):
    print(f"Color {color}: count={count}")
