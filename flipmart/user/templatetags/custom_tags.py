from user.models import Cart

from django import template

register = template.Library()

@register.simple_tag
def user_cart_quantity(user, product):
    cart = Cart.objects.filter(user=user, product=product).first()
    if cart:
        return cart.quantity
    return 0