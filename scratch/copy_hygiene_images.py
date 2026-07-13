import os
import shutil

src_dir = r"c:\Users\SRUTHI\Desktop\petland oman\Hygiene suppliments\bioline\bioline"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\product list\hygiene"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

files = os.listdir(src_dir)
print(f"Found {len(files)} files to copy.")

for f in files:
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif')):
        src_path = os.path.join(src_dir, f)
        
        # Clean and standardize names
        clean_name = f.lower().replace(" ", "_")
        
        # Specific mappings for the known products
        if "earmitetreatment" in clean_name:
            clean_name = "bioline_ear_mite_treatment_30ml.webp"
        elif "kittenshampoo" in clean_name:
            clean_name = "bioline_kitten_shampoo_200ml.webp"
        elif "aloevera-conditioner" in clean_name:
            clean_name = "bioline_aloevera_conditioner.webp"
        elif "beaphar-dental-powder" in clean_name:
            clean_name = "beaphar_dental_powder_75g.webp"
        elif "bioline-ear-care" in clean_name:
            clean_name = "bioline_ear_care_50ml.webp"
        elif "bioline-tear-stain-remover" in clean_name:
            clean_name = "bioline_tear_stain_remover_50ml.webp"
        elif "dry-foam-shampoo" in clean_name:
            clean_name = "bioline_dry_foam_shampoo_220ml.jpg"
        
        dest_path = os.path.join(dest_dir, clean_name)
        shutil.copy(src_path, dest_path)
        print(f"  Copied: {f} -> {clean_name}")

print("All files processed and copied successfully to:", dest_dir)
