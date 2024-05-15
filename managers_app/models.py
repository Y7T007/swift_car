from djongo import models

class Manager(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    agence_id = models.IntegerField(default=0)
    salary = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    cin = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)  # Unique email for authentication
    password = models.CharField(max_length=128)  # Password field for authentication

    def __str__(self):
        return self.name

    class Meta:
        abstract = True  # This makes the model abstract

class CustomManager(Manager):
    pass
