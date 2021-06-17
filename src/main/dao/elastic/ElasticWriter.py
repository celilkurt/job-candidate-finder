import logging
from typing import List

from elasticsearch import Elasticsearch
from src.main.dao.DataSourceI import DataSourceI


class ElasticWriter(DataSourceI):
    es: Elasticsearch = Elasticsearch()

    def save_data(self, index: str, cv):
        try:
            self.es.index(index=index, id=cv['id'], body=cv)
        except:
            logging.error("elastic writing failed for record=" + str(cv) + " and index=" + index)

    def save_all_data(self, index: str, data: []):
        for i_data in data:
            try:
                self.es.index(index=index, id=i_data['id'], body=i_data)
            except:
                logging.error("elastic writing failed for record=" + str(i_data) + " and index=" + index)

    def get_data_by_ids(self, index: str, ids: List[str]):
        query_body = {"query": {
            "ids": {
                "values": ids
            }
        }
        }
        result = None
        try:
            result = self.es.search(index=index, body=query_body)['hits']['hits']
        except:
            logging.error("records not found for ids=" + str(ids) + " and index=" + index)
        return result

    def get_data_by_id(self, index: str, id: str):
        result = None
        try:
            result = self.es.get(index=index, id=id)['_source']
        except:
            logging.error("record not found for id=" + id + " and index=" + index)
        return result

    def get_data_by_keywords(self, index: str, keywords_str: str):

        query_body = {"query": {
            "query_string": {
                "query": "*:" + keywords_str}
        }
        }

        try:
            cvs = \
            self.es.search(index=index, body=query_body, _source_includes=['date', 'cv', 'id'], size=1000)['hits'][
                'hits']
            cv_list = []
            for temp_cv in cvs:
                try:
                    cv_list.append(temp_cv['_source'])
                except:
                    pass
            return cv_list
        except Exception as e:
            logging.error('get_data_by_keywords error for ' + keywords_str + '\n' + e.__str__())
            return []

    def get_data_by_keywords_and_field(self, index: str, keywords_str: str, field: str):

        query_body = {"query": {
            "query_string": {
                "query": "*:" + keywords_str}
        }
        }

        try:
            cvs = self.es.search(index=index, body=query_body, size=2000)['hits']['hits']
            cv_list = []
            for temp_cv in cvs:
                try:
                    cv_dict = {'score': temp_cv['_score'], 'id': temp_cv['_id'], 'date': temp_cv['_source']['date']}
                    cv_list.append(cv_dict)
                except:
                    pass
            return cv_list
        except Exception as e:
            logging.error("get_data_by_keywords error for " + keywords_str + '\n' + e.__str__())
            return []

    def get_cvs_by_keywords_for_ranking(self, index: str, keywords_str: str, cv_count: int, field: str = 'keywords'):

        query_body = {"query": {
            "query_string": {
                "query": "keywords:" + keywords_str}
        }
        }

        try:
            cvs = \
            self.es.search(index=index, body=query_body, _source_includes=['date', 'cv', 'url'], size=cv_count)['hits'][
                'hits']
            cv_list = []
            for temp_cv in cvs:
                try:
                    cv_dict = {'score': temp_cv['_score'], 'id': temp_cv['_id'], 'date': temp_cv['_source']['date'],
                               'cv': temp_cv['_source']['cv'], 'url': temp_cv['_source']['url']}
                    cv_list.append(cv_dict)
                except:
                    pass
            return cv_list
        except Exception as e:
            logging.error("get_data_by_keywords error for " + keywords_str + '\n' + e.__str__())
            return []

    """
        'date' field'ı belli bir zaman aralığında olanları getir.
    """
    # date:[2021-04-18 TO 2021-04-18]
    # ((quick AND fox) OR (brown AND fox) OR fox) AND NOT news
