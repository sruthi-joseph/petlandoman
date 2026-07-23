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

# Load bags
hairball_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL\26297.webp"
maxi_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI\25489.webp"
kitten_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36813.webp"

bag_left = segment_bag(hairball_path)
bag_center = segment_bag(maxi_path)
bag_right = segment_bag(kitten_path)

cx, cy = 1200, 906
R_max = 765

# Let's test a candidate layout
# Height of center: h_c, height of side: h_s
# dx: horizontal shift
# y_c_bottom, y_s_bottom: bottoms
# Let's try h_c = 1100, scale = 0.85 (h_s = 935), dx = 330, y_c_bottom = 1420, y_s_bottom = 1380
h_c = 1100
h_s = 935
dx = 330
y_c_bottom = 1420
y_s_bottom = 1380

w_c = int(bag_center.width * (h_c / bag_center.height))
w_l = int(bag_left.width * (h_s / bag_left.height))
w_r = int(bag_right.width * (h_s / bag_right.height))

# Check pixels
def get_global_pixels(bag, w_new, h_new, x_center, y_bottom):
    resized = bag.resize((w_new, h_new), Image.Resampling.BILINEAR)
    alpha = np.array(resized.split()[3]) > 0
    ys, xs = np.where(alpha)
    glob_x = x_center - w_new // 2 + xs
    glob_y = y_bottom - h_new + ys
    return glob_x, glob_y

cx_c, cy_c = get_global_pixels(bag_center, w_c, h_c, cx, y_c_bottom)
cx_l, cy_l = get_global_pixels(bag_left, w_l, h_s, cx - dx, y_s_bottom)
cx_r, cy_r = get_global_pixels(bag_right, w_r, h_s, cx + dx, y_s_bottom)

all_x = np.concatenate([cx_c, cx_l, cx_r])
all_y = np.concatenate([cy_c, cy_l, cy_r])

dists = np.sqrt((all_x - cx)**2 + (all_y - cy)**2)
max_dist = dists.max()
print(f"Candidate layout results:")
print(f"  Max pixel distance: {max_dist:.2f} (Radius limit: {R_max})")
print(f"  Fits in circle? {max_dist <= R_max}")
print(f"  Center bottom y: {y_c_bottom}, Side bottom y: {y_s_bottom}")
print(f"  Overlaps:")
print(f"    Left edge of center bag: {cx - w_c // 2}")
print(f"    Right edge of left bag: {cx - dx + w_l // 2}")
print(f"    Right edge of center bag: {cx + w_c // 2}")
print(f"    Left edge of right bag: {cx + dx - w_r // 2}")
