from cart.models import CartItem

def cart(request):
    total_cart_item = 0
    if request.user.is_authenticated:
        cart = CartItem.objects.filter(user=request.user)
        for item in cart:
            total_cart_item += item.quantity
    return {'total_cart_item': total_cart_item}