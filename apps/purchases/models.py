from django.db import models
from apps.inventory.models import Product
from apps.suppliers.models import Supplier

class Purchase(models.Model):
    fournisseur = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    numero_facture = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    montant_total = models.IntegerField(default=0)
    utilisateur = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Achat"
        verbose_name_plural = "Achats"

    def __str__(self):
        return f"Achat {self.id} - {self.date.strftime('%d/%m/%Y')}"

class PurchaseItem(models.Model):
    achat = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_achat = models.IntegerField()
    sous_total = models.IntegerField(editable=False)

    class Meta:
        verbose_name = "Ligne d'achat"
        verbose_name_plural = "Lignes d'achat"

    def save(self, *args, **kwargs):
        self.sous_total = self.quantite * self.prix_achat
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"