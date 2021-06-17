import re
import unittest

from src.main.Main import is_up_to_date


class URLBuilderTest(unittest.TestCase):

    def test_up_to_date_func(self):
        self.assertEqual(is_up_to_date('1968-04-25', 5), False, 'is must be False')

    def test_up_to_date_func_2(self):
        self.assertEqual(is_up_to_date('2021-04-12', 6), True, 'is must be True')

    def test_regex(self):
        res = re.sub('[^0-9a-zA-Z ]+', ' ', 'elem_  texts[1]')
        self.assertEqual(res, 'elem   texts 1 ', 'is must be True')
