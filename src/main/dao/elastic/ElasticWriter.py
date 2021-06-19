import logging
from typing import List

from elasticsearch import Elasticsearch
from src.main.dao.DataSourceI import DataSourceI


class ElasticWriter(DataSourceI):
    es: Elasticsearch = Elasticsearch()

    def save_data(self, index: str, cv):
        try:
            self.es.index(index=index, id=cv['id'], body=cv)
        except Exception as e:
            logging.error("elastic writing failed for record=" + str(cv) + " and index=" + index)

    def save_all_data(self, index: str, cvs: []):
        for cv in cvs:
            self.save_data(index, cv)

    @staticmethod
    def __get_query_body_for_searching_by_ids(ids: List[str]) -> {}:
        return {"query": {
            "ids": {
                "values": ' '.join(ids)
            }
        }}

    def get_data_by_ids(self, index: str, ids: List[str]) -> []:
        query_body = self.__get_query_body_for_searching_by_ids(ids)

        try:
            return self.es.search(index=index, body=query_body)['hits']['hits']
        except Exception as e:
            logging.error("records not found for ids=" + str(ids) + " and index=" + index)

    def get_data_by_id(self, index: str, id: str) -> {}:

        try:
            return self.es.get(index=index, id=id)['_source']
        except Exception as e:
            logging.error("record not found for id=" + id + " and index=" + index)

    @staticmethod
    def __get_query_body_for_searching_by_keywords(keywords_str: str, query_field: str = '*') -> {}:
        return {"query": {
            "query_string": {
                "query": query_field + ":" + keywords_str}
        }
        }

    def get_data_by_keywords(self, index: str, keywords_str: str):

        query_body = self.__get_query_body_for_searching_by_keywords(keywords_str)
        cvs = []
        try:
            cvs = \
                self.es.search(index=index, body=query_body, _source_includes=['date', 'cv', 'id'], size=1000)['hits'][
                    'hits']
        except Exception as e:
            logging.error('get_data_by_keywords error for ' + keywords_str + '\n' + e.__str__())

        return self.__get_hits_without_metadata(cvs)

    @staticmethod
    def __get_hits_without_metadata(cvs: []) -> []:
        cv_list = []
        for cv in cvs:
            if '_source' in cv:
                cv_list.append(cv['_source'])

        return cv_list

    def get_data_by_keywords_and_field(self, index: str, keywords_str: str, field: str = 'keywords'):

        query_body = self.__get_query_body_for_searching_by_keywords(keywords_str, field)
        cvs = []
        try:
            cvs = self.es.search(index=index, body=query_body, _source_includes=['date'], size=2000)['hits']['hits']
        except Exception as e:
            logging.error("get_data_by_keywords error for " + keywords_str + '\n' + e.__str__())

        cv_list = []
        for cv in cvs:
            cv_reformatted = {}
            if 'date' in cv['_source']:
                cv_reformatted['date'] = cv['_source']['date']
            else:
                continue
            cv_reformatted['score'] = cv['_score']
            cv_reformatted['id'] = cv['_id']
            cv_list.append(cv_reformatted)

        return cv_list

    def get_cvs_by_keywords_for_ranking(self, index: str, keywords_str: str, cv_count: int, field: str = 'keywords'):

        query_body = self.__get_query_body_for_searching_by_keywords(keywords_str, field)
        cvs = []
        try:
            cvs = \
                self.es.search(index=index, body=query_body, _source_includes=['date', 'cv', 'url'], size=cv_count)[
                    'hits']['hits']
        except Exception as e:
            logging.error("get_data_by_keywords error for " + keywords_str + '\n' + e.__str__())

        cv_list = []
        for cv in cvs:
            reformatted_cv = {'score': cv['_score'], 'id': cv['_id']}

            if 'cv' in cv['_source']:
                reformatted_cv['cv'] = cv['_source']['cv']
            if 'date' in cv['_source']:
                reformatted_cv['date'] = cv['_source']['date']
            if 'url' in cv['_source']:
                reformatted_cv['url'] = cv['_source']['url']

            cv_list.append(reformatted_cv)
        return cv_list
