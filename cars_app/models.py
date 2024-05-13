from django.db import models
from auth_app.models import User

class Manager(User):
    manager_id = models.IntegerField()
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1)
    contact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    agence_id = models.IntegerField()
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    cin = models.CharField(max_length=255)