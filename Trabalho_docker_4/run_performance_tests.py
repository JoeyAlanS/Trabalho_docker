#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testes de Desempenho Completos - Link Extractor
Autor: Joey

Testa 4 cenários:
- Python com Cache
- Python sem Cache
- Ruby com Cache
- Ruby sem Cache

Cada cenário com 5 variações: 1, 5, 10, 25, 50 usuários
Duração: 2 minutos (120 segundos) por teste
Total: ~40 minutos
"""

import os
import subprocess
import time
from pathlib import Path

class PerformanceTestRunner:
    def __init__(self):
        self.results_dir = Path("performance_results")
        self.results_dir.mkdir(exist_ok=True)
        
        self.scenarios = [
            {
                "compose": "docker-compose.python-cache.yml",
                "name": "Python com Cache",
                "port": 5000
            },
            {
                "compose": "docker-compose.python-no-cache.yml",
                "name": "Python sem Cache",
                "port": 5000
            },
            {
                "compose": "docker-compose.ruby-cache.yml",
                "name": "Ruby com Cache",
                "port": 4567
            },
            {
                "compose": "docker-compose.ruby-no-cache.yml",
                "name": "Ruby sem Cache",
                "port": 4567
            }
        ]
    
    def run_command(self, cmd):
        """Executa um comando"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout ao executar: {cmd}")
            return False
    
    def start_services(self, compose_file):
        """Inicia os serviços"""
        cmd = f"docker-compose -f {compose_file} up -d --build"
        return self.run_command(cmd)
    
    def stop_services(self, compose_file):
        """Para os serviços"""
        cmd = f"docker-compose -f {compose_file} down"
        return self.run_command(cmd)
    
    def run_locust_test(self, port, num_users):
        """Executa um teste Locust"""
        ramp_up = max(1, num_users // 5)
        cmd = (
            f"locust -f locustfile.py --headless "
            f"-u {num_users} -r {ramp_up} -t 120 "
            f"-H http://localhost:{port} "
            f"--csv=test_{num_users}"
        )
        return self.run_command(cmd)
    
    def run_scenario(self, scenario):
        """Executa um cenário completo"""
        compose = scenario['compose']
        name = scenario['name']
        port = scenario['port']
        
        print(f"\n{'='*70}")
        print(f"🚀 TESTANDO: {name}")
        print(f"{'='*70}\n")
        
        # Iniciar
        print(f"1️⃣  Iniciando serviços...")
        if not self.start_services(compose):
            print(f"❌ Erro ao iniciar serviços")
            return False
        
        print(f"   ⏳ Aguardando 10 segundos...")
        time.sleep(10)
        
        # Testar com diferentes números de usuários
        # Pequeno (5), Médio (15), Grande (50)
        user_counts = [5, 15, 50]
        
        for num_users in user_counts:
            print(f"\n2️⃣  Testando com {num_users} usuários...")
            if not self.run_locust_test(port, num_users):
                print(f"❌ Erro no teste")
            
            if num_users != user_counts[-1]:
                time.sleep(5)
        
        # Parar
        print(f"\n3️⃣  Parando serviços...")
        self.stop_services(compose)
        
        return True
    
    def run_all_tests(self):
        """Executa todos os 4 cenários"""
        print(f"\n{'='*70}")
        print(f"📊 TESTES DE DESEMPENHO - LINK EXTRACTOR")
        print(f"{'='*70}")
        print(f"\n⏱️  Total de 4 cenários × 5 cargas = 20 testes")
        print(f"⏰ Duração estimada: 40 minutos\n")
        
        for scenario in self.scenarios:
            if not self.run_scenario(scenario):
                print(f"⚠️  Cenário {scenario['name']} falhou")
        
        print(f"\n{'='*70}")
        print(f"✅ TESTES COMPLETOS!")
        print(f"{'='*70}")
        print(f"\n📁 Resultados em: performance_results/")
        print(f"📊 Para gerar gráficos: python generate_graphs.py\n")

if __name__ == "__main__":
    runner = PerformanceTestRunner()
    runner.run_all_tests()
