from PIL import Image
import os

images = {
    "730a2d1_pet_food.jpeg": "scratch/730a2d1_pet_food.jpeg",
    "head_pet_food.jpeg": "scratch/head_pet_food.jpeg",
    "current_pet_food.jpeg": "assets/images/product_card_images/pet food.jpeg",
    "730a2d1_card_prod_food_new.png": "scratch/730a2d1_card_prod_food_new.png",
    "head_card_prod_food_new.png": "scratch/head_card_prod_food_new.png",
    "current_card_prod_food_new.png": "assets/images/extracted_images/card_prod_food_new.png",
    "730a2d1_product_1.png": "scratch/730a2d1_product_1.png",
    "head_product_1.png": "scratch/head_product_1.png",
    "current_product_1.png": "assets/images/extracted_images/product_1.png"
}

for name, path in images.items():
    if os.path.exists(path):
        with Image.open(path) as img:
            print(f"{name}: size={img.size}, mode={img.mode}")
    else:
        print(f"{name} does not exist!")
