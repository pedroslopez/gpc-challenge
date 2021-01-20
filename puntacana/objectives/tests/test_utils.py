from unittest import TestCase

from objectives.utils import linear_interpolation


class UtilsTest(TestCase):
    def test_linear_interpolation(self):
        p1 = (5, 80)
        p2 = (7, 90)
        x = 6

        result = linear_interpolation(x, p1, p2)

        self.assertEqual(result, 85)

    def test_inverse_linear_interpolation(self):
        p1 = (7, 80)
        p2 = (5, 90)
        x = 6

        result = linear_interpolation(x, p1, p2)

        self.assertEqual(result, 85)
