import shutil
import os

brain_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\d7344ec0-3c55-4d54-9497-0adca2bc614e"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

images_map = {
    "grooming_shower_1782985193264.png": "grooming_shower.png",
    "grooming_haircut_1782985216768.png": "grooming_haircut.png",
    "grooming_deshedding_1782985233345.png": "grooming_deshedding.png",
    "grooming_full_1782985251369.png": "grooming_full.png"
}

os.makedirs(dest_dir, exist_ok=True)

for src_name, dest_name in images_map.items():
    src_path = os.path.join(brain_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"Copied {src_name} to {dest_name}")
    else:
        print(f"Source not found: {src_path}")
