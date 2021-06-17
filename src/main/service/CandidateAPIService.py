from random import random
from typing import List

from flask import jsonify

from src.main.entity.Keyword import Keyword
from src.main.entity.Query import Query
from src.main.service.KeywordFinder import KeywordFinder


class CandidateAPIService:

    @staticmethod
    def get_optional_cv_count(request_data, default_value) -> int:
        cv_count: int
        if 'cv_count' in request_data:
            cv_count = int(request_data['cv_count'])
        else:
            cv_count = default_value

        if cv_count > 0:
            return cv_count
        else:
            return 1

    @staticmethod
    def create_query_from_job_text(job_text: str, key_finder: KeywordFinder) -> Query:
        keyword_list: List[Keyword] = key_finder.find_keys(job_text)
        random.shuffle(keyword_list)
        return Query(key_list=keyword_list)

    @staticmethod
    def create_response_entity(candidates: []):
        max_score = 0
        if len(candidates) != 0:
            max_score = candidates[0]['score']
        response = {'cv_count': len(candidates), 'max_score': max_score, 'candidates': candidates}
        return jsonify(response)


    @staticmethod
    def create_key_list(keywords_str: str) -> List[Keyword]:
        keyword_list = []
        if keywords_str:
            keyword_list = [keyword.strip() for keyword in keywords_str.split(',')]

        return [Keyword('', keyword) for keyword in keyword_list]