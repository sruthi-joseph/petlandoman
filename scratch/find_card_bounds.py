import os
from PIL import Image
import numpy as np

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_pdf_images\page_8_img_16.png"
if not os.path.exists(img_path):
    print("Source image not found!")
    exit()

img = Image.open(img_path).convert("RGB")
data = np.array(img)
r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]

# Detect yellow pixels (fcc203 corresponds to 252, 194, 3)
# We can use a relaxed threshold to catch all yellow shades in the card
yellow_mask = (r > 230) & (g > 170) & (b < 40)

h, w = yellow_mask.shape

# Let's divide into 4 quadrant regions to find the bounds of each card individually
# Top-Left: y in [0, h//2], x in [0, w//2]
# Top-Right: y in [0, h//2], x in [w//2, w]
# Bottom-Left: y in [h//2, h], x in [0, w//2]
# Bottom-Right: y in [h//2, h], x in [w//2, w]

quadrants = {
    "Nutritional (Top-Left)": (0, 0, w//2, h//2),
    "Obedience (Top-Right)": (w//2, 0, w, h//2),
    "Spa Grooming (Bottom-Left)": (0, h//2, w//2, h),
    "Daycare (Bottom-Right)": (w//2, h//2, w, h)
}

cropped_boxes = {}
print("Detecting Card Bounding Boxes:")
for name, (x1, y1, x2, y2) in quadrants.items():
    quad_mask = yellow_mask[y1:y2, x1:x2]
    ys, xs = np.where(quad_mask)
    if len(ys) > 0:
        # absolute coordinates
        ax1 = x1 + xs.min()
        ax2 = x1 + xs.max()
        ay1 = y1 + ys.min()
        ay2 = y1 + ys.max()
        print(f"  {name}: x = {ax1} to {ax2} (width {ax2 - ax1 + 1}), y = {ay1} to {ay2} (height {ay2 - ay1 + 1})")
        cropped_boxes[name] = (ax1, ay1, ax2 + 1, ay2 + 1)
    else:
        print(f"  {name}: No yellow pixels found!")

# Let's crop and save them perfectly cropped
out_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"
for name, box in cropped_boxes.items():
    short_name = "card_" + name.split()[0].lower().replace("(", "")
    if "nutritional" in short_name:
        fn = "card_nutritional.png"
    elif "obedience" in short_name:
        fn = "card_obedience.png"
    elif "spa" in short_name:
        fn = "card_grooming.png"
    else:
        fn = "card_daycare.png"
        
    cropped = img.crop(box)
    cropped.save(os.path.join(out_dir, fn))
    print(f"Saved perfectly cropped {fn} from box {box}")
