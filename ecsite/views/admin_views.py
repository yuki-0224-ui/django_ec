from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from basicauth.decorators import basic_auth_required
from ecsite.models import Product
from ecsite.forms.admin_forms import ProductForm
from ecsite.models.order import Order

basic_auth = basic_auth_required()


@method_decorator(basic_auth, name='dispatch')
class AdminProductListView(ListView):
    model = Product
    template_name = 'ecsite/admin/product_list.html'
    context_object_name = 'products'


@method_decorator(basic_auth, name='dispatch')
class AdminProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'ecsite/admin/product_form.html'
    success_url = reverse_lazy('ecsite:admin_product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_form().formset
        return context


@method_decorator(basic_auth, name='dispatch')
class AdminProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'ecsite/admin/product_form.html'
    success_url = reverse_lazy('ecsite:admin_product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_form().formset
        return context


@method_decorator(basic_auth, name='dispatch')
class AdminProductDeleteView(DeleteView):
    model = Product
    template_name = 'ecsite/admin/product_confirm_delete.html'
    success_url = reverse_lazy('ecsite:admin_product_list')


@method_decorator(basic_auth, name='dispatch')
class AdminOrderListView(ListView):
    model = Order
    template_name = 'ecsite/admin/order/list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']
        context['total_orders'] = len(orders)
        context['total_amount'] = sum(order.total_amount for order in orders)
        return context


@method_decorator(basic_auth, name='dispatch')
class AdminOrderDetailView(DetailView):
    model = Order
    template_name = 'ecsite/admin/order/detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.items.select_related(
            'product').all()
        return context
