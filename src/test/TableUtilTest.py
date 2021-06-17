from src.main.service.webscraper.jobspider.TableUtil import TableUtil

import unittest


class URLBuilderTest(unittest.TestCase):

    tableUtil = TableUtil()

    def test_cv_id_extraction(self):
        actual_id = self.tableUtil.get_cv_id_from_url('https://www.jobspider.com/job/view-resume-81871.html')
        expected_id = '81871'
        self.assertEqual(actual_id, expected_id, "id is not found!")

