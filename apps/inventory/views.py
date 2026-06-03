from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Category, Product, StockMovement
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockAdjustmentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Inventory, InventoryItem, Product
from .forms import InventoryStartForm
from django.db import transaction

class InventoryListView(LoginRequiredMixin, ListView):
    model = Inventory
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'inventories'
    paginate_by = 15

class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryStartForm
    template_name = 'inventory/inventory_form.html'
    success_url = None  # sera redirigé dynamiquement

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.utilisateur = self.request.user
        obj.statut = 'BROUILLON'
        obj.save()
        return redirect('inventory_count', pk=obj.pk)

class InventoryCountView(LoginRequiredMixin, DetailView):
    model = Inventory
    template_name = 'inventory/inventory_count.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory = self.object
        # Filtrer les produits
        produits = Product.objects.filter(actif=True)
        if inventory.categorie:
            produits = produits.filter(categorie=inventory.categorie)
        context['produits'] = produits
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        inventory = self.object
        # Récupérer les données du formulaire
        produits_ids = request.POST.getlist('produit_id')
        stock_reels = request.POST.getlist('stock_reel')

        # Créer les InventoryItem
        for pid, reel_str in zip(produits_ids, stock_reels):
            if not reel_str.strip():
                continue  # ignorer les lignes vides
            try:
                reel = int(reel_str)
            except ValueError:
                messages.error(request, f"Valeur invalide pour la quantité (ID {pid})")
                return redirect('inventory_count', pk=inventory.pk)
            produit = get_object_or_404(Product, pk=pid)
            # Créer ou mettre à jour
            InventoryItem.objects.update_or_create(
                inventaire=inventory,
                produit=produit,
                defaults={
                    'stock_theorique': produit.stock_actuel,
                    'stock_reel': reel,
                }
            )
        inventory.statut = 'EN_COURS'
        inventory.save()
        return redirect('inventory_confirm', pk=inventory.pk)

class InventoryConfirmView(LoginRequiredMixin, DetailView):
    model = Inventory
    template_name = 'inventory/inventory_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.items.all()
        context['items'] = items
        context['ecarts'] = items.filter(ecart__isnull=False).exclude(ecart=0)
        return context

class InventoryApplyView(LoginRequiredMixin, View):
    def post(self, request, pk):
        inventory = get_object_or_404(Inventory, pk=pk, statut='EN_COURS')
        with transaction.atomic():
            for item in inventory.items.all():
                if item.ecart is None or item.ecart == 0:
                    continue
                produit = item.produit
                produit.stock_actuel = item.stock_reel  # aligner le stock sur le réel
                produit.save()
                # Mouvement de stock
                type_mvt = 'ENTREE' if item.ecart > 0 else 'SORTIE'
                StockMovement.objects.create(
                    produit=produit,
                    type_mouvement=type_mvt,
                    quantite=abs(item.ecart),
                    utilisateur=request.user,
                    reference=f"Inventaire #{inventory.id}"
                )
            inventory.statut = 'VALIDE'
            inventory.date_validation = timezone.now()
            inventory.save()
        messages.success(request, "Les ajustements ont été appliqués et les stocks sont à jour.")
        return redirect('inventory_detail', pk=inventory.pk)

class InventoryDetailView(LoginRequiredMixin, DetailView):
    model = Inventory
    template_name = 'inventory/inventory_detail.html'

# --- Catégories (inchangé) ---
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['nom', 'description']
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['nom', 'description']
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'inventory/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

# --- Produits ---
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.select_related('categorie').all()
        q = self.request.GET.get('q')
        categorie = self.request.GET.get('categorie')
        if q:
            queryset = queryset.filter(
                Q(code__icontains=q) | Q(nom__icontains=q) | Q(description__icontains=q)
            )
        if categorie:
            queryset = queryset.filter(categorie_id=categorie)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['code', 'nom', 'categorie', 'description', 'unite',
              'prix_achat', 'prix_vente', 'stock_actuel', 'stock_minimum', 'actif']
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['code', 'nom', 'categorie', 'description', 'unite',
              'prix_achat', 'prix_vente', 'stock_actuel', 'stock_minimum', 'actif']
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_or_superuser)
def stock_adjustment(request):
    if request.method == 'POST':
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            produit = form.cleaned_data['produit']
            quantite = form.cleaned_data['quantite']
            motif = form.cleaned_data['motif']

            if quantite > 0:
                type_mvt = 'ENTREE'
                produit.stock_actuel += quantite
            else:
                type_mvt = 'SORTIE'
                produit.stock_actuel += quantite  # quantite est négative

            produit.save()

            StockMovement.objects.create(
                produit=produit,
                type_mouvement=type_mvt,
                quantite=abs(quantite),
                utilisateur=request.user,
                reference=f"Ajustement manuel - {motif[:50]}"
            )

            messages.success(request, f"Stock de {produit.nom} ajusté ({type_mvt} de {abs(quantite)}).")
            return redirect('stock_adjustment')
    else:
        form = StockAdjustmentForm()
    return render(request, 'inventory/stock_adjustment.html', {'form': form})

class StockMovementListView(LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = 'inventory/stock_movement_list.html'
    context_object_name = 'movements'
    paginate_by = 20

    def get_queryset(self):
        queryset = StockMovement.objects.select_related('produit', 'utilisateur').all()
        produit_id = self.request.GET.get('produit')
        type_mvt = self.request.GET.get('type')
        date_debut = self.request.GET.get('date_debut')
        date_fin = self.request.GET.get('date_fin')

        if produit_id:
            queryset = queryset.filter(produit_id=produit_id)
        if type_mvt:
            queryset = queryset.filter(type_mouvement=type_mvt)
        if date_debut:
            queryset = queryset.filter(date__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date__lte=date_fin)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produits'] = Product.objects.all()
        context['types_mouvement'] = StockMovement.MovementType.choices
        return context
    

from django.db.models import F, Q

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.select_related('categorie').all()
        q = self.request.GET.get('q')
        categorie = self.request.GET.get('categorie')
        stock_faible = self.request.GET.get('stock_faible')

        if q:
            queryset = queryset.filter(
                Q(code__icontains=q) | Q(nom__icontains=q) | Q(description__icontains=q)
            )
        if categorie:
            queryset = queryset.filter(categorie_id=categorie)
        if stock_faible:
            queryset = queryset.filter(stock_actuel__lte=F('stock_minimum'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context