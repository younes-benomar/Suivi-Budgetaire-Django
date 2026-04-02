import csv
import json
from django.shortcuts import render, redirect # <-- Zidna redirect hna
from django.http import HttpResponse
from django.db.models import Sum
from .models import Transaction, Objectif
from .forms import TransactionForm # <-- Jbna l-Formulaire li yalah sawbna
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# --- L-MANTIQ DYAL SÉCURITÉ ---

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Mlli ytsjjel, dkhlo nichan bla may3awed ykteb l-mot de passe
            return redirect('liste_transactions')
    else:
        form = UserCreationForm()
    return render(request, 'budget/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('liste_transactions')
    else:
        form = AuthenticationForm()
    return render(request, 'budget/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login') # Mlli ykhrej, sifto l-sf7at login



def liste_transactions(request):
    # L-Mantiq dyal l-Formulaire (Ajouter une dépense)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save() # Kikhbi l-m3loumat f l-base de données
            return redirect('liste_transactions') # Ki-actualiser s-sf7a
    else:
        form = TransactionForm() # Formulaire khawi ila yalah dkhlti

    transactions = Transaction.objects.all().order_by('-date')
    
    total_depenses = transactions.filter(type_transaction='DEPENSE').aggregate(Sum('montant'))['montant__sum'] or 0
    total_revenus = transactions.filter(type_transaction='REVENU').aggregate(Sum('montant'))['montant__sum'] or 0
    solde = total_revenus - total_depenses
    
    # L-Mantiq dyal l-Graphique
    depenses_par_cat = transactions.filter(type_transaction='DEPENSE').values('categorie__nom').annotate(total=Sum('montant'))
    
    labels_graphique = []
    data_graphique = []
    
    for item in depenses_par_cat:
        nom_cat = item['categorie__nom'] if item['categorie__nom'] else 'Autre'
        labels_graphique.append(nom_cat)
        data_graphique.append(float(item['total']))

    # L-Mantiq dyal les Objectifs
    objectifs_db = Objectif.objects.all()
    objectifs_list = []
    
    for obj in objectifs_db:
        if obj.montant_cible > 0:
            pourcentage = (solde / obj.montant_cible) * 100
            pourcentage = min(float(pourcentage), 100) 
        else:
            pourcentage = 0
            
        objectifs_list.append({
            'titre': obj.titre,
            'montant_cible': obj.montant_cible,
            'date_limite': obj.date_limite,
            'pourcentage': round(pourcentage, 1)
        })

    context = {
        'transactions': transactions,
        'total_depenses': total_depenses,
        'total_revenus': total_revenus,
        'solde': solde,
        'labels_json': json.dumps(labels_graphique),
        'data_json': json.dumps(data_graphique),
        'objectifs': objectifs_list,
        'form': form, # <-- Siftna l-formulaire l-HTML
    }
    
    return render(request, 'budget/liste.html', context)

# (Khli fonction export_excel kima hiya l-ta7t)

def export_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historique_budget.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Titre', 'Categorie', 'Type', 'Montant (DH)'])
    
    transactions = Transaction.objects.all().order_by('-date')
    for t in transactions:
        nom_cat = t.categorie.nom if t.categorie else 'Autre'
        writer.writerow([t.date, t.titre, nom_cat, t.type_transaction, t.montant])
        
    return response