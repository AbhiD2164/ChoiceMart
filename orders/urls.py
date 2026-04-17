from django.urls import path
from .views import checkout, order_success

urlpatterns = [
    path('checkout/', checkout, name='order_checkout'),    
    path("success/<int:order_id>/", order_success, name="order_success"),
]