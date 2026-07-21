from PIL import Image
import numpy as np
import os

def check_image(path):
    name = os.path.basename(path)
    if not os.path.exists(path):
        print(f"{name} does not exist")
        return
    with Image.open(path) as img:
        if img.mode != 'RGBA':
            print(f"{name}: mode is {img.mode} (no alpha)")
            return
        arr = np.array(img)
        alpha = arr[:, :, 3]
        total_pixels = alpha.size
        zero_alpha = np.sum(alpha == 0)
        full_alpha = np.sum(alpha == 255)
        partial_alpha = total_pixels - zero_alpha - full_alpha
        print(f"{name}: total={total_pixels}, transparent={zero_alpha} ({zero_alpha/total_pixels*100:.1f}%), opaque={full_alpha} ({full_alpha/total_pixels*100:.1f}%), partial={partial_alpha} ({partial_alpha/total_pixels*100:.1f}%)")

dir_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
check_image(os.path.join(dir_path, "logo_transparent.png"))
check_image(os.path.join(dir_path, "logo_white_transparent.png"))
check_image(os.path.join(dir_path, "logo.png"))

folder = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images"
for f in ["img_0_R21.png", "img_4_R15.png", "img_2_R18.png"]:
    check_image(os.path.join(folder, f))
