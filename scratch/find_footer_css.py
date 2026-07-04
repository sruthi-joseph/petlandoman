import re

with open("style.css", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find all CSS rules containing footer
# We can find blocks that contain the word "footer" or ".footer"
# A block is roughly text followed by { then text then }
blocks = re.findall(r'([^{}]*footer[^{}]*\{[^{}]*\})', content, re.IGNORECASE | re.DOTALL)

print("Found CSS blocks containing 'footer':")
for i, block in enumerate(blocks):
    print(f"\n--- Block {i+1} ---")
    print(block.strip())
