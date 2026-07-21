import os
from PIL import Image, ImageDraw, ImageFont

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"
erased_path = os.path.join(artifact_dir, "erased_text.png")

# Background color for reference or text color: dark brown
text_color = (80, 48, 24, 255)

# We want to draw "ROYAL CANIN" centered at X=280, Y=140-163 (center Y=152)
center_x = 280
center_y = 152

fonts_to_test = [
    ("Outfit-Medium", r"c:\Users\SRUTHI\Desktop\petland oman\scratch\Outfit-Medium.ttf", 20),
    ("Outfit-Medium-22", r"c:\Users\SRUTHI\Desktop\petland oman\scratch\Outfit-Medium.ttf", 22),
    ("Arial-Bold", "arialbd.ttf", 19),
    ("Arial-Bold-21", "arialbd.ttf", 21)
]

for name, path, size in fonts_to_test:
    img = Image.open(erased_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(path, size)
    except IOError:
        # If font fails, skip or try local search
        print(f"Font {name} not found at {path}")
        continue
        
    # Get text size using getbbox or textlength/textbbox
    # For PIL >= 8.0, use textbbox
    bbox = draw.textbbox((0, 0), "ROYAL CANIN", font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    # Calculate position to center the text at (center_x, center_y)
    x = center_x - text_w // 2
    y = center_y - text_h // 2
    
    # Draw text
    draw.text((x, y), "ROYAL CANIN", font=font, fill=text_color)
    
    # Save test file
    img.save(os.path.join(artifact_dir, f"test_{name}.png"))
    print(f"Saved test_{name}.png (size: {text_w}x{text_h}, position: {x},{y})")
