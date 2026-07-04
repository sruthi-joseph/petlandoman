from PIL import Image
import os

products = [
    "pet food.jpeg",
    "toys & fun.jpeg",
    "groomin products.jpeg",
    "accessories.jpeg"
]

center_x, center_y = 1200, 892

for name in products:
    if not os.path.exists(name):
        print(f"{name} not found")
        continue
    img = Image.open(name).convert("RGB")
    w, h = img.size
    
    # Starting color at center
    center_color = img.getpixel((center_x, center_y))
    print(f"\nAnalyzing {name} (size: {w}x{h}, center color: {center_color}):")
    
    # Scan horizontally left from center
    left_x = center_x
    while left_x > 0:
        rgb = img.getpixel((left_x, center_y))
        # If it gets very dark (e.g. sum of rgb < 80), it might be the black outline or border
        if sum(rgb) < 120:
            break
        left_x -= 1
        
    # Scan horizontally right from center
    right_x = center_x
    while right_x < w - 1:
        rgb = img.getpixel((right_x, center_y))
        if sum(rgb) < 120:
            break
        right_x += 1
        
    # Scan vertically up from center
    top_y = center_y
    while top_y > 0:
        rgb = img.getpixel((center_x, top_y))
        if sum(rgb) < 120:
            break
        top_y -= 1
        
    # Scan vertically down from center
    bottom_y = center_y
    while bottom_y < h - 1:
        rgb = img.getpixel((center_x, bottom_y))
        if sum(rgb) < 120:
            break
        bottom_y += 1
        
    width_circle = right_x - left_x
    height_circle = bottom_y - top_y
    print(f"  Circle Horizontal Bounds: {left_x} to {right_x} (width: {width_circle}, center_x: {(left_x + right_x)/2})")
    print(f"  Circle Vertical Bounds: {top_y} to {bottom_y} (height: {height_circle}, center_y: {(top_y + bottom_y)/2})")
