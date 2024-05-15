from django.db import models

class Voiture(models.Model):
    voiture_id = models.IntegerField()
    marque = models.CharField(max_length=255)
    famille = models.CharField(max_length=255)
    couleur = models.CharField(max_length=255)
    capacite_sieges = models.IntegerField()
    matricule = models.CharField(max_length=255)
    carte_grise_id = models.IntegerField()
    assurance_date_fin = models.DateField()
    vignette_date_fin = models.DateField()
    visite_date_fin = models.DateField()
    visite_etat = models.IntegerField()
    agence_id = models.IntegerField()
    prix_par_jour = models.FloatField()
    disponibilite = models.BooleanField()
    puissance_fiscale = models.IntegerField()
    vitesse_max = models.IntegerField()
    kilometrage = models.IntegerField()
    transmission = models.CharField(max_length=255)
    carburant = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)

def save(self, *args, **kwargs):
    # Call the "real" save() method.
    super(Voiture, self).save(*args, **kwargs)