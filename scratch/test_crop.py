from PIL import Image
import os

img = Image.open("products & service  image.png")

# Create output dir
os.makedirs("extracted_images", exist_ok=True)

# Top row (products)
# Center positions for 4 columns: 192, 576, 960, 1344
# Let's try width=380, height=380, y from 60 to 440
y_start = 60
y_end = 440
box1 = (192 - 190, y_start, 192 + 190, y_end)
box2 = (576 - 190, y_start, 576 + 190, y_end)
box3 = (960 - 190, y_start, 960 + 190, y_end)
box4 = (1344 - 190, y_start, 1344 + 190, y_end)

img.crop(box1).save("extracted_images/prod1.png")
img.crop(box2).save("extracted_images/prod2.png")
img.crop(box3).save("extracted_images/prod3.png")
img.crop(box4).save("extracted_images/prod4.png")

# Bottom row (services)
# Center positions for 3 columns: 256, 768, 1280
# 1536 / 3 = 512 per column.
# Col 1: center X = 256
# Col 2: center X = 768
# Col 3: center X = 1280
# Let's try y from 540 to 940 (height 400)
# Width in columns can be 420 (from center-210 to center+210)
y_svc_start = 540
y_svc_end = 940
svc_box1 = (256 - 210, y_svc_start, 256 + 210, y_svc_end)
svc_box2 = (768 - 210, y_svc_start, 768 + 210, y_svc_end)
svc_box3 = (1280 - 210, y_svc_start, 1280 + 210, y_svc_end)

img.crop(svc_box1).save("extracted_images/svc1.png")
img.crop(svc_box2).save("extracted_images/svc2.png")
img.crop(svc_box3).save("extracted_images/svc3.png")

print("Done cropping.")
