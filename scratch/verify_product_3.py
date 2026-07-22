import os
from PIL import Image

p = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\product_3.png"
if os.path.exists(p):
    im = Image.open(p)
    print(f"File exists: {p}")
    print(f"Mode: {im.mode}, Size: {im.size}")
    assert im.size == (500, 500), f"Expected (500, 500), got {im.size}"
    assert im.mode == "RGBA", f"Expected RGBA, got {im.mode}"
    print("Verification PASSED!")
else:
    print(f"File DOES NOT exist: {p}")
