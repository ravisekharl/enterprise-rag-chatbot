import fitz
from docx import Document
from pathlib import Path

def extract_pdf_text(file_path):

    document = fitz.open(file_path)
    text = ""
    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_docx_text(file_path):

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"
        return text


def extract_text(file_path: Path) ->str:
    """
    Extract text from a supported document.
    """
    extension = file_path.suffix.lower()
    if extension == ".pdf":
        return extract_pdf_text(file_path)
    elif extension == ".docx":
        return extract_docx_text(file_path)

    raise ValueError(f"Unsupported file type: {extension}")
