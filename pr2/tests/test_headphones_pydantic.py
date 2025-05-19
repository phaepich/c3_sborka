import unittest
from pydantic import ValidationError
from headphones_pydantic import HeadphonesPydantic


class TestHeadphonesPydantic(unittest.TestCase):

    def test_valid_data(self):
        data = {
            'brand': 'JBL',
            'wireless': True,
            'impedance': 24,
            'color': 'black',
            'form_factor': 'вкладыши',
            'weight': 200
        }
        hp = HeadphonesPydantic(**data)
        self.assertTrue(hp.is_portable())

    def test_invalid_form_factor(self):
        data = {
            'brand': 'JBL',
            'wireless': True,
            'impedance': 24,
            'color': 'black',
            'form_factor': 'капельки'
        }
        with self.assertRaises(ValidationError):
            HeadphonesPydantic(**data)
