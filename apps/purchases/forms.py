from django import forms
from .models import Purchase, PurchaseItem
from apps.inventory.models import Product

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['fournisseur', 'numero_facture']

PurchaseItemFormset = forms.inlineformset_factory(
    Purchase, PurchaseItem,
    fields=('produit', 'quantite', 'prix_achat'),
    extra=1, can_delete=True
)