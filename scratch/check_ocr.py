libs = ["pytesseract", "easyocr", "cv2", "fitz", "pdfplumber"]
for lib in libs:
    try:
        __import__(lib)
        print(f"{lib} is available")
    except ImportError:
        print(f"{lib} is NOT available")
