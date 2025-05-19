from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP


class FormFactor(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Headphones(models.Model):
    article = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100)
    wireless = models.BooleanField()
    impedance = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(null=True, blank=True)
    color = models.CharField(max_length=50)
    form_factor = models.ForeignKey(FormFactor, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за штуку")
    wholesale_price_small = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Мелкий опт", default=0)
    wholesale_qty_small = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во для мелкого опта")
    wholesale_price_big = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Крупный опт",
        default=0)
    wholesale_qty_big = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во для крупного опта")

    def __str__(self):
        return f"{self.brand} ({self.article})"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        total = sum(item.get_price() for item in self.items.all())
        total = Decimal(total)
        if total > Decimal('10000'):
            total = total * Decimal('0.95')
        return total.quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE)
    product = models.ForeignKey(Headphones, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_price(self):
        qty = self.quantity
        product = self.product
        if (qty >= product.wholesale_qty_big and
                product.wholesale_price_big > 0):
            price = product.wholesale_price_big
        elif (qty >= product.wholesale_qty_small and
              product.wholesale_price_small > 0):
            price = product.wholesale_price_small
        else:
            price = product.price
        return price * qty
