from PIL import Image
import numpy as np

def check_image_pixels(path):
    with Image.open(path) as img:
        arr = np.array(img.convert("RGBA"))
        h, w, _ = arr.shape
        # Let's check some pixels in the center of the image
        center_y, center_x = h // 2, w // 2
        print(f"Image: {path}")
        print(f"Center pixel: {arr[center_y, center_x]}")
        
        # Let's count pixels of different colors with alpha > 128
        opaque_mask = arr[:, :, 3] > 128
        opaque_pixels = arr[opaque_mask]
        
        # Count white pixels (R>240, G>240, B>240)
        white_mask = (opaque_pixels[:, 0] > 240) & (opaque_pixels[:, 1] > 240) & (opaque_pixels[:, 2] > 240)
        num_white = np.sum(white_mask)
        
        # Count dark pixels (R<20, G<20, B<20)
        dark_mask = (opaque_pixels[:, 0] < 20) & (opaque_pixels[:, 1] < 20) & (opaque_pixels[:, 2] < 20)
        num_dark = np.sum(dark_mask)
        
        total_opaque = len(opaque_pixels)
        print(f"Total opaque: {total_opaque}")
        print(f"Opaque white: {num_white} ({num_white/total_opaque*100:.1f}%)")
        print(f"Opaque dark: {num_dark} ({num_dark/total_opaque*100:.1f}%)")

check_image_pixels(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images\img_4_R15.png")
check_image_pixels(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png")
