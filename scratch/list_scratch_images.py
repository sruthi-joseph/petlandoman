from PIL import Image
import os

scratch_dir = "scratch"
for f in os.listdir(scratch_dir):
    ext = os.path.splitext(f)[1].lower()
    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
        p = os.path.join(scratch_dir, f)
        try:
            with Image.open(p) as img:
                print(f"File: {f}, Size={img.size}, Mode={img.mode}")
        except Exception as e:
            print(f"File: {f}, Error={e}")
