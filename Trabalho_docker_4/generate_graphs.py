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

# Configurar matplotlib para usar fonte que suporte acentuação
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

# Criar pasta para gráficos
output_dir = "output_graphs"
Path(output_dir).mkdir(exist_ok=True)

# Ler dados do CSV
csv_file = "performance_results/resultados_completos.csv"

if not os.path.exists(csv_file):
    print(f"[ERRO] Arquivo nao encontrado: {csv_file}")
    print("Execute: python run_performance_tests.py")
    exit(1)

# Ler com UTF-8
df = pd.read_csv(csv_file, encoding='utf-8')
df.columns = df.columns.str.strip()

# Garantir que Taxa de Falha seja numérica
if 'Taxa de Falha (%)' in df.columns:
    df['Taxa de Falha (%)'] = pd.to_numeric(df['Taxa de Falha (%)'], errors='coerce').fillna(0)

# Cores para cada cenário
colors = {
    'Python com Cache': '#2E86AB',
    'Python sem Cache': '#A23B72',
    'Ruby com Cache': '#F18F01',
    'Ruby sem Cache': '#C73E1D',
}

# Obter cenários
scenarios = df['Cenário'].unique()

print(f"\n[LENDO] Dados de {csv_file}")
print(f"   Cenários: {list(scenarios)}")
print(f"   Usuários: {sorted(df['Usuários'].unique())}")
print()

# ============================================================================
# 1. TEMPO MÉDIO vs USUÁRIOS
# ============================================================================
plt.figure(figsize=(12, 7))
for scenario in scenarios:
    scenario_data = df[df['Cenário'] == scenario].sort_values('Usuários')
    plt.plot(scenario_data['Usuários'], scenario_data['Tempo Médio (ms)'], 
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
print("[GERADO] Grafico 1: Tempo Medio vs Usuarios")

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
print("[GERADO] Grafico 2: RPS vs Usuarios")

# ============================================================================
# 3. P95% vs USUÁRIOS
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
print("[GERADO] Grafico 3: P95% vs Usuarios")

# ============================================================================
# 4. TAXA DE FALHA vs USUÁRIOS
# ============================================================================
try:
    if 'Taxa de Falha (%)' not in df.columns:
        print(f"[AVISO] Coluna 'Taxa de Falha (%)' nao encontrada. Colunas disponiveis:")
        print(f"   {list(df.columns)}")
    else:
        plt.figure(figsize=(12, 7))
        has_data = False
        
        for scenario in scenarios:
            scenario_data = df[df['Cenário'] == scenario].sort_values('Usuários')
            if len(scenario_data) > 0:
                has_data = True
                taxa_falha = scenario_data['Taxa de Falha (%)'].values
                usuarios = scenario_data['Usuários'].values
                
                # Debug: mostrar dados
                print(f"   DEBUG {scenario}: Usuários={usuarios}, Taxa de Falha={taxa_falha}")
                
                plt.plot(usuarios, taxa_falha, 
                         marker='D', linewidth=2.5, markersize=8, label=scenario,
                         color=colors.get(scenario, None))
        
        if has_data:
            plt.xlabel('Número de Usuários', fontsize=12, fontweight='bold')
            plt.ylabel('Taxa de Falha (%)', fontsize=12, fontweight='bold')
            plt.title('Testes de Desempenho - Link Extractor\nTaxa de Falha vs Usuários (2 min)', 
                      fontsize=14, fontweight='bold')
            plt.axhline(y=10, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='Limite 10%')
            plt.grid(True, alpha=0.3)
            plt.legend(fontsize=10, loc='upper left')
            plt.ylim([-0.5, max(20, df['Taxa de Falha (%)'].max() + 2)])
            plt.tight_layout()
            plt.savefig(f'{output_dir}/04_taxa_falha_vs_usuarios.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("[GERADO] Grafico 4: Taxa de Falha vs Usuarios")
        else:
            print("[ERRO] Nenhum dado encontrado para grafico de Taxa de Falha")
except Exception as e:
    print(f"[ERRO] Erro ao gerar grafico 4: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# 5. COMPARAÇÃO MIN/MED/MAX por Cenário
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 7))
x_pos = 0
width = 0.2
positions = []
labels_x = []

for scenario in scenarios:
    scenario_data = df[df['Cenário'] == scenario].sort_values('Usuários')
    for idx, (_, row) in enumerate(scenario_data.iterrows()):
        pos = x_pos
        
        # Min
        ax.bar(pos, row['Min (ms)'], width, color=colors.get(scenario), alpha=0.3)
        # Médio
        ax.bar(pos, row['Tempo Médio (ms)'], width, color=colors.get(scenario), alpha=0.7)
        # Max
        ax.bar(pos, row['Max (ms)'] - row['Tempo Médio (ms)'], width, 
               bottom=row['Tempo Médio (ms)'], color=colors.get(scenario), alpha=0.3, hatch='//')
        
        if idx == 0:
            labels_x.append(f"{scenario}\n({row['Usuários']}u)")
        else:
            labels_x.append(f"{row['Usuários']}u")
        
        positions.append(pos)
        x_pos += width + 0.05

ax.set_xticks(positions)
ax.set_xticklabels(labels_x, fontsize=9, rotation=45, ha='right')
ax.set_ylabel('Tempo (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nComparação Min/Médio/Max por Cenário (2 min)', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
fig.tight_layout()
plt.savefig(f'{output_dir}/05_min_med_max_por_cenario.png', dpi=300, bbox_inches='tight')
plt.close()
print("[GERADO] Grafico 5: Min/Med/Max por Cenario")

# ============================================================================
# 6. IMPACTO DO CACHE - PYTHON
# ============================================================================
python_cache = df[df['Cenário'] == 'Python com Cache'].sort_values('Usuários')
python_no_cache = df[df['Cenário'] == 'Python sem Cache'].sort_values('Usuários')

fig, ax = plt.subplots(figsize=(12, 7))
x = range(len(python_cache))
width = 0.35

ax.bar([i - width/2 for i in x], python_cache['Tempo Médio (ms)'], width, 
       label='Com Cache', color='#2E86AB')
ax.bar([i + width/2 for i in x], python_no_cache['Tempo Médio (ms)'], width, 
       label='Sem Cache', color='#A23B72')

ax.set_xlabel('Número de Usuários', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nImpacto do Cache - Python (2 min)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(python_cache['Usuários'].values)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
fig.tight_layout()
plt.savefig(f'{output_dir}/06_impacto_cache_python.png', dpi=300, bbox_inches='tight')
plt.close()
print("[GERADO] Grafico 6: Impacto Cache - Python")

# ============================================================================
# 7. IMPACTO DO CACHE - RUBY
# ============================================================================
ruby_cache = df[df['Cenário'] == 'Ruby com Cache'].sort_values('Usuários')
ruby_no_cache = df[df['Cenário'] == 'Ruby sem Cache'].sort_values('Usuários')

fig, ax = plt.subplots(figsize=(12, 7))
x = range(len(ruby_cache))
width = 0.35

ax.bar([i - width/2 for i in x], ruby_cache['Tempo Médio (ms)'], width, 
       label='Com Cache', color='#F18F01')
ax.bar([i + width/2 for i in x], ruby_no_cache['Tempo Médio (ms)'], width, 
       label='Sem Cache', color='#C73E1D')

ax.set_xlabel('Número de Usuários', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nImpacto do Cache - Ruby (2 min)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(ruby_cache['Usuários'].values)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
fig.tight_layout()
plt.savefig(f'{output_dir}/07_impacto_cache_ruby.png', dpi=300, bbox_inches='tight')
plt.close()
print("[GERADO] Grafico 7: Impacto Cache - Ruby")

# ============================================================================
# 8. PYTHON vs RUBY (COM CACHE)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))
x = range(len(python_cache))
width = 0.35

ax.bar([i - width/2 for i in x], python_cache['Tempo Médio (ms)'], width, 
       label='Python', color='#2E86AB')
ax.bar([i + width/2 for i in x], ruby_cache['Tempo Médio (ms)'], width, 
       label='Ruby', color='#F18F01')

ax.set_xlabel('Número de Usuários', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nComparação Python vs Ruby (Com Cache, 2 min)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(python_cache['Usuários'].values)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
fig.tight_layout()
plt.savefig(f'{output_dir}/08_python_vs_ruby_cache.png', dpi=300, bbox_inches='tight')
plt.close()
print("[GERADO] Grafico 8: Python vs Ruby (Com Cache)")

# ============================================================================
# 9. PYTHON vs RUBY (SEM CACHE)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))
x = range(len(python_no_cache))
width = 0.35

ax.bar([i - width/2 for i in x], python_no_cache['Tempo Médio (ms)'], width, 
       label='Python', color='#A23B72')
ax.bar([i + width/2 for i in x], ruby_no_cache['Tempo Médio (ms)'], width, 
       label='Ruby', color='#C73E1D')

ax.set_xlabel('Número de Usuários', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Testes de Desempenho - Link Extractor\nComparação Python vs Ruby (Sem Cache, 2 min)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(python_no_cache['Usuários'].values)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
fig.tight_layout()
plt.savefig(f'{output_dir}/09_python_vs_ruby_no_cache.png', dpi=300, bbox_inches='tight')
plt.close()
print("[GERADO] Grafico 9: Python vs Ruby (Sem Cache)")

print(f"\n[SUCESSO] Todos os 9 graficos foram gerados em: {output_dir}/")
