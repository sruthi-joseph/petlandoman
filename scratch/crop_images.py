from PIL import Image
import os

crop_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\cropped_images"
os.makedirs(crop_dir, exist_ok=True)

def crop_and_save(label, path):
    if not os.path.exists(path):
        print(f"{label} does not exist")
        return
    with Image.open(path) as img:
        bbox = img.getbbox()
        if bbox:
            cropped = img.crop(bbox)
            out_path = os.path.join(crop_dir, f"{label}_cropped.png")
            cropped.save(out_path)
            print(f"Cropped {label} to {cropped.size} and saved to {out_path}")
        else:
            print(f"{label} is empty")

crop_and_save("existing_logo_transparent", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png")
crop_and_save("existing_logo_white_transparent", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_white_transparent.png")

folder = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images"
for f in sorted(os.listdir(folder)):
    if f.endswith(".png") or f.endswith(".jpg"):
        crop_and_save(f.replace(".", "_"), os.path.join(folder, f))
