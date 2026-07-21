import os
import shutil
import numpy as np
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

logo_trans_path = os.path.join(image_dir, "logo_transparent.png")
logo_white_path = os.path.join(image_dir, "logo_white_transparent.png")

# Backups
logo_trans_backup = os.path.join(image_dir, "logo_transparent_backup_phone.png")
logo_white_backup = os.path.join(image_dir, "logo_white_transparent_backup_phone.png")

print("1. Creating backups...")
shutil.copy2(logo_trans_path, logo_trans_backup)
print(f"Backed up logo_transparent.png to {logo_trans_backup}")
shutil.copy2(logo_white_path, logo_white_backup)
print(f"Backed up logo_white_transparent.png to {logo_white_backup}")

def erase_phone_number(img_path):
    print(f"\nProcessing {img_path}...")
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    print(f"Current dimensions: {w}x{h}")
    
    # Convert to numpy array to easily manipulate rows
    arr = np.array(img)
    
    # Set rows 1050 to 1151 (inclusive) to transparent (alpha = 0)
    # We clear the entire width (0 to w)
    arr[1050:1152, :, 3] = 0
    
    # Save back
    new_img = Image.fromarray(arr, "RGBA")
    new_img.save(img_path, format="PNG")
    print(f"Saved modified image to {img_path} (new size: {new_img.size})")
    return new_img

# Process both logos
new_trans = erase_phone_number(logo_trans_path)
new_white = erase_phone_number(logo_white_path)

print("\n2. Generating verification crops...")
# Crop Y=1000 to 1152 to verify the change
crop_trans = new_trans.crop((0, 1000, new_trans.width, 1152))
bbox_trans = crop_trans.getbbox()
if bbox_trans:
    crop_trans.crop(bbox_trans).save(os.path.join(artifact_dir, "verify_bottom_transparent.png"))
    print("Saved verify_bottom_transparent.png")
else:
    print("verify_bottom_transparent.png: Empty (no active pixels in bottom region)")

crop_white = new_white.crop((0, 1000, new_white.width, 1152))
bbox_white = crop_white.getbbox()
if bbox_white:
    # paste on black bg
    cropped_img = crop_white.crop(bbox_white)
    bg = Image.new("RGBA", cropped_img.size, (30, 30, 30, 255))
    bg.paste(cropped_img, (0, 0), cropped_img)
    bg.save(os.path.join(artifact_dir, "verify_bottom_white.png"))
    print("Saved verify_bottom_white.png")
else:
    print("verify_bottom_white.png: Empty (no active pixels in bottom region)")

print("\nProcessing complete!")
