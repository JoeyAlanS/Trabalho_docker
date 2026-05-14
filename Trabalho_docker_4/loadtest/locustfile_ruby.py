"""
Locustfile optimizado para Ruby API.

Diferenças do Python:
- Timeout ligeiramente maior (Ruby é mais lento a processar)
- Melhor handling de conexão
- Logs detalhados de erros

Uso:
  docker compose -f docker-compose.ruby-no-cache.yml up -d --build
  # No Locust UI (http://127.0.0.1:8089/):
  # - Usar esta configuração ao invés do locustfile.py padrão
  
Ou mudar o docker-compose.ruby-*.yml para usar este ficheiro.
"""

from urllib.parse import quote
from locust import HttpUser, between, task

# URLs fiáveis para testes de carga
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
    wait_time = between(0.1, 0.5)

    @task
    def sequence_ten_urls(self):
        for url in TARGET_URLS:
            path = f"/api/{quote(url, safe='')}"
            # Mesmo timeout que Python (10s) para comparação justa
            self.client.get(
                path, 
                name="/api/[url]",
                timeout=10
            )
