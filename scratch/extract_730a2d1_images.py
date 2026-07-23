import subprocess
import os

files_to_extract = [
    ("assets/images/extracted_images/card_prod_food_new.png", "scratch/730a2d1_card_prod_food_new.png"),
    ("assets/images/extracted_images/product_1.png", "scratch/730a2d1_product_1.png"),
    ("assets/images/product_card_images/pet food.jpeg", "scratch/730a2d1_pet_food.jpeg")
]

for git_path, local_path in files_to_extract:
    cmd = ["git", "show", f"730a2d1:{git_path}"]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        with open(local_path, "wb") as f:
            f.write(proc.stdout)
        print(f"Extracted 730a2d1:{git_path} to {local_path} (Size: {len(proc.stdout)} bytes)")
    except Exception as e:
        print(f"Failed to extract {git_path}: {e}")
