from django.db import models
from apps.inventory.models import Product
from apps.customers.models import Customer

class Sale(models.Model):
    client = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    utilisateur = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"

    def __str__(self):
        return f"Vente {self.id} - {self.date.strftime('%d/%m/%Y')}"

class SaleItem(models.Model):
    vente = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_vente = models.IntegerField()
    sous_total = models.IntegerField(editable=False)

    class Meta:
        verbose_name = "Ligne de vente"
        verbose_name_plural = "Lignes de vente"

    def save(self, *args, **kwargs):
        self.sous_total = self.quantite * self.prix_vente
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"