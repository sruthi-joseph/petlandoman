import os
import numpy as np
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images"
img_path = os.path.join(image_dir, "product_1.png")
img = Image.open(img_path).convert("RGBA")
arr = np.array(img)

# Let's search for pixels that look like the text: dark brown
# We inspect region X: 150 to 350, Y: 100 to 200
sub_arr = arr[100:200, 150:350, :]

# Let's find coordinates of dark pixels: e.g. R < 100, G < 80, B < 60 and alpha > 0
# The bag color is yellow (R > 200, G > 180, B < 100)
# So the text pixels should have a low R, G, B value.
y_indices, x_indices = np.where((sub_arr[:, :, 0] < 120) & 
                                (sub_arr[:, :, 1] < 100) & 
                                (sub_arr[:, :, 2] < 80) & 
                                (sub_arr[:, :, 3] > 0))

if len(x_indices) > 0:
    min_x = np.min(x_indices) + 150
    max_x = np.max(x_indices) + 150
    min_y = np.min(y_indices) + 100
    max_y = np.max(y_indices) + 100
    print(f"Text bounding box found: X = {min_x} to {max_x}, Y = {min_y} to {max_y} (size: {max_x-min_x+1}x{max_y-min_y+1})")
else:
    print("No text pixels found")
