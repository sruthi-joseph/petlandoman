from PIL import Image
import os

products = [
    ("pet food.jpeg", 892),
    ("toys & fun.jpeg", 892),
    ("groomin products.jpeg", 892),
    ("accessories.jpeg", 892)
]

for name, cy in products:
    if not os.path.exists(name):
        continue
    img = Image.open(name).convert("RGB")
    w, h = img.size
    print(f"\n=================== {name} (y={cy}) ===================")
    
    # Let's inspect the transition on the left side (x from 250 to 500)
    print("Left transition area (x, R, G, B):")
    left_points = []
    for x in range(250, 500):
        r, g, b = img.getpixel((x, cy))
        # Find transition where it stops being black/dark background and becomes colored or border
        left_points.append((x, (r, g, b)))
    
    # Print some points where color changes significantly
    # Let's print points where brightness increases
    last_brightness = sum(left_points[0][1])
    for x, rgb in left_points:
        brightness = sum(rgb)
        if abs(brightness - last_brightness) > 15:
            print(f"  x={x}: {rgb} (brightness: {brightness})")
        last_brightness = brightness
        
    # Let's inspect the right side (x from 1900 to 2150)
    print("Right transition area (x, R, G, B):")
    right_points = []
    for x in range(1900, 2150):
        r, g, b = img.getpixel((x, cy))
        right_points.append((x, (r, g, b)))
        
    last_brightness = sum(right_points[0][1])
    for x, rgb in right_points:
        brightness = sum(rgb)
        if abs(brightness - last_brightness) > 15:
            print(f"  x={x}: {rgb} (brightness: {brightness})")
        last_brightness = brightness
