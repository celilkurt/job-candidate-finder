from typing import List

import requests
import logging
from bs4 import BeautifulSoup

from src.main.service.webscraper.jobspider.URLBuilder import URLBuilder

'''
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
'''


class TableUtil:
    __urlBuilder = URLBuilder()
    '''
    URL: Arama sonucunun listelendiği sayfanın URL'i.
    İlk aşamada verilen adresten html sayfasını çeker. 
    Bu sayfanın arama sonuç sayfası olması beklenir.
    Sayfa, en fazla 50 CV içeren bir tablo içerir.
    Tablodaki URL'ler elde edilir ve herbiri için aşağıdaki işlemler yapılır.
        - URL bir CV'nin detay sayfasıdır.
        - Sayfa içeriği 'getCVByURL' fonksiyonu ile string tipinde elde edilir.
        - CV text formatında kaydedilir.
    '''

    '''
        cv'leri içeren bir tablo ve pagination
        linkleri olduğu varsayılan bir url alır.
    '''
    '''
            örnek pagination_urls elemanı: '/job/resume-search-results.asp'
            örnek full_url: 'https..jobspider.com/job/resume...'
    '''

    def get_cv_urls(self, url) -> List[str]:
        pagination_urls: list = self.get_pagination_urls(url)
        # logging.info('Jobspider scraper: Found ' + str(len(pagination_urls)) + ' table page urls for -> ' + url)
        url_list = []
        for temp_url in pagination_urls:
            full_url = self.__urlBuilder.get_search_url(temp_url)
            url_list = url_list + self.__get_cv_detail_urls_by_table_url(full_url)

        return url_list

    def get_pagination_urls(self, url):
        labels = ['form', 'a']

        page = self.__get_page_by_url(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soups = self.__get_elems_by_label_list(soup, labels)

        urls = []

        for temp_soup in soups:
            temp_url = temp_soup['href']
            # Eğer temp boş değilse
            if temp_url:
                urls.append(temp_url)

        '''
            Bu aşamada elimize sayfadaki bütün url'ler geçtiğinden
            sadece pagination url'leri kalacak şekilde filtreliyoruz.
        '''
        filtered_list = self.__filter_urls(urls, '/job/resume-search-results.asp')
        # list'teki son url next link'inden geliyor, bu url list'te bulunduğundan siliniyor.
        filtered_list = filtered_list[0: -1]
        # filtered_list'deki url'ler page 2'den başlıyor, filtered_list'e ilk sayfanın url'i de ekleniyor.
        filtered_list.append(url[25:])
        return filtered_list[:10]

    def __filter_urls(self, urls, prefix) -> List[str]:
        new_list: list = []
        for elem in urls:
            if elem.startswith(prefix):
                new_list.append(elem)

        return new_list

    '''
        Verilen url'deki sayfayı çeker,
        Sayfadaki tablonun içerdiği cv detay url'lerini elde eder,
        Cv detaylarını çekip txt formatında yazdırır.
    '''

    def get_cv_id_from_url(self, url):
        return str(url).split("-")[-1][0:-5]

    def __get_page_by_url(self, url):
        return requests.get(url)

    '''
        HTML sayfasındaki tablonun içerdiği cv url'lerini döndürür.
    '''

    def __get_cv_detail_urls_by_table_url(self, url: str) -> list:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = self.__get_elems_by_label_list(soup, label_list=['form', 'a'])

        urls = []
        for result in results:
            url = result['href']
            if url:
                urls.append(url)

        return self.__filter_urls(urls, "/job/view-resume")

    def __get_elems_by_label_list(self, soup, label_list):
        results = [soup]  # soup('form')
        for query in label_list:
            new_results = []
            for result in results:
                temp = result(query)
                if temp:
                    new_results += temp

            results = new_results

        return results
