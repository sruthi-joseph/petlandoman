import os
from PIL import Image

def generate_new_logos():
    src_logo_path = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images\img_4_R15.png"
    orig_logo_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png"
    
    out_logo_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png"
    out_white_logo_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_white_transparent.png"
    
    # 1. Load source image and crop to active bounding box
    src_img = Image.open(src_logo_path).convert("RGBA")
    src_bbox = src_img.getbbox()
    if not src_bbox:
        print("Error: Source image is empty")
        return
    src_active = src_img.crop(src_bbox)
    src_w, src_h = src_active.size
    print(f"Source active size: {src_w}x{src_h} (aspect ratio: {src_w/src_h:.4f})")
    
    # 2. Load original image and find its active bounding box
    orig_img = Image.open(orig_logo_path).convert("RGBA")
    orig_bbox = orig_img.getbbox()
    if not orig_bbox:
        print("Error: Original image is empty")
        return
    orig_active_w = orig_bbox[2] - orig_bbox[0]
    orig_active_h = orig_bbox[3] - orig_bbox[1]
    print(f"Original active size: {orig_active_w}x{orig_active_h} (aspect ratio: {orig_active_w/orig_active_h:.4f})")
    
    # 3. Calculate scaling factor to contain the new active area inside original active area
    scale_w = orig_active_w / src_w
    scale_h = orig_active_h / src_h
    scale = min(scale_w, scale_h)
    
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    print(f"Resizing new active logo to: {new_w}x{new_h} using LANCZOS")
    
    # Resize using high-quality LANCZOS filter
    resized_active = src_active.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 4. Center the resized logo inside the original active bounding box position
    dx = (orig_active_w - new_w) // 2
    dy = (orig_active_h - new_h) // 2
    
    dest_x = orig_bbox[0] + dx
    dest_y = orig_bbox[1] + dy
    print(f"Placing resized logo at ({dest_x}, {dest_y}) on the 2048x1152 canvas")
    
    # 5. Create new transparent canvas and paste
    new_logo_img = Image.new("RGBA", orig_img.size, (0, 0, 0, 0))
    new_logo_img.paste(resized_active, (dest_x, dest_y), resized_active)
    
    # Backup original logo before overwriting
    backup_path = orig_logo_path + "_backup.png"
    if not os.path.exists(backup_path):
        orig_img.save(backup_path, format="PNG")
        print(f"Backup saved to {backup_path}")
        
    # Save new logo
    new_logo_img.save(out_logo_path, format="PNG")
    print(f"Saved new logo to {out_logo_path}")
    
    # 6. Generate the white version (logo_white_transparent.png)
    # Get pixel data
    pixels = new_logo_img.load()
    width, height = new_logo_img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 0:
                # Keep original alpha but change color to white
                pixels[x, y] = (255, 255, 255, a)
                
    # Save white logo
    new_logo_img.save(out_white_logo_path, format="PNG")
    print(f"Saved new white logo to {out_white_logo_path}")

if __name__ == "__main__":
    generate_new_logos()
