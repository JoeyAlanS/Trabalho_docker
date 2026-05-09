#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testes de Desempenho - Link Extractor
"""

from locust import HttpUser, task, between, events
import random
import json
import time
from pathlib import Path

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


# Evento para exportar estatísticas em formato JSON
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Executado quando o teste para"""
    stats = environment.stats
    
    results = {
        "timestamp": int(time.time()),
        "total_requests": stats.total.num_requests,
        "total_failures": stats.total.num_failures,
        "avg_response_time": stats.total.avg_response_time,
        "min_response_time": stats.total.min_response_time,
        "max_response_time": stats.total.max_response_time,
        "rps": stats.total.total_rps,
        "requests": []
    }
    
    for req_name in sorted(stats.entries.keys()):
        req_stats = stats.entries[req_name]
        results["requests"].append({
            "name": req_name,
            "num_requests": req_stats.num_requests,
            "num_failures": req_stats.num_failures,
            "avg_response_time": req_stats.avg_response_time,
            "min_response_time": req_stats.min_response_time,
            "max_response_time": req_stats.max_response_time,
            "rps": req_stats.total_rps
        })
    
    # Salvar em arquivo JSON
    results_dir = Path("performance_results")
    results_dir.mkdir(exist_ok=True)
    report_file = results_dir / f"report_{int(time.time())}.json"
    
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nRelatório salvo em: {report_file}")
