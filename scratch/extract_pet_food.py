import os
import zipfile

src_dir = r"c:\Users\SRUTHI\Desktop\petland oman\products-pet food\royal canin"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\product list\pet food"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

zip_files = [f for f in os.listdir(src_dir) if f.lower().endswith(".zip")]

for zf in zip_files:
    zip_path = os.path.join(src_dir, zf)
    print(f"Extracting {zf}...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        # Extract files
        for member in zip_ref.namelist():
            # Check if it's a file, not a directory
            if not member.endswith("/"):
                # Clean name: remove directory prefix if any
                base_name = os.path.basename(member)
                # Keep it in a subfolder named after the zip base name (e.g. HAIRBALL, INDOOR)
                sub_folder_name = os.path.splitext(zf)[0].upper()
                target_sub_folder = os.path.join(dest_dir, sub_folder_name)
                if not os.path.exists(target_sub_folder):
                    os.makedirs(target_sub_folder)
                
                target_path = os.path.join(target_sub_folder, base_name)
                with open(target_path, "wb") as f_out:
                    f_out.write(zip_ref.read(member))
                print(f"  Extracted: {member} -> {target_path}")
