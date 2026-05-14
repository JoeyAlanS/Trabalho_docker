"""
Ponto de entrada na raiz do repositório.

Assim pode executar na pasta do projeto:

    python -m locust -H http://127.0.0.1:5000

sem precisar de `-f loadtest/locustfile.py` (o Locust usa por defeito `./locustfile.py`).
"""
from loadtest.locustfile import LinkExtractorUser

__all__ = ["LinkExtractorUser"]
