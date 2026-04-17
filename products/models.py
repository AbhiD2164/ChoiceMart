from django.db import models
from django.core.exceptions import ValidationError
from slugify import slugify


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):

    PRODUCT_TYPE = (
        ('fixed', 'Fixed Price'),
        ('bargain', 'Bargain Product'),
        ('discount', 'Discounted Product'),
    )

    name = models.CharField(max_length=200, unique=True)
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    product_type = models.CharField(
        max_length=10,
        choices=PRODUCT_TYPE
    )
    
    # Bargaining
    minimum_bargain_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Discount
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to='product_images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def clean(self):

        if self.product_type == 'bargain' and not self.minimum_bargain_price:
            raise ValidationError("Bargain products must have minimum bargain price")

        if self.product_type == 'discount' and not self.discount_price:
            raise ValidationError("Discount products must have discount percentage or discount price")