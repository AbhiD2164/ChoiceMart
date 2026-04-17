from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total = 0

        for item in self.items.all():

            if item.negotiated_price:
                price = item.negotiated_price

            elif item.product.product_type == "discount" and item.product.discount_price:
                price = item.product.discount_price

            else:
                price = item.product.price

            total += price * item.quantity

        return total

    def __str__(self):
        return f"Cart - {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    bargain_attempts = models.IntegerField(default=0)
    max_attempts = 5

    negotiated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    bargain_status = models.CharField(
        max_length=20,
        default="pending"
    )
    
    counter_offer = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    @property
    def subtotal(self):
        price=0

        if self.negotiated_price:
            price = self.negotiated_price

        elif self.product.product_type == "discount" and self.product.discount_price:
            price = self.product.discount_price

        else:
            price = self.product.price

        return price * self.quantity