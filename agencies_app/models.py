from django.db import models
from djongo import models as djongo_models


class Agence(models.Model):
    _id = djongo_models.ObjectIdField()
    agence_id = models.IntegerField()
    name = models.CharField(max_length=255)
    date_of_creation = models.DateField()
    ville = models.CharField(max_length=255)
    fix_fax = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_maps = models.TextField()