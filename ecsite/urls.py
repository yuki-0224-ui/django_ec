from django.urls import path
from .views import ProductListView, ProductDetailView
from .views.admin_views import (
    AdminProductListView,
    AdminProductCreateView,
    AdminProductUpdateView,
    AdminProductDeleteView
)

app_name = 'ecsite'
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('admin/products/', AdminProductListView.as_view(),
         name='admin_product_list'),
    path('admin/products/create/', AdminProductCreateView.as_view(),
         name='admin_product_create'),
    path('admin/products/<slug:slug>/update/',
         AdminProductUpdateView.as_view(), name='admin_product_update'),
    path('admin/products/<slug:slug>/delete/',
         AdminProductDeleteView.as_view(), name='admin_product_delete'),
]
