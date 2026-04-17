from django.shortcuts import redirect
from django.contrib import messages
from products.models import Product
from .models import Negotiation
from .services import can_user_negotiate, evaluate_offer


def negotiate_price(request, product_id):

    product = Product.objects.get(id=product_id)

    offered_price = float(request.POST.get("price"))

    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    allowed, message = can_user_negotiate(request.user, product)

    if not allowed:
        messages.error(request, message)
        return redirect("product_detail", pk=product_id)

    attempt_number = Negotiation.objects.filter(
        user=request.user,
        product=product
    ).count() + 1

    status = evaluate_offer(product, offered_price)

    Negotiation.objects.create(
        user=request.user,
        product=product,
        session_key=session_key,
        offered_price=offered_price,
        attempt_number=attempt_number,
        status=status
    )

    if status == "accepted":
        messages.success(request, "Offer accepted!")

    else:
        messages.error(request, "Offer rejected.")

    return redirect("product_detail", pk=product_id)