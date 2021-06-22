from typing import List

import flask
from flask import request
import logging

from src.main.dao.elastic.ElasticWriter import ElasticWriter
from src.main.entity.Keyword import Keyword
from src.main.entity.Query import Query
from src.main.service.KeywordFinder import KeywordFinder
from src.main.service.QueryService import QueryService
from src.main.service.webscraper import ScraperListBuilder
from src.main.service.CandidateAPIService import CandidateAPIService

app = flask.Flask(__name__)
app.config["DEBUG"] = True

scraper_list = ScraperListBuilder.get_scraper_list()
logging.basicConfig(level=logging.INFO)
key_finder = KeywordFinder()
elastic = ElasticWriter()
response_cv_count_default = 20


@app.route('/api/v1/candidates_by_job', methods=['GET'])
def get_candidates_by_job():
    request_data = request.get_json()
    job_text = request_data['job']
    cv_count = CandidateAPIService.get_cv_count_for_response(request_data, response_cv_count_default)

    query = CandidateAPIService.create_query_obj_from_job_text(job_text, key_finder)
    candidates: [] = QueryService.run_query_for_all_scrapers(query, scraper_list, elastic, key_finder, cv_count)

    return CandidateAPIService.create_response_entity(candidates)


@app.route('/api/v1/candidates_by_keywords', methods=['GET'])
def get_candidates_by_keywords():
    request_data = request.get_json()
    keyword_list: List[Keyword] = CandidateAPIService.create_keyword_list(request_data['keywords'])
    cv_count = CandidateAPIService.get_cv_count_for_response(request_data, response_cv_count_default)

    query = Query(key_list=keyword_list)
    candidates: [] = QueryService.run_query_for_all_scrapers(query, scraper_list, elastic, key_finder, cv_count)
    return CandidateAPIService.create_response_entity(candidates)




app.run()
