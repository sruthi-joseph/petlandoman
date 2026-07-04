import os
from PIL import Image
import numpy as np

img_names = ["svc_nutritional_final.png", "svc_training_final.png", "svc_grooming_final.png", "svc_daycare_final.png"]
base_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

for name in img_names:
    path = os.path.join(base_dir, name)
    if not os.path.exists(path):
        continue
    img = Image.open(path).convert("RGBA")
    data = np.array(img)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Let's count how many pixels are white (255, 255, 255, 255)
    white_opaque = np.sum((r == 255) & (g == 255) & (b == 255) & (a == 255))
    white_any_alpha = np.sum((r == 255) & (g == 255) & (b == 255) & (a > 0))
    
    print(f"Image: {name}")
    print(f"  Opaque white pixels: {white_opaque}")
    print(f"  Any-alpha white pixels: {white_any_alpha}")
    
    # Check if there are pixels with high brightness that are opaque
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    bright_pixels = np.sum((brightness > 240) & (a > 0))
    print(f"  Bright pixels (brightness > 240): {bright_pixels}")
