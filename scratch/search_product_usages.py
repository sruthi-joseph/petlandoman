import os

for root, dirs, files in os.walk(r"c:\Users\SRUTHI\Desktop\petland oman"):
    for f in files:
        if f.endswith((".html", ".js", ".css")):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                if "product_1" in content or "product 1" in content or "card_prod_food" in content:
                    print(f"Match in: {p}")
