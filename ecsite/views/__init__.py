from .admin_views import (
    AdminProductListView,
    AdminProductCreateView,
    AdminProductUpdateView,
    AdminProductDeleteView,
)
from .product_view import ProductListView, ProductDetailView

__all__ = [
    'AdminProductListView',
    'AdminProductCreateView',
    'AdminProductUpdateView',
    'AdminProductDeleteView',
    'ProductListView',
    'ProductDetailView',
]
