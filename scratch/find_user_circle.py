from PIL import Image
import numpy as np

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food-home.jpeg"
img = Image.open(img_path).convert("RGB")
data = np.array(img)
h, w, c = data.shape

# Let's find pixels that match the peach circle background color.
# We know the peach color is approximately R=248, G=233, B=202.
# Let's find all pixels where:
# R is in [245, 252]
# G is in [230, 238]
# B is in [195, 210]
r_ch, g_ch, b_ch = data[:,:,0], data[:,:,1], data[:,:,2]
mask = (r_ch >= 245) & (r_ch <= 252) & (g_ch >= 230) & (g_ch <= 238) & (b_ch >= 195) & (b_ch <= 210)

ys, xs = np.where(mask)
if len(xs) > 0 and len(ys) > 0:
    print(f"Detected peach pixels: {len(xs)}")
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    print(f"Bounding box of peach pixels: X=[{x_min}, {x_max}], Y=[{y_min}, {y_max}]")
    cx = (x_min + x_max) // 2
    cy = (y_min + y_max) // 2
    # Estimate radius as half the average width/height
    diameter = max(x_max - x_min, y_max - y_min)
    print(f"Center: ({cx}, {cy}), Estimated diameter: {diameter}, radius: {diameter // 2}")
else:
    print("No peach pixels found within thresholds!")
