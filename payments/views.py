from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from orders.models import Order
from users.models import Wallet
from cart.models import Cart
from .mock_gateway import process_payment
import random
import time

def pay(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)
    wallet = Wallet.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)

    if wallet.balance < order.total_price:
        return render(request, "payments/failed.html", {
            "error": "Insufficient wallet balance"
        })

    success = process_payment()

    if not success:
        return redirect("/payments/failed/")

    try:
        with transaction.atomic():

            # Deduct stock from each product
            for item in cart.items.all():

                product = item.product

                if product.stock < item.quantity:
                    return render(request, "payments/failed.html", {
                        "error": f"{product.name} is out of stock"
                    })

                product.stock -= item.quantity
                product.save()

            # Deduct wallet
            wallet.balance -= order.total_price
            wallet.save()

            # Update order
            order.status = "paid"
            order.save()

            # Clear cart
            cart.items.all().delete()

        return redirect("/payments/success/")

    except Exception as e:
        return render(request, "payments/failed.html", {
            "error": "Payment processing failed"
        })    

def payment_success(request):
    return render(request, "payments/success.html")

def payment_failed(request):
    return render(request, "payments/failed.html", {
        "error" : "Internet error, try again.."
    })