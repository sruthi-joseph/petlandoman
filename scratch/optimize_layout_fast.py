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

# Get boundary points of each bag mask
def get_boundary_points(bag):
    alpha = np.array(bag.split()[3]) > 0
    # Use simple gradient to find boundary
    import scipy.ndimage as ndimage
    eroded = ndimage.binary_erosion(alpha)
    boundary = alpha & ~eroded
    ys, xs = np.where(boundary)
    # Normalize coordinates to range [0, 1] relative to bag size
    h, w = alpha.shape
    return ys / h, xs / w

ys_c, xs_c = get_boundary_points(bag_center)
ys_l, xs_l = get_boundary_points(bag_left)
ys_r, xs_r = get_boundary_points(bag_right)

print(f"Boundary points count: Center: {len(xs_c)}, Left: {len(xs_l)}, Right: {len(xs_r)}")

best_h_c = 0
best_params = {}

for h_c in range(950, 1350, 10):
    for scale_ratio in [0.80, 0.82, 0.85, 0.88, 0.90]:
        h_s = int(h_c * scale_ratio)
        
        w_c = int(bag_center.width * (h_c / bag_center.height))
        w_l = int(bag_left.width * (h_s / bag_left.height))
        w_r = int(bag_right.width * (h_s / bag_right.height))
        
        # Real pixel coordinates of boundaries
        c_x_rel = (xs_c * w_c).astype(np.int32)
        c_y_rel = (ys_c * h_c).astype(np.int32)
        
        l_x_rel = (xs_l * w_l).astype(np.int32)
        l_y_rel = (ys_l * h_s).astype(np.int32)
        
        r_x_rel = (xs_r * w_r).astype(np.int32)
        r_y_rel = (ys_r * h_s).astype(np.int32)
        
        # Grid search for positions
        dx_min = int(w_c * 0.35)
        dx_max = int(w_c * 0.55)
        
        for dx in range(dx_min, dx_max, 10):
            for y_c_bottom in range(cy + 250, cy + 450, 10):
                for dy_s in range(0, 150, 10):
                    y_s_bottom = y_c_bottom - dy_s
                    
                    # Coordinates on the global canvas
                    c_x_glob = cx - w_c // 2 + c_x_rel
                    c_y_glob = y_c_bottom - h_c + c_y_rel
                    
                    l_x_glob = cx - dx - w_l // 2 + l_x_rel
                    l_y_glob = y_s_bottom - h_s + l_y_rel
                    
                    r_x_glob = cx + dx - w_r // 2 + r_x_rel
                    r_y_glob = y_s_bottom - h_s + r_y_rel
                    
                    # Combine all global coordinates
                    all_x = np.concatenate([c_x_glob, l_x_glob, r_x_glob])
                    all_y = np.concatenate([c_y_glob, l_y_glob, r_y_glob])
                    
                    # Compute distance from (cx, cy)
                    dists_sq = (all_x - cx)**2 + (all_y - cy)**2
                    max_dist = np.sqrt(dists_sq.max())
                    
                    if max_dist <= R_max:
                        # Check overlap constraints
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
