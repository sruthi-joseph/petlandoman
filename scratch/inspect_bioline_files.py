import os
import hashlib
from PIL import Image

bioline_dir = r"c:\Users\SRUTHI\Desktop\petland oman\Hygiene suppliments\bioline\bioline"
files = os.listdir(bioline_dir)

print(f"Total files: {len(files)}")

def get_md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

file_info = []

for f in files:
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif')):
        path = os.path.join(bioline_dir, f)
        size = os.path.getsize(path)
        md5 = get_md5(path)
        try:
            with Image.open(path) as img:
                width, height = img.size
                fmt = img.format
        except Exception as e:
            width, height = 0, 0
            fmt = "UNKNOWN"
        file_info.append({
            "name": f,
            "size": size,
            "md5": md5,
            "dims": f"{width}x{height}",
            "format": fmt
        })

# Group by MD5
md5_groups = {}
for info in file_info:
    md5 = info["md5"]
    if md5 not in md5_groups:
        md5_groups[md5] = []
    md5_groups[md5].append(info)

print("\n--- File List ---")
for info in sorted(file_info, key=lambda x: x["name"]):
    print(f"{info['name']} | Size: {info['size']} | Dims: {info['dims']} | Format: {info['format']} | MD5: {info['md5']}")

print("\n--- Duplicate Files ---")
for md5, group in md5_groups.items():
    if len(group) > 1:
        names = [g["name"] for g in group]
        print(f"Duplicates: {names}")
