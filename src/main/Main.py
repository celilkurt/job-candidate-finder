import logging
from typing import List
import random

from src.main.entity.Keyword import Keyword
from src.main.service.KeywordFinder import KeywordFinder
from src.main.entity.CVMetadata import CVMetadata
from src.main.entity.Query import Query
from src.main.service.webscraper import ScraperListBuilder
from src.main.dao.elastic.ElasticWriter import ElasticWriter
from datetime import datetime, timedelta

from src.main.service.webscraper.WebScraperI import WebScraperI

'''
Metadata'sı elde edilen cv'lerden elimizde olanlar kafka'ya yazılır
Elimizde olmayan cvler yada güncel olmayan cvler crawl edilip kafka'ya yazılır
Not: Kafka'ya cvler liste halinde topluca yazılmaktansa her bir cv elde edildikten sonra yazılırsa 
hem paralelde puanlama işlemi yapılacağından hem de cv'lerin çekildiği sitelere daha az sıklıkla istek
yapılacağı için daha iyi olur.
'''

key_finder = KeywordFinder()
elastic = ElasticWriter()


def get_elastic_query_for_semantic_search(keywords: List[Keyword]) -> str:
    keyword_list: List[str] = []
    for keyword in keywords:
        keyword_str = '\"' + keyword.__str__() + '\"'
        keyword_list.append(keyword_str)

    return ' OR '.join(keyword_list)


def run_query_for_each_crawler(q: Query, crawler_list: List[WebScraperI]):
    elastic_query_for_ranking = get_elastic_query_for_semantic_search(q.keywords)
    scraping_keywords_str: str = q.to_str_without_labels()

    logging.info('web crawling keywords: ' + str(scraping_keywords_str.split(' ')))

    for crawler in crawler_list:
        crawler_name: str = crawler.__class__.__name__

        '''
        Burası crawling'in aşamalarından soyutlanmalı, buradaki 3-4 fonksiyon 'get_cvs_from_sources' gibi bir 
        fonksiyonda birleştirilmeli 
        '''

        # Elmizde var olup güncel olan cv'leri tespit etmek için cv url'lerini ve id'lerini topluyoruz
        crawling_candid_metadata: List[CVMetadata] = crawler.get_crawling_candid_metadata(q)
        logging.info(crawler_name + ':crawling_candid_metadata.size: ' + str(len(crawling_candid_metadata)))

        # DataSource'tan alınan cv'leri bir dict'te tutmaktansa bir obje'de tutmak daha iyi olur.
        cvs_from_database = elastic.get_data_by_keywords_and_field('test', scraping_keywords_str, 'keywords')
        logging.info(crawler_name + ':cvs_from_database.size: ' + str(len(cvs_from_database)))


        # crawling_candid_metadata, güncel hali elimizde olanlar hariç elenecek şekilde filtrelenir.
        suitable_for_crawling = get_suitable_for_crawling_cvs(crawling_candid_metadata, cvs_from_database, interval=5)
        logging.info(crawler_name + ':suitable_for_crawling.size: ' + str(len(suitable_for_crawling)))

        # suitable_for_crawling list'inde bilgileri bulunan cv'lerden ilk 'limit' tanesini çekiyoruz
        cvs_from_scraping = crawler.get_cvs(suitable_for_crawling, limit=50)
        logging.info(crawler_name + ':cvs_from_scraping.size: ' + str(len(cvs_from_scraping)))

        # logging.info(crawler_name + ':elastic query: ' + elastic_query_for_ranking)
        '''
        cv'lerden Model yardımıyla keywords elde edilmeli ve keywords'ler cv 
        dict'ine kaydedilmeli.
        '''
        cvs_from_scraping = find_keywords_with_nlp(cvs_from_scraping)
        # print_keywords_for_each_cv(cvs_from_scraping, crawler_name)

        crawler.save_cvs_to_sink(cvs_from_scraping, elastic)

    get_ranked_cvs(elastic_query_for_ranking)


def print_keywords_for_each_cv(cvs: [], crawler_name: str):
    for cv in cvs:
        logging.info(crawler_name + ":" + cv['source'] + '/' + cv['id'] + '\'s keywords: ' + cv['keywords'])


def find_keywords_with_nlp(cvs: []) -> []:
    for cv in cvs:
        cv_keywords: List[Keyword] = key_finder.find_keys(cv['cv'])
        cv['keywords'] = ' '.join([keyword.__str__() for keyword in cv_keywords])

    return cvs


def get_ranked_cvs(elastic_query_for_ranking: str):
    cvs_from_database = elastic.get_data_by_keywords_and_field('test', elastic_query_for_ranking, 'keywords')
    print(len(cvs_from_database))
    for cv in cvs_from_database:
        print(str(cv))


"""
    Elimizde güncel kopyaları olan cv'leri filtreleyip kalanını döndürüyoruz.
"""


def get_suitable_for_crawling_cvs(crawling_candidates: List[CVMetadata], cvs_from_source: [], interval: int) -> List[CVMetadata]:
    suitable_for_crawling = []

    source_cv_dict = {}
    for cv in cvs_from_source:
        try:
            source_cv_dict[cv['id']] = cv
        except:
            continue

    for cv_metadata in crawling_candidates:
        if cv_metadata.cv_id in source_cv_dict.keys():
            if is_up_to_date(source_cv_dict[cv_metadata.cv_id], interval):
                suitable_for_crawling.append(cv_metadata)
        else:
            suitable_for_crawling.append(cv_metadata)

    return suitable_for_crawling



"""
   Verilen 'date' bugün ve interval gün öncesi arasında bir tarihte 
   çekildiyse True değilse False döner.
"""


def is_up_to_date(date: str, interval: int) -> bool:
    try:
        up_to_date_until = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=interval)
        return datetime.today().date() <= up_to_date_until.date()
    except:
        return False

def get_text_file_as_string(path: str):
    file_str = ""
    for line in open(path, 'r'):
        file_str += line + '\n'
    return file_str


def main():
    crawler_list = ScraperListBuilder.get_scraper_list()
    logging.basicConfig(level=logging.INFO)

    job_text = get_text_file_as_string('../../job.txt')
    keyword_list: List[Keyword] = key_finder.find_keys(job_text)
    random.shuffle(keyword_list)
    query = Query(key_list=keyword_list)
    run_query_for_each_crawler(query, crawler_list)


if __name__ == "__main__":
    main()
