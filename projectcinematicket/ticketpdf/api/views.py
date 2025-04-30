import io
import base64
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode
from PIL import Image

@csrf_exempt
def generate_pdf(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        name = data.get('name')
        film = data.get('film_id')
        time_ = data.get('session_id')
        row = data.get('row')
        seat = data.get('seat')
        ticket_id = data.get('ticket_id', '')

        qr_data = {
            "name": name,
            "film": film,
            "time": time_,
            "row": row,
            "seat": seat,
            "ticket_id": ticket_id
        }
        qr_text = json.dumps(qr_data, ensure_ascii=False)
        qr_img = qrcode.make(qr_text)

        buffer = io.BytesIO()

        # Регистрируем шрифт с поддержкой кириллицы
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont("DejaVuSans", 14)
        p.drawString(100, 800, f"Имя: {name}")
        p.drawString(100, 780, f"Фильм: {film}")
        p.drawString(100, 760, f"Время: {time_}")
        p.drawString(100, 740, f"Ряд: {row}")
        p.drawString(100, 720, f"Место: {seat}")
        if ticket_id:
            p.drawString(100, 700, f"Ticket ID: {ticket_id}")

        img_buffer = io.BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        p.drawInlineImage(Image.open(img_buffer), 100, 600, width=120, height=120)

        p.showPage()
        p.save()
        buffer.seek(0)
        pdf_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return JsonResponse({'token': pdf_base64})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Error generating PDF: {e}'}, status=500)