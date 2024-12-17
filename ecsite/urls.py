from django.urls import path
from ecsite.views.product_view import ProductListView, ProductDetailView
from ecsite.views.admin_views import (
    AdminProductListView,
    AdminProductCreateView,
    AdminProductUpdateView,
    AdminProductDeleteView,
    AdminOrderListView,
    AdminOrderDetailView
)
from ecsite.views.cart_views import CartDetailView, CartAddView, CartRemoveView

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
    path('admin/orders/', AdminOrderListView.as_view(), name='admin_order_list'),
    path('admin/orders/<int:pk>/', AdminOrderDetailView.as_view(),
         name='admin_order_detail'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/',
         CartRemoveView.as_view(), name='cart_remove'),
]
