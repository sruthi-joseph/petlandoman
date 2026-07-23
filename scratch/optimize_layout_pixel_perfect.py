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

cx, cy = 1200, 906
R_max = 760  # safety margin

# We will search for:
# - Center height h_c from 900 to 1400
# - Scale ratio s_r from 0.8 to 0.9
# - dx (offset of side bags) from 250 to w_c // 2 + w_s // 4
# - y_c_bottom (bottom of center bag) from cy + 200 to cy + 500
# - dy_s (vertical offset of side bags relative to center bottom) from 0 to 150
# To speed up, we can do a coarse search and then fine search.

best_h_c = 0
best_params = {}

for h_c in range(950, 1350, 20):
    for scale_ratio in [0.80, 0.85, 0.90]:
        h_s = int(h_c * scale_ratio)
        
        w_c = int(bag_center.width * (h_c / bag_center.height))
        w_l = int(bag_left.width * (h_s / bag_left.height))
        w_r = int(bag_right.width * (h_s / bag_right.height))
        
        # Calculate alpha arrays for the resized bags
        mask_c = np.array(bag_center.split()[3].resize((w_c, h_c), Image.Resampling.BILINEAR)) > 0
        mask_l = np.array(bag_left.split()[3].resize((w_l, h_s), Image.Resampling.BILINEAR)) > 0
        mask_r = np.array(bag_right.split()[3].resize((w_r, h_s), Image.Resampling.BILINEAR)) > 0
        
        # Get coordinates of product pixels relative to their own box
        ys_c, xs_c = np.where(mask_c)
        ys_l, xs_l = np.where(mask_l)
        ys_r, xs_r = np.where(mask_r)
        
        # Coarse grid search for positions
        for dx in range(int(w_c * 0.35), int(w_c * 0.55), 20):
            for y_c_bottom in range(cy + 250, cy + 450, 20):
                for dy_s in [0, 30, 60, 90]:
                    y_s_bottom = y_c_bottom - dy_s
                    
                    # Coordinates on the global canvas:
                    # Center bag:
                    c_x_glob = cx - w_c // 2 + xs_c
                    c_y_glob = y_c_bottom - h_c + ys_c
                    
                    # Left bag:
                    l_x_glob = cx - dx - w_l // 2 + xs_l
                    l_y_glob = y_s_bottom - h_s + ys_l
                    
                    # Right bag:
                    r_x_glob = cx + dx - w_r // 2 + xs_r
                    r_y_glob = y_s_bottom - h_s + ys_r
                    
                    # Combine all global coordinates
                    all_x = np.concatenate([c_x_glob, l_x_glob, r_x_glob])
                    all_y = np.concatenate([c_y_glob, l_y_glob, r_y_glob])
                    
                    # Compute distance from (cx, cy)
                    dists_sq = (all_x - cx)**2 + (all_y - cy)**2
                    max_dist = np.sqrt(dists_sq.max())
                    
                    if max_dist <= R_max:
                        # Ensure side bags don't overlap too much or too little
                        # The left edge of the right bag is: cx + dx - w_r // 2
                        # The right edge of the center bag is: cx + w_c // 2
                        # We want some overlap, e.g. left edge of right bag should be less than right edge of center bag,
                        # but not too far to the left.
                        right_edge_c = cx + w_c // 2
                        left_edge_r = cx + dx - w_r // 2
                        overlap_r = right_edge_c - left_edge_r
                        
                        if 100 < overlap_r < w_r * 0.4:
                            if h_c > best_h_c:
                                best_h_c = h_c
                                best_params = {
                                    "h_c": h_c,
                                    "h_s": h_s,
                                    "dx": dx,
                                    "y_c_bottom": y_c_bottom,
                                    "y_s_bottom": y_s_bottom,
                                    "scale_ratio": scale_ratio,
                                    "max_dist": max_dist
                                }

print(f"Best pixel-perfect center height: {best_h_c}")
print(f"Best parameters: {best_params}")
