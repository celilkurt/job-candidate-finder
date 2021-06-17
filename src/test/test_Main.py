import unittest

from src.main.Main import is_up_to_date


class MainTest(unittest.TestCase):

    def test_is_up_to_date(self):
        date_str = "2021-05-18"
        self.assert_(is_up_to_date(date_str, 5), date_str + " is a up to date date")