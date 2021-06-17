import unittest
from typing import List

from src.main.entity.Keyword import Keyword
from src.main.service.KeywordFinder import KeywordFinder


class KeyFinderTest(unittest.TestCase):
    keyFinder = KeywordFinder()


    def test_is_model_work(self):
        text = "experience reading software code in one or more languages such as java, javascript, python"
        keywords: List[Keyword] = self.keyFinder.find_keys(text)

        for keyword in keywords:
            print(keyword.__str__())


if __name__ == '__main__':
    unittest.main()