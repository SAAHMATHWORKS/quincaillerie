from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from apps.accounts.views import CustomLoginView, CustomLogoutView, CustomPasswordChangeView, home

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('apps.dashboard.urls')),
    # path('', home, name='home'),

    # Authentification
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change/done/',
         TemplateView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    # Inclusion des URLs restantes de django.contrib.auth (réinitialisation de mot de passe etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
    path('customers/', include('apps.customers.urls')),
    path('purchases/', include('apps.purchases.urls')),
    path('sales/', include('apps.sales.urls')),
    path('audit/', include('apps.audit.urls')),
]