from django.contrib import admin
from .models import Category, Product, StockMovement, Inventory, InventoryItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'date_creation')
    search_fields = ('nom', 'description')
    list_filter = ('date_creation',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'categorie', 'prix_achat', 'prix_vente', 'stock_actuel', 'stock_minimum', 'actif')
    list_filter = ('actif', 'categorie')
    search_fields = ('code', 'nom', 'description')
    list_editable = ('prix_achat', 'prix_vente', 'stock_actuel', 'stock_minimum', 'actif')
    readonly_fields = ('date_creation',)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('date', 'produit', 'type_mouvement', 'quantite', 'utilisateur', 'reference')
    list_filter = ('type_mouvement', 'date')
    search_fields = ('produit__nom', 'reference')
    readonly_fields = ('date',)
    date_hierarchy = 'date'

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation', 'categorie', 'statut', 'utilisateur')
    list_filter = ('statut', 'categorie')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('inventaire', 'produit', 'stock_theorique', 'stock_reel', 'ecart')
    list_filter = ('inventaire',)