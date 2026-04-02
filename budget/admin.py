from django.contrib import admin
from .models import Categorie, Transaction, Objectif

# Hna kngoulo l Django: "A wdi 7et lina had les tables f l-Admin Panel bach nt7kmo fihom"
admin.site.register(Categorie)
admin.site.register(Transaction)
admin.site.register(Objectif)