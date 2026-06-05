from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('sous_total',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'client', 'total', 'utilisateur')
    list_filter = ('date', 'client')
    date_hierarchy = 'date'
    inlines = [SaleItemInline]
    readonly_fields = ('total',)

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('vente', 'produit', 'quantite', 'prix_vente', 'sous_total')
    list_filter = ('vente__date',)