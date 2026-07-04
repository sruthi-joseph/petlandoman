from PIL import Image
import os

path = r"c:\Users\SRUTHI\Desktop\petland oman\grooming services.jpeg"
img = Image.open(path)
w, h = img.size

# Let's crop the three pet images from the flyer.
# Based on flyer layout (width=2400, height=1792):
# 1. White dog (top right)
# 2. Orange cat (middle left)
# 3. Dark dog (bottom right)

# Let's save a few different crop coordinates to verify or use.
os.makedirs("extracted_images", exist_ok=True)

# White dog in top right:
# Let's crop from x: 1350 to 2250 (width 900) and y: 300 to 1100 (height 800)
white_dog = img.crop((1350, 300, 2250, 1100))
white_dog.save("extracted_images/grooming_shower_dog.png")

# Orange cat in middle left:
# Let's crop from x: 150 to 1100 (width 950) and y: 650 to 1550 (height 900)
orange_cat = img.crop((150, 650, 1100, 1550))
orange_cat.save("extracted_images/grooming_haircut_cat.png")

# Dark dog in bottom right:
# Let's crop from x: 1350 to 2250 (width 900) and y: 950 to 1750 (height 800)
dark_dog = img.crop((1350, 950, 2250, 1750))
dark_dog.save("extracted_images/grooming_deshedding_dog.png")

print("Crops created successfully!")
