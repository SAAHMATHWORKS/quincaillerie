from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

        # ... (catégories)
    path('produits/', views.ProductListView.as_view(), name='product_list'),
    path('produits/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('produits/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('produits/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('ajustement/', views.stock_adjustment, name='stock_adjustment'),
    path('mouvements/', views.StockMovementListView.as_view(), name='stock_movement_list'),

    # inventaire
    path('inventaires/', views.InventoryListView.as_view(), name='inventory_list'),
    path('inventaires/nouveau/', views.InventoryCreateView.as_view(), name='inventory_create'),
    path('inventaires/<int:pk>/compter/', views.InventoryCountView.as_view(), name='inventory_count'),
    path('inventaires/<int:pk>/confirmation/', views.InventoryConfirmView.as_view(), name='inventory_confirm'),
    path('inventaires/<int:pk>/appliquer/', views.InventoryApplyView.as_view(), name='inventory_apply'),
    path('inventaires/<int:pk>/', views.InventoryDetailView.as_view(), name='inventory_detail'),
]