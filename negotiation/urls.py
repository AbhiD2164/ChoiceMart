from django.urls import path
from .views import negotiate_price

urlpatterns = [

    path(
        "bargain/<int:product_id>/",
        negotiate_price,
        name="negotiate_price"
    ),

]