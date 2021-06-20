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
        cvs: [] = self.e_writer.get_data_by_keywords_and_field('test', 'keyword_for_empty_result')

        for cv in cvs:
            print(cv['id'])
        print('Elasticsearch bağlantısı başarılı!')

