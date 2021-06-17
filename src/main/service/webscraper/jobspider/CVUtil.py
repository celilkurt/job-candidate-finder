from typing import List

import requests
import logging
from datetime import datetime

from bs4 import BeautifulSoup

from src.main.entity.CVMetadata import CVMetadata
from src.main.service.webscraper.jobspider.URLBuilder import URLBuilder


class CVUtil:
    __urlBuilder = URLBuilder()

    def get_cv(self, cv_metadata: CVMetadata):
        try:
            page = requests.get(cv_metadata.url)
            cv = self.get_cv_data_from_html(page.content)
            cv['id'] = cv_metadata.cv_id

            return cv
        except Exception as e:
            logging.error(e.__class__, ": get_cv error for " + cv_metadata.cv_id)
            return None

    def get_cv_data_from_html(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        label_list = ['html', 'font']
        results = self.get_elems_by_label_list(soup, label_list)
        return self.soup_list_to_cv_object(results)

    def get_elems_by_label_list(self, soup, label_list):
        results = soup('form')
        for query in label_list:
            new_results = []
            for result in results:
                temp = result(query)
                if temp:
                    new_results += temp

            results = new_results

        return results

    def soup_list_to_cv_object(self, soup_list):
        cv = {}

        for soup_elem in soup_list:
            if soup_elem.text.strip().startswith('Willing'):
                cv['cv'] = ''
            else:
                cv['cv'] = cv.get('cv', '') + '\n' + soup_elem.text.strip().replace('|', ' ')

        '''for soup_elem in soup_list:
            elem_text = soup_elem.text.strip()
            elem_texts = elem_text.split(":", 1)
            sub_title_candid = elem_texts[0].strip()
            if len(elem_texts) == 2 and self.sub_titles.__contains__(sub_title_candid):
                cv[sub_title_candid] = elem_texts[1]
                # cv[sub_title_candid] = re.sub('[^0-9a-zA-Z ]+', ' ', elem_texts[1])
                # setattr(cv, elem_texts[0].lower(), elem_texts[1])
            else:
                cv['unamed'] = cv.get('unamed', '') + ' ' + elem_text
                # cv['unamed'] = cv.get('unamed', '') + ' ' + re.sub('[^0-9a-zA-Z ]+', ' ', elem_text) + ' '

        # tanımlanamayan kısımlar tanımlanamayan diye kaydedilmeli'''
        cv['source'] = 'jobspider'
        cv['date'] = datetime.now().date().__str__()

        return cv

    def get_cvs(self, cvs_metadata: List[CVMetadata], limit: int):
        cv_list = []
        counter = 0
        for cv_metadata in cvs_metadata:
            cv_metadata.url = self.__urlBuilder.create_cv_detail_url(cv_metadata.url)
            cv = self.get_cv(cv_metadata)  # Cv'yi 'jobspider' index'ine kaydeder.
            if cv:
                cv['url'] = cv_metadata.url
                cv_list.append(cv)

            if counter < limit:
                counter += 1
            else:
                break

        return cv_list

    def get_cv_id_from_url(self, url: str):
        return url.split("-")[-1][0:-5]
