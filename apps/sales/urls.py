from django.urls import path
from . import views

urlpatterns = [
    path('', views.SaleListView.as_view(), name='sale_list'),
    path('create/', views.SaleCreateView.as_view(), name='sale_create'),
    path('<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    path('<int:pk>/receipt/', views.SaleReceiptView.as_view(), name='sale_receipt'),

    path('<int:pk>/modal/', views.sale_detail_modal, name='sale_detail_modal'),

    path('<int:pk>/facture-pdf/', views.SaleInvoicePDFView.as_view(), name='sale_invoice_pdf'),
]