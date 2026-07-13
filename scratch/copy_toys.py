import os
import shutil

src_dir = r"c:\Users\SRUTHI\Desktop\petland oman\products-pet toys and fun"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\product list\toys"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

files = os.listdir(src_dir)
print(f"Found {len(files)} files to copy.")

for f in files:
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        src_path = os.path.join(src_dir, f)
        # Replace spaces with underscores and lowercase the extension
        clean_name = f.replace(" ", "_")
        name_part, ext_part = os.path.splitext(clean_name)
        clean_name = name_part + ext_part.lower()
        
        dest_path = os.path.join(dest_dir, clean_name)
        shutil.copy(src_path, dest_path)
        print(f"  Copied: {f} -> {clean_name}")
