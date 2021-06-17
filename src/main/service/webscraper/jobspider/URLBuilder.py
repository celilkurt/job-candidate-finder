'''
İş arama için üç farklı seçenek var.
    - all of my keywords: bütün kelimeleri, CV'nin herhangi bir yerinde içerenleri listeler.
    Bunun için URL'in sonuna 'searchtype_1' parametresi eklenir.
        - 'java mava' keywords'ü için:
        https://www.jobspider.com/job/job-search-results.asp/words_java+mava/searchtype_1
    - any of my keywords: verilen kelimelerden herhangi birini içeren CV'leri listeler.
    Bunun için URL'in sonuna 'searchtype_2' parametresi eklenir.
        - 'java' keywords'ü için:
        https://www.jobspider.com/job/job-search-results.asp/words_java/searchtype_2
    - this exact phrase: verilen kelime veya kelimelerin verildiği sırayla ve bütünüyle
    bulunduğu CV'leri listeler. Bunun için URL'in sonuna 'searchtype_3' parametresi eklenir.
        - 'java' keywords'ü için:
        https://www.jobspider.com/job/job-search-results.asp/words_java/searchtype_3

Şehrin kullanıldığı URL de şu şekildedir.
city: los angeles
category: category_23 (computer/software)
keywords: java maven sql
searchtype: any of my keywords
miles: default'u 10'dur. Şehir belirtildiğinde 10, 20, 40, 100 ve 200'den biri seçilmelidir.
https://www.jobspider.com/job/resume-search-results.asp/county_los+angeles/miles_10/category_23/words_java+maven+sql/searchtype_2


'''


class URLBuilder:
    __base_url = 'https://www.jobspider.com'
    __baseurl_for_search = 'https://www.jobspider.com/job/resume-search-results.asp'
    __default_search_type = '1'
    __valid_search_types = ['1', '2', '3']
    __default_miles = '10'
    __valid_miles = ['10', '20', '40', '100', '200']

    # örnek URL: /job/view-resume-81871.html
    def create_cv_detail_url(self, url) -> str:
        try:
            if url.startswith("/job/view-resume"):
                return self.__base_url + url
            else:
                raise ValueError("URL is not valid!")
        except ValueError as ve:
            print(ve)

    def __get_miles_param(self, miles) -> str:
        if self.__valid_miles.__contains__(miles):
            return '/miles_' + miles
        else:
            return '/miles_' + self.__default_miles

    def __get_words_param(self, keywords, search_type) -> str:
        if search_type == '2':
            return  '/words_' + keywords.replace(' ', '+')
        else:
            return '/words_' + keywords.replace(' ', '+')

    def __get_city_param(self, city) -> str:
        return '/county_' + city.replace(' ', '+')

    def __get_category_param(self, category) -> str:
        return '/category_' + category

    def __get_search_type_param(self, search_type) -> str:
        if self.__valid_search_types.__contains__(search_type):
            return '/searchtype_' + search_type
        else:
            return '/searchtype_' + self.__default_search_type

    def get_search_url(self, url) -> str:
        return self.__base_url + url

    def get_search_url_by_keys(self, keywords: str) -> str:
        words_param = self.__get_words_param(keywords, self.__default_search_type)
        search_type_param = self.__get_search_type_param('')
        return self.__baseurl_for_search + words_param + search_type_param

    def get_search_url_by_keys_and_type(self, keywords: str, searchtype: str) -> str:
        words_param = self.__get_words_param(keywords, searchtype)
        search_type_param = self.__get_search_type_param(searchtype)
        return self.__baseurl_for_search + words_param + search_type_param

    # Örnek URL: https://www.jobspider.com/job/resume-search-results.asp/category_14/words_a/searchtype_1
    def get_search_url_by_keys_and_type_and_cat(self, keywords: str, searchtype: str, category: str) -> str:
        words_param = self.__get_words_param(keywords, searchtype)
        search_type_param = self.__get_search_type_param(searchtype)
        category_param = self.__get_category_param(category)
        return self.__baseurl_for_search + category_param + words_param + search_type_param

    # Örnek URL: https://www.jobspider.com/job/resume-search-results.asp/county_los+angeles/miles_10/words_a/searchtype_1
    def get_search_url_by_keys_and_type_and_city_and_mil(self, keywords: str, searchtype: str, city: str, miles: str) -> str:
        words_param = self.__get_words_param(keywords, searchtype)
        search_type_param = self.__get_search_type_param(searchtype)
        city_param = self.__get_city_param(city)
        miles_param = self.__get_miles_param(miles)
        return self.__baseurl_for_search + city_param + miles_param + words_param + search_type_param

    # https://www.jobspider.com/job/resume-search-results.asp/county_los+angeles/miles_10/category_23/words_a/searchtype_1
    def get_search_url_by_keys_and_type_and_cat_and_city_and_mil(self, keywords: str, searchtype: str, category: str, city: str, miles: str) -> str:
        words_param = self.__get_words_param(keywords, searchtype)
        search_type_param = self.__get_search_type_param(searchtype)
        city_param = self.__get_city_param(city)
        miles_param = self.__get_miles_param(miles)
        category_param = self.__get_category_param(category)
        return self.__baseurl_for_search + city_param + miles_param + category_param + words_param + search_type_param





