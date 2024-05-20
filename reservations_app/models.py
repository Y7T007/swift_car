from django.db import models
from djongo import models as djongo_models

class Reservation(models.Model):
    reservation_id = models.IntegerField()
    client_id = djongo_models.ObjectIdField()
    manager_id = djongo_models.ObjectIdField()
    date_reservation = models.DateField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    voiture_id = models.IntegerField()
    prix= models.DecimalField(max_digits=8, decimal_places=2)