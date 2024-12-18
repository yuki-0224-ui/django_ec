from django.db import models
from .product import Product
from .promotion import PromotionCode


class Cart(models.Model):
    class Meta:
        db_table = 'carts'

    promotion_code = models.ForeignKey(
        'PromotionCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_item(self, product: Product, quantity: int = 1) -> 'CartItem':
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    def remove_item(self, product: Product) -> None:
        CartItem.objects.filter(cart=self, product=product).delete()

    def check_stock_exceed(self, product: Product, add_quantity: int) -> tuple[bool, int]:
        try:
            current_quantity = self.items.get(product=product).quantity
        except CartItem.DoesNotExist:
            current_quantity = 0
        return (current_quantity + add_quantity) > product.stock, current_quantity

    def get_total_amount(self) -> int:
        cart_items = self.items.select_related('product').all()
        subtotal = sum(item.get_subtotal() for item in cart_items)

        if self.promotion_code and not self.promotion_code.is_used:
            return max(0, subtotal - self.promotion_code.discount_amount)
        return subtotal

    def apply_promotion_code(self, code: str) -> tuple[bool, str]:
        try:
            promotion = PromotionCode.objects.get(code=code, is_used=False)
            if self.promotion_code:
                return False, 'プロモーションコードは既に適用されています。'
            self.promotion_code = promotion
            self.save()
            return True, f'プロモーションコードを適用しました。{promotion.discount_amount}円割引されます。'
        except PromotionCode.DoesNotExist:
            return False, '無効なプロモーションコードです。'


class CartItem(models.Model):
    class Meta:
        db_table = 'cart_items'

    cart = models.ForeignKey(Cart, related_name='items',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_subtotal(self) -> int:
        return self.product.price * self.quantity
