import unittest


def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    pass


class TestFactorize(unittest.TestCase):
    """
        Test func factorize
    """
    def test_wrong_types_raise_exception(self):
        for item in 'string', 1.5:
            with self.subTest(case=item):
                self.assertRaises(TypeError, factorize, item)

    def test_negative(self):
        for item in -1, -10, -100:
            with self.subTest(case=item):
                self.assertRaises(ValueError, factorize, item)

    def test_zero_and_one_cases(self):
        for item, resp in (0, (0,)), (1, (1,)):
            with self.subTest(case=item):
                self.assertEqual(factorize(item), resp)

    def test_simple_numbers(self):
        for item in 3, 13, 29:
            with self.subTest(case=item):
                self.assertEqual(factorize(item), (item,))

    def test_two_simple_multipliers(self):
        for item, resp in (6, (2, 3)), (26, (2, 13)), (121, (11, 11)):
            with self.subTest(case=item):
                self.assertEqual(factorize(item), resp)

    def test_many_multipliers(self):
        for item, resp in (1001, (7, 11, 13)), (9699690, (2, 3, 5, 7, 11, 13, 17, 19)):
            with self.subTest(case=item):
                self.assertEqual(factorize(item), resp)


if __name__ == '__main__':
    unittest.main()
