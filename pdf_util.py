import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """Extracts and returns text from an uploaded PDF file."""
    pdf_bytes = uploaded_file.read()
    doc = fitz.open("pdf", pdf_bytes)
    text = "\n".join([page.get_text("text") for page in doc])
    return text
