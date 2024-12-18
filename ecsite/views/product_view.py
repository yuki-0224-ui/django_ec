from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from ecsite.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'ecsite/products/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.get_available().prefetch_related('images')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecsite/products/detail.html'

    def get_queryset(self):
        return Product.get_available().prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.get_available()\
            .prefetch_related('images')\
            .exclude(pk=self.object.pk)[:6]
        return context
