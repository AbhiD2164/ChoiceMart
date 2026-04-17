from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from users.models import Wallet
from .models import Cart, CartItem
from orders.models import Order
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required

@require_GET
@login_required(login_url="/users/login/")
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.items.select_related("product")

    total = cart.get_total_price()

    return render(request, "cart/cart.html", {
        "items": items,
        "total": total
    })

@login_required(login_url="/users/login/")
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
    else:
        item.quantity = 1

    item.save()

    messages.success(request, "Product added to cart")

    return redirect("view_cart")

@login_required
def checkout(request):

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related("product")

    if not items.exists():
        return redirect("view_cart")

    total = cart.get_total_price()

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    return render(request, "orders/checkout.html", {
        "items": items,
        "total": total,
        "order": order
    })

@login_required
@require_POST
def pay_now(request):

    cart = get_object_or_404(Cart, user=request.user)
    wallet = get_object_or_404(Wallet, user=request.user)

    total = cart.get_total_price()

    # apply cart bargain if exists
    cart_offer = request.session.get("cart_discount")
    if cart_offer:
        total = float(cart_offer)

    if total <= 0:
        messages.error(request, "Invalid cart total")
        return redirect("view_cart")

    if wallet.balance < total:
        messages.error(request, "Payment Failed: Insufficient Wallet Balance")
        return redirect("view_cart")
    

    wallet.balance -= total
    wallet.save()

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    cart.items.all().delete()

    if "cart_discount" in request.session:
        del request.session["cart_discount"]

    messages.success(request, "Payment Successful")

    return redirect("order_success", order_id=order.id)

@login_required
@require_POST
def bargain(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if cart_item.bargain_attempts >= cart_item.max_attempts:
        messages.error(request, "Bargain attempts finished")
        return redirect("view_cart")

    offer = float(request.POST.get("offer_price"))

    product = cart_item.product
    min_price = product.minimum_bargain_price
    mrp = product.price

    # increase attempt
    cart_item.bargain_attempts += 1
    remaining_attempts = cart_item.max_attempts - cart_item.bargain_attempts

    # Accept if offer >= min price
    if offer >= min_price:
        cart_item.negotiated_price = offer
        cart_item.counter_offer = offer
        cart_item.bargain_status = "accepted"
        cart_item.save()

        messages.success(request, f"Offer accepted at ₹{offer}")
        return redirect("view_cart")

    # ALWAYS generate counter offer (your requirement)
    difference = mrp - min_price

    # progressive negotiation engine
    negotiation_step = difference / 10
    new_counter = mrp - (negotiation_step * cart_item.bargain_attempts)

    # ensure counter never goes below min_price
    if new_counter < min_price:
        new_counter = min_price

    cart_item.counter_offer = round(new_counter, 2)
    cart_item.bargain_status = "counter"
    cart_item.save()

    messages.warning(
        request,
        f"Your offer: ₹{offer} | Counter offer: ₹{cart_item.counter_offer} "
        f"(Attempts left: {remaining_attempts})"
    )

    return redirect("view_cart")

"""
@login_required
def bargain_cart_total(request):

    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    total = sum(
        (i.negotiated_price or i.product.price) * i.quantity
        for i in items
    )

    min_total = total * 0.85

    offer = float(request.POST.get("offer"))

    if offer >= min_total:
        request.session["cart_discount"] = offer
        messages.success(request, "Cart deal accepted")
    else:
        counter = (offer + min_total) / 2
        messages.warning(request, f"Counter cart offer: ₹{counter}")

    return redirect("view_cart")
"""

@login_required
def accept_counter(request, item_id):

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if cart_item.counter_offer:
        cart_item.negotiated_price = cart_item.counter_offer
        cart_item.counter_offer = None
        cart_item.save()

        messages.success(request, "Counter offer accepted")

    return redirect("view_cart")

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    if not cart.items.count():
        return redirect('/')
    return redirect("view_cart")

@login_required
@require_POST
def update_quantity(request, item_id):

    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    quantity = int(request.POST.get("quantity"))

    if quantity < 1:
        quantity = 1

    item.quantity = quantity
    item.save()

    return redirect("view_cart")