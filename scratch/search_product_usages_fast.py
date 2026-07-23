import os

for root, dirs, files in os.walk(r"c:\Users\SRUTHI\Desktop\petland oman"):
    # Ignore node_modules, .git, and scratch
    if "node_modules" in root or ".git" in root or "scratch" in root:
        continue
    for f in files:
        if f.endswith((".html", ".js", ".css")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8") as file:
                    content = file.read()
                    if "product_1" in content or "product 1" in content or "card_prod_food" in content or "pet food.jpeg" in content:
                        print(f"Match in: {p}")
            except Exception as e:
                pass
print("Done!")
