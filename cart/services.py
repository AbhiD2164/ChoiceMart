from .models import CartItem
from .models import Product
from orders.models import Order


def add_to_cart(user, product, price):

    cart = user.cart

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"price_at_time": price}
    )

    if not created:
        item.stock += 1
        item.save()

    return item



def checkout_cart(user):

    cart = user.cart

    orders = []

    for item in cart.items.all():

        order = Order.objects.create(
            user=user,
            product=item.product,
            price=item.price_at_time
        )

        orders.append(order)

    cart.items.all().delete()

    return orders