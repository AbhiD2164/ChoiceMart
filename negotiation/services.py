from django.utils import timezone
from orders.models import Order
from .models import Negotiation


def can_user_negotiate(user, product):

    today = timezone.now().date()

    # limit: 2 products per day
    product_count_today = Negotiation.objects.filter(
        user=user,
        created_at__date=today
    ).values("product").distinct().count()

    if product_count_today >= 2:
        return False, "You can bargain only 2 products per day."

    # limit: 5 attempts per product
    attempts = Negotiation.objects.filter(
        user=user,
        product=product
    ).count()

    if attempts >= 5:
        return False, "Maximum bargain attempts reached for this product."

    return True, None

def evaluate_offer(user, product, offered_price):
    base = float(product.price)
    min_price = float(product.minimum_bargain_price)

    # Example loyalty logic
    from orders.models import Order
    total_orders = Order.objects.filter(user=user).count()

    if offered_price >= min_price or offered_price >= base * 0.85:
        return "accepted", offered_price
    elif offered_price >= base * 0.7:
        return "countered", base * 0.9
    else:
        return "rejected", base