import os
import numpy as np
from PIL import Image

card_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet food.jpeg"
if os.path.exists(card_path):
    img = Image.open(card_path).convert("RGB")
    w, h = img.size
    arr = np.array(img)
    
    # We want to find the circle center (cx, cy) and radius R in this 1671x941 card.
    # In the high-res image (2400x1792), the circle was at cx=1200, cy=906, R=765.
    # Let's inspect the transition to the golden border.
    # The golden border in the card should be roughly at similar proportional locations:
    # Proportions in high-res:
    # cx / w = 1200 / 2400 = 0.50
    # cy / h = 906 / 1792 = 0.505
    # R / w = 765 / 2400 = 0.318
    #
    # If the card is 1671x941:
    # Proportional cx = 1671 * 0.50 = 835.5
    # Proportional cy = 941 * 0.505 = 475.2
    # Proportional R = 1671 * 0.318 = 532.6
    # Let's scan along these estimated coordinates to find the exact golden border!
    
    cx_est = 835.5
    cy_est = 475.2
    
    # Let's scan horizontally from center to the right
    # Inside the circle, it is light cream. Outside, it is light cream too, but the border is golden!
    # Golden border has a high R, G but lower B.
    # Let's print the colors from x = 1100 to 1450 at y = 475 to find the right border.
    print("Horizontal scan from x=1100 to 1450 at y=475:")
    for x in range(1100, 1451, 10):
        r, g, b = img.getpixel((x, int(cy_est)))
        print(f"x={x}: R={r}, G={g}, B={b}")
else:
    print("Card image not found!")
