from django.views.generic import FormView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from ..models import Product, Cart
from ecsite.forms.order_forms import OrderForm
from ecsite.forms.promotion_forms import PromotionCodeForm
from ecsite.email_service import send_order_confirmation


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


class CartDetailView(CartMixin, FormView):
    template_name = 'ecsite/cart/detail.html'
    form_class = OrderForm
    success_url = reverse_lazy('ecsite:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.cart = self.get_cart(create=False)
        if not self.cart or not self.cart.items.exists():
            messages.warning(request, 'カートが空です。')
            return redirect('ecsite:product_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.cart

        if cart.promotion_code:
            if not cart.promotion_code.is_used:
                context['discount_amount'] = cart.promotion_code.discount_amount
                context['total_after_discount'] = cart.get_total_amount()
            else:
                cart.promotion_code = None
                cart.save()

        if not cart.promotion_code:
            context['promotion_form'] = PromotionCodeForm()

        return context

    def post(self, request, *args, **kwargs):
        if 'apply_promotion' not in request.POST:
            return super().post(request, *args, **kwargs)

        cart = self.cart
        promotion_form = PromotionCodeForm(request.POST)

        if not promotion_form.is_valid():
            error_message = promotion_form.errors.get(
                'code', ["無効なプロモーションコードです"])[0]
            messages.error(request, error_message)
            return redirect('ecsite:cart_detail')

        success, message = cart.apply_promotion_code(
            promotion_form.cleaned_data['code'])
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect('ecsite:cart_detail')

    def form_valid(self, form):
        cart = self.cart
        if not cart or not cart.items.exists():
            messages.error(self.request, 'カートが空です。')
            return redirect('ecsite:product_list')

        for item in cart.items.select_related('product').all():
            if item.quantity > item.product.stock:
                messages.error(
                    self.request,
                    f'{item.product.name}の在庫が不足しています。'
                )
                return self.form_invalid(form)

        order = form.save(commit=False)
        order.create_order_items(cart)

        if order.email:
            send_order_confirmation(order)

        cart.delete()
        if 'cart_id' in self.request.session:
            del self.request.session['cart_id']

        messages.success(self.request, '購入ありがとうございます')
        return super().form_valid(form)


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
