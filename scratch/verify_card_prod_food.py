import os
from PIL import Image

p = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\card_prod_food_new.png"
if os.path.exists(p):
    im = Image.open(p)
    print(f"File exists: {p}")
    print(f"Mode: {im.mode}, Size: {im.size}")
    assert im.size == (800, 446), f"Expected (800, 446), got {im.size}"
    assert im.mode == "RGBA", f"Expected RGBA, got {im.mode}"
    print("Verification PASSED!")
else:
    print(f"File DOES NOT exist: {p}")
