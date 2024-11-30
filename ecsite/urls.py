from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = 'ecsite'
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
