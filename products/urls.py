from django.urls import path
from .views import product_detail, product_list


urlpatterns = [

    path("", product_list, name="product_list"),
    path("products/<int:pk>/",product_detail, name="product_detail"),
    path("category/<slug:category_slug>/",
         product_list,
         name="products_by_category"),
]