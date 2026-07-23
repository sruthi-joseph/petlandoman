import os
import numpy as np
from PIL import Image

card_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet food.jpeg"
if os.path.exists(card_path):
    img = Image.open(card_path).convert("RGB")
    w, h = img.size
    print(f"Card image size: {w}x{h}")
    # Let's check where the light circle is.
    # We can scan horizontally along h//2 (which is 470)
    cy = h // 2
    row = np.array(img)[cy, :, :]
    # Let's find indices of light pixels (R+G+B > 600)
    light_indices = np.where(np.sum(row, axis=1) > 600)[0]
    if len(light_indices) > 0:
        print(f"  Horizontal light bounds: {light_indices.min()} to {light_indices.max()} (width: {light_indices.max() - light_indices.min()})")
        print(f"  Center x: {(light_indices.min() + light_indices.max())/2}")
else:
    print("Card image not found!")
