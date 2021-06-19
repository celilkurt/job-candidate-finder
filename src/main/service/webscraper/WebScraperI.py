from typing import List

from src.main.dao.DataSourceI import DataSourceI
from src.main.entity.CVMetadata import CVMetadata
from src.main.entity.Query import Query


class WebScraperI:
    topic: str
    """
    Güncellik kontrolü yapılabilmesi için CV id ve CV URL'i gibi
    bilgileri içeren list'i döndürür.
    """

    def get_crawling_candid_metadata(self, query: Query) -> List[CVMetadata]:
        pass

    """
    'filtered_cv_list'te url'i belirtilen cv'ler ilgili web sitesinden çekilir ve döndürülür.
    """

    def get_cvs(self, filtered_cv_list: List[CVMetadata], limit: int) -> []:
        pass

    """
    'sink' şimdilik sadece elasticsearch olabilir. Daha sonra eklenen başka veri tabanları da olabilir.
    'sink' DataSource adında bir class'ın subclass'ı olarak tanımlanmalı
    """

    def save_cvs_to_sink(self, cv_list: [], sink: DataSourceI):
        pass

    def get_cvs_by_keywords_from_source(self, keywords: List[str], source: DataSourceI):
        pass

    """ 
    Scraper'lar yukarıdaki metodları implement etmeli
    CV entity'lerinin tanımlanması gerek,
    DAO'ler için bir interface tanımlanmalı
    """
