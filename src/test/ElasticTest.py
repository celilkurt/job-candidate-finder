import unittest
import time
import logging

from src.main.dao.elastic.ElasticWriter import ElasticWriter


class ElasticTest(unittest.TestCase):

    logging.basicConfig(level=logging.INFO)
    e_writer = ElasticWriter()
    # 'https://www.jobspider.com/job/view-resume-81541.html'

    def test_cv_id_extraction(self):
        url = 'https://www.jobspider.com/job/view-resume-81871.html'
        self.e_writer.save_cv_id_with_date('81871')
        time.sleep(2)
        result = self.e_writer.get_creation_date_by_cv_id('81871')
        print(str(result))
