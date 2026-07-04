from PIL import Image
import os

pets_path = "extracted_images/footer_pets.png"
if not os.path.exists(pets_path):
    print("footer_pets.png not found")
    exit()

img = Image.open(pets_path)
print(f"footer_pets.png size: {img.size}, mode: {img.mode}")

# Let's inspect the corner pixel (0,0) and some edge pixels
# to see if they are transparent (alpha = 0) or white (255, 255, 255, 255)
corners = [(0,0), (img.width-1, 0), (0, img.height-1), (img.width-1, img.height-1)]
for p in corners:
    print(f"  Pixel at {p}: {img.getpixel(p)}")
