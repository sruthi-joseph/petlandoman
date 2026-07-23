import subprocess
import os

files_to_extract = [
    ("assets/images/extracted_images/card_prod_food_new.png", "scratch/head_card_prod_food_new.png"),
    ("assets/images/extracted_images/product_1.png", "scratch/head_product_1.png"),
    ("assets/images/product_card_images/pet food.jpeg", "scratch/head_pet_food.jpeg"),
    ("assets/images/product_card_images/pet_food card.jpeg", "scratch/head_pet_food_card.jpeg")
]

for git_path, local_path in files_to_extract:
    # Run git show HEAD:git_path and write as binary
    cmd = ["git", "show", f"HEAD:{git_path}"]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        with open(local_path, "wb") as f:
            f.write(proc.stdout)
        print(f"Extracted {git_path} to {local_path} (Size: {len(proc.stdout)} bytes)")
    except Exception as e:
        print(f"Failed to extract {git_path}: {e}")
