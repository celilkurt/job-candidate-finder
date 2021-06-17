from typing import List

from src.main.entity.Keyword import Keyword


class Query:
    keywords: List[Keyword]

    '''
    Sorgu keyword'ler şeklinde yapılırsa
    '''
    def __init__(self, keywords_str: str):
        for keyword in keywords_str.split(" "):
            self.keywords.append(Keyword('', keyword))

    def __init__(self, key_list: List[Keyword]):
        self.keywords = key_list

    def to_str_without_labels(self) -> str:

        keyword_str = ' '.join([keyword.value for keyword in self.keywords])
        return keyword_str
