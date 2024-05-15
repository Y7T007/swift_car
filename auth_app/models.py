from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # your fields here
    phone_number = models.CharField(max_length=15, blank=True, null=True)