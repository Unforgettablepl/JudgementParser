from pypdf import PdfReader

def extractRawText(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    with open("logs.txt",'a') as f:
        f.write(f"Pages: {len(reader.pages)}\n")
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text