from pypdf import PdfReader
import os

pdf_path = r"c:\Users\SRUTHI\Desktop\petland oman\Ui (2).pdf"
if not os.path.exists(pdf_path):
    print("PDF not found!")
    exit()

reader = PdfReader(pdf_path)
print(f"Number of pages: {len(reader.pages)}")

# Print text of first few pages to see what it is
for idx, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f"--- Page {idx+1} ({len(text)} chars) ---")
    if text:
        print(text[:300])
