import os
import numpy as np
from PIL import Image
from scipy.optimize import least_squares

card_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet food.jpeg"
if os.path.exists(card_path):
    img = Image.open(card_path).convert("RGB")
    w, h = img.size
    arr = np.array(img)
    
    # Let's find the circle center in the card.
    # We can scan inwards from the borders of the card.
    # Outside the circle, the card background might be light or dark.
    # Let's inspect some pixels:
    print("Corner pixels:")
    print("  (0, 0):", arr[0, 0])
    print("  (w-1, 0):", arr[0, -1])
    print("  (0, h-1):", arr[-1, 0])
    print("  (w-1, h-1):", arr[-1, -1])
    
    # Let's scan horizontally at cy = 470
    cy_est = 470
    cx_est = 835
    
    # Let's find boundary points by checking where the color goes from light cream to dark background
    # (since the original circle has a dark background around it? Or wait! Does the card have a dark background around the circle?)
    # Let's print the colors along the center horizontal line to see if there is a dark region.
    print("\nHorizontal scan at y=470:")
    for x in range(0, w, 100):
        print(f"  x={x}: {arr[cy_est, x]}")
else:
    print("Card image not found!")
