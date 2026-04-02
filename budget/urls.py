from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_transactions, name='liste_transactions'),
    # Hada howa s-sṭer li na9es awla mazal mamsauvegardach:
    path('export/', views.export_excel, name='export_excel'), 
]