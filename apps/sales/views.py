from io import BytesIO

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.db import transaction, models as db_models
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormset
from apps.inventory.models import StockMovement
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
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


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sale_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = SaleItemFormset(self.request.POST)
        else:
            context['items_formset'] = SaleItemFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.utilisateur = self.request.user
            self.object.total = 0

            if not items_formset.is_valid():
                return self.form_invalid(form)

            # Vérifier les stocks avant toute écriture
            for item_form in items_formset:
                if item_form.cleaned_data.get('quantite') is None:
                    continue
                if item_form.cleaned_data.get('DELETE'):
                    continue
                produit = item_form.cleaned_data['produit']
                quantite = item_form.cleaned_data['quantite']
                if produit.stock_actuel < quantite:
                    messages.error(self.request, f"Stock insuffisant pour {produit.nom} (stock actuel : {produit.stock_actuel}, demandé : {quantite}).")
                    return self.form_invalid(form)

            self.object.save()

            total = 0
            for item_form in items_formset:
                if item_form.cleaned_data.get('DELETE'):
                    continue
                if item_form.cleaned_data.get('quantite') is not None:
                    item = item_form.save(commit=False)
                    item.vente = self.object
                    item.save()
                    total += item.sous_total

                    # Mise à jour du stock (soustraction)
                    produit = item.produit
                    produit.stock_actuel -= item.quantite
                    produit.save()

                    # Mouvement de stock
                    StockMovement.objects.create(
                        produit=produit,
                        type_mouvement='SORTIE',
                        quantite=item.quantite,
                        utilisateur=self.request.user,
                        reference=f"Vente #{self.object.id}",
                        vente=self.object 
                    )

            self.object.total = total
            self.object.save()

        messages.success(self.request, "Vente enregistrée et stock mis à jour.")
        return super().form_valid(form)

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
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

class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'

class SaleReceiptView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sale_receipt.html'
    context_object_name = 'sale'


@login_required
def sale_detail_modal(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    html = f"""
    <div class="modal-header">
        <h5 class="modal-title">Vente #{sale.id}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fermer"></button>
    </div>
    <div class="modal-body">
        <p><strong>Date :</strong> {sale.date.strftime('%d/%m/%Y %H:%M')}</p>
        <p><strong>Client :</strong> {sale.client.nom if sale.client else 'Client divers'}</p>
        <p><strong>Total :</strong> {sale.total} €</p>
        <h6>Articles</h6>
        <ul>
        {''.join(f'<li>{item.produit.nom} x{item.quantite} = {item.sous_total} €</li>' for item in sale.items.all())}
        </ul>
    </div>
    """
    return HttpResponse(html)


class SaleInvoicePDFView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sale_invoice_pdf.html'

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
        response['Content-Disposition'] = f'inline; filename="facture_vente_{self.object.id}.pdf"'
        return response