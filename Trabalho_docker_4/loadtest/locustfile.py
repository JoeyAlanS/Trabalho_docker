from urllib.parse import quote

from locust import HttpUser, between, task

# URLs fiáveis para testes de carga (sem bloqueios de bots)
TARGET_URLS = [
    "https://httpbin.org/html",
    "https://httpbin.org/links/199",
    "https://httpbin.org/links/100",
    "https://httpbin.org/forms/post",
    "https://crawler-test.com/",
    "https://news.ycombinator.com/news",
    "https://en.wikipedia.org/wiki/Wikipedia:Contents/Portals",
    "https://en.wikipedia.org/wiki/Wikipedia:Contents/Outlines",
    "https://en.wikipedia.org/wiki/Wikipedia:Contents/Lists",
    "https://projects.apache.org/projects.html"

]


class LinkExtractorUser(HttpUser):
    wait_time = between(0.1, 0.5)  # delay realista entre requisições

    @task
    def sequence_ten_urls(self):
        for url in TARGET_URLS:
            path = f"/api/{quote(url, safe='')}"
            self.client.get(path, name="/api/[url]")
