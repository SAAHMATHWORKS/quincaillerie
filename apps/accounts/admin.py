from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Personnalisation de l'affichage des utilisateurs
UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
UserAdmin.list_filter = ('is_active', 'is_staff', 'groups')

# Réenregistrer le modèle User avec la configuration personnalisée
admin.site.unregister(User)
admin.site.register(User, UserAdmin)