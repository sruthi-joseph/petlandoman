from PIL import Image
import numpy as np
import os

TARGET_R, TARGET_G, TARGET_B = 252, 194, 3   # #FCC203

images = [
    "extracted_images/svc_nutritional.png",
    "extracted_images/svc_training.png",
    "extracted_images/svc_grooming.png",
    "extracted_images/svc_daycare.png",
]

for path in images:
    if not os.path.exists(path):
        print(f"NOT FOUND: {path}")
        continue

    img = Image.open(path).convert("RGBA")
    data = np.array(img, dtype=np.int32)

    R, G, B, A = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

    # Detect near-white pixels: high brightness & low saturation
    brightness = (R.astype(int) + G.astype(int) + B.astype(int)) // 3
    max_ch = np.maximum(np.maximum(R, G), B)
    min_ch = np.minimum(np.minimum(R, G), B)
    saturation = (max_ch - min_ch)

    # White/near-white: brightness > 210 AND saturation < 40
    mask = (brightness > 210) & (saturation < 40) & (A > 10)

    # Replace matched pixels with #FCC203
    data[mask, 0] = TARGET_R
    data[mask, 1] = TARGET_G
    data[mask, 2] = TARGET_B
    data[mask, 3] = 255

    result = Image.fromarray(data.astype(np.uint8), "RGBA")
    # Save as PNG keeping RGBA
    result.save(path)
    print(f"Done: {path}  (replaced {mask.sum()} pixels)")

print("All done.")
