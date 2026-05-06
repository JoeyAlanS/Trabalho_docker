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
# DADOS DOS 4 CENÁRIOS - ATUALIZADOS
# ============================================================================

cenario1 = {
    'nome': 'Cenário 1: Imagem 1MB - 2 minutos',
    'tipo': 'Imagem 1MB',
    'dados': [
        {'inst': 1, 'rampup': 2,  'usuarios': 600,   'req_s': 6319,  'mediana': 170,   'p95': 850,    'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 10, 'usuarios': 1200,  'req_s': 11665, 'mediana': 3400,  'p95': 7900,   'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 50, 'usuarios': 1500,  'req_s': 11479, 'mediana': 5000,  'p95': 13000,  'falhas': 1252, 'taxa_falha': 0.11},
        {'inst': 2, 'rampup': 2,  'usuarios': 570,   'req_s': 2484,  'mediana': 2700,  'p95': 6100,   'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 10, 'usuarios': 700,   'req_s': 2984,  'mediana': 8600,  'p95': 35000,  'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 50, 'usuarios': 900,   'req_s': 33844, 'mediana': 2600,  'p95': 15000,  'falhas': 3486, 'taxa_falha': 0.10},
        {'inst': 3, 'rampup': 2,  'usuarios': 520,   'req_s': 4685,  'mediana': 180,   'p95': 720,    'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 10, 'usuarios': 600,   'req_s': 4591,  'mediana': 7400,  'p95': 23000,  'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 40, 'usuarios': 1000,  'req_s': 39544, 'mediana': 4600,  'p95': 18000,  'falhas': 4787, 'taxa_falha': 0.12},
    ]
}

cenario2 = {
    'nome': 'Cenário 2: Texto 400KB - 2 minutos',
    'tipo': 'Texto 400KB',
    'dados': [
        {'inst': 1, 'rampup': 10, 'usuarios': 520,  'req_s': 8849,  'mediana': 3200, 'p95': 7400,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 15, 'usuarios': 570,  'req_s': 12139, 'mediana': 2900, 'p95': 4200,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 25, 'usuarios': 635,  'req_s': 10804, 'mediana': 4500, 'p95': 6500,  'falhas': 603, 'taxa_falha': 0.06},
        {'inst': 2, 'rampup': 5,  'usuarios': 510,  'req_s': 8999,  'mediana': 1700, 'p95': 4200,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 10, 'usuarios': 520,  'req_s': 8182,  'mediana': 2300, 'p95': 1000,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 15, 'usuarios': 580,  'req_s': 10412, 'mediana': 2400, 'p95': 9300,  'falhas': 488, 'taxa_falha': 0.05},
        {'inst': 3, 'rampup': 5,  'usuarios': 515,  'req_s': 8296,  'mediana': 1800, 'p95': 5400,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 8,  'usuarios': 520,  'req_s': 8798,  'mediana': 2300, 'p95': 9000,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 10, 'usuarios': 580,  'req_s': 9009,  'mediana': 3200, 'p95': 9200,  'falhas': 795, 'taxa_falha': 0.05},
    ]
}

cenario3 = {
    'nome': 'Cenário 3: Imagem 300KB - 2 minutos',
    'tipo': 'Imagem 300KB',
    'dados': [
        {'inst': 1, 'rampup': 5,  'usuarios': 540,  'req_s': 9159,  'mediana': 1900, 'p95': 3900,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 10, 'usuarios': 560,  'req_s': 10569, 'mediana': 3300, 'p95': 4500,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 20, 'usuarios': 640,  'req_s': 10269, 'mediana': 4300, 'p95': 6900,  'falhas': 697, 'taxa_falha': 0.07},
        {'inst': 2, 'rampup': 5,  'usuarios': 520,  'req_s': 8615,  'mediana': 1300, 'p95': 6600,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 8,  'usuarios': 523,  'req_s': 9191,  'mediana': 1900, 'p95': 8100,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 12, 'usuarios': 575,  'req_s': 8702,  'mediana': 2700, 'p95': 1100,  'falhas': 538, 'taxa_falha': 0.06},
        {'inst': 3, 'rampup': 10, 'usuarios': 520,  'req_s': 11009, 'mediana': 2600, 'p95': 3800,  'falhas': 0,   'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 15, 'usuarios': 550,  'req_s': 12862, 'mediana': 2300, 'p95': 4300,  'falhas': 1,   'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 25, 'usuarios': 620,  'req_s': 12572, 'mediana': 2800, 'p95': 10000, 'falhas': 865, 'taxa_falha': 0.07},
    ]
}

cenario4 = {
    'nome': 'Cenário 4: Híbrido - 2 minutos',
    'tipo': 'Híbrido',
    'dados': [
        {'inst': 1, 'rampup': 2,  'usuarios': 800,   'req_s': 7922,  'mediana': 170,  'p95': 1100,  'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 10, 'usuarios': 1000,  'req_s': 12096, 'mediana': 4200, 'p95': 8500,  'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 1, 'rampup': 30, 'usuarios': 1250,  'req_s': 14095, 'mediana': 4500, 'p95': 13000, 'falhas': 704,  'taxa_falha': 0.05},
        {'inst': 2, 'rampup': 2,  'usuarios': 1000,  'req_s': 7952,  'mediana': 250,  'p95': 1100,  'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 10, 'usuarios': 1200,  'req_s': 12558, 'mediana': 2600, 'p95': 10000, 'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 2, 'rampup': 30, 'usuarios': 1400,  'req_s': 37285, 'mediana': 4500, 'p95': 13000, 'falhas': 745,  'taxa_falha': 0.02},
        {'inst': 3, 'rampup': 2,  'usuarios': 1200,  'req_s': 7969,  'mediana': 230,  'p95': 1100,  'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 10, 'usuarios': 1560,  'req_s': 11407, 'mediana': 2600, 'p95': 19000, 'falhas': 0,    'taxa_falha': 0.00},
        {'inst': 3, 'rampup': 30, 'usuarios': 1700,  'req_s': 24405, 'mediana': 1952, 'p95': 29000, 'falhas': 1952, 'taxa_falha': 0.08},
    ]
}

cenarios = [cenario1, cenario2, cenario3, cenario4]

# ============================================================================
# GRÁFICOS PARA CADA CENÁRIO - NOVOS GRÁFICOS
# ============================================================================

for cenario in cenarios:
    nome_arquivo = cenario['nome'].replace(' ', '_').replace(':', '').replace('-', '').replace('ó', 'o').replace('á', 'a')
    
    # Organizar dados por instâncias
    instancias = sorted(set([d['inst'] for d in cenario['dados']]))
    usuarios_por_inst = {}
    
    for inst in instancias:
        usuarios_por_inst[inst] = sorted(set([d['usuarios'] for d in cenario['dados'] if d['inst'] == inst]))
    
    # --- Gráfico 1: P95 vs Usuários (Linha) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for inst in instancias:
        usuarios = usuarios_por_inst[inst]
        p95_values = [next((d['p95'] for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == u), None) 
                     for u in usuarios]
        ax.plot(usuarios, p95_values, marker='o', linewidth=2, markersize=8, label=f'{inst} instância(s)')
    
    ax.set_xlabel('Número de usuários', fontsize=12, fontweight='bold')
    ax.set_ylabel('P95 de tempo de resposta (ms)', fontsize=12, fontweight='bold')
    ax.set_title(f"{cenario['nome']} - P95 vs Usuários", fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{nome_arquivo}_p95_vs_usuarios.png", dpi=150)
    plt.close()
    
    # --- Gráfico 2: Taxa de Falha vs Usuários (Linha) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for inst in instancias:
        usuarios = usuarios_por_inst[inst]
        taxa_falha = [next((d['taxa_falha'] * 100 for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == u), None) 
                     for u in usuarios]
        ax.plot(usuarios, taxa_falha, marker='s', linewidth=2, markersize=8, label=f'{inst} instância(s)')
    
    ax.set_xlabel('Número de usuários', fontsize=12, fontweight='bold')
    ax.set_ylabel('Taxa de Falha (%)', fontsize=12, fontweight='bold')
    ax.set_title(f"{cenario['nome']} - Taxa de Falha vs Usuários", fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{nome_arquivo}_taxa_falha_vs_usuarios.png", dpi=150)
    plt.close()
    
    # --- Gráfico 3: P95 vs Instâncias (Barras) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    usuarios_unicos = sorted(set([d['usuarios'] for d in cenario['dados']]))
    x = np.arange(len(instancias))
    width = 0.25
    
    for idx, usuarios in enumerate(usuarios_unicos):
        p95_values = [next((d['p95'] for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == usuarios), 0) 
                     for inst in instancias]
        ax.bar(x + idx*width, p95_values, width, label=f'{usuarios} usuários')
    
    ax.set_xlabel('Número de instâncias', fontsize=12, fontweight='bold')
    ax.set_ylabel('P95 de tempo de resposta (ms)', fontsize=12, fontweight='bold')
    ax.set_title(f"{cenario['nome']} - P95 vs Instâncias", fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(instancias)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{nome_arquivo}_p95_vs_instancias.png", dpi=150)
    plt.close()
    
    # --- Gráfico 4: Taxa de Falha vs Instâncias (Barras) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for idx, usuarios in enumerate(usuarios_unicos):
        taxa_falha_percent = [next((d['taxa_falha'] * 100 for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == usuarios), 0) 
                             for inst in instancias]
        ax.bar(x + idx*width, taxa_falha_percent, width, label=f'{usuarios} usuários')
    
    ax.set_xlabel('Número de instâncias', fontsize=12, fontweight='bold')
    ax.set_ylabel('Taxa de Falha (%)', fontsize=12, fontweight='bold')
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

# Gráfico: P95 com máxima carga - Comparação entre cenários
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(1, 4)
width = 0.2

for idx, cenario in enumerate(cenarios):
    instancias = sorted(set([d['inst'] for d in cenario['dados']]))
    max_usuarios_cenario = max([d['usuarios'] for d in cenario['dados']])
    p95_max = [next((d['p95'] for d in cenario['dados'] if d['inst'] == inst and d['usuarios'] == max_usuarios_cenario), 0) 
              for inst in instancias]
    ax.bar(x + idx*width, p95_max, width, label=cenario['tipo'])

ax.set_xlabel('Número de instâncias', fontsize=12, fontweight='bold')
ax.set_ylabel('P95 de tempo de resposta (ms)', fontsize=12, fontweight='bold')
ax.set_title('Comparação: P95 com Máxima Carga entre Cenários', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(['1', '2', '3'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f"{output_dir}/comparacao_p95_max_carga.png", dpi=150)
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

print(f"✓ Gráficos gerados com sucesso na pasta '{output_dir}'!")
print(f"  - {len([f for f in os.listdir(output_dir) if f.endswith('.png')])} arquivos PNG criados")
print(f"  - Gráficos novos: P95 vs Usuários, Taxa de Falha vs Usuários")
print(f"  - Gráficos de barras: P95 vs Instâncias, Taxa de Falha vs Instâncias")
