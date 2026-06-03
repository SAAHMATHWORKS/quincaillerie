from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['nom', 'telephone', 'email', 'adresse']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['nom', 'telephone', 'email', 'adresse']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')


@login_required
def customer_create_ajax(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        email = request.POST.get('email', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        if nom:
            customer = Customer.objects.create(
                nom=nom,
                telephone=telephone,
                email=email,
                adresse=adresse
            )
            return JsonResponse({'success': True, 'id': customer.id, 'nom': customer.nom})
        else:
            return JsonResponse({'success': False, 'error': 'Le nom est obligatoire.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'}, status=400)