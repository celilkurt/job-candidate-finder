import unittest
from datetime import datetime
from datetime import timedelta

from src.main.service.QueryService import QueryService


class QueryServiceTest(unittest.TestCase):

    def test_up_to_date_func(self):
        self.assertEqual(QueryService.is_up_to_date('1968-04-25', 5), False, 'is must be False')

    def test_up_to_date_func_2(self):
        three_day_ago = datetime.now() + timedelta(days=-3)
        three_day_ago_str = three_day_ago.strftime("%Y-%m-%d")
        self.assertEqual(QueryService.is_up_to_date(three_day_ago_str, 4), True, 'is must be True')

