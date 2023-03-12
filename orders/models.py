from django.conf import settings
from django.db import models
from catalog.models import Cake


# variables for foreign key
DEFAULT_STATUS_ID = 1
# Create your models here.


class DeliveryOption(models.Model):
    delivery_type = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    slug = models.SlugField(max_length=50, null=True)

    def __str__(self):
        return str(self.delivery_type)


class OrderStatus(models.Model):
    status = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return str(self.status)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user", blank=True,
                             null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="order_status",
                                     default=DEFAULT_STATUS_ID)
    payment_type = models.CharField(max_length=100, blank=True)
    delivery = models.ForeignKey(DeliveryOption, on_delete=models.CASCADE, related_name="order_delivery")
    tracking_code = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.id)

    def total_price(self):
        total = sum(item.get_total_cost() for item in self.units.all())
        total += self.delivery.price
        return total


class OrderUnit(models.Model):
    order = models.ForeignKey(Order, related_name="units", on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, related_name="order_cake", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return self.price * self.quantity
