with open(r"c:\Users\SRUTHI\Desktop\petland oman\style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

def print_block(start_idx):
    for i in range(start_idx, start_idx + 15):
        if i < len(lines):
            print(f"Line {i+1}: {lines[i].strip()}")

print("--- Block at Line 101 ---")
print_block(100)

print("\n--- Block at Line 2282 ---")
print_block(2281)
