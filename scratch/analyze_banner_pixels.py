from PIL import Image
import numpy as np

for name in ["landing banner-pet products.png", "landing banner-pet services.png"]:
    p = rf"c:\Users\SRUTHI\Desktop\petland oman\assets\images\{name}"
    img = Image.open(p).convert("RGB")
    data = np.array(img)
    h, w, c = data.shape
    
    # Check top-left corner
    print(f"\n=== {name} ===")
    print("Top-left pixel (0,0) color:", data[0, 0])
    print("Top-right pixel (0, w-1) color:", data[0, w-1])
    print("Bottom-left pixel (h-1, 0) color:", data[h-1, 0])
    print("Bottom-right pixel (h-1, w-1) color:", data[h-1, w-1])
    
    # Check if there is a flat white border all around the image.
    # Let's count how many rows/cols at the edges are completely white (i.e. RGB all >= 254)
    top_white_rows = 0
    for y in range(h):
        if np.all(data[y, :, :] >= 254):
            top_white_rows += 1
        else:
            break
            
    bottom_white_rows = 0
    for y in range(h - 1, -1, -1):
        if np.all(data[y, :, :] >= 254):
            bottom_white_rows += 1
        else:
            break
            
    left_white_cols = 0
    for x in range(w):
        if np.all(data[:, x, :] >= 254):
            left_white_cols += 1
        else:
            break
            
    right_white_cols = 0
    for x in range(w - 1, -1, -1):
        if np.all(data[:, x, :] >= 254):
            right_white_cols += 1
        else:
            break
            
    print(f"Completely white borders: top={top_white_rows}, bottom={bottom_white_rows}, left={left_white_cols}, right={right_white_cols}")
