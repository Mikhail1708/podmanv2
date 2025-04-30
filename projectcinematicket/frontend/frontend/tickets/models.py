from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Можно добавить поле для постера, жанра и т.д.

    def str(self):
        return self.title

class Session(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='sessions')
    time = models.TimeField()
    date = models.DateField()
    # Можно добавить зал, цену и т.д.

    def str(self):
        return f"{self.film.title} {self.date} {self.time}"

class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='tickets')
    row = models.IntegerField()
    seat = models.IntegerField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.name} - {self.session} (ряд {self.row}, место {self.seat})"