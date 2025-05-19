from django.test import TestCase
from django.contrib.auth.models import User
from headphones.models import Headphones, FormFactor, Cart, CartItem


class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', password='123')
        ff = FormFactor.objects.create(name="Вкладыши")
        self.hp = Headphones.objects.create(
            article="123",
            brand="TestBrand",
            wireless=True,
            impedance=16,
            weight=220,
            color="red",
            form_factor=ff,
            price=1000,
            wholesale_price_small=950,
            wholesale_qty_small=10,
            wholesale_price_big=900,
            wholesale_qty_big=100)

    def test_cart_add_and_total(self):
        self.client.login(username='test', password='123')
        self.client.get(f"/cart/add/{self.hp.pk}/")
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.total_price(), 1000)

    def test_cart_update_quantity_and_discount(self):
        self.client.login(username='test', password='123')
        cart, _ = Cart.objects.get_or_create(user=self.user)
        item = CartItem.objects.create(
            cart=cart, product=self.hp, quantity=101)
        # Цена за 1 — должна быть по крупному опту (900)
        self.assertEqual(item.get_price(), 101 * 900)
        # А на всё — ещё 5% скидка
        self.assertEqual(cart.total_price(), round(101 * 900 * 0.95, 2))
