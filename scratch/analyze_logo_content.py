from PIL import Image
import numpy as np

def analyze_logo(path, label):
    with Image.open(path) as img:
        img_rgba = img.convert("RGBA")
        arr = np.array(img_rgba)
        alpha = arr[:, :, 3]
        
        # Calculate horizontal and vertical profiles
        row_sum = np.sum(alpha > 10, axis=1)
        col_sum = np.sum(alpha > 10, axis=0)
        
        # Find first and last index with significant content (e.g. > 5 pixels)
        rows_with_content = np.where(row_sum > 5)[0]
        cols_with_content = np.where(col_sum > 5)[0]
        
        if len(rows_with_content) > 0 and len(cols_with_content) > 0:
            ymin, ymax = rows_with_content[0], rows_with_content[-1]
            xmin, xmax = cols_with_content[0], cols_with_content[-1]
            print(f"{label}: size={img.size}, content_bbox=({xmin}, {ymin}, {xmax}, {ymax}), content_size={xmax-xmin}x{ymax-ymin}")
        else:
            print(f"{label}: no content found")

analyze_logo(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png", "logo_transparent.png")
analyze_logo(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images\img_4_R15.png", "img_4_R15.png")
