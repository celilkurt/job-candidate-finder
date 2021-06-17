class CVMetadata:
    url: str
    cv_id: str

    def __init__(self, url, cv_id):
        self.url = url
        self.cv_id = cv_id

    def __str__(self):
        return self.cv_id + ': ' + self.url
