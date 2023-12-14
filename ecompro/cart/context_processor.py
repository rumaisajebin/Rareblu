from cart.models import CartItem,Wishlist

def cart(request):
    total_cart_item = 0
    if request.user.is_authenticated:
        cart = CartItem.objects.filter(user=request.user)
        for item in cart:
            total_cart_item += item.quantity
    return {'total_cart_item': total_cart_item}


def wishlist_processor(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_items = 0
    return {'wishlist_items': wishlist_items}