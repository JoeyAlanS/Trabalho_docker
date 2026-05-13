#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testes de Desempenho REAIS - Link Extractor
Sem usar Locust (que tem bug com Python 3.14)
Faz requisições HTTP reais e coleta métricas verdadeiras
"""

import os
import sys
import subprocess
import time
import csv
import json
import threading
import requests
from pathlib import Path
from datetime import datetime
from statistics import mean, median
from urllib.parse import quote

# Forçar UTF-8 output no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class RealPerformanceTest:
    # Constantes de configuração (mesmo para todos os testes)
    RAMP_UP_DELAY = 0.2  # segundos por usuário (ramp-up rápido: 300 × 0.2 = 60s)
    THINK_TIME = 2.0     # segundos entre requisições (aumentado para reduzir RPS e equilibrar carga)
    TEST_DURATION = 180  # segundos por carga (mesmo tempo total para todos os testes)
    REQUEST_TIMEOUT = 45  # timeout aumentado para 45s
    
    # Headers para parecer um navegador real
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    def __init__(self):
        self.results_dir = Path("performance_results")
        self.results_dir.mkdir(exist_ok=True)
        
        self.user_loads = {
            80: "Pequeno",      # 0% falha esperada
            160: "Médio",        # 0-1% falha esperada
            300: "Grande"        # 5-10% falha esperada
        }
        
        self.scenarios = [
            {
                "compose": "docker-compose.python-cache.yml",
                "name": "Python com Cache",
                "port": 5000,
                "language": "Python",
                "cache": "Sim"
            },
            {
                "compose": "docker-compose.python-no-cache.yml",
                "name": "Python sem Cache",
                "port": 5000,
                "language": "Python",
                "cache": "Não"
            },
            {
                "compose": "docker-compose.ruby-cache.yml",
                "name": "Ruby com Cache",
                "port": 4567,
                "language": "Ruby",
                "cache": "Sim"
            },
            {
                "compose": "docker-compose.ruby-no-cache.yml",
                "name": "Ruby sem Cache",
                "port": 4567,
                "language": "Ruby",
                "cache": "Não"
            }
        ]
        
        self.all_results = []
        
        # URLs de teste - substituidas por URLs mais estáveis
        self.test_urls = [
            "https://tracker.debian.org/pkg/apt", "https://news.ycombinator.com/news",
            "https://www.python.org/",
            "https://www.github.com/",
            "https://stackoverflow.com/",
            "https://www.amazon.com/",
        ]
    
    def run_command(self, cmd, timeout=300):
        """Executa comando"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Timeout"
        except Exception as e:
            return False, "", str(e)
    
    def start_services(self, compose_file):
        """Inicia serviços Docker"""
        cmd = f"docker-compose -f {compose_file} up -d --build"
        print(f"   [INICIANDO] {compose_file}", flush=True)
        success, _, _ = self.run_command(cmd, timeout=120)
        
        if success:
            # Aguardar um pouco e testar se está rodando
            time.sleep(5)
            print(f"   [VERIFICANDO] Containers...", flush=True)
        
        return success
    
    def stop_services(self, compose_file):
        """Para serviços Docker"""
        cmd = f"docker-compose -f {compose_file} down"
        success, _, _ = self.run_command(cmd, timeout=60)
        return success
    
    def make_request(self, port, url):
        """Faz uma requisição com retry e retorna tempo em ms"""
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                start = time.time()
                api_url = f"http://localhost:{port}/api/{quote(url, safe=':/?=&')}"
                response = requests.get(
                    api_url, 
                    timeout=self.REQUEST_TIMEOUT,
                    headers=self.HEADERS
                )
                elapsed = (time.time() - start) * 1000  # em ms
                success = response.status_code == 200
                
                return elapsed, success, response.status_code
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(1)  # Aguarda 1s antes de retry
                    continue
                return None, False, "Timeout"
            except requests.exceptions.ConnectionError:
                return None, False, "ConnError"
            except Exception as e:
                return None, False, str(type(e).__name__)
        
        return None, False, "MaxRetries"
    
    def simulate_users(self, port, num_users, duration_secs=120):
        """
        Simula N usuários fazendo requisições em paralelo
        Cada usuário faz requisições aleatórias durante o período
        """
        print(f"      [SIMULANDO] {num_users} usuarios por {duration_secs}s...", flush=True)
        print(f"      [TIMEOUT] {self.REQUEST_TIMEOUT}s | [THINK_TIME] {self.THINK_TIME}s", flush=True)
        print(f"      [URLs] {self.test_urls[0][:50]}... (+{len(self.test_urls)-1} outras)", flush=True)
        
        response_times = []
        failures = 0
        requests_made = 0
        status_codes = {}  # Para rastrear diferentes status codes
        
        lock = threading.Lock()
        
        def user_thread():
            nonlocal failures, requests_made
            start_time = time.time()
            first_error = True  # Para mostrar apenas o primeiro erro
            
            while time.time() - start_time < duration_secs:
                url = self.test_urls[requests_made % len(self.test_urls)]
                elapsed, success, status = self.make_request(port, url)
                time.sleep(self.THINK_TIME)  # Think time entre requisições
                
                with lock:
                    requests_made += 1
                    if elapsed is not None:
                        response_times.append(elapsed)
                        if not success:
                            failures += 1
                            if first_error and requests_made <= 5:
                                status_codes[status] = status_codes.get(status, 0) + 1
                                first_error = False
                    else:
                        failures += 1
                        if first_error and requests_made <= 5:
                            status_codes[status] = status_codes.get(status, 0) + 1
                            first_error = False
        
        # Criar e rodar threads
        threads = []
        start_time = time.time()
        
        for i in range(num_users):
            t = threading.Thread(target=user_thread, daemon=True)
            threads.append(t)
            t.start()
            time.sleep(self.RAMP_UP_DELAY)  # Ramp-up: mesmo delay para todos
        
        # Esperar conclusão
        for t in threads:
            t.join(timeout=duration_secs + 10)
        
        elapsed_total = time.time() - start_time
        
        # Calcular métricas
        if not response_times:
            return None
        
        response_times.sort()
        metrics = {
            "usuarios": num_users,
            "tempo_medio": mean(response_times),
            "tempo_min": min(response_times),
            "tempo_max": max(response_times),
            "p95": response_times[int(len(response_times) * 0.95)] if len(response_times) > 0 else 0,
            "rps": requests_made / elapsed_total if elapsed_total > 0 else 0,
            "total_reqs": requests_made,
            "falhas": failures,
            "taxa_falha": (failures / requests_made * 100) if requests_made > 0 else 0
        }
        
        print(f"      [OK] {requests_made} requisicoes | Tempo medio: {metrics['tempo_medio']:.0f}ms | Falhas: {failures} ({metrics['taxa_falha']:.2f}%)", flush=True)
        
        # Debug: mostrar status codes de erro se houver
        if status_codes and failures > 0:
            print(f"      [DEBUG] Status codes com erro: {status_codes}", flush=True)
        
        return metrics
    
    def run_scenario(self, scenario):
        """Executa um cenário com 3 cargas de usuários"""
        name = scenario['name']
        compose = scenario['compose']
        port = scenario['port']
        language = scenario['language']
        cache_mode = scenario['cache']
        
        print(f"\n{'='*70}", flush=True)
        print(f"[TESTANDO] {name}", flush=True)
        print(f"{'='*70}\n", flush=True)
        
        # Iniciar Docker
        print(f"[PASSO 1] Iniciando servicos...", flush=True)
        if not self.start_services(compose):
            print(f"[ERRO] Falha ao iniciar Docker", flush=True)
            return False
        
        print(f"   [AGUARDANDO] 10 segundos para estabilizar...", flush=True)
        time.sleep(10)
        
        # Executar testes com 3 cargas
        print(f"\n[PASSO 2] Executando testes com 3 cargas...", flush=True)
        
        for num_users, tamanho in sorted(self.user_loads.items()):
            print(f"\n   [TESTE] {num_users} usuarios ({tamanho})...", flush=True)
            
            metrics = self.simulate_users(port, num_users, duration_secs=self.TEST_DURATION)
            
            if metrics is None:
                print(f"   [ERRO] Falha ao coletar metricas", flush=True)
                return False
            
            result = {
                "Cenário": name,
                "Linguagem": language,
                "Cache": cache_mode,
                "Usuários": metrics["usuarios"],
                "Tamanho": tamanho,
                "Tempo Médio (ms)": round(metrics["tempo_medio"], 1),
                "Min (ms)": round(metrics["tempo_min"], 1),
                "Max (ms)": round(metrics["tempo_max"], 1),
                "P95 (ms)": round(metrics["p95"], 1),
                "RPS": round(metrics["rps"], 1),
                "Total Requisições": metrics["total_reqs"],
                "Falhas": metrics["falhas"],
                "Taxa de Falha (%)": round(metrics["taxa_falha"], 2)
            }
            
            # Print detalhado com todos os dados REAIS
            print(f"\n      [RESUMO]", flush=True)
            print(f"         Usuarios: {result['Usuários']} ({tamanho}) | Ramp-up: {self.RAMP_UP_DELAY}s", flush=True)
            print(f"         Resposta (ms): Min={result['Min (ms)']} | Media={result['Tempo Médio (ms)']} | Max={result['Max (ms)']} | P95={result['P95 (ms)']}", flush=True) 
            print(f"         RPS: {result['RPS']} | Total Reqs: {result['Total Requisições']}", flush=True)
            print(f"         Falhas: {result['Falhas']} ({result['Taxa de Falha (%)']}%)", flush=True)
            self.all_results.append(result)
            time.sleep(5)
        
        # Parar Docker
        print(f"\n[PASSO 3] Parando servicos...", flush=True)
        self.stop_services(compose)
        time.sleep(5)
        
        return True
    
    def save_results(self):
        """Salva resultados em CSV e JSON"""
        csv_file = self.results_dir / "resultados_completos.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.all_results[0].keys())
            writer.writeheader()
            writer.writerows(self.all_results)
        
        print(f"[SALVO] CSV: {csv_file}")
        
        json_file = self.results_dir / f"relatorio_{int(time.time())}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_testes": len(self.all_results),
                "resultados": self.all_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"[SALVO] JSON: {json_file}")
    
    def run_all(self):
        """Executa todos os cenários"""
        print(f"\n{'='*70}", flush=True)
        print(f"TESTES DE DESEMPENHO REAIS - LINK EXTRACTOR", flush=True)
        print(f"{'='*70}", flush=True)
        print(f"\n[CONFIGURACAO]", flush=True)
        print(f"   - 4 Cenarios (Python±Cache, Ruby±Cache)", flush=True)
        print(f"   - 3 Cargas: 80, 160, 300 usuarios", flush=True)
        print(f"   - {self.TEST_DURATION}s por teste (TEMPO IGUAL PARA TODOS)", flush=True)
        print(f"   - Requisicoes HTTP REAIS (sem simulacao)", flush=True)
        print(f"   - Ramp-up: {self.RAMP_UP_DELAY}s por usuario (300 × {self.RAMP_UP_DELAY}s = 60s)", flush=True)
        print(f"   - Think Time: {self.THINK_TIME}s entre requisicoes", flush=True)
        print(f"   - Timeout: {self.REQUEST_TIMEOUT}s por requisicao", flush=True)
        print(f"   - Tempo total: ~20-25 minutos\n", flush=True)
        
        print("[AGUARDANDO] Iniciando em 3 segundos...", flush=True)
        time.sleep(3)
        
        start_time = time.time()
        completed = 0
        
        for i, scenario in enumerate(self.scenarios, 1):
            print(f"\n[{i}/4]", flush=True)
            if self.run_scenario(scenario):
                completed += 1
            else:
                print(f"[AVISO] Cenario {scenario['name']} falhou", flush=True)
                break
        
        elapsed = time.time() - start_time
        
        if self.all_results:
            print(f"\n{'='*70}", flush=True)
            print(f"[SUCESSO] TESTES CONCLUIDOS!", flush=True)
            print(f"{'='*70}\n", flush=True)
            print(f"[RESULTADO]", flush=True)
            print(f"   Cenarios: {completed}/4", flush=True)
            print(f"   Testes: {len(self.all_results)}/12", flush=True)
            print(f"   Ramp-up: {self.RAMP_UP_DELAY}s por usuario", flush=True)
            print(f"   Tempo total: {elapsed/60:.1f} minutos", flush=True)
            
            self.save_results()
            
            print(f"\n[PROXIMO] python generate_graphs.py\n", flush=True)
        else:
            print(f"\n[ERRO] Nenhum resultado coletado", flush=True)

if __name__ == "__main__":
    tester = RealPerformanceTest()
    tester.run_all()
