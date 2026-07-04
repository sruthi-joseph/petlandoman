from PIL import Image
import numpy as np

img = Image.open("products & service  image.png")
data = np.array(img)
alpha = data[:, :, 3]

# The circles have very solid alphas and represent massive chunks of pixels
# Let's find for each product column, the exact center Y of the circle.
# We can do this by looking at the density of alpha > 0 in a column.
# A circle of radius ~160 will have maximum width at its center.

prod_cols = [
    (76, 395),
    (423, 744),
    (787, 1105),
    (1140, 1461)
]

for idx, (x1, x2) in enumerate(prod_cols):
    col_alpha = alpha[0:512, x1:x2]
    # Sum along x-axis to see width at each Y
    widths = np.sum(col_alpha > 0, axis=1)
    
    # The circle will have high width (near 320) for about 320 pixels.
    # Let's find Y values where widths > 200 (to filter out small watermarks)
    circle_ys = np.where(widths > 200)[0]
    if len(circle_ys) > 0:
        cy_start = circle_ys[0]
        cy_end = circle_ys[-1]
        cy = (cy_start + cy_end) // 2
        cx = (x1 + x2) // 2
        print(f"Product {idx+1}: center=({cx}, {cy}), diameter={cy_end - cy_start}")
    else:
        print(f"Product {idx+1}: no solid circle found")
