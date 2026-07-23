import numpy as np
from PIL import Image
from scipy.optimize import least_squares

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
img = Image.open(img_path).convert("RGB")
w, h = img.size
arr = np.array(img)

# Center of image is around (1200, 896)
cx_est = 1200
cy_est = 896

boundary_points = []

# Scan from outside (dist = 1100) inwards (to dist = 500)
for angle_deg in range(360):
    angle = np.radians(angle_deg)
    dx = np.cos(angle)
    dy = np.sin(angle)
    
    # We walk inwards from dist = 1100 to 500
    for dist in range(1100, 500, -1):
        x = int(cx_est + dx * dist)
        y = int(cy_est + dy * dist)
        if 0 <= x < w and 0 <= y < h:
            r, g, b = arr[y, x]
            brightness = int(r) + int(g) + int(b)
            # When we transition from dark background (brightness < 120) to light (brightness >= 120)
            if brightness >= 120:
                boundary_points.append((x, y))
                break

boundary_points = np.array(boundary_points)
print(f"Found {len(boundary_points)} boundary points.")

# Fit circle using least squares
def calc_R(xc, yc):
    return np.sqrt((boundary_points[:, 0] - xc)**2 + (boundary_points[:, 1] - yc)**2)

def f_2(c):
    Ri = calc_R(*c)
    return Ri - Ri.mean()

center_estimate = [cx_est, cy_est]
res_2 = least_squares(f_2, center_estimate)
xc, yc = res_2.x
R = calc_R(xc, yc).mean()

print(f"Fitted circle:")
print(f"  Center: ({xc:.4f}, {yc:.4f})")
print(f"  Radius: {R:.4f}")
print(f"  Min radius distance: {calc_R(xc, yc).min():.4f}, Max radius distance: {calc_R(xc, yc).max():.4f}")
