from django.contrib import admin
from .models import Purchase, PurchaseItem

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0
    readonly_fields = ('sous_total',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'fournisseur', 'numero_facture', 'montant_total', 'utilisateur')
    list_filter = ('date', 'fournisseur')
    search_fields = ('numero_facture', 'fournisseur__nom')
    date_hierarchy = 'date'
    inlines = [PurchaseItemInline]
    readonly_fields = ('montant_total',)

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('achat', 'produit', 'quantite', 'prix_achat', 'sous_total')
    list_filter = ('achat__date',)