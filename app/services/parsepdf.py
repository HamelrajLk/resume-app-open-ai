from PyPDF2 import PdfReader


def extract_text_from_pdf(file) -> str:
    try:
        reader = PdfReader(file)
    except Exception as e:
        raise ValueError(f"Could not read PDF file: {e}")

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    text = text.strip()
    if not text:
        raise ValueError("No extractable text found in the PDF. The file may be scanned or image-based.")

    return text
