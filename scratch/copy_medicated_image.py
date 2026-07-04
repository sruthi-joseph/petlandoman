import shutil
import os

brain_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\d7344ec0-3c55-4d54-9497-0adca2bc614e"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

src_path = os.path.join(brain_dir, "grooming_medicated_1782985875259.png")
dest_path = os.path.join(dest_dir, "grooming_medicated.png")

os.makedirs(dest_dir, exist_ok=True)
if os.path.exists(src_path):
    shutil.copy(src_path, dest_path)
    print("Copied medicated wash image successfully!")
else:
    print("Source not found:", src_path)
