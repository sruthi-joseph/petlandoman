import numpy as np
from PIL import Image
from scipy.optimize import least_squares

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
img = Image.open(img_path).convert("RGB")
w, h = img.size
arr = np.array(img)

# Approximate center
cx_est = 1200
cy_est = 906

# We'll sample 360 radial directions to find the exact edge.
# The edge is the transition between the dark background outside and the light background inside.
# Since outside is dark (r+g+b < 100) and inside is light (r+g+b > 600),
# the edge is very sharp!
edge_points = []

for angle_deg in range(360):
    angle = np.radians(angle_deg)
    dx = np.cos(angle)
    dy = np.sin(angle)
    
    # Scan from center outwards
    # Max distance is about 900
    for dist in range(1, 950):
        x = int(cx_est + dx * dist)
        y = int(cy_est + dy * dist)
        if 0 <= x < w and 0 <= y < h:
            r, g, b = arr[y, x]
            brightness = int(r) + int(g) + int(b)
            # If it gets dark, we crossed the boundary!
            if brightness < 150: # boundary threshold
                edge_points.append((x, y))
                break

edge_points = np.array(edge_points)
print(f"Found {len(edge_points)} edge points.")

# Fit circle using least squares: (x - xc)^2 + (y - yc)^2 = R^2
def calc_R(xc, yc):
    return np.sqrt((edge_points[:, 0] - xc)**2 + (edge_points[:, 1] - yc)**2)

def f_2(c):
    # Calculate distance of each edge point from the center c=(xc, yc)
    Ri = calc_R(*c)
    return Ri - Ri.mean()

center_estimate = [cx_est, cy_est]
res_2 = least_squares(f_2, center_estimate)
xc, yc = res_2.x
R = calc_R(xc, yc).mean()

print(f"Fitted circle:")
print(f"  Center: ({xc:.4f}, {yc:.4f})")
print(f"  Radius: {R:.4f}")
print(f"  Min distance: {calc_R(xc, yc).min():.4f}, Max distance: {calc_R(xc, yc).max():.4f}")
