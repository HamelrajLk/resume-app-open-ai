from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    text = ""
    for page in PdfReader(file).pages:
        text += page.extract_text()
    return text.strip()