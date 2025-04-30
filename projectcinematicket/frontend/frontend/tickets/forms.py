from django import forms

ROW_CHOICES = [(str(i), f'Ряд {i}') for i in range(1, 11)]  # ряды 1-10
SEAT_CHOICES = [(str(i), f'Место {i}') for i in range(1, 21)]  # места 1-20

class TicketForm(forms.Form):
    row = forms.ChoiceField(label='Ряд', choices=ROW_CHOICES)
    seat = forms.ChoiceField(label='Место', choices=SEAT_CHOICES)
    name = forms.CharField(label='ФИО')