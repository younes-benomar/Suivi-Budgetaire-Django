from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # Hna kangoulo l-Django chno homa l-khaanat li bghina n-affichiow l-user
        fields = ['titre', 'montant', 'categorie', 'type_transaction']
        
        # Hna kanzidou class CSS l-dik blassat l-ktaba bach nqaddouha mn b3d
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Tacos...'}),
            'montant': forms.NumberInput(attrs={'class': 'form-input'}),
            'categorie': forms.Select(attrs={'class': 'form-input'}),
            'type_transaction': forms.Select(attrs={'class': 'form-input'}),
        }