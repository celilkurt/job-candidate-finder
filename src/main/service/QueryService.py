import logging
from typing import List, Dict

from src.main.entity.Keyword import Keyword
from src.main.service.KeywordFinder import KeywordFinder
from src.main.entity.CVMetadata import CVMetadata
from src.main.entity.Query import Query
from src.main.dao.elastic.ElasticWriter import ElasticWriter
from datetime import datetime, timedelta

from src.main.service.webscraper.WebScraperI import WebScraperI


class QueryService:

    @staticmethod
    def get_elastic_query_for_semantic_search(keywords: List[Keyword]) -> str:
        keyword_list: List[str] = []
        for keyword in keywords:
            keyword_str = '\"' + keyword.__str__() + '\"'
            keyword_list.append(keyword_str)

        return ' OR '.join(keyword_list)

    @staticmethod
    def run_query_for_all_scrapers(q: Query, scraper_list: List[WebScraperI], elastic: ElasticWriter,
                                   key_finder: KeywordFinder, cv_count: int) -> []:
        elastic_query_for_ranking = QueryService.get_elastic_query_for_semantic_search(q.keywords)
        scraping_keywords_str: str = q.to_str_without_labels()

        # DataSource'tan alınan cv'leri bir dict'te tutmaktansa bir obje'de tutmak daha iyi olur.
        cvs_from_database = elastic.get_data_by_keywords_and_field('test', scraping_keywords_str, 'cv')
        logging.info(':cvs_from_database.size: ' + str(len(cvs_from_database)))

        logging.info('web scraping keywords: ' + scraping_keywords_str)

        for scraper in scraper_list:
            scraper_name: str = scraper.__class__.__name__

            scraping_candid_metadata: List[CVMetadata] = scraper.get_scraping_candid_metadata(q)
            logging.info(scraper_name + ':scraping_candid_metadata.size: ' + str(len(scraping_candid_metadata)))

            suitable_for_scraping = QueryService.get_suitable_cvmetadatas_for_scraping(scraping_candid_metadata,
                                                                                       cvs_from_database, interval=5)
            logging.info(scraper_name + ':suitable_for_scraping.size: ' + str(len(suitable_for_scraping)))

            cvs_from_scraping = scraper.get_cvs(suitable_for_scraping, limit=400)
            logging.info(scraper_name + ':cvs_from_scraping.size: ' + str(len(cvs_from_scraping)))

            cvs_from_scraping = QueryService.find_keywords_with_nlp(cvs_from_scraping, key_finder)

            scraper.save_cvs_to_datasource(cvs_from_scraping, elastic)

        return QueryService.get_ranked_cvs(elastic_query_for_ranking, elastic, cv_count)

    @staticmethod
    def print_keywords_for_each_cv(cvs: [], scraper_name: str):
        for cv in cvs:
            logging.info(scraper_name + ":" + cv['source'] + '/' + cv['id'] + '\'s keywords: ' + cv['keywords'])

    @staticmethod
    def find_keywords_with_nlp(cvs: [], key_finder: KeywordFinder) -> []:
        for cv in cvs:
            cv_keywords: List[Keyword] = key_finder.find_keys(cv['cv'])
            cv['keywords'] = ' '.join([keyword.__str__() for keyword in cv_keywords])

        return cvs

    @staticmethod
    def get_ranked_cvs(elastic_query_for_ranking: str, elastic: ElasticWriter, cv_count: int) -> []:
        cvs_from_database = elastic.get_cvs_by_keywords_for_ranking('test', elastic_query_for_ranking, cv_count,
                                                                    'keywords')
        print(len(cvs_from_database))
        return cvs_from_database

    """
        Elimizde güncel kopyaları olan cv'leri filtreleyip kalanlarını döndürüyoruz.
    """

    @staticmethod
    def get_suitable_cvmetadatas_for_scraping(scraping_candidates: List[CVMetadata], cvs_from_source: List[Dict], interval: int) \
            -> List[CVMetadata]:
        suitable_for_scraping = []

        source_cv_dict = {}
        for cv in cvs_from_source:
            try:
                source_cv_dict[cv['id']] = cv
            except:
                continue
        source_cvs_keys = source_cv_dict.keys()
        for cv_metadata in scraping_candidates:
            if cv_metadata.cv_id in source_cvs_keys:
                if QueryService.is_up_to_date(source_cv_dict[cv_metadata.cv_id]['date'], interval):
                    suitable_for_scraping.append(cv_metadata)
            else:
                suitable_for_scraping.append(cv_metadata)

        return suitable_for_scraping


    @staticmethod
    def is_up_to_date(date: str, interval: int) -> bool:
        try:
            up_to_date_until = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=interval)
            return datetime.today().date() <= up_to_date_until.date()
        except:
            return False

    @staticmethod
    def get_text_file_as_string(path: str):
        file_str = ""
        for line in open(path, 'r'):
            file_str += line + '\n'
        return file_str
