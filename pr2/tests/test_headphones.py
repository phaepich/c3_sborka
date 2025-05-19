import unittest
from headphones import Headphones, InvalidProductData


class TestHeadphones(unittest.TestCase):

    def test_valid_data(self):
        data = {
            'brand': 'Sony',
            'wireless': True,
            'impedance': 32,
            'color': 'black',
            'form_factor': 'накладные',
            'noise_cancelling': False,
            'weight': 250
        }
        hp = Headphones(data)
        self.assertEqual(hp.brand, 'Sony')
        self.assertTrue(hp.wireless)
        self.assertEqual(hp.impedance, 32)
        self.assertEqual(hp.color, 'black')
        self.assertEqual(hp.form_factor, 'накладные')
        self.assertFalse(hp.noise_cancelling)
        self.assertEqual(hp.weight, 250)

    def test_missing_required_field(self):
        data = {
            'wireless': True,
            'impedance': 32,
            'color': 'black',
            'form_factor': 'вкладыши'
        }
        with self.assertRaises(InvalidProductData):
            Headphones(data)

    def test_invalid_type(self):
        data = {
            'brand': 'Sony',
            'wireless': 'да',  # должно быть булевым
            'impedance': 32,
            'color': 'black',
            'form_factor': 'накладные'
        }
        with self.assertRaises(InvalidProductData):
            Headphones(data)

    def test_invalid_choice(self):
        data = {
            'brand': 'Sony',
            'wireless': True,
            'impedance': 32,
            'color': 'black',
            'form_factor': 'капельки'
        }
        with self.assertRaises(InvalidProductData):
            Headphones(data)

    def test_portability(self):
        data = {
            'brand': 'Sony',
            'wireless': True,
            'impedance': 32,
            'color': 'black',
            'form_factor': 'накладные',
            'weight': 299
        }
        hp = Headphones(data)
        self.assertTrue(hp.is_portable())

        data['weight'] = 400
        hp = Headphones(data)
        self.assertFalse(hp.is_portable())

        data['wireless'] = False
        hp = Headphones(data)
        self.assertFalse(hp.is_portable())


if __name__ == '__main__':
    unittest.main()
