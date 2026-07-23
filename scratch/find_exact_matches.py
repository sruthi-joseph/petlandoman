import os

files = [
    r"c:\Users\SRUTHI\Desktop\petland oman\index.html",
    r"c:\Users\SRUTHI\Desktop\petland oman\pages\accessories.html",
    r"c:\Users\SRUTHI\Desktop\petland oman\pages\products.html"
]

keywords = ["product_1", "product 1", "card_prod_food", "pet food.jpeg"]

for p in files:
    print(f"\nMatches in {p}:")
    with open(p, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            for kw in keywords:
                if kw in line:
                    print(f"  Line {idx}: {line.strip()}")
