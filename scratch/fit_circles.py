from PIL import Image
import os
import math

products = [
    "pet food.jpeg",
    "toys & fun.jpeg",
    "groomin products.jpeg",
    "accessories.jpeg"
]

for name in products:
    if not os.path.exists(name):
        print(f"{name} not found")
        continue
    img = Image.open(name).convert("RGB")
    w, h = img.size
    
    # We will scan from the border of the image inwards towards the center (w//2, h//2)
    # along 360 radial directions
    center_x = w // 2
    center_y = h // 2
    
    boundary_points = []
    
    # Scan angles from 0 to 359 degrees
    for angle_deg in range(0, 360, 5):
        angle = math.radians(angle_deg)
        dx = math.cos(angle)
        dy = math.sin(angle)
        
        # Start far away (outside the circle, e.g. at distance 1100 from center)
        # and walk inwards (reducing distance)
        # Note: diagonal of 2400x1792 is ~3000, half diagonal is ~1500
        found = False
        for dist in range(1200, 200, -2):
            px = int(center_x + dx * dist)
            py = int(center_y + dy * dist)
            
            # Check bounds
            if 0 <= px < w and 0 <= py < h:
                r, g, b = img.getpixel((px, py))
                brightness = r + g + b
                
                # If brightness is high, we hit the circle!
                # Let's use a threshold of 250 for brightness
                if brightness > 250:
                    boundary_points.append((px, py, dist))
                    found = True
                    break
        
    if len(boundary_points) < 10:
        print(f"Error: could not find boundary points for {name}")
        continue
        
    # Fit a circle to boundary_points
    # Simple average to find center and radius
    avg_x = sum(p[0] for p in boundary_points) / len(boundary_points)
    avg_y = sum(p[1] for p in boundary_points) / len(boundary_points)
    avg_r = sum(p[2] for p in boundary_points) / len(boundary_points)
    
    # Let's refine the center and radius by calculating distance of all boundary points from the average center
    distances = [math.sqrt((p[0] - avg_x)**2 + (p[1] - avg_y)**2) for p in boundary_points]
    mean_radius = sum(distances) / len(distances)
    
    print(f"\nResults for {name}:")
    print(f"  Detected Center: ({avg_x:.2f}, {avg_y:.2f})")
    print(f"  Detected Radius: {mean_radius:.2f}")
    print(f"  Min Radius among points: {min(distances):.2f}, Max Radius: {max(distances):.2f}")
    print(f"  Number of boundary points: {len(boundary_points)}")
