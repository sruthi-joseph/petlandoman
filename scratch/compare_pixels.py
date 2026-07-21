from PIL import Image
import numpy as np
import os

cropped_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\cropped_images"

def compare_images(name1, name2):
    p1 = os.path.join(cropped_dir, name1)
    p2 = os.path.join(cropped_dir, name2)
    if not os.path.exists(p1) or not os.path.exists(p2):
        print(f"One of the files doesn't exist: {name1}, {name2}")
        return
    with Image.open(p1) as img1, Image.open(p2) as img2:
        if img1.size != img2.size:
            print(f"{name1} and {name2} have different sizes: {img1.size} vs {img2.size}")
            return
        if img1.mode != img2.mode:
            print(f"{name1} and {name2} have different modes: {img1.mode} vs {img2.mode}")
            return
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        diff = np.sum(arr1 != arr2)
        if diff == 0:
            print(f"{name1} and {name2} are PIXEL IDENTICAL!")
        else:
            percent = diff / arr1.size * 100
            print(f"{name1} and {name2} differ by {diff} pixels ({percent:.3f}%)")

compare_images("img_0_R21_png_cropped.png", "existing_logo_transparent_cropped.png")
compare_images("img_11_R21_png_cropped.png", "existing_logo_transparent_cropped.png")
compare_images("img_4_R15_png_cropped.png", "existing_logo_transparent_cropped.png")
