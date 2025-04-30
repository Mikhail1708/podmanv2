from django.urls import path
from . import views

urlpatterns = [
    path('buy/', views.buy_ticket, name='buy_ticket'),

]