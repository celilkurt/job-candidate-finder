import requests


import unittest

from src.main.service.webscraper.jobspider.CVUtil import CVUtil


class CVUtilTest(unittest.TestCase):

    cvUtil = CVUtil()
    # 'https://www.jobspider.com/job/view-resume-81541.html'

    def test_cv_id_extraction(self):
        url = 'https://www.jobspider.com/job/view-resume-81871.html'
        page = requests.get(url)
        cv = self.cvUtil.get_cv_data_from_html(page.content)
        print(cv)

