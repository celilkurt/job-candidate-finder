from typing import List

from src.main.dao.DataSourceI import DataSourceI
from src.main.entity.CV import CV
from src.main.entity.CVMetadata import CVMetadata
from src.main.entity.Query import Query
from src.main.service.webscraper.WebCrawlerI import WebCrawlerI
from src.main.service.webscraper.jobspider.CVUtil import CVUtil
from src.main.service.webscraper.jobspider.TableUtil import TableUtil
from src.main.service.webscraper.jobspider.URLBuilder import URLBuilder


class JobSpiderCrawler(WebCrawlerI):
    __url_builder: URLBuilder
    __cv_util: CVUtil()
    __table_util: TableUtil

    def __init__(self, topic):
        self.topic = topic
        self.__table_util = TableUtil()
        self.__url_builder = URLBuilder()
        self.__cv_util = CVUtil()

    def get_crawling_candid_metadata(self, query: Query) -> List[CVMetadata]:
        keywords_str = query.to_str_without_labels()
        search_page_url = self.__url_builder.get_search_url_by_keys_and_type(keywords_str, '2')

        url_list = self.__table_util.get_cv_urls(search_page_url)
        metadata_list = []
        for url in url_list:
            metadata_list.append(CVMetadata(url, self.__get_cv_id_from_url(url)))

        return metadata_list

    @staticmethod
    def __get_cv_id_from_url(url):
        try:
            return str(url).split("-")[-1][0:-5]
        except:
            pass

    def get_cvs(self, filtered_cv_list: List[CVMetadata], limit: int) -> List[CV]:
        return self.__cv_util.get_cvs(filtered_cv_list, limit)

    """
        Kafka'nın ilgili topic'ine cv'ler yazdırılır.
        """

    def save_cvs_to_sink(self, cv_list: [], sink: DataSourceI):
        sink.save_all_data(index='test', data=cv_list)

    '''
    Kafka'ya yazar
    '''

    def get_cvs_by_keywords_from_source(self, keywords: List[str], source: DataSourceI):
        source.get_data_by_keywords(self.topic, keywords)


