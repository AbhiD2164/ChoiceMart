from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order

@login_required
def checkout(request):

    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return redirect("/cart/")

    items = cart.items.all()

    if not items.exists():
        return redirect("/cart/")

    total = 0
    for item in items:
        price = getattr(item, 'negotiated_price', None) or item.product.price
        total += price * item.quantity

    # Bulk purchase discount
    if total > 500:  # threshold
        total *= 0.95  # 5% discount

    # ✅ CREATE ORDER (MANDATORY)
    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    print("ORDER CREATED:", order.id)  # DEBUG

    return render(request, "orders/checkout.html", {
        "order": order,
        "total": total
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/success.html", {"order": order})