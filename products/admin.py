from django.contrib import admin
from .models import Product, Category

admin.site.register(Product)
admin.site.register(Category)

# in admin.py

class ProductAdmin(admin.ModelAdmin):

    def get_fields(self, request, obj=None):

        fields = ['name', 'category', 'price', 'product_type', 'stock']

        if obj and obj.product_type == 'bargain':
            fields.append('minimum_bargain_price')

        if obj and obj.product_type == 'discount':
            fields.append('discount_percentage')

        return fields