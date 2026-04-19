from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.product_list, name='admin_product_list'),
    path('products/add/', views.add_product, name='admin_add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='admin_edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='admin_delete_product'),
    path('orders/', views.order_list, name='admin_order_list'),
    path('users/', views.user_list, name='admin_user_list'),
    path('logout/', views.admin_logout, name='admin_logout'),
]