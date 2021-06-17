from typing import List

from src.main.service.webscraper.WebCrawlerI import WebCrawlerI
from src.main.service.webscraper.jobspider.JobSpiderScareper import JobSpiderCrawler
from src.main.service.webscraper.livecareer.LivecareerScraper import LivecareerScraper


def get_crawler_list() -> List[WebCrawlerI]:
    crawler_list: List[WebCrawlerI] = [
        # LivecareerScraper(topic='livecareer'),
        JobSpiderCrawler(topic='jobspider')
    ]
    """
    listFor = WebCrawlerI.__subclasses__()
    print(len(listFor))
    for subClass in listFor:
        crawlerList.append(subClass.__name__)

    for subClass in crawlerList:
        print(subClass.__str__())
    """

    return crawler_list
