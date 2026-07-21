import pypdf

pdf_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\docs\logo.pdf"
reader = pypdf.PdfReader(pdf_path)
page = reader.pages[0]
text = page.extract_text()
print("Extracted Text:")
print(repr(text))
