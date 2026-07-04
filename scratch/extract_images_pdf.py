import os
from pypdf import PdfReader

pdf_path = r"c:\Users\SRUTHI\Desktop\petland oman\Ui (2).pdf"
output_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_pdf_images"
os.makedirs(output_dir, exist_ok=True)

reader = PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

image_counter = 0
for page_num, page in enumerate(reader.pages):
    print(f"Checking page {page_num + 1}...")
    for img_file_object in page.images:
        image_counter += 1
        name = img_file_object.name
        # Some images might not have a proper extension in their name
        ext = os.path.splitext(name)[1]
        if not ext:
            ext = ".png" # default to png
        
        out_name = f"page_{page_num + 1}_img_{image_counter}{ext}"
        out_path = os.path.join(output_dir, out_name)
        with open(out_path, "wb") as fp:
            fp.write(img_file_object.data)
        print(f"  Extracted: {out_name} (size: {len(img_file_object.data)} bytes)")

print(f"Done. Extracted {image_counter} images in total.")
