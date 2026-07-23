from PIL import Image
import os
import numpy as np

def compare(p1, p2, name):
    if not os.path.exists(p1) or not os.path.exists(p2):
        print(f"{name}: One or both files do not exist!")
        return
    img1 = Image.open(p1)
    img2 = Image.open(p2)
    if img1.size == img2.size and img1.mode == img2.mode:
        diff = np.abs(np.array(img1).astype(int) - np.array(img2).astype(int))
        print(f"{name}: Size={img1.size}, Mode={img1.mode}, identical={diff.max() == 0}, max_diff={diff.max()}, mean_diff={diff.mean():.4f}")
    else:
        print(f"{name}: Different size or mode: {img1.size}/{img1.mode} vs {img2.size}/{img2.mode}")

compare("scratch/orig_card.jpeg", "scratch/head_pet_food.jpeg", "orig_card vs head_pet_food")
compare("scratch/orig_card.jpeg", "assets/images/product_card_images/pet food.jpeg", "orig_card vs current_pet_food")
compare("scratch/orig_product_1.png", "scratch/head_product_1.png", "orig_product_1 vs head_product_1")
compare("scratch/orig_product_1.png", "assets/images/extracted_images/product_1.png", "orig_product_1 vs current_product_1")
