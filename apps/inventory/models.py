from django.db import models

class Category(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom
    

class Product(models.Model):
    code = models.CharField("Code produit", max_length=50, unique=True)
    nom = models.CharField(max_length=150)
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField(blank=True, null=True)
    unite = models.CharField("Unité", max_length=30, default='pièce')  # pièce, kg, litre...
    prix_achat = models.IntegerField()
    prix_vente = models.IntegerField()
    stock_actuel = models.PositiveIntegerField(default=0)
    stock_minimum = models.PositiveIntegerField(default=5)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return f"{self.code} - {self.nom}"
    

class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        ENTREE = 'ENTREE', 'Entrée'
        SORTIE = 'SORTIE', 'Sortie'
        AJUSTEMENT = 'AJUSTEMENT', 'Ajustement'

    produit = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mouvements')
    type_mouvement = models.CharField(max_length=15, choices=MovementType.choices)
    quantite = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    # Nouvelles relations pour lier la facture source
    vente = models.ForeignKey('sales.Sale', on_delete=models.SET_NULL, null=True, blank=True, related_name='mouvements')
    achat = models.ForeignKey('purchases.Purchase', on_delete=models.SET_NULL, null=True, blank=True, related_name='mouvements')

    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date']

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.quantite})"
    

class Inventory(models.Model):
    STATUS = (
        ('BROUILLON', 'Brouillon'),
        ('EN_COURS', 'En cours'),
        ('VALIDE', 'Validé'),
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(max_length=15, choices=STATUS, default='BROUILLON')
    utilisateur = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Inventaire"
        verbose_name_plural = "Inventaires"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Inventaire #{self.id} du {self.date_creation.strftime('%d/%m/%Y')}"


class InventoryItem(models.Model):
    inventaire = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock_theorique = models.PositiveIntegerField()
    stock_reel = models.PositiveIntegerField(null=True, blank=True)
    ecart = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Ligne d'inventaire"
        verbose_name_plural = "Lignes d'inventaire"
        unique_together = ('inventaire', 'produit')

    def save(self, *args, **kwargs):
        if self.stock_reel is not None:
            self.ecart = self.stock_reel - self.stock_theorique
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produit.nom} : {self.stock_theorique} -> {self.stock_reel}"