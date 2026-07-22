from PIL import Image, ImageDraw
import numpy as np

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg"
im = Image.open(img_path).convert("RGBA")

cx, cy = 1200, 896

for r in [700, 720, 725, 730, 740]:
    box = (cx - r, cy - r, cx + r, cy + r)
    cropped = im.crop(box)
    
    mask = Image.new("L", (r * 2, r * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, r * 2, r * 2), fill=255)
    
    cropped.putalpha(mask)
    final_img = cropped.resize((500, 500), Image.Resampling.LANCZOS)
    
    # Check max RGB in corner pixels to verify no dark blue ring remains
    arr = np.array(final_img)
    # Check alpha > 0 pixels near edge
    edge_mask = (arr[:,:,3] > 128)
    min_rgb = arr[:,:,:3][edge_mask].min(axis=0)
    mean_edge_rgb = arr[:,:,:3][edge_mask].mean(axis=0)
    
    print(f"Radius r={r}px -> Edge Mean RGB: {mean_edge_rgb.round(1)}, Edge Min RGB: {min_rgb}")
    final_img.save(f"c:\\Users\\SRUTHI\\Desktop\\petland oman\\scratch\\product_3_no_ring_r{r}.png")
