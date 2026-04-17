from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from orders.models import Order
from products.models import Product
from adminpanel.decorators import admin_required

User = get_user_model()

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")   # ✅ FIXED
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, "adminpanel/login.html")

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("admin_login")   # ✅ FIXED

    context = {
        "total_users": User.objects.count(),
        "total_orders": Order.objects.count(),
        "total_products": Product.objects.count(),
    }

    return render(request, "adminpanel/dashboard.html", context)


def admin_logout(request):
    logout(request)
    return redirect('/')   # ✅ FIXED

@admin_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "adminpanel/products_list.html", {"products": products})


@admin_required
def add_product(request):
    from products.models import Category  # assuming model exists

    categories = Category.objects.all()

    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            category_id=request.POST.get("category")  # important
        )
        return redirect("admin_product_list")

    return render(request, "adminpanel/products_add.html", {
        "categories": categories
    })


@admin_required
def edit_product(request, pk):
    from products.models import Category

    product = Product.objects.get(id=pk)
    categories = Category.objects.all()

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.category_id = request.POST.get("category")  # important
        product.save()

        return redirect("admin_product_list")

    return render(request, "adminpanel/products_edit.html", {
        "product": product,
        "categories": categories
    })


@admin_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("admin_product_list")

@admin_required
def order_list(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, "adminpanel/orders_list.html", {"orders": orders})


@admin_required
def user_list(request):
    users = User.objects.all().order_by('-id')
    return render(request, "adminpanel/users_list.html", {"users": users})