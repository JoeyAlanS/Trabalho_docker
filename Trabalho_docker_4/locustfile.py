#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testes de Desempenho - Link Extractor
Autor: Joey
"""

from locust import HttpUser, task, between
import random

class LinkExtractorUser(HttpUser):
    """
    Simula um usuário virtual que faz requisições ao serviço de extração de links.
    Cada usuário realiza uma sequência de 10 invocações com URLs diferentes.
    """
    
    wait_time = between(1, 3)  # Espera entre 1 e 3 segundos entre requisições
    
    # Lista de URLs para teste (diferentes URLs)
    test_urls = [
        "http://example.com/",
        "https://www.python.org/",
        "https://www.wikipedia.org/",
        "https://www.github.com/",
        "https://stackoverflow.com/",
        "https://www.amazon.com/",
        "https://www.google.com/",
        "https://www.youtube.com/",
        "https://www.twitter.com/",
        "https://www.linkedin.com/"
    ]
    
    def on_start(self):
        """Executado quando o usuário inicia"""
        self.request_count = 0
    
    @task
    def extract_links(self):
        """
        Tarefa que simula a extração de links.
        Faz requisições ao serviço de extração de links com URLs diferentes.
        """
        # Seleciona uma URL aleatória da lista
        url = random.choice(self.test_urls)
        
        # Faz a requisição ao serviço de API
        with self.client.get(
            f"/api/{url}",
            catch_response=True,
            name="/api/[URL]"  # Agrupa todas as URLs sob um nome único para melhor análise
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
        
        self.request_count += 1
    
    def on_stop(self):
        """Executado quando o usuário para"""
        print(f"Usuário completou {self.request_count} requisições")
