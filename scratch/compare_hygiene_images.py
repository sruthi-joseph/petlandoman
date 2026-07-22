from PIL import Image
import numpy as np

img1 = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\hygiene suppliments.jpeg").convert("RGB")
img2 = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\product page card-hygiene and supplements.jpeg").convert("RGB")

arr1 = np.array(img1, dtype=np.int16)
arr2 = np.array(img2, dtype=np.int16)

diff = np.abs(arr1 - arr2)
max_diff = diff.max(axis=2)

diff_pixels = np.where(max_diff > 30)
print(f"Number of differing pixels (>30 threshold): {len(diff_pixels[0])}")

if len(diff_pixels[0]) > 0:
    ymin, ymax = diff_pixels[0].min(), diff_pixels[0].max()
    xmin, xmax = diff_pixels[1].min(), diff_pixels[1].max()
    print(f"Differing region bounding box: Y=[{ymin}, {ymax}], X=[{xmin}, {xmax}]")
    print(f"Width of diff: {xmax - xmin + 1}, Height of diff: {ymax - ymin + 1}")
