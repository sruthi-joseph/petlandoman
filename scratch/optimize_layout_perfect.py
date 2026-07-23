import os
import numpy as np
from PIL import Image

def segment_and_cut_shadow(path, y_bottom_crop):
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
    if not bbox:
        return None
    x_min, y_min, x_max, y_max = bbox
    cropped_img = img.crop((x_min, y_min, x_max, y_bottom_crop))
    cropped_alpha = alpha.crop((x_min, y_min, x_max, y_bottom_crop))
    
    # Erode to clean up edges
    import scipy.ndimage as ndimage
    mask_arr = np.array(cropped_alpha) > 0
    eroded = ndimage.binary_erosion(mask_arr, iterations=1)
    clean_mask = Image.fromarray((eroded * 255).astype(np.uint8))
    cropped_img.putalpha(clean_mask)
    return cropped_img

hairball_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL\26297.webp"
maxi_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI\25489.webp"
kitten_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36813.webp"

bag_left = segment_and_cut_shadow(hairball_path, 1163)
bag_center = segment_and_cut_shadow(maxi_path, 1166)
bag_right = segment_and_cut_shadow(kitten_path, 1230)

cx, cy = 1200, 906
R_max = 760

def get_boundary_points(bag):
    alpha = np.array(bag.split()[3]) > 0
    import scipy.ndimage as ndimage
    eroded = ndimage.binary_erosion(alpha)
    boundary = alpha & ~eroded
    ys, xs = np.where(boundary)
    h, w = alpha.shape
    xs_ds = xs[::8]
    ys_ds = ys[::8]
    return ys_ds / h, xs_ds / w

ys_c, xs_c = get_boundary_points(bag_center)
ys_l, xs_l = get_boundary_points(bag_left)
ys_r, xs_r = get_boundary_points(bag_right)

best_h_c = 0
best_params = {}

for h_c in range(850, 1250, 10):
    for scale_ratio in [0.75, 0.80, 0.83, 0.85]:
        h_s = int(h_c * scale_ratio)
        
        w_c = int(bag_center.width * (h_c / bag_center.height))
        w_l = int(bag_left.width * (h_s / bag_left.height))
        w_r = int(bag_right.width * (h_s / bag_right.height))
        
        c_x_rel = (xs_c * w_c).astype(np.int32)
        c_y_rel = (ys_c * h_c).astype(np.int32)
        
        l_x_rel = (xs_l * w_l).astype(np.int32)
        l_y_rel = (ys_l * h_s).astype(np.int32)
        
        r_x_rel = (xs_r * w_r).astype(np.int32)
        r_y_rel = (ys_r * h_s).astype(np.int32)
        
        dx_min = int(w_c * 0.35)
        dx_max = int(w_c * 0.55)
        
        for dx in range(dx_min, dx_max, 10):
            for y_c_bottom in range(cy + 250, cy + 450, 10):
                for dy_s in [0, 25, 50, 75]:
                    y_s_bottom = y_c_bottom - dy_s
                    
                    c_x_glob = cx - w_c // 2 + c_x_rel
                    c_y_glob = y_c_bottom - h_c + c_y_rel
                    
                    l_x_glob = cx - dx - w_l // 2 + l_x_rel
                    l_y_glob = y_s_bottom - h_s + l_y_rel
                    
                    r_x_glob = cx + dx - w_r // 2 + r_x_rel
                    r_y_glob = y_s_bottom - h_s + r_y_rel
                    
                    all_x = np.concatenate([c_x_glob, l_x_glob, r_x_glob])
                    all_y = np.concatenate([c_y_glob, l_y_glob, r_y_glob])
                    
                    dists_sq = (all_x - cx)**2 + (all_y - cy)**2
                    max_dist = np.sqrt(dists_sq.max())
                    
                    if max_dist <= R_max:
                        right_edge_l = cx - dx + w_l // 2
                        left_edge_c = cx - w_c // 2
                        right_edge_c = cx + w_c // 2
                        left_edge_r = cx + dx - w_r // 2
                        
                        if right_edge_l > left_edge_c + 50 and left_edge_r < right_edge_c - 50:
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
