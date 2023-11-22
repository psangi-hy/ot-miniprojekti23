import requests

class AppLibrary:
    def __init__(self):
        self._base_url = "http://localhost:5000"

        self.reset_application()

    def reset_application(self):
        requests.post(f"{self._base_url}/tests/reset")

    def create_article(
            self, key, author, title, journal, year, volume, pages
    ):
        data = {
            "key": key,
            "author": author,
            "title": title,
            "journal": journal,
            "year": year,
            "volume": volume,
            "pages": pages
        }

        requests.post(f"{self._base_url}/new", json=data)
