from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from src.main.dao.DataSourceI import DataSourceI
from src.main.dao.elastic.ElasticWriter import ElasticWriter
from src.main.entity.CVMetadata import CVMetadata
from src.main.entity.Query import Query
from src.main.service.webscraper.WebCrawlerI import WebCrawlerI


class LivecareerScraper(WebCrawlerI):
    __elas_writer = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate"}

    def __init__(self, topic):
        self.__elas_writer = ElasticWriter()
        self.topic = topic

    def get_crawling_candid_metadata(self, query: Query) -> List[CVMetadata]:
        keywords_param = query.to_str_without_labels().replace(' ', '%20')
        search_url = "https://www.livecareer.com/resume-search/search?jt=" + keywords_param

        page = requests.get(search_url, headers=self.headers).text
        soup = BeautifulSoup(page, 'html.parser')

        uld = soup.find('ul', class_='pagination')
        uld_item = uld.find_all('li')
        page_count = int(uld_item[-2].text)
        links = []

        for i in range(1, page_count + 1):
            page = requests.get(search_url + "&pg=" + str(i), headers=self.headers).text
            soup = BeautifulSoup(page, 'html.parser')
            ul = soup.find('ul', class_='resume-list list-unstyled')
            li_items = ul.find_all('li')[1:]

            for li in li_items:
                links.append(CVMetadata('https://www.livecareer.com/' + li.a['href'], li.a['href'].split("-")[-1]))

        return links

    def get_cvs(self, filtered_cv_list: List[CVMetadata], limit: int) -> []:
        all_cv = []
        counter = 0
        for cv_metadata in filtered_cv_list:
            cv_elems = self.get_cv_by_url(cv_metadata.url)

            if cv_elems:
                cv_elems['id'] = cv_metadata.cv_id
                cv_elems['date'] = datetime.now().date().__str__()
                cv_elems['source'] = 'livecareer'
                cv_elems['url'] = cv_metadata.url
                all_cv.append(cv_elems)
                counter += 1
                if counter > limit:
                    break

        return all_cv

    def get_cv_by_url(self, url: str):

        cv_elems = {}

        cv_detail_page = requests.get(url, headers=self.headers).text

        soup = BeautifulSoup(cv_detail_page, 'html.parser')
        divt = soup.find('div', class_='name')
        div = soup.find('div', class_='fontsize fontface vmargins hmargins linespacing pagesize')
        if div == None:
            div = soup.find('div', class_='LCA skn-cbg1 fontsize fontface vmargins hmargins pagesize')
        if div == None:
            return None
        section = soup.find_all('div', class_='section')

        # Ana Başlık: print(divt.text)

        for s in section:
            bas = ''
            para = ''
            try:
                asd = s.find('div', class_='heading')
                bas = asd.text
            except:
                continue

            try:
                par = s.find_all('div', class_='paragraph')
                para2 = ''
                for p in par:
                    try:
                        sp = p.find('span', class_='paddedline')
                        jt = sp.find('span', 'jobtitle')
                        dw = sp.find('span', class_='datesWrapper')
                        para2 = para2 + " " + jt.text + " " + dw.text
                    except:
                        para2 = para2 + " " + p.text
                para = para2

            except:
                continue

            cv_elems[bas] = para

        all_cv_str = ''
        for value in cv_elems.values():
            all_cv_str = all_cv_str + ' ' + value

        cv_elems = {'cv': all_cv_str}


        return cv_elems


    """
    'sink' şimdilik sadece elasticsearch olabilir. Daha sonra eklenen başka veri tabanları da olabilir.
    'sink' DataSource adında bir class'ın subclass'ı olarak tanımlanmalı
    """

    def save_cvs_to_sink(self, cv_list: [], sink: DataSourceI):

        for cv_temp in cv_list:
            self.__elas_writer.save_data(index="test", cv=cv_temp)

            # self.__elas_writer.get_cv_by_cv_id_and_index(index="livecareer", cv_id=cv_id)


    def get_cvs_by_keywords_from_source(self, keywords: List[str], source: DataSourceI):

        source.get_data_by_keywords(self.topic, keywords)

    """ 
    Scraper'lar yukarıdaki metodları implement etmeli
    CV entity'lerinin tanımlanması gerek,
    DAO'ler için bir interface tanımlanmalı
    """