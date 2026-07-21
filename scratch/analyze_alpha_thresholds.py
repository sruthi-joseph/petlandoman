from PIL import Image
import numpy as np
import os

def get_bbox_threshold(img_path, threshold):
    with Image.open(img_path) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        arr = np.array(img)
        alpha = arr[:, :, 3]
        # Find where alpha > threshold
        non_zero = np.argwhere(alpha > threshold)
        if len(non_zero) == 0:
            return None
        # argwhere returns [row, col] which corresponds to [y, x]
        y_min, x_min = non_zero.min(axis=0)
        y_max, x_max = non_zero.max(axis=0)
        # bbox is (left, top, right, bottom), right and bottom are exclusive (+1)
        return (int(x_min), int(y_min), int(x_max + 1), int(y_max + 1))

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png"
print("For logo_transparent.png:")
for t in [0, 1, 2, 5, 10, 20, 50, 100]:
    bbox = get_bbox_threshold(img_path, t)
    if bbox:
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        print(f"  threshold > {t:3d}: bbox={bbox}, size={w}x{h}")
    else:
        print(f"  threshold > {t:3d}: empty")

new_logo_path = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images\img_4_R15.png"
print("\nFor img_4_R15.png:")
for t in [0, 1, 2, 5, 10, 20, 50, 100]:
    bbox = get_bbox_threshold(new_logo_path, t)
    if bbox:
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        print(f"  threshold > {t:3d}: bbox={bbox}, size={w}x{h}")
    else:
        print(f"  threshold > {t:3d}: empty")
