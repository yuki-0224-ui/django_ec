from ecsite.models.cart import Cart


def cart(request):
    DEFAULT_CART_DATA = {
        'cart_items': [],
        'cart_quantity': 0,
        'total': 0
    }

    cart_id = request.session.get('cart_id')
    if not cart_id:
        return DEFAULT_CART_DATA

    try:
        cart = Cart.objects.prefetch_related('items__product').get(id=cart_id)
        cart_items = cart.items.all()

        items_data = [
            {
                'id': item.product.id,
                'name': item.product.name,
                'quantity': item.quantity,
                'subtotal': item.get_subtotal()
            }
            for item in cart_items
        ]

        return {
            'cart_items': items_data,
            'cart_quantity': sum(item.quantity for item in cart_items),
            'total': sum(item['subtotal'] for item in items_data)
        }
    except Cart.DoesNotExist:
        return DEFAULT_CART_DATA
