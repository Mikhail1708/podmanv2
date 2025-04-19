from io import BytesIO

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

#регистрация шрифта
pdfmetrics.registerFont(TTFont('PT_Serif', 'PT_Serif.ttf'))


def generate_pdf(data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("PT_Serif", 12)
    pdf.setFont("PT_Serif", 16)
    pdf.drawString(50, 800, ("Электронный билет"))

    y = 750
    fields = [
        ("Фильм", data['movie']),
        ("Дата", data['date']),
        ("Место", f"Ряд {data['row']}, Место {data['seat']}"),
        ("Имя", data['name'])
    ]

    for label, value in fields:
        pdf.drawString(50, y,(f"{label}: {value}"))
        y -= 30
    pdf.save()
    buffer.seek(0)
    return buffer