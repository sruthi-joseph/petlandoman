import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

os.makedirs(artifact_dir, exist_ok=True)

# 1. logo.png (no crop, just copy)
logo_path = os.path.join(image_dir, "logo.png")
if os.path.exists(logo_path):
    img = Image.open(logo_path)
    img.save(os.path.join(artifact_dir, "logo_crop.png"))
    print("Saved logo_crop.png")

# 2. logo_transparent.png (crop to non-transparent bbox)
logo_trans_path = os.path.join(image_dir, "logo_transparent.png")
if os.path.exists(logo_trans_path):
    img = Image.open(logo_trans_path)
    bbox = img.getbbox()
    if bbox:
        cropped = img.crop(bbox)
        cropped.save(os.path.join(artifact_dir, "logo_trans_crop.png"))
        print(f"Saved logo_trans_crop.png (bbox={bbox})")

# 3. logo_white_transparent.png (crop and paste on a dark background so it is visible)
logo_white_path = os.path.join(image_dir, "logo_white_transparent.png")
if os.path.exists(logo_white_path):
    img = Image.open(logo_white_path)
    bbox = img.getbbox()
    if bbox:
        cropped = img.crop(bbox)
        # paste on black bg
        bg = Image.new("RGBA", cropped.size, (30, 30, 30, 255))
        bg.paste(cropped, (0, 0), cropped)
        bg.save(os.path.join(artifact_dir, "logo_white_crop.png"))
        print(f"Saved logo_white_crop.png (bbox={bbox})")
