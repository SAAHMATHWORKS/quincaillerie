from django import forms
from .models import Sale, SaleItem

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['client']

SaleItemFormset = forms.inlineformset_factory(
    Sale, SaleItem,
    fields=('produit', 'quantite', 'prix_vente'),
    extra=1,
    can_delete=True
)