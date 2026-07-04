from PIL import Image
import numpy as np
import os

# Original white-background versions saved earlier
sources = [
    ("C:/Users/SRUTHI/.gemini/antigravity-ide/brain/22fa6263-8c42-49d6-9c65-fef095efda85/svc_nutritional_w_1782479425931.png",
     "extracted_images/svc_nutritional.png"),
    ("C:/Users/SRUTHI/.gemini/antigravity-ide/brain/22fa6263-8c42-49d6-9c65-fef095efda85/svc_training_w_1782479437862.png",
     "extracted_images/svc_training.png"),
    ("C:/Users/SRUTHI/.gemini/antigravity-ide/brain/22fa6263-8c42-49d6-9c65-fef095efda85/svc_grooming_w_1782479451439.png",
     "extracted_images/svc_grooming.png"),
    ("C:/Users/SRUTHI/.gemini/antigravity-ide/brain/22fa6263-8c42-49d6-9c65-fef095efda85/svc_daycare_w_1782479464274.png",
     "extracted_images/svc_daycare.png"),
]

for src, dest in sources:
    if not os.path.exists(src):
        print(f"NOT FOUND: {src}")
        continue

    img = Image.open(src).convert("RGBA")
    data = np.array(img, dtype=np.int32)

    R, G, B, A = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

    # Detect near-white/light-grey background pixels
    brightness = (R + G + B) // 3
    max_ch = np.maximum(np.maximum(R, G), B)
    min_ch = np.minimum(np.minimum(R, G), B)
    saturation = (max_ch - min_ch)

    # Near-white: bright AND low saturation → make fully transparent
    mask = (brightness > 210) & (saturation < 40) & (A > 10)
    data[mask, 3] = 0   # alpha = 0 → transparent

    result = Image.fromarray(data.astype(np.uint8), "RGBA")
    result.save(dest)
    print(f"Done: {dest}  ({mask.sum()} pixels made transparent)")

print("All done.")
