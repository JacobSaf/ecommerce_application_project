from django.db import models
from django.conf import settings
from products.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.user.username})"

    @property
    def total_price(self):
        return sum(item.total for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    @property
    def total(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    # Logged-in user (optional)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    billing_email = models.EmailField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    # Guest checkout fields
    guest_name = models.CharField(max_length=255, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_address = models.CharField(max_length=255, null=True, blank=True)
    guest_city = models.CharField(max_length=100, null=True, blank=True)
    guest_state = models.CharField(max_length=100, null=True, blank=True)
    guest_zip = models.CharField(max_length=20, null=True, blank=True)
    guest_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255, null=True, blank=True) 
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shipping_addresses'
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='shipping_address'
    )
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')

    def __str__(self):
        return f"{self.address_line1}, {self.city}"