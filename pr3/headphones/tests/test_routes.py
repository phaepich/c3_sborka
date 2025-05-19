from django.test import TestCase
from django.urls import reverse
from headphones.models import Headphones, FormFactor


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        ff = FormFactor.objects.create(name="Вкладыши")
        Headphones.objects.create(
            article="1001", brand="Sony", wireless=True, impedance=32,
            weight=200, color="black", form_factor=ff,
            price=1000, wholesale_price_small=950, wholesale_qty_small=10,
            wholesale_price_big=900, wholesale_qty_big=100
        )

    def test_main_page(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail(self):
        hp = Headphones.objects.first()
        response = self.client.get(reverse('product_detail', args=[hp.pk]))
        self.assertEqual(response.status_code, 200)
