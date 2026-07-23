from PIL import Image
import os
import numpy as np

pairs = [
    ("card_prod_food_new.png", "scratch/head_card_prod_food_new.png", "assets/images/extracted_images/card_prod_food_new.png"),
    ("product_1.png", "scratch/head_product_1.png", "assets/images/extracted_images/product_1.png"),
    ("pet food.jpeg", "scratch/head_pet_food.jpeg", "assets/images/product_card_images/pet food.jpeg"),
    ("pet_food card.jpeg", "scratch/head_pet_food_card.jpeg", "assets/images/product_card_images/pet_food card.jpeg")
]

for name, head_p, curr_p in pairs:
    print(f"=== {name} ===")
    if not os.path.exists(head_p) or not os.path.exists(curr_p):
        print("One of the files is missing!")
        continue
    img_head = Image.open(head_p)
    img_curr = Image.open(curr_p)
    print(f"HEAD: Size={img_head.size}, Mode={img_head.mode}")
    print(f"CURR: Size={img_curr.size}, Mode={img_curr.mode}")
    
    # Check if they are pixel-identical
    if img_head.size == img_curr.size and img_head.mode == img_curr.mode:
        arr_head = np.array(img_head)
        arr_curr = np.array(img_curr)
        diff = np.abs(arr_head.astype(int) - arr_curr.astype(int))
        if diff.max() == 0:
            print("Pixel identical: YES")
        else:
            print(f"Pixel identical: NO, max difference={diff.max()}, mean diff={diff.mean():.4f}")
    else:
        print("Pixel identical: NO (different sizes/modes)")
