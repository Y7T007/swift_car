from djongo import models as djongo_models
from django.db import models
from managers_app.models import Manager

class Client(models.Model):
    _id = djongo_models.ObjectIdField()
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1)
    contact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    cin = models.CharField(max_length=255)
    fidelity_score = models.IntegerField()
    permis_conductor = models.CharField(max_length=255)