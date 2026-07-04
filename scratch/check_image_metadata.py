import os
import time

brain_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\d7344ec0-3c55-4d54-9497-0adca2bc614e"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

files_map = {
    "grooming_shower_1782985193264.png": "grooming_shower.png",
    "grooming_haircut_1782985216768.png": "grooming_haircut.png",
    "grooming_deshedding_1782985233345.png": "grooming_deshedding.png",
    "grooming_full_1782985251369.png": "grooming_full.png",
    "grooming_medicated_1782985875259.png": "grooming_medicated.png"
}

for src_name, dest_name in files_map.items():
    src_path = os.path.join(brain_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if os.path.exists(src_path):
        src_mtime = time.ctime(os.path.getmtime(src_path))
        src_size = os.path.getsize(src_path)
        print(f"Original: {src_name} | Size: {src_size} | Modified: {src_mtime}")
    else:
        print(f"Original NOT FOUND: {src_path}")
        
    if os.path.exists(dest_path):
        dest_mtime = time.ctime(os.path.getmtime(dest_path))
        dest_size = os.path.getsize(dest_path)
        print(f"Destination: {dest_name} | Size: {dest_size} | Modified: {dest_mtime}")
    else:
        print(f"Destination NOT FOUND: {dest_path}")
    print("-" * 50)
