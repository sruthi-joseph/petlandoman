import os
import numpy as np
from PIL import Image

card_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images"
cards = ["pet food.jpeg", "accessories.jpeg", "toys and fun.jpeg", "hygiene suppliments.jpeg"]

for card in cards:
    p = os.path.join(card_dir, card)
    if os.path.exists(p):
        with Image.open(p) as img:
            arr = np.array(img.convert("RGB"))
            # Let's inspect the color near the top-left of the circle interior: (1200 - 300, 906 - 300) = (900, 606)
            color = arr[606, 900]
            print(f"{card}: size={img.size}, color at (900, 606)={color}")
    else:
        print(f"Not found: {p}")
