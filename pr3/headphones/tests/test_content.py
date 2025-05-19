from django.test import TestCase
from headphones.models import Headphones, FormFactor
from django.urls import reverse


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        ff1 = FormFactor.objects.create(name="Вкладыши")
        ff2 = FormFactor.objects.create(name="Накладные")
        Headphones.objects.create(
            article="1001",
            brand="Sony",
            wireless=True,
            impedance=16,
            weight=150,
            color="white",
            form_factor=ff1,
            price=1000,
            wholesale_price_small=950,
            wholesale_qty_small=10,
            wholesale_price_big=900,
            wholesale_qty_big=100)
        Headphones.objects.create(
            article="1002",
            brand="JBL",
            wireless=False,
            impedance=32,
            weight=180,
            color="black",
            form_factor=ff2,
            price=1200,
            wholesale_price_small=1100,
            wholesale_qty_small=8,
            wholesale_price_big=1050,
            wholesale_qty_big=80)
        Headphones.objects.create(
            article="1003",
            brand="Apple",
            wireless=True,
            impedance=24,
            weight=220,
            color="red",
            form_factor=ff1,
            price=2000,
            wholesale_price_small=1900,
            wholesale_qty_small=5,
            wholesale_price_big=1800,
            wholesale_qty_big=50)

    def test_sort_brand(self):
        url = reverse('product_list') + "?sort=brand"
        response = self.client.get(url)
        self.assertContains(response, "Apple")
        self.assertContains(response, "JBL")
        self.assertContains(response, "Sony")

    def test_sort_impedance(self):
        url = reverse('product_list') + "?sort=impedance"
        response = self.client.get(url)
        self.assertContains(response, "16")
        self.assertContains(response, "24")
        self.assertContains(response, "32")

    def test_sort_weight(self):
        url = reverse('product_list') + "?sort=weight"
        response = self.client.get(url)
        self.assertContains(response, "150")
        self.assertContains(response, "220")

    def test_group_form_factor(self):
        ff1 = FormFactor.objects.get(name="Вкладыши")
        url = reverse('product_list') + f"?form_factor={ff1.id}"
        response = self.client.get(url)
        self.assertContains(response, "Sony")
        self.assertContains(response, "Apple")
