from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncMonth
from apps.inventory.models import Product
from apps.suppliers.models import Supplier
from apps.customers.models import Customer
from apps.sales.models import Sale, SaleItem
from apps.purchases.models import Purchase, PurchaseItem
from django.utils.timezone import make_aware



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupération des paramètres de période
        date_debut_str = self.request.GET.get('date_debut')
        date_fin_str = self.request.GET.get('date_fin')

        # Par défaut : du 1er jour du mois en cours à aujourd'hui
        today = datetime.now().date()
        if not date_debut_str:
            date_debut = today.replace(day=1)
        else:
            date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
        if not date_fin_str:
            date_fin = today
        else:
            date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date()

        # Pour les filtres ORM, on utilise des dates avec heure min et max
        dt_debut = make_aware(datetime.combine(date_debut, datetime.min.time()))
        dt_fin = make_aware(datetime.combine(date_fin, datetime.max.time()))
        # dt_debut = datetime.combine(date_debut, datetime.min.time())
        # dt_fin = datetime.combine(date_fin, datetime.max.time())

        context['date_debut'] = date_debut
        context['date_fin'] = date_fin

        # Cartes statistiques
        context['nb_produits'] = Product.objects.filter(actif=True).count()
        context['nb_fournisseurs'] = Supplier.objects.filter(actif=True).count()
        context['nb_clients'] = Customer.objects.count()
        context['nb_stock_faible'] = Product.objects.filter(
            actif=True, stock_actuel__lte=F('stock_minimum')
        ).count()
        context['nb_ventes_periode'] = Sale.objects.filter(
            date__gte=dt_debut, date__lte=dt_fin
        ).count()
        context['total_ventes_periode'] = Sale.objects.filter(
            date__gte=dt_debut, date__lte=dt_fin
        ).aggregate(total=Sum('total'))['total'] or 0
        context['nb_achats_periode'] = Purchase.objects.filter(
            date__gte=dt_debut, date__lte=dt_fin
        ).count()
        context['total_achats_periode'] = Purchase.objects.filter(
            date__gte=dt_debut, date__lte=dt_fin
        ).aggregate(total=Sum('montant_total'))['total'] or 0

        # Graphique 1 : Ventes mensuelles sur la période (ou sur l'année si période > 12 mois ?)
        # On groupe par mois toutes les ventes, on filtre sur la période si nécessaire
        ventes_mensuelles = (
            Sale.objects.filter(date__gte=dt_debut, date__lte=dt_fin)
            .annotate(mois=TruncMonth('date'))
            .values('mois')
            .annotate(total=Sum('total'))
            .order_by('mois')
        )
        ventes_labels = [v['mois'].strftime('%b %Y') for v in ventes_mensuelles]
        ventes_data = [float(v['total']) for v in ventes_mensuelles]
        context['ventes_labels'] = ventes_labels
        context['ventes_data'] = ventes_data

        # Graphique 2 : Achats mensuels
        achats_mensuels = (
            Purchase.objects.filter(date__gte=dt_debut, date__lte=dt_fin)
            .annotate(mois=TruncMonth('date'))
            .values('mois')
            .annotate(total=Sum('montant_total'))
            .order_by('mois')
        )
        achats_labels = [a['mois'].strftime('%b %Y') for a in achats_mensuels]
        achats_data = [float(a['total']) for a in achats_mensuels]
        context['achats_labels'] = achats_labels
        context['achats_data'] = achats_data

        # Graphique 3 : Top produits vendus sur la période (quantité)
        top_produits = (
            SaleItem.objects.filter(vente__date__gte=dt_debut, vente__date__lte=dt_fin)
            .values('produit__nom')
            .annotate(total_qte=Sum('quantite'))
            .order_by('-total_qte')[:10]
        )
        top_labels = [p['produit__nom'] for p in top_produits]
        top_qtes = [p['total_qte'] for p in top_produits]
        context['top_labels'] = top_labels
        context['top_qtes'] = top_qtes

        return context