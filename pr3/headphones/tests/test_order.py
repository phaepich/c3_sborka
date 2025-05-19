from django.test import TestCase
from django.contrib.auth.models import User, Group
from headphones.models import Headphones, FormFactor, Cart, CartItem


class OrderTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user('man', password='123')
        g2 = Group.objects.create(name="Менеджер по продажам")
        self.manager.groups.add(g2)
        ff = FormFactor.objects.create(name="Вкладыши")
        self.hp = Headphones.objects.create(
            article="zxc",
            brand="OrderBrand",
            wireless=True,
            impedance=32,
            weight=100,
            color="red",
            form_factor=ff,
            price=1000,
            wholesale_price_small=900,
            wholesale_qty_small=10,
            wholesale_price_big=800,
            wholesale_qty_big=100)
        self.client.login(username='man', password='123')
        cart, _ = Cart.objects.get_or_create(user=self.manager)
        CartItem.objects.create(cart=cart, product=self.hp, quantity=2)

    def test_make_order_and_cart_empty(self):
        resp = self.client.post("/make_order/")
        self.assertContains(resp, "Заказ успешно оформлен", status_code=200)
        cart = Cart.objects.get(user=self.manager)
        self.assertEqual(cart.items.count(), 0)
