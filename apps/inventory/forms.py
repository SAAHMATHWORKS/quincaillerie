from django import forms
from .models import Product
from .models import Category, Inventory

class StockAdjustmentForm(forms.Form):
    produit = forms.ModelChoiceField(queryset=Product.objects.filter(actif=True))
    quantite = forms.IntegerField(
        label="Quantité (positive = entrée, négative = sortie)",
        help_text="Exemple : 10 pour ajouter, -5 pour retirer."
    )
    motif = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label="Motif de l'ajustement",
        help_text="Raison obligatoire (casse, perte, rééquilibrage…)"
    )

    def clean_quantite(self):
        qte = self.cleaned_data['quantite']
        if qte == 0:
            raise forms.ValidationError("La quantité ne peut pas être zéro.")
        return qte

    def clean(self):
        cleaned_data = super().clean()
        produit = cleaned_data.get('produit')
        quantite = cleaned_data.get('quantite')
        if produit and quantite is not None and quantite < 0:
            if produit.stock_actuel < abs(quantite):
                raise forms.ValidationError(
                    f"Stock insuffisant pour {produit.nom} (stock actuel : {produit.stock_actuel}, "
                    f"sortie demandée : {abs(quantite)})."
                )
        return cleaned_data


class InventoryStartForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['categorie', 'commentaire']
        widgets = {
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'commentaire': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'categorie': 'Catégorie (laisser vide pour tous les produits)',
        }