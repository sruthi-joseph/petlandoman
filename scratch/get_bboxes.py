from PIL import Image
import os

def print_bbox(label, img_path):
    try:
        with Image.open(img_path) as img:
            bbox = img.getbbox()
            print(f"{label}: size={img.size}, mode={img.mode}, bbox={bbox}")
    except Exception as e:
        print(f"Error {label}: {e}")

print_bbox("Existing logo_transparent.png", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png")
print_bbox("Existing logo_white_transparent.png", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_white_transparent.png")
print_bbox("Existing logo.png", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo.png")

folder = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images"
for f in sorted(os.listdir(folder)):
    print_bbox(f"Extracted {f}", os.path.join(folder, f))
