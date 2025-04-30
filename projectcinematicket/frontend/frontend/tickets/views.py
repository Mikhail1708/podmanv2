import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import TicketForm
from .models import Film, Session
import requests

PDF_SERVICE_URL = 'http://10.100.1.233:5001/api/generate-pdf/'  # URL сервиса генерации PDF

def buy_ticket(request):
    films = Film.objects.all().prefetch_related('sessions')

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Получаем выбранный сеанс из POST (в форме должен быть select с именем 'session')
            session_id = request.POST.get('session')
            if not session_id:
                return HttpResponse("Сеанс не выбран", status=400)

            session = get_object_or_404(Session, id=session_id)

            # Добавляем в данные для ticketpdf необходимые поля
            data['film_id'] = session.film.title  # Название фильма
            data['session_id'] = f"{session.date} {session.time}"
            print(data)
            # Отправляем данные на сервис генерации PDF
            try:
                pdf_service_response = requests.post(PDF_SERVICE_URL, json=data, timeout=100)
            except requests.RequestException as e:
                return HttpResponse(f"Ошибка связи с сервисом генерации PDF: {e}", status=500)

            if pdf_service_response.status_code != 200:
                return HttpResponse("Ошибка генерации PDF на ticketpdf", status=500)

            json_response = pdf_service_response.json()
            base64_pdf = json_response.get('token')
            if not base64_pdf:
                return HttpResponse("PDF не получен от ticketpdf", status=500)

            # Если base64 содержит префикс, убираем его
            if base64_pdf.startswith('data:'):
                base64_pdf = base64_pdf.split(',', 1)[1]

            # Декодируем base64 в бинарный PDF
            try:
                pdf_content = base64.b64decode(base64_pdf)
            except Exception as e:
                return HttpResponse(f"Ошибка декодирования PDF: {e}", status=500)

            # Отдаём бинарный PDF клиенту с правильными заголовками
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
            return response

    else:
        form = TicketForm()

    return render(request, 'tickets/buy_ticket.html', {
        'form': form,
        'films': films,
    })