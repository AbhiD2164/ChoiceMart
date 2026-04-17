from django.urls import path
from .views import pay, payment_success, payment_failed

urlpatterns = [
    path('pay/<int:order_id>/', pay, name='pay'),
    path('success/', payment_success, name='payment_success'),
    path('failed/', payment_failed, name='payment_failed'),
]