from PIL import Image
try:
    with Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\docs\logo.pdf") as img:
        print("Success! Pillow opened the PDF directly.")
        print(f"Format: {img.format}, Size: {img.size}")
except Exception as e:
    print(f"Pillow failed to open PDF: {e}")
