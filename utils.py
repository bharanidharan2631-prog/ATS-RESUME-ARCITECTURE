from PyPDF2 import PdfReader
from docx import Document

def read_file(path):

    if path.endswith(".pdf"):

        reader = PdfReader(path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

        return text

    elif path.endswith(".docx"):

        doc = Document(path)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

        return text

    with open(path, "r", encoding="utf-8") as f:
        return f.read()