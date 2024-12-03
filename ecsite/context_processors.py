from .cart import Cart


def cart(request):
    cart_data = request.session.get('cart')
    return {'cart': Cart.from_dict(cart_data)}
