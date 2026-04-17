from django.shortcuts import render
from .models import Category, Product
from negotiation.models import Negotiation
from .models import Product, Category

def product_list(request):

    category_name = request.GET.get('category')

    categories = Category.objects.all()

    if category_name:
        products = Product.objects.filter(category__name=category_name)
    else:
        products = Product.objects.all()

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories
    })


def product_detail(request, pk):

    product = Product.objects.get(id=pk)

    session_key = request.session.session_key

    negotiated_price = None

    if session_key:

        negotiation = Negotiation.objects.filter(
            user=request.user,
            product=product,
            session_key=session_key,
            status="accepted"
        ).first()

        if negotiation:
            negotiated_price = negotiation.offered_price

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "negotiated_price": negotiated_price
        }
    )