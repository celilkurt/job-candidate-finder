import unittest

from src.main.service.webscraper.ScraperListBuilder import get_scraper_list


class ScraperListBuilderTest(unittest.TestCase):

    def test_get_scraper_list(self):
        for scraper in get_scraper_list():
            print(type(scraper).__name__)
        print('ScraperListBuilder is work!')

if __name__ == '__main__':
    unittest.main()