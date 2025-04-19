from django.urls import path
from integration_framework.views import generate_ticket

urlpatterns = [
    path('api/generate-ticket/', generate_ticket, name='generate_ticket'),

]