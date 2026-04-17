from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("pay/", views.pay_now, name="pay_now"),
    path("bargain/<int:item_id>/", views.bargain, name="bargain"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("accept/<int:item_id>/", views.accept_counter, name="accept_counter"),
    path("update/<int:item_id>/",views.update_quantity, name="update"),
]