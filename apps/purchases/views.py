from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Purchase, PurchaseItem
from .forms import PurchaseForm, PurchaseItemFormset
from apps.inventory.models import StockMovement, Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import base64
from django.conf import settings
import os


def get_logo_base64():
    """Retourne le logo en base64 ou None si absent."""
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpeg')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchases/purchase_form.html'
    success_url = reverse_lazy('purchase_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = PurchaseItemFormset(self.request.POST)
        else:
            context['items_formset'] = PurchaseItemFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.utilisateur = self.request.user
            self.object.montant_total = 0  # sera calculé

            if not items_formset.is_valid():
                return self.form_invalid(form)

            self.object.save()

            total = 0
            for item_form in items_formset:
                if item_form.cleaned_data.get('quantite') is not None:
                    item = item_form.save(commit=False)
                    item.achat = self.object
                    item.save()
                    total += item.sous_total

                    # Mise à jour du stock
                    produit = item.produit
                    produit.stock_actuel += item.quantite
                    produit.save()

                    # Mouvement de stock
                    StockMovement.objects.create(
                        produit=produit,
                        type_mouvement='ENTREE',
                        quantite=item.quantite,
                        utilisateur=self.request.user,
                        reference=self.object.numero_facture or f"Achat #{self.object.id}"
                    )

            self.object.montant_total = total
            self.object.save()

        messages.success(self.request, "Achat enregistré et stock mis à jour.")
        return super().form_valid(form)

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'purchases/purchase_list.html'
    context_object_name = 'purchases'
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        date_debut = self.request.GET.get('date_debut')
        date_fin = self.request.GET.get('date_fin')
        if date_debut:
            queryset = queryset.filter(date__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date__lte=date_fin)
        return queryset

class PurchaseDetailView(LoginRequiredMixin, DetailView):
    model = Purchase
    template_name = 'purchases/purchase_detail.html'


@login_required
def purchase_detail_modal(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    html = f"""
    <div class="modal-header">
        <h5 class="modal-title">Achat #{purchase.id}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fermer"></button>
    </div>
    <div class="modal-body">
        <p><strong>Date :</strong> {purchase.date.strftime('%d/%m/%Y %H:%M')}</p>
        <p><strong>Fournisseur :</strong> {purchase.fournisseur.nom if purchase.fournisseur else '-'}</p>
        <p><strong>Facture :</strong> {purchase.numero_facture or '-'}</p>
        <p><strong>Total :</strong> {purchase.montant_total} €</p>
        <h6>Articles</h6>
        <ul>
        {''.join(f'<li>{item.produit.nom} x{item.quantite} = {item.sous_total} €</li>' for item in purchase.items.all())}
        </ul>
    </div>
    """
    return HttpResponse(html)

class PurchaseOrderPDFView(LoginRequiredMixin, DetailView):
    model = Purchase
    template_name = 'purchases/purchase_order_pdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo_base64'] = get_logo_base64()
        return context

    def render_to_response(self, context, **response_kwargs):
        html = render_to_string(self.template_name, context, request=self.request)
        result = BytesIO()
        try:
            HTML(string=html).write_pdf(result)
        except Exception as e:
            return HttpResponse(f"Erreur de génération PDF : {e}", status=500)
        result.seek(0)
        response = HttpResponse(result.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="bon_achat_{self.object.id}.pdf"'
        return response