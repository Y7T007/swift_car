from django.db import models
from djongo import models as djongo_models

class Manager(models.Model):
    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    agence_id = models.IntegerField(default=0)
    salary = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    cin = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)