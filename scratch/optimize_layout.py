import os
import numpy as np
from PIL import Image

def segment_bag(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    from PIL import ImageDraw
    temp_img = img.copy()
    ImageDraw.floodfill(temp_img, (0, 0), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (w - 1, 0), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (0, h - 1), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (w - 1, h - 1), (0, 0, 0, 0), thresh=10)
    alpha = temp_img.split()[3]
    bbox = alpha.getbbox()
    if bbox:
        cropped = img.crop(bbox)
        mask = alpha.crop(bbox)
        cropped.putalpha(mask)
        return cropped
    return None

# Load the three bags
hairball_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL\26297.webp"
maxi_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI\25489.webp"
kitten_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36813.webp"

bag_left = segment_bag(hairball_path)
bag_center = segment_bag(maxi_path)
bag_right = segment_bag(kitten_path)

print(f"Left bag size: {bag_left.size}")
print(f"Center bag size: {bag_center.size}")
print(f"Right bag size: {bag_right.size}")

# Let's search for layout parameters:
# Center bag height: h_c
# Side bag height: h_s
# Horizontal offset: dx
# Vertical center offset: dy (where the bottom of center bag is relative to circle center 906)
# We want to make the bags as large as possible, so we'll search for the maximum h_c.
# We'll set h_s = h_c * scale_ratio (e.g. scale_ratio = 0.85)

cx, cy = 1200, 906
R_max = 760 # leave 5px safety margin from the inner circle border (765)

best_h_c = 0
best_params = {}

# Grid search for the largest center height that fits completely inside the circle
for h_c in range(800, 1300, 10):
    for scale_ratio in [0.80, 0.82, 0.85, 0.88, 0.90]:
        h_s = int(h_c * scale_ratio)
        
        # Determine sizes of resized bags
        w_c = int(bag_center.width * (h_c / bag_center.height))
        w_l = int(bag_left.width * (h_s / bag_left.height))
        w_r = int(bag_right.width * (h_s / bag_right.height))
        
        # Grid search for dx and vertical alignment
        # dx is the shift of left/right bag centers from the center 1200.
        # We want the side bags to overlap nicely, but not too much.
        # Typically dx is around w_c / 2 + w_s / 4
        dx_min = int(w_c * 0.4)
        dx_max = int(w_c * 0.6)
        
        for dx in range(dx_min, dx_max, 10):
            # y_c_bottom is the bottom y-coord of the center bag.
            # We want the bottoms of all bags to fit inside the circle.
            # Let's try bottom positions for center bag relative to cy
            for y_c_bottom in range(cy + 200, cy + 500, 10):
                # Side bags bottom alignment: they can be slightly higher
                # Let's try side bags bottom at y_c_bottom - dy_s
                for dy_s in range(0, 150, 10):
                    y_s_bottom = y_c_bottom - dy_s
                    
                    # Compute bounding boxes of the three bags in the canvas (2400x1792)
                    # Center bag:
                    c_x1 = cx - w_c // 2
                    c_y1 = y_c_bottom - h_c
                    c_x2 = c_x1 + w_c
                    c_y2 = y_c_bottom
                    
                    # Left bag:
                    l_x1 = cx - dx - w_l // 2
                    l_y1 = y_s_bottom - h_s
                    l_x2 = l_x1 + w_l
                    l_y2 = y_s_bottom
                    
                    # Right bag:
                    r_x1 = cx + dx - w_r // 2
                    r_y1 = y_s_bottom - h_s
                    r_x2 = r_x1 + w_r
                    r_y2 = y_s_bottom
                    
                    # Check if the bounding boxes are within the circle's bounding box to speed up
                    if (l_x1 < cx - R_max or r_x2 > cx + R_max or 
                        c_y1 < cy - R_max or c_y2 > cy + R_max or
                        l_y1 < cy - R_max or r_y1 < cy - R_max or
                        l_y2 > cy + R_max or r_y2 > cy + R_max):
                        continue
                        
                    # Let's verify pixel-perfect containment
                    # We will sample the boundary pixels of the resized bags' masks
                    # and check if they are all within R_max of (cx, cy).
                    # For a resized bag at (x1, y1), its pixel at (x, y) relative to the bag
                    # maps to (x1 + x, y1 + y) in the canvas.
                    
                    # Since checking all pixels is slow, we can just check the bounding boxes' corners
                    # and some outer boundary points. Or we can resize the alpha masks and check.
                    # Let's do a quick mathematical check on the corners of the bags.
                    # Since the bags are roughly rectangular, if their top-left, top-right, bottom-left, bottom-right corners
                    # are within the circle, the rest is very likely inside.
                    # Let's check the corners of each bag:
                    corners = [
                        (c_x1, c_y1), (c_x2, c_y1), (c_x1, c_y2), (c_x2, c_y2),
                        (l_x1, l_y1), (l_x2, l_y1), (l_x1, l_y2), (l_x2, l_y2),
                        (r_x1, r_y1), (r_x2, r_y1), (r_x1, r_y2), (r_x2, r_y2)
                    ]
                    
                    outside = False
                    for x, y in corners:
                        if (x - cx)**2 + (y - cy)**2 > R_max**2:
                            outside = True
                            break
                            
                    if not outside:
                        # Found a valid layout!
                        if h_c > best_h_c:
                            best_h_c = h_c
                            best_params = {
                                "h_c": h_c,
                                "h_s": h_s,
                                "dx": dx,
                                "y_c_bottom": y_c_bottom,
                                "y_s_bottom": y_s_bottom,
                                "scale_ratio": scale_ratio
                            }

print(f"Best center height: {best_h_c}")
print(f"Best parameters: {best_params}")
