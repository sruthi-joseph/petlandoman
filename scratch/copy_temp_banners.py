import shutil
import os

src_products = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\5b0debc6-9cea-4d38-b726-b356ae133ac1\.tempmediaStorage\media_5b0debc6-9cea-4d38-b726-b356ae133ac1_1784836535924.png"
src_services = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\5b0debc6-9cea-4d38-b726-b356ae133ac1\.tempmediaStorage\media_5b0debc6-9cea-4d38-b726-b356ae133ac1_1784836662977.png"

dest_products = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet products.png"
dest_services = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet services.png"

if os.path.exists(src_products):
    shutil.copy2(src_products, dest_products)
    print(f"Copied products banner to {dest_products}")
else:
    print(f"Products src not found: {src_products}")

if os.path.exists(src_services):
    shutil.copy2(src_services, dest_services)
    print(f"Copied services banner to {dest_services}")
else:
    print(f"Services src not found: {src_services}")
