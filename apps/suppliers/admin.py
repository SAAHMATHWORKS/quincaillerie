from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'email', 'ville', 'actif', 'date_creation')
    list_filter = ('actif', 'ville')
    search_fields = ('nom', 'email', 'telephone')
    list_editable = ('actif',)