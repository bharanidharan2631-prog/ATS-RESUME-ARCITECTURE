from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import re

def clean_text(text):
    # remove markdown bold/italic
    text = re.sub(r"\*+", "", text)

    # fix multiple spaces
    text = re.sub(r" +", " ", text)

    return text

def build_resume_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    text = clean_text(text)

    lines = text.split("\n")

    y = height - 50

    for line in lines:
        line = line.strip()

        if y < 50:
            c.showPage()
            y = height - 50

        if not line:
            y -= 10
            continue

        # Heading detection (simple rule)
        if line.isupper() and len(line) < 60:
            y -= 5
            c.drawString(40, y, line)
            y -= 15
            continue

        # Bullet lines
        if line.startswith("-"):
            line = "•" + line[1:]

        # Wrap long lines
        chunks = [line[i:i+100] for i in range(0, len(line), 100)]

        for chunk in chunks:
            c.drawString(40, y, chunk)
            y -= 14

        y -= 3

    c.save()
    return output_path