from django.urls import path
from . import views

urlpatterns = [
    path('', views.PurchaseListView.as_view(), name='purchase_list'),
    path('create/', views.PurchaseCreateView.as_view(), name='purchase_create'),
    path('<int:pk>/', views.PurchaseDetailView.as_view(), name='purchase_detail'),

    path('<int:pk>/modal/', views.purchase_detail_modal, name='purchase_detail_modal'),
    path('<int:pk>/bon-pdf/', views.PurchaseOrderPDFView.as_view(), name='purchase_order_pdf'),
]