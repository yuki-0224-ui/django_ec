from django.views.generic import TemplateView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest
from ecsite.cart import Cart
from ecsite.models import Product


class CartDetailView(TemplateView):
    template_name = 'ecsite/cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_data = self.request.session.get('cart')
        cart = Cart.from_dict(cart_data)

        products = cart.get_products(Product)

        cart_items = [
            {
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'quantity': cart.items[p.id],
                'subtotal': p.price * cart.items[p.id],
                'stock': p.stock,
            }
            for p in products
        ]

        context['cart_items'] = cart_items
        context['total'] = sum(item['subtotal'] for item in cart_items)
        return context


class CartAddView(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart_data = request.session.get('cart')
        cart = Cart.from_dict(cart_data)

        if product.is_sold_out():
            messages.error(request, '申し訳ありません。この商品は在庫切れです。')
            return redirect(request.META.get('HTTP_REFERER', 'ecsite:product_list'))

        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return HttpResponseBadRequest('Invalid quantity')

        if cart.would_exceed_quantity(product.id, quantity, product.stock):
            messages.error(
                request,
                f'在庫数を超える数量は指定できません。(現在のカート内数量: {cart.get_quantity(
                    product.id)}, 在庫数: {product.stock})'
            )
            return redirect(request.META.get('HTTP_REFERER', 'ecsite:product_list'))

        cart.add(product.id, quantity)
        request.session['cart'] = cart.to_dict()
        messages.success(request, f'{product.name}をカートに追加しました。')
        return redirect(request.META.get('HTTP_REFERER', 'ecsite:product_list'))


class CartRemoveView(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        cart_data = request.session.get('cart')
        cart = Cart.from_dict(cart_data)

        cart.remove(product_id)
        request.session['cart'] = cart.to_dict()
        return redirect('ecsite:cart_detail')


class CartClearView(View):
    def post(self, request, *args, **kwargs):
        cart_data = request.session.get('cart')
        cart = Cart.from_dict(cart_data)

        cart.clear()
        request.session['cart'] = cart.to_dict()

        messages.success(request, 'カートを空にしました。')
        return redirect('ecsite:cart_detail')
