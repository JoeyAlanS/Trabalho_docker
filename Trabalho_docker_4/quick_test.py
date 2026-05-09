#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testes de Desempenho - Link Extractor
Autor: Joey

Script de teste rápido para um cenário específico
Uso: python quick_test.py [python-cache|python-no-cache|ruby-cache|ruby-no-cache] [num_users]
"""

import sys
import time
import os

def run_test(scenario, num_users):
    """Executa um teste rápido para um cenário"""
    
    scenario_map = {
        "python-cache": {
            "compose": "docker-compose.python-cache.yml",
            "name": "Python com Cache",
            "port": 5000
        },
        "python-no-cache": {
            "compose": "docker-compose.python-no-cache.yml",
            "name": "Python sem Cache",
            "port": 5000
        },
        "ruby-cache": {
            "compose": "docker-compose.ruby-cache.yml",
            "name": "Ruby com Cache",
            "port": 4567
        },
        "ruby-no-cache": {
            "compose": "docker-compose.ruby-no-cache.yml",
            "name": "Ruby sem Cache",
            "port": 4567
        }
    }
    
    if scenario not in scenario_map:
        print(f"❌ Cenário inválido: {scenario}")
        print(f"✅ Opções: {', '.join(scenario_map.keys())}")
        return
    
    config = scenario_map[scenario]
    
    print(f"\n{'='*70}")
    print(f"🧪 TESTE RÁPIDO - {config['name']}")
    print(f"{'='*70}\n")
    
    print(f"📊 Configuração:")
    print(f"   Cenário: {config['name']}")
    print(f"   Usuários: {num_users}")
    print(f"   Duração: 2 minutos (120 segundos)")
    print(f"\n{'='*70}\n")
    
    # Step 1: Iniciar serviços
    print("1️⃣  Iniciando containers Docker...")
    cmd = f"docker-compose -f {config['compose']} up -d --build"
    os.system(cmd)
    
    print("\n   ⏳ Aguardando 10 segundos para estabilizar...")
    time.sleep(10)
    
    # Step 2: Executar teste
    print(f"\n2️⃣  Executando teste Locust (2 minutos)...")
    api_url = f"http://localhost:{config['port']}"
    ramp_up = max(1, num_users // 5)
    cmd = (
        f"locust -f locustfile.py --headless "
        f"-u {num_users} -r {ramp_up} -t 120 "
        f"-H {api_url}"
    )
    os.system(cmd)
    
    # Step 3: Parar serviços
    print(f"\n3️⃣  Parando containers Docker...")
    cmd = f"docker-compose -f {config['compose']} down"
    os.system(cmd)
    
    print(f"\n{'='*70}")
    print(f"✅ TESTE CONCLUÍDO!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n📋 Uso: python quick_test.py [cenário] [num_usuarios]")
        print("\n✅ Cenários disponíveis:")
        print("  - python-cache")
        print("  - python-no-cache")
        print("  - ruby-cache")
        print("  - ruby-no-cache")
        print("\n📌 Exemplo: python quick_test.py python-cache 10\n")
        sys.exit(1)
    
    scenario = sys.argv[1]
    num_users = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    run_test(scenario, num_users)

