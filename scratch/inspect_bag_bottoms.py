import os
import numpy as np
from PIL import Image

def inspect_bottom(name, path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    
    # Let's segment it using floodfill first to see what pixels are left
    from PIL import ImageDraw
    temp_img = img.copy()
    ImageDraw.floodfill(temp_img, (0, 0), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (w - 1, 0), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (0, h - 1), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (w - 1, h - 1), (0, 0, 0, 0), thresh=10)
    
    alpha = np.array(temp_img.split()[3])
    # Find the bounding box
    ys, xs = np.where(alpha > 0)
    y_min, y_max = ys.min(), ys.max()
    x_min, x_max = xs.min(), xs.max()
    
    # Let's inspect the last 150 rows at the bottom of the detected product bounding box
    # print out the row sum of alpha (number of non-transparent pixels in each row near the bottom)
    print(f"\n{name} (bbox height from {y_min} to {y_max}):")
    print("Row index (from bottom) and count of non-transparent pixels:")
    for offset in range(150, -1, -5):
        y = y_max - offset
        if y_min <= y <= y_max:
            row_alpha = alpha[y, x_min:x_max+1]
            non_bg = np.sum(row_alpha > 0)
            # Print average color of non-bg pixels in this row
            row_colors = np.array(img)[y, x_min:x_max+1, :3]
            avg_color = row_colors[row_alpha > 0].mean(axis=0) if non_bg > 0 else [0,0,0]
            print(f"  Row {y_max - y:3d} (y={y}): non-bg pixels = {non_bg:4d}, avg_color = {avg_color.round(1)}")

inspect_bottom("HAIRBALL_26297", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL\26297.webp")
inspect_bottom("KITTEN_36813", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36813.webp")
inspect_bottom("MAXI_25489", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI\25489.webp")
