from src.main.service.webscraper.jobspider.URLBuilder import URLBuilder
import unittest


class URLBuilderTest(unittest.TestCase):


    urlBuilder = URLBuilder()

    def test_cv_detail_url_creation(self):
        actual_url = self.urlBuilder.create_cv_detail_url('/job/view-resume-81871.html')
        expected_url = 'https://www.jobspider.com/job/view-resume-81871.html'
        self.assertEqual(actual_url, expected_url, "createCVDetailURL is failed!")



    def test_url_creation_with_keywords(self):
        actual_url = self.urlBuilder.get_search_url_by_keys('java')
        expected_url = 'https://www.jobspider.com/job/resume-search-results.asp/words_java/searchtype_1'
        self.assertEqual(actual_url, expected_url, "createCVSearchURLWithKeywords is failed!")

    def test_url_creation_with_keys_and_type(self):
        actual_url = self.urlBuilder.get_search_url_by_keys_and_type('java maven', '2')
        expected_url = 'https://www.jobspider.com/job/resume-search-results.asp/words_java+maven/searchtype_2'
        self.assertEqual(actual_url, expected_url, "createCVSearchURLWithKeywords is failed!")


if __name__ == '__main__':
    unittest.main()
