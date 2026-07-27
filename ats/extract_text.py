import pdfplumber
from docx import Document

def load_text(path):
    path_lower = path.lower()

    # ----- TXT -----
    if path_lower.endswith(".txt"):
        with open(path, "rb") as f:
            raw = f.read()
        return raw.decode("utf-8", errors="ignore")

    # ----- PDF -----
    if path_lower.endswith(".pdf"):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        return text

    # ----- DOCX -----
    if path_lower.endswith(".docx"):
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])

    raise ValueError("Unsupported file format: " + path)
