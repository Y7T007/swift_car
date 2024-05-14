from django.db import models
from clients_app.models import Client
from managers_app.models import Manager

class Reservation(models.Model):
    reservation_id = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    date_reservation = models.DateField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    voiture_id = models.IntegerField()