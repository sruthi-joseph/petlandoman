libs = ["fitz", "pdf2image", "pypdf", "pdfplumber", "reportlab", "openpyxl"]
for lib in libs:
    try:
        __import__(lib)
        print(f"{lib} is available")
    except ImportError:
        print(f"{lib} is NOT available")
