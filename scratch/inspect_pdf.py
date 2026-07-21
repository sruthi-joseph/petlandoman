import pypdf
import os

pdf_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\docs\logo.pdf"
reader = pypdf.PdfReader(pdf_path)

print(f"Number of pages: {len(reader.pages)}")
for idx, page in enumerate(reader.pages):
    print(f"Page {idx+1}:")
    print(f"MediaBox: {page.mediabox}")
    images = page.images
    print(f"Number of images on page: {len(images)}")
    for img_idx, img in enumerate(images):
        print(f"  Image {img_idx+1}: {img.name}, size: {len(img.data)} bytes")
