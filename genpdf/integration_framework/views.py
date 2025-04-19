from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from genpdf import generate_pdf


@csrf_exempt
def generate_ticket(request):
    if request.method == 'POST':
        try:
            data = {
                'movie': request.POST.get('movie'),
                'date': request.POST.get('date'),
                'row': request.POST.get('row'),
                'seat': request.POST.get('seat'),
                'name': request.POST.get('name'),
                'ticket_id': request.POST.get('ticket_id')
            }

            # Проверяем, что все поля заполнены
            required_fields = ['movie', 'date', 'row', 'seat', 'name', 'ticket_id']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'Поле "{field}" обязательно'}, status=400)

            # Генерация PDF
            pdf_buffer = generate_pdf(data)
            return FileResponse(pdf_buffer, filename='ticket.pdf', content_type='application/pdf')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)