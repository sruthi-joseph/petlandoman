from PIL import Image
import numpy as np

img_old = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\hygiene suppliments.jpeg").convert("RGB")
img_new = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\product page card-hygiene and supplements.jpeg").convert("RGB")

arr_old = np.array(img_old, dtype=np.int16)
arr_new = np.array(img_new, dtype=np.int16)

diff = np.max(np.abs(arr_old - arr_new), axis=2) > 30

# Check diff per column (X)
cols_with_diff = np.where(diff.any(axis=0))[0]
rows_with_diff = np.where(diff.any(axis=1))[0]

print("Columns (X) with diff min/max:", cols_with_diff.min(), cols_with_diff.max())
print("Rows (Y) with diff min/max:", rows_with_diff.min(), rows_with_diff.max())

# Slice into 4 horizontal quarters across X
w = 2752
q1 = np.sum(diff[:, 0:w//4])
q2 = np.sum(diff[:, w//4:2*w//4])
q3 = np.sum(diff[:, 2*w//4:3*w//4])
q4 = np.sum(diff[:, 3*w//4:])

print(f"Diff pixel counts across X quarters: Q1(left)={q1}, Q2={q2}, Q3={q3}, Q4(right)={q4}")
