from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'email', 'adresse', 'date_creation')
    search_fields = ('nom', 'email', 'telephone')