#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gerador de Dados de Exemplo - Testes de Desempenho
Autor: Joey

Cria arquivo CSV com dados realistas para teste
Cargas: Pequeno (5 usuários), Médio (15 usuários), Grande (50 usuários)
Falhas: 0% para pequeno/médio, até 10% para grande
"""

import os
import csv
from pathlib import Path

# Criar pasta para resultados
results_dir = Path("performance_results")
results_dir.mkdir(exist_ok=True)

# Dados realistas para os 4 cenários × 3 cargas
test_data = []

scenarios = [
    ("Python com Cache", 1.0),
    ("Python sem Cache", 1.5),
    ("Ruby com Cache", 1.2),
    ("Ruby sem Cache", 1.8),
]

# Pequeno, Médio, Grande
users_list = [5, 15, 50]

for scenario_name, multiplier in scenarios:
    for idx, users in enumerate(users_list):
        # Valores base crescem com usuários e multiplicador
        avg = int(50 * multiplier + (users * 12 * multiplier))
        min_val = int(avg * 0.3)
        max_val = int(avg * 3)
        p95 = int(avg * 2.2)
        rps = max(1, int(60 / (avg / 1000)))
        total_req = int(rps * 120)
        
        # Falhas: 0% para pequeno/médio, até 10% para grande
        if idx == 2:  # Grande (50 usuários)
            # Falhas crescem com a carga e tipo de cenário
            if "sem Cache" in scenario_name:
                fail_rate = 8 + (multiplier - 1.0) * 5  # 8-10%
            else:
                fail_rate = 3 + (multiplier - 1.0) * 3  # 3-6%
            fail_rate = min(10, max(1, fail_rate))  # Limita entre 1-10%
            failures = int((total_req * fail_rate) / 100)
        else:
            fail_rate = 0
            failures = 0
        
        test_data.append({
            "Cenário": scenario_name,
            "Usuários": users,
            "Tamanho": ["Pequeno", "Médio", "Grande"][idx],
            "Média (ms)": avg,
            "Min (ms)": min_val,
            "Max (ms)": max_val,
            "P95 (ms)": p95,
            "RPS": rps,
            "Total Requisições": total_req,
            "Falhas": failures,
            "Taxa de Falha (%)": round(fail_rate, 1)
        })

# Salvar CSV
csv_file = results_dir / "sample_comparison.csv"
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Cenário", "Usuários", "Tamanho", "Média (ms)", "Min (ms)", "Max (ms)", 
        "P95 (ms)", "RPS", "Total Requisições", "Falhas", "Taxa de Falha (%)"
    ])
    writer.writeheader()
    writer.writerows(test_data)

print(f"✅ Dados de exemplo criados: {csv_file}")
print(f"📊 {len(test_data)} linhas geradas")
print(f"📈 Cargas: 5 usuários (Pequeno), 15 usuários (Médio), 50 usuários (Grande)")
print(f"⚠️  Falhas: 0% em pequeno/médio, até 10% em grande")
