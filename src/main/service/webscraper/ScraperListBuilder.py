from typing import List

from src.main.service.webscraper.WebScraperI import WebScraperI
from src.main.service.webscraper.JobSpiderScraper import JobSpiderScraper
from os import walk
import importlib

module = importlib.import_module('src.main.service.webscraper')
scrapers_root_directory = '/home/celil/Desktop/job-candidate-finder/src/main/service/webscraper'


def get_file_names_in_directory(file_address: str) -> List[str]:
    return next(walk(file_address), (None, None, []))[2]


def filter_file_names_by_ends(file_names: List[str], filtered_by: str) -> List[str]:
    scrapers_names: List[str] = []
    for file_name in file_names:
        if file_name.endswith(filtered_by):
            # '.py' hariç class ismi
            scrapers_names.append(file_name[:-3])
    return scrapers_names


def get_scrapers_class_names() -> List[str]:
    file_names: List[str] = get_file_names_in_directory(scrapers_root_directory)
    return filter_file_names_by_ends(file_names, filtered_by='Scraper.py')


def get_class_instance_by_class_name(class_name: str) -> WebScraperI:
    module = importlib.import_module('src.main.service.webscraper.' + class_name)
    class_ = getattr(module, class_name)
    return class_(class_name.lower())


def get_scraper_list() -> List[WebScraperI]:
    scraper_list: List[WebScraperI] = []
    scrapers_class_names = get_scrapers_class_names()

    for class_name in scrapers_class_names:
        scraper_list.append(get_class_instance_by_class_name(class_name))

    return scraper_list
