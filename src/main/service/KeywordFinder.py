import re
from typing import List

import spacy

from src.main.entity.Keyword import Keyword


class KeywordFinder:
    __model = None
    __valid_labels = ['ORG', 'GPE', 'PERSON', 'WORK_OF_ART', 'PRODUCT', 'SKILLS']

    def __init__(self):
        self.__model = spacy.load('/home/celil/Desktop/job-candidate-finder/model/model_15_05_21')

    def find_keys(self, cv: str) -> List[Keyword]:

        cv = self.reformat_cv(cv)
        doc = self.__model(cv)

        keyword_list: List[Keyword] = []
        for ent in doc.ents:
            # Tekrarlı anahtar kelimeleri silmek gerek
            if self.__valid_labels.__contains__(ent.label_):
                keyword = Keyword(ent.label_, ent.text.replace('\n', ' '))
                keyword_list.append(keyword)

        return keyword_list

    def reformat_cv(self, cv: str):
        cv = cv.replace("\t", " ")
        cv = cv.replace("|", " ")
        cv = cv.replace("/", " ")
        cv = cv.replace("●", " ")
        cv = cv.replace("...", ".")
        cv = re.sub("’", "'", cv)
        cv = re.sub("`", "'", cv)
        cv = re.sub("“", '"', cv)
        cv = re.sub("？", "?", cv)
        cv = re.sub("é", "e", cv)

        # Kısaltmaları yok say
        cv = re.sub("\'s", " ", cv)  # "Sam is" or "Sam's" 's i siliyoruz
        cv = re.sub(r"(\W|^)([0-9]+)[kK](\W|$)", r"\1\g<2>000\3", cv)
        cv = re.sub("\(s\)", " ", cv, flags=re.IGNORECASE)

        # Sayılar arasındaki ,'ü kaldır.
        cv = re.sub('(?<=[0-9])\,(?=[0-9])', "", cv)

        # ascii olmayan kelimeleri yok say
        cv = re.sub('[^\x00-\x7F]+', " ", cv)

        cv = re.sub(' s ', " ", cv)
        cv = cv.strip()

        return cv




