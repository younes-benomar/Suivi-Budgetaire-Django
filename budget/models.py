from django.db import models
from django.contrib.auth.models import User 

class Categorie(models.Model):
    # s7i7a
    nom = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.nom

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('REVENU', 'Revenu'),
        ('DEPENSE', 'Dépense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Bddelna max_width b max_length hna
    titre = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    # Bddelna max_width b max_length hna
    type_transaction = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.montant} DH"

class Objectif(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Bddelna max_width b max_length hna
    titre = models.CharField(max_length=100)
    montant_cible = models.DecimalField(max_digits=10, decimal_places=2)
    date_limite = models.DateField()

    def __str__(self):
        return self.titre