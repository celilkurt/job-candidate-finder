
'''
NLP modeli çıktılarının tutulması için
'''
class Keyword:

    label: str
    value: str

    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

    def __str__(self) -> str:
        return self.label + ' ' + self.value




