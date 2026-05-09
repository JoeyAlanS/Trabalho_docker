#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gerador de Gráficos - Testes de Desempenho Link Extractor
Autor: Joey

Lê dados do CSV e gera gráficos comparativos
Gráficos: Tempo Médio, RPS, P95%, Taxa de Falha, Comparações
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
# CRIAR PASTA PARA GRÁFICOS
# ============================================================================
output_dir = "output_graphs"
Path(output_dir).mkdir(exist_ok=True)

# ============================================================================
# LER DADOS DO CSV
# ============================================================================
csv_file = "performance_results/sample_comparison.csv"

if not os.path.exists(csv_file):
    print(f"❌ Arquivo não encontrado: {csv_file}")
    print("Execute: python generate_sample_results.py")
    exit(1)

try:
    df = pd.read_csv(csv_file, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(csv_file, encoding='latin-1')
    except:
        df = pd.read_csv(csv_file, encoding='cp1252')

# Remover espaços nas colunas
df.columns = df.columns.str.strip()

# Preencher NaN em Taxa de Falha
if 'Taxa de Falha (%)' in df.columns:
    df['Taxa de Falha (%)'] = df['Taxa de Falha (%)'].fillna(0)
else:
    df['Taxa de Falha (%)'] = 0

# ============================================================================
# PREPARAR DADOS POR CENÁRIO
# ============================================================================

scenarios = df['Cenário'].unique()
colors = {
    'Python com Cache': '#2E86AB',
    'Python sem Cache': '#A23B72',
    'Ruby com Cache': '#F18F01',
    'Ruby sem Cache': '#C73E1D',
}

# ============================================================================
# 1. TEMPO MÉDIO vs USUÁRIOS (com 3 cargas)
# ============================================================================
plt.figure(figsize=(12, 7))
for scenario in scenarios:
    scenario_data = df[df['Cenário'] == scenario].sort_values('Usuários')
    plt.plot(scenario_data['Usuários'], scenario_data['Média (ms)'], 
             marker='o', linewidth=2.5, markersize=8, label=scenario, 
             color=colors.get(scenario, None))

plt.xlabel('Número de Usuários', fontsize=12, fontweight='bold')
plt.ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
plt.title('Testes de Desempenho - Link Extractor\nTempo Médio vs Usuários (2 min)', 
          fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10, loc='upper left')
plt.tight_layout()
plt.savefig(f'{output_dir}/01_tempo_medio_vs_usuarios.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 1: Tempo Médio vs Usuários")

# ============================================================================
# 2. RPS vs USUÁRIOS
# ============================================================================
plt.figure(figsize=(12, 7))
for scenario in scenarios:
    scenario_data = df[df['Cenário'] == scenario].sort_values('Usuários')
    plt.plot(scenario_data['Usuários'], scenario_data['RPS'], 
             marker='s', linewidth=2.5, markersize=8, label=scenario,
             color=colors.get(scenario, None))

plt.xlabel('Número de Usuários', fontsize=12, fontweight='bold')
plt.ylabel('Requisições por Segundo (RPS)', fontsize=12, fontweight='bold')
plt.title('Testes de Desempenho - Link Extractor\nThroughput (RPS) vs Usuários (2 min)', 
          fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10, loc='upper right')
plt.tight_layout()
plt.savefig(f'{output_dir}/02_rps_vs_usuarios.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 2: RPS vs Usuários")

# ============================================================================
# 3. P95% vs USUÁRIOS (NOVO)
# ============================================================================
plt.figure(figsize=(12, 7))
for scenario in scenarios:
    scenario_data = df[df['Cenário'] == scenario].sort_values('Usuários')
    plt.plot(scenario_data['Usuários'], scenario_data['P95 (ms)'], 
             marker='^', linewidth=2.5, markersize=8, label=scenario,
             color=colors.get(scenario, None))

plt.xlabel('Número de Usuários', fontsize=12, fontweight='bold')
plt.ylabel('P95 (ms)', fontsize=12, fontweight='bold')
plt.title('Testes de Desempenho - Link Extractor\nPercentil P95% vs Usuários (2 min)', 
          fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10, loc='upper left')
plt.tight_layout()
plt.savefig(f'{output_dir}/03_p95_vs_usuarios.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 3: P95% vs Usuários")

# ============================================================================
# 4. TAXA DE FALHA vs USUÁRIOS (NOVO)
# ============================================================================
plt.figure(figsize=(12, 7))
for scenario in scenarios:
    scenario_data = df[df['Cenário'] == scenario].sort_values('Usuários')
    plt.plot(scenario_data['Usuários'], scenario_data['Taxa de Falha (%)'], 
             marker='D', linewidth=2.5, markersize=8, label=scenario,
             color=colors.get(scenario, None))

plt.xlabel('Número de Usuários', fontsize=12, fontweight='bold')
plt.ylabel('Taxa de Falha (%)', fontsize=12, fontweight='bold')
plt.title('Testes de Desempenho - Link Extractor\nTaxa de Falha vs Usuários (2 min)', 
          fontsize=14, fontweight='bold')
plt.axhline(y=10, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='Limite 10%')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10, loc='upper left')
plt.ylim([-0.5, 12])
plt.tight_layout()
plt.savefig(f'{output_dir}/04_taxa_falha_vs_usuarios.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 4: Taxa de Falha vs Usuários")

# ============================================================================
# 5. COMPARAÇÃO MIN/MED/MAX por Cenário
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 7))

x_pos = []
x_labels = []
pos = 0

for scenario in scenarios:
    scenario_data = df[df['Cenário'] == scenario].sort_values('Usuários')
    for idx, (_, row) in enumerate(scenario_data.iterrows()):
        # Min
        ax.bar(pos, row['Min (ms)'], color=colors.get(scenario, None), alpha=0.3, width=0.8)
        # Média
        ax.bar(pos, row['Média (ms)'], color=colors.get(scenario, None), alpha=0.7, width=0.8)
        # Max (adicionar acima da média)
        ax.bar(pos, row['Max (ms)'] - row['Média (ms)'], bottom=row['Média (ms)'],
               color=colors.get(scenario, None), alpha=0.3, width=0.8, hatch='//')
        
        x_labels.append(f"{scenario}\n{int(row['Usuários'])}u")
        x_pos.append(pos)
        pos += 1
    pos += 0.5

ax.set_xticks(x_pos)
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_ylabel('Tempo de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nComparação Min/Médio/Max por Cenário (2 min)', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{output_dir}/05_min_med_max_por_cenario.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 5: Comparação Min/Med/Max")

# ============================================================================
# 6. IMPACTO DO CACHE - PYTHON
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

python_cache = df[df['Cenário'] == 'Python com Cache'].sort_values('Usuários')
python_no_cache = df[df['Cenário'] == 'Python sem Cache'].sort_values('Usuários')

x = range(len(python_cache))
width = 0.35

ax.bar([i - width/2 for i in x], python_cache['Média (ms)'], width, 
       label='Com Cache', color='#2E86AB')
ax.bar([i + width/2 for i in x], python_no_cache['Média (ms)'], width, 
       label='Sem Cache', color='#A23B72')

ax.set_xlabel('Número de Usuários', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nImpacto do Cache - Python (2 min)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(python_cache['Usuários'].astype(int))
ax.grid(True, alpha=0.3, axis='y')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{output_dir}/06_impacto_cache_python.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 6: Impacto Cache Python")

# ============================================================================
# 7. IMPACTO DO CACHE - RUBY
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

ruby_cache = df[df['Cenário'] == 'Ruby com Cache'].sort_values('Usuários')
ruby_no_cache = df[df['Cenário'] == 'Ruby sem Cache'].sort_values('Usuários')

x = range(len(ruby_cache))
width = 0.35

ax.bar([i - width/2 for i in x], ruby_cache['Média (ms)'], width, 
       label='Com Cache', color='#F18F01')
ax.bar([i + width/2 for i in x], ruby_no_cache['Média (ms)'], width, 
       label='Sem Cache', color='#C73E1D')

ax.set_xlabel('Número de Usuários', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nImpacto do Cache - Ruby (2 min)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(ruby_cache['Usuários'].astype(int))
ax.grid(True, alpha=0.3, axis='y')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{output_dir}/07_impacto_cache_ruby.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 7: Impacto Cache Ruby")

# ============================================================================
# 8. PYTHON vs RUBY (Com Cache)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

python_cache = df[df['Cenário'] == 'Python com Cache'].sort_values('Usuários')
ruby_cache = df[df['Cenário'] == 'Ruby com Cache'].sort_values('Usuários')

x = range(len(python_cache))
width = 0.35

ax.bar([i - width/2 for i in x], python_cache['Média (ms)'], width, 
       label='Python', color='#2E86AB')
ax.bar([i + width/2 for i in x], ruby_cache['Média (ms)'], width, 
       label='Ruby', color='#F18F01')

ax.set_xlabel('Número de Usuários', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nComparação Python vs Ruby (Com Cache, 2 min)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(python_cache['Usuários'].astype(int))
ax.grid(True, alpha=0.3, axis='y')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{output_dir}/08_python_vs_ruby_cache.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 8: Python vs Ruby (Com Cache)")

# ============================================================================
# 9. PYTHON vs RUBY (Sem Cache)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

python_no_cache = df[df['Cenário'] == 'Python sem Cache'].sort_values('Usuários')
ruby_no_cache = df[df['Cenário'] == 'Ruby sem Cache'].sort_values('Usuários')

x = range(len(python_no_cache))
width = 0.35

ax.bar([i - width/2 for i in x], python_no_cache['Média (ms)'], width, 
       label='Python', color='#A23B72')
ax.bar([i + width/2 for i in x], ruby_no_cache['Média (ms)'], width, 
       label='Ruby', color='#C73E1D')

ax.set_xlabel('Número de Usuários', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nComparação Python vs Ruby (Sem Cache, 2 min)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(python_no_cache['Usuários'].astype(int))
ax.grid(True, alpha=0.3, axis='y')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{output_dir}/09_python_vs_ruby_no_cache.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 9: Python vs Ruby (Sem Cache)")

print(f"\n{'='*70}")
print(f"✅ TODOS OS GRÁFICOS GERADOS COM SUCESSO!")
print(f"{'='*70}")
print(f"📁 Pasta: {output_dir}/")
print(f"📊 Total: 9 gráficos PNG")
print(f"🎯 Métricas: Tempo, RPS, P95%, Taxa de Falha")
