from django.db import models
from .product import Product
from .cart import Cart


class Order(models.Model):
    class Meta:
        db_table = 'orders'

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    card_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    card_expiration = models.CharField(max_length=5)
    card_cvv = models.CharField(max_length=4)

    total_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"注文 #{self.id} - {self.last_name} {self.first_name} ({self.created_at: %Y-%m-%d})"

    def create_order_items(self, cart: Cart):
        order_items = []
        for cart_item in cart.items.all():
            order_item = OrderItem(
                order=self,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            order_items.append(order_item)

            product = cart_item.product
            product.stock -= cart_item.quantity
            product.sold_quantity += cart_item.quantity
            product.save()

        OrderItem.objects.bulk_create(order_items)


class OrderItem(models.Model):
    class Meta:
        db_table = 'order_items'

    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.id}の注文商品 - {self.product.name} x {self.quantity}"

    def get_subtotal(self):
        return self.price * self.quantity
