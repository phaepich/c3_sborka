from django.contrib.auth.models import User, Group
from django.test import TestCase
from headphones.models import Headphones, FormFactor


class RolesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('guest', password='123')
        self.warehouseman = User.objects.create_user('wh', password='123')
        self.manager = User.objects.create_user('man', password='123')
        g1 = Group.objects.create(name="Товаровед")
        g2 = Group.objects.create(name="Менеджер по продажам")
        self.warehouseman.groups.add(g1)
        self.manager.groups.add(g2)
        ff = FormFactor.objects.create(name="Вкладыши")
        self.hp = Headphones.objects.create(
            article="test",
            brand="Test",
            wireless=True,
            impedance=32,
            weight=100,
            color="red",
            form_factor=ff,
            price=1000,
            wholesale_price_small=950,
            wholesale_qty_small=10,
            wholesale_price_big=900,
            wholesale_qty_big=100)

    def test_guest_cant_edit(self):
        resp = self.client.get(f'/product/{self.hp.pk}/edit/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp.url)

    def test_warehouseman_can_edit(self):
        self.client.login(username='wh', password='123')
        resp = self.client.get(f'/product/{self.hp.pk}/edit/')
        self.assertEqual(resp.status_code, 200)

    def test_manager_can_make_order(self):
        self.client.login(username='man', password='123')
        resp = self.client.get('/make_order/')
        self.assertEqual(resp.status_code, 200)

    def test_guest_cant_make_order(self):
        resp = self.client.get('/make_order/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp.url)

    def test_admin_can_edit(self):
        self.client.login(username='admin', password='123')
        resp = self.client.get(f'/product/{self.hp.pk}/edit/')
        self.assertEqual(resp.status_code, 200)
