import unittest
import math
from dual_function import dual_function


class TestDualFunction(unittest.TestCase):
    def test_left_function(self):
        n = 5
        x = 4.999
        expected = x - math.sqrt(x)
        result = dual_function(x, n)
        self.assertAlmostEqual(result, expected, places=6)

    def test_right_function(self):
        n = 3
        x = 3
        expected = 1 / (x * x - 4) + math.sqrt(abs(x))
        result = dual_function(x, n)
        self.assertAlmostEqual(result, expected, places=6)

    def test_edge_case(self):
        n = 4
        x = 4
        expected = 1 / (x * x - 4) + math.sqrt(abs(x))
        result = dual_function(x, n)
        self.assertAlmostEqual(result, expected, places=6)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            dual_function("a", 5)
        with self.assertRaises(TypeError):
            dual_function(5, "n")

    def test_multiple_values(self):
        n = 4
        test_values = [0.5, 1, 3.9, 4, 4.1, 10]
        for x in test_values:
            with self.subTest(x=x):
                if x < n:
                    expected = x - math.sqrt(x)
                else:
                    expected = 1 / (x * x - 4) + math.sqrt(abs(x))
                result = dual_function(x, n)
                self.assertAlmostEqual(result, expected, places=6)


if __name__ == '__main__':
    unittest.main()
