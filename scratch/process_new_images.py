import os
import time
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

brain_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\d7344ec0-3c55-4d54-9497-0adca2bc614e"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"
os.makedirs(dest_dir, exist_ok=True)

image_files = {
    "grooming_shower_new_1782988206810.png": "grooming_shower.png",
    "grooming_haircut_new_1782988230946.png": "grooming_haircut.png",
    "grooming_deshedding_new_1782988254019.png": "grooming_deshedding.png",
    "grooming_full_new_1782988467341.png": "grooming_full.png",
    "grooming_medicated_new_1782988531023.png": "grooming_medicated.png"
}

def remove_background_floodfill(src_path, dest_path):
    print(f"Processing: {os.path.basename(src_path)}")
    start_time = time.time()
    
    img = Image.open(src_path).convert("RGBA")
    data = np.array(img)
    h, w, c = data.shape
    R, G, B = data[:,:,0], data[:,:,1], data[:,:,2]
    
    # Background candidate mask: pixels very close to white/light grey
    # Threshold 225 is very safe for pure white studio background
    is_bg_candidate = (R > 225) & (G > 225) & (B > 225)
    
    visited = np.zeros((h, w), dtype=bool)
    queue = deque()
    
    # Seed queue with border pixels that are candidates
    for y in range(h):
        if is_bg_candidate[y, 0]:
            queue.append((y, 0))
            visited[y, 0] = True
        if is_bg_candidate[y, w-1]:
            queue.append((y, w-1))
            visited[y, w-1] = True
            
    for x in range(w):
        if is_bg_candidate[0, x]:
            queue.append((0, x))
            visited[0, x] = True
        if is_bg_candidate[h-1, x]:
            queue.append((h-1, x))
            visited[h-1, x] = True
            
    # Run BFS
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        cy, cx = queue.popleft()
        for dy, dx in directions:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w:
                if not visited[ny, nx] and is_bg_candidate[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((ny, nx))
                    
    # Set background alpha to 0
    data[visited, 3] = 0
    
    # Save temporary alpha mask for feathering
    alpha_mask = Image.fromarray(data[:, :, 3], mode="L")
    # Blur mask to smooth edges
    blurred_alpha = alpha_mask.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    # Reassemble RGB and blurred alpha
    clean_rgb = Image.fromarray(data[:, :, :3], mode="RGB")
    final_img = Image.new("RGBA", (w, h))
    final_img.paste(clean_rgb, (0, 0))
    final_img.putalpha(blurred_alpha)
    
    # Save as PNG
    final_img.save(dest_path, "PNG")
    print(f"  Saved to: {dest_path} | Time: {time.time() - start_time:.2f}s")

for src_name, dest_name in image_files.items():
    src_path = os.path.join(brain_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        remove_background_floodfill(src_path, dest_path)
    else:
        print(f"ERROR: {src_name} not found in brain directory.")

print("All new images processed successfully!")
