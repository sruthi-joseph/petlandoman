import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

img = Image.open(os.path.join(image_dir, "logo_transparent.png")).convert("RGBA")

# Crop bottom blocks
# We know Block 0 ends at 1040, Block 1 is 1073 to 1151.
# Let's crop from Y=900 to 1050 (bottom of Block 0)
# and from Y=1050 to 1152 (Block 1)

crop1 = img.crop((0, 900, img.width, 1050))
# crop1 has a lot of transparent padding, let's crop to its bbox
bbox1 = crop1.getbbox()
if bbox1:
    crop1.crop(bbox1).save(os.path.join(artifact_dir, "bottom_block_0.png"))
    print("Saved bottom_block_0.png")

crop2 = img.crop((0, 1050, img.width, 1152))
bbox2 = crop2.getbbox()
if bbox2:
    crop2.crop(bbox2).save(os.path.join(artifact_dir, "bottom_block_1.png"))
    print("Saved bottom_block_1.png")
