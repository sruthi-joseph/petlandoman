import os
import numpy as np
from PIL import Image

def segment_and_cut_shadow(path, y_bottom_crop):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    
    # Flood-fill background from corners
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
    
    # We crop the bottom at y_bottom_crop
    # Note that y_bottom_crop is relative to the original image coordinate!
    # Let's crop y from y_min to y_bottom_crop, and x from x_min to x_max
    cropped_img = img.crop((x_min, y_min, x_max, y_bottom_crop))
    cropped_alpha = alpha.crop((x_min, y_min, x_max, y_bottom_crop))
    
    # Apply clean mask (erode slightly to remove white fringes)
    import scipy.ndimage as ndimage
    mask_arr = np.array(cropped_alpha) > 0
    eroded = ndimage.binary_erosion(mask_arr, iterations=1)
    clean_mask = Image.fromarray((eroded * 255).astype(np.uint8))
    
    cropped_img.putalpha(clean_mask)
    return cropped_img

hairball_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL\26297.webp"
maxi_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI\25489.webp"
kitten_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36813.webp"

# Let's test these crop bounds
bag_left = segment_and_cut_shadow(hairball_path, 1163)
bag_center = segment_and_cut_shadow(maxi_path, 1166)
bag_right = segment_and_cut_shadow(kitten_path, 1230)

print(f"Left bag (Hairball) size: {bag_left.size}")
print(f"Center bag (Maxi) size: {bag_center.size}")
print(f"Right bag (Kitten) size: {bag_right.size}")

# Let's verify the bottom 5 rows of each cropped image to see if there is any white/grey shadow
for name, bag in [("Hairball", bag_left), ("Maxi", bag_center), ("Kitten", bag_right)]:
    print(f"\n{name} bottom rows average color:")
    arr = np.array(bag)
    h, w, c = arr.shape
    for y_offset in range(5):
        y = h - 1 - y_offset
        row = arr[y, :, :]
        alpha = row[:, 3]
        prod_pixels = row[alpha > 0, :3]
        if len(prod_pixels) > 0:
            avg_color = prod_pixels.mean(axis=0)
            print(f"  Row {y_offset} (y={y}): active_pixels={len(prod_pixels)}, avg={avg_color.round(1)}")
        else:
            print(f"  Row {y_offset} (y={y}): no active pixels")
