from typing import List


class DataSourceI:

    def save_data(self, index: str, data):
        pass

    def save_all_data(self, index: str, data: []):
        pass

    def get_data_by_ids(self, index: str, ids: List[str]):
        pass

    def get_data_by_id(self, index: str, id: str):
        pass

    def get_data_by_keywords(self, index: str, keywords_str: str):
        pass

    def get_data_by_keywords_and_field(self, index: str, keywords: List[str], field: str):
        pass


    '''
    delete_cv
    update_cv
    get_cvs
    '''
