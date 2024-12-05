from django.views.generic import TemplateView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest
from ..models import Product, Cart


class CartMixin:
    def get_cart(self, create=True):
        cart_id = self.request.session.get('cart_id')

        if cart_id:
            try:
                return Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                if not create:
                    return None

        if create:
            cart = Cart.objects.create()
            self.request.session['cart_id'] = cart.id
            return cart

        return None


class CartDetailView(CartMixin, TemplateView):
    template_name = 'ecsite/cart/detail.html'


class CartAddView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart = self.get_cart()

        if product.is_sold_out():
            messages.error(request, '申し訳ありません。この商品は在庫切れです。')
            return redirect(request.META.get('HTTP_REFERER', 'ecsite:product_list'))

        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return HttpResponseBadRequest('Invalid quantity')

        is_exceeded, current_quantity = cart.check_stock_exceed(
            product, quantity)
        if is_exceeded:
            messages.error(
                request,
                f'在庫数を超える数量は指定できません。(現在のカート内数量: {current_quantity}, 在庫数: {
                    product.stock})'
            )
            return redirect(request.META.get('HTTP_REFERER', 'ecsite:product_list'))

        cart.add_item(product, quantity)
        messages.success(request, f'{product.name}をカートに追加しました。')
        return redirect(request.META.get('HTTP_REFERER', 'ecsite:product_list'))


class CartRemoveView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart = self.get_cart(create=False)

        if cart:
            cart.remove_item(product)

        return redirect('ecsite:cart_detail')
