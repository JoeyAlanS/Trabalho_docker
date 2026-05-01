import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

# ============================================================================
# CRIAR PASTA PARA GRÁFICOS
# ============================================================================
output_dir = "output_graphs"
Path(output_dir).mkdir(exist_ok=True)

# ============================================================================
# DADOS DOS 4 CENÁRIOS - NOVOS
# ============================================================================

cenario1 = {
    'nome': 'Cenário 1: Imagem 1MB - 2 minutos',
    'tipo': 'Imagem 1MB',
    'dados': [
        {'inst': 1, 'rampup': 2,  'usuarios': 120, 'req_s': 485,   'mediana': 46000, 'p95': 68000, 'falhas': 24,   'taxa_falha': 0.06},
        {'inst': 1, 'rampup': 10, 'usuarios': 170, 'req_s': 319,   'mediana': 45000, 'p95': 61000, 'falhas': 9,    'taxa_falha': 0.03},
        {'inst': 1, 'rampup': 50, 'usuarios': 250, 'req_s': 256,   'mediana': 59000, 'p95': 86000, 'falhas': 18,   'taxa_falha': 0.07},
        {'inst': 2, 'rampup': 2,  'usuarios': 120, 'req_s': 12266, 'mediana': 610,   'p95': 1200,  'falhas': 176,  'taxa_falha': 0.01},
        {'inst': 2, 'rampup': 10, 'usuarios': 170, 'req_s': 6289,  'mediana': 1100,  'p95': 2000,  'falhas': 657,  'taxa_falha': 0.10},
        {'inst': 2, 'rampup': 50, 'usuarios': 250, 'req_s': 12372, 'mediana': 3200,  'p95': 9100,  'falhas': 1558, 'taxa_falha': 0.13},
        {'inst': 3, 'rampup': 2,  'usuarios': 120, 'req_s': 4107,  'mediana': 510,   'p95': 1600,  'falhas': 138,  'taxa_falha': 0.03},
        {'inst': 3, 'rampup': 10, 'usuarios': 170, 'req_s': 7170,  'mediana': 230,   'p95': 920,   'falhas': 265,  'taxa_falha': 0.04},
        {'inst': 3, 'rampup': 50, 'usuarios': 250, 'req_s': 12277, 'mediana': 290,   'p95': 3500,  'falhas': 1300, 'taxa_falha': 0.11},
    ]
}

cenario2 = {
    'nome': 'Cenário 2: Texto 400KB - 2 minutos',
    'tipo': 'Texto 400KB',
    'dados': [
        {'inst': 1, 'rampup': 15, 'usuarios': 570,  'req_s': 12139, 'mediana': 2900, 'p95': 4200,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 20, 'usuarios': 600,  'req_s': 10045, 'mediana': 4500, 'p95': 6500,  'falhas': 227, 'taxa_falha': 0.02},
        {'inst': 1, 'rampup': 25, 'usuarios': 635,  'req_s': 10804, 'mediana': 4500, 'p95': 6500,  'falhas': 603, 'taxa_falha': 0.06},
        {'inst': 2, 'rampup': 5,  'usuarios': 560,  'req_s': 8846,  'mediana': 1500, 'p95': 4600,  'falhas': 40,  'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 10, 'usuarios': 570,  'req_s': 9486,  'mediana': 2100, 'p95': 8900,  'falhas': 172, 'taxa_falha': 0.02},
        {'inst': 2, 'rampup': 15, 'usuarios': 580,  'req_s': 10412, 'mediana': 2400, 'p95': 9300,  'falhas': 488, 'taxa_falha': 0.05},
        {'inst': 3, 'rampup': 15, 'usuarios': 580,  'req_s': 11392, 'mediana': 3000, 'p95': 5600,  'falhas': 60,  'taxa_falha': 0.01},
        {'inst': 3, 'rampup': 25, 'usuarios': 610,  'req_s': 11966, 'mediana': 2900, 'p95': 8100,  'falhas': 552, 'taxa_falha': 0.05},
        {'inst': 3, 'rampup': 30, 'usuarios': 630,  'req_s': 124840, 'mediana': 2500, 'p95': 8500, 'falhas': 795, 'taxa_falha': 0.06},
    ]
}

cenario3 = {
    'nome': 'Cenário 3: Imagem 300KB - 2 minutos',
    'tipo': 'Imagem 300KB',
    'dados': [
        {'inst': 1, 'rampup': 15, 'usuarios': 570,  'req_s': 11957, 'mediana': 2900, 'p95': 4800,  'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 20, 'usuarios': 600,  'req_s': 11463, 'mediana': 3700, 'p95': 5900,  'falhas': 307,  'taxa_falha': 0.03},
        {'inst': 1, 'rampup': 25, 'usuarios': 650,  'req_s': 12563, 'mediana': 4000, 'p95': 5300,  'falhas': 1204, 'taxa_falha': 0.10},
        {'inst': 2, 'rampup': 15, 'usuarios': 550,  'req_s': 10906, 'mediana': 2300, 'p95': 7200,  'falhas': 51,   'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 20, 'usuarios': 600,  'req_s': 11715, 'mediana': 2900, 'p95': 8000,  'falhas': 505,  'taxa_falha': 0.04},
        {'inst': 2, 'rampup': 25, 'usuarios': 615,  'req_s': 11189, 'mediana': 2500, 'p95': 9200,  'falhas': 1065, 'taxa_falha': 0.10},
        {'inst': 3, 'rampup': 15, 'usuarios': 550,  'req_s': 12862, 'mediana': 2300, 'p95': 4300,  'falhas': 1,    'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 20, 'usuarios': 600,  'req_s': 11832, 'mediana': 2600, 'p95': 8300,  'falhas': 322,  'taxa_falha': 0.03},
        {'inst': 3, 'rampup': 25, 'usuarios': 620,  'req_s': 12572, 'mediana': 2800, 'p95': 10000, 'falhas': 865,  'taxa_falha': 0.07},
    ]
}

cenario4 = {
    'nome': 'Cenário 4: Híbrido - 2 minutos',
    'tipo': 'Híbrido',
    'dados': [
        {'inst': 1, 'rampup': 2,  'usuarios': 500, 'req_s': 4746,  'mediana': 1300,  'p95': 4200,  'falhas': 33,   'taxa_falha': 0.01},
        {'inst': 1, 'rampup': 10, 'usuarios': 600, 'req_s': 3887,  'mediana': 11000, 'p95': 21000, 'falhas': 91,   'taxa_falha': 0.02},
        {'inst': 1, 'rampup': 30, 'usuarios': 700, 'req_s': 4095,  'mediana': 19000, 'p95': 25000, 'falhas': 429,  'taxa_falha': 0.10},
        {'inst': 2, 'rampup': 2,  'usuarios': 500, 'req_s': 7423,  'mediana': 22000, 'p95': 1900,  'falhas': 246,  'taxa_falha': 0.03},
        {'inst': 2, 'rampup': 10, 'usuarios': 600, 'req_s': 8184,  'mediana': 4600,  'p95': 10000, 'falhas': 1879, 'taxa_falha': 0.10},
        {'inst': 2, 'rampup': 30, 'usuarios': 700, 'req_s': 37285, 'mediana': 4500,  'p95': 13000, 'falhas': 4312, 'taxa_falha': 0.12},
        {'inst': 3, 'rampup': 2,  'usuarios': 500, 'req_s': 4630,  'mediana': 1400,  'p95': 4700,  'falhas': 176,  'taxa_falha': 0.04},
        {'inst': 3, 'rampup': 10, 'usuarios': 600, 'req_s': 4883,  'mediana': 6600,  'p95': 25000, 'falhas': 63,   'taxa_falha': 0.01},
        {'inst': 3, 'rampup': 30, 'usuarios': 700, 'req_s': 4405,  'mediana': 26000, 'p95': 29000, 'falhas': 289,  'taxa_falha': 0.07},
    ]
}

cenarios = [cenario1, cenario2, cenario3, cenario4]

# ============================================================================
# GRÁFICOS PARA CADA CENÁRIO
# ============================================================================

for cenario in cenarios:
    nome_arquivo = cenario['nome'].replace(' ', '_').replace(':', '').replace('-', '')
    
    # Organizar dados por instâncias
    instancias = sorted(set([d['inst'] for d in cenario['dados']]))
    usuarios_por_inst = {}
    
    for inst in instancias:
        usuarios_por_inst[inst] = sorted(set([d['usuarios'] for d in cenario['dados'] if d['inst'] == inst]))
    
    # --- Gráfico 1: Tempo Mediano vs Usuários (Linha) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for inst in instancias:
        usuarios = usuarios_por_inst[inst]
        medianas = [next((d['mediana'] for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == u), None) 
                   for u in usuarios]
        ax.plot(usuarios, medianas, marker='o', linewidth=2, markersize=8, label=f'{inst} instância(s)')
    
    ax.set_xlabel('Número de usuários', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mediana de tempo de resposta (ms)', fontsize=12, fontweight='bold')
    ax.set_title(f"{cenario['nome']} - Tempo Mediano vs Usuários", fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{nome_arquivo}_tempo_vs_usuarios.png", dpi=150)
    plt.close()
    
    # --- Gráfico 2: Req/s vs Instâncias (Barras) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Encontrar os usuários únicos para este cenário
    usuarios_unicos = sorted(set([d['usuarios'] for d in cenario['dados']]))
    x = np.arange(len(instancias))
    width = 0.25
    
    for idx, usuarios in enumerate(usuarios_unicos):
        req_s_values = [next((d['req_s'] for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == usuarios), 0) 
                       for inst in instancias]
        ax.bar(x + idx*width, req_s_values, width, label=f'{usuarios} usuários')
    
    ax.set_xlabel('Número de instâncias', fontsize=12, fontweight='bold')
    ax.set_ylabel('Requisições por segundo', fontsize=12, fontweight='bold')
    ax.set_title(f"{cenario['nome']} - Requisições/s vs Instâncias", fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(instancias)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{nome_arquivo}_req_s_vs_instancias.png", dpi=150)
    plt.close()
    
    # --- Gráfico 3: Taxa de Falha (%) vs Usuários (Barras) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for idx, usuarios in enumerate(usuarios_unicos):
        taxa_falha_percent = [next((d['taxa_falha'] * 100 for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == usuarios), 0) 
                             for inst in instancias]
        ax.bar(x + idx*width, taxa_falha_percent, width, label=f'{usuarios} usuários')
    
    ax.set_xlabel('Número de instâncias', fontsize=12, fontweight='bold')
    ax.set_ylabel('Taxa de falha (%)', fontsize=12, fontweight='bold')
    ax.set_title(f"{cenario['nome']} - Taxa de Falha vs Instâncias", fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(instancias)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{nome_arquivo}_taxa_falha_vs_instancias.png", dpi=150)
    plt.close()

# ============================================================================
# GRÁFICOS COMPARATIVOS ENTRE CENÁRIOS
# ============================================================================

# Gráfico: Req/s com máxima carga - Comparação entre cenários
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(1, 4)
width = 0.2

for idx, cenario in enumerate(cenarios):
    instancias = sorted(set([d['inst'] for d in cenario['dados']]))
    # Usar máximo de usuários para cada cenário
    max_usuarios_cenario = max([d['usuarios'] for d in cenario['dados']])
    req_max = [next((d['req_s'] for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == max_usuarios_cenario), 0) 
              for inst in instancias]
    ax.bar(x + idx*width, req_max, width, label=cenario['tipo'])

ax.set_xlabel('Número de instâncias', fontsize=12, fontweight='bold')
ax.set_ylabel('Requisições por segundo', fontsize=12, fontweight='bold')
ax.set_title('Comparação: Req/s com Máxima Carga entre Cenários', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(['1', '2', '3'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f"{output_dir}/comparacao_req_s_max_carga.png", dpi=150)
plt.close()

# Gráfico: Taxa de Falha com máxima carga - Comparação entre cenários
fig, ax = plt.subplots(figsize=(12, 6))

for idx, cenario in enumerate(cenarios):
    instancias = sorted(set([d['inst'] for d in cenario['dados']]))
    max_usuarios_cenario = max([d['usuarios'] for d in cenario['dados']])
    taxa_max = [next((d['taxa_falha'] * 100 for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == max_usuarios_cenario), 0) 
               for inst in instancias]
    ax.bar(x + idx*width, taxa_max, width, label=cenario['tipo'])

ax.set_xlabel('Número de instâncias', fontsize=12, fontweight='bold')
ax.set_ylabel('Taxa de falha (%)', fontsize=12, fontweight='bold')
ax.set_title('Comparação: Taxa de Falha com Máxima Carga entre Cenários', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(['1', '2', '3'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f"{output_dir}/comparacao_taxa_falha_max_carga.png", dpi=150)
plt.close()

# Gráfico: Tempo Mediano com máxima carga - Comparação entre cenários
fig, ax = plt.subplots(figsize=(12, 6))

for idx, cenario in enumerate(cenarios):
    instancias = sorted(set([d['inst'] for d in cenario['dados']]))
    max_usuarios_cenario = max([d['usuarios'] for d in cenario['dados']])
    mediana_max = [next((d['mediana'] for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == max_usuarios_cenario), 0) 
                  for inst in instancias]
    ax.bar(x + idx*width, mediana_max, width, label=cenario['tipo'])

ax.set_xlabel('Número de instâncias', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Mediano de Resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Comparação: Tempo Mediano com Máxima Carga entre Cenários', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(['1', '2', '3'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f"{output_dir}/comparacao_mediana_max_carga.png", dpi=150)
plt.close()

print(f"✓ Gráficos gerados com sucesso na pasta '{output_dir}'!")
print(f"  - {len([f for f in os.listdir(output_dir) if f.endswith('.png')])} arquivos PNG criados")
