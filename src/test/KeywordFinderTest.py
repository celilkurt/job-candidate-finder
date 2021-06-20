from typing import List
import unittest

from src.main.dao.elastic.ElasticWriter import ElasticWriter
from src.main.entity.Keyword import Keyword
from src.main.service.KeywordFinder import KeywordFinder


class KeyFinderTest(unittest.TestCase):
    cv_str = "You possess exceptional analytical and conceptual thinking skills You have a passion for data science, " \
             "machine learning and artificial intelligence You're a humble, hardworking and self-learner profile " \
             "with an insatiable curiosity You're preferably familiar with e-commerce ecosystem Minimum " \
             "Requirements: BSc degree in Computer/Industrial Engineering or similar academic disciplines " \
             "Proficiency at MSSQL, MySQL, MongoDB Competency and considerable experience in Python Experience in " \
             "creating and deploying machine learning systems and pipelines  would be a great asset Fundamentals in " \
             "predictive modeling, statistics and ML techniques, libraries and  frameworks (NumPy, Pandas, " \
             "Scikit-learn, SciPy, Anaconda and Jupyter  Notebook etc.) Fluency in English (written & spoken) " \
             "Nice-to-have Qualifications: Experience in relational databases Experience in ETL pipeline " \
             "implementations and maintenance by using SSIS Exposure to Docker and Containerization ecosystem " \
             "Experience in TensorFlow, SageMaker Exposure to machine learning, big data ecosystem and technologies " \
             "would be  preferable (Spark, Hadoop, Hive etc.) Experience in AWS EC2, Beanstalk, Lambda, " \
             "S3 and deploying ML services to  cloud Experience in distributed computing, messaging and event driven " \
             "architectures Familiarity with graph databases Competency in C, C++, Scala and Elasticsearch What we " \
             "offer: Working remotely Dynamic work ecosystem where you can take initiative and responsibility " \
             "Enjoyable team/company activities Netflix, BluTV, YouTube Premium and portable modem Dress code: you " \
             "can wear whatever you want "

    key_finder = KeywordFinder()
    # elasticsearch = ElasticWriter()
    # cv_list = self.elasticsearch.get_data_by_keywords('test', 'scala java sql maven')

    def test_is_model_work(self):

        keywords: List[Keyword] = self.key_finder.find_keys(self.cv_str)
        print(self.cv_str)
        print("keywords count: " + str(len(keywords)))
        print('\n'.join([keyword.__str__() for keyword in keywords]))


