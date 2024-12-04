from ecsite.models import Cart


def cart(request):
    if hasattr(request, 'cart_data'):
        return request.cart_data

    DEFAULT_CART_DATA = {
        'cart': None,
        'cart_items': [],
        'total': 0,
        'cart_quantity': 0
    }

    cart_id = request.session.get('cart_id')
    if not cart_id:
        return DEFAULT_CART_DATA

    try:
        cart = Cart.objects.get(id=cart_id)
        cart_items = list(cart.items.select_related('product').all())
        cart_data = {
            'cart': cart,
            'cart_items': [
                {
                    'id': item.product.id,
                    'name': item.product.name,
                    'price': item.product.price,
                    'quantity': item.quantity,
                    'subtotal': item.get_subtotal(),
                    'stock': item.product.stock,
                }
                for item in cart_items
            ],
            'total': sum(item.get_subtotal() for item in cart_items),
            'cart_quantity': sum(item.quantity for item in cart_items)
        }
    except Cart.DoesNotExist:
        cart_data = DEFAULT_CART_DATA

    request.cart_data = cart_data
    return cart_data
