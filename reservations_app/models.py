from django.db import models
from djongo import models as djongo_models
from cars_app.models import Voiture
from clients_app.models import Client
from managers_app.models import Manager

class Reservation(models.Model):
    _id = djongo_models.ObjectIdField()
    reservation_id = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    date_reservation = models.DateField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    prix= models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=255)