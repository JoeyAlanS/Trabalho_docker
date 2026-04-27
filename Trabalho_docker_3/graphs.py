import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# DADOS DOS CENÁRIOS
# ============================================================================

# Cenário 1: Imagem 1MB - 2 minutos - Ramp up 2,10,50
cenario1 = {
    'nome': 'Cenário 1: Imagem 1MB',
    'dados': [
        {'inst': 1, 'usuarios': 10,   'req_s': 55,    'mediana': 180,  'p95': 390,   'falha': 0},
        {'inst': 1, 'usuarios': 100,  'req_s': 5436,  'mediana': 120,  'p95': 320,   'falha': 0},
        {'inst': 1, 'usuarios': 1000, 'req_s': 27871, 'mediana': 2800, 'p95': 3600,  'falha': 9308},
        {'inst': 2, 'usuarios': 10,   'req_s': 387,   'mediana': 190,  'p95': 570,   'falha': 0},
        {'inst': 2, 'usuarios': 100,  'req_s': 5282,  'mediana': 160,  'p95': 450,   'falha': 0},
        {'inst': 2, 'usuarios': 1000, 'req_s': 38743, 'mediana': 450,  'p95': 2400,  'falha': 28160},
        {'inst': 3, 'usuarios': 10,   'req_s': 503,   'mediana': 250,  'p95': 700,   'falha': 0},
        {'inst': 3, 'usuarios': 100,  'req_s': 5387,  'mediana': 160,  'p95': 470,   'falha': 0},
        {'inst': 3, 'usuarios': 1000, 'req_s': 36491, 'mediana': 610,  'p95': 3000,  'falha': 27001},
    ]
}

# Cenário 2: Texto 400KB - 2 minutos - Ramp up 2,10,50
cenario2 = {
    'nome': 'Cenário 2: Texto 400KB',
    'dados': [
        {'inst': 1, 'usuarios': 10,   'req_s': 533,   'mediana': 170,  'p95': 390,   'falha': 0},
        {'inst': 1, 'usuarios': 100,  'req_s': 5429,  'mediana': 120,  'p95': 320,   'falha': 0},
        {'inst': 1, 'usuarios': 1000, 'req_s': 26355, 'mediana': 2800, 'p95': 5100,  'falha': 10199},
        {'inst': 2, 'usuarios': 10,   'req_s': 541,   'mediana': 170,  'p95': 370,   'falha': 0},
        {'inst': 2, 'usuarios': 100,  'req_s': 5383,  'mediana': 130,  'p95': 390,   'falha': 0},
        {'inst': 2, 'usuarios': 1000, 'req_s': 26031, 'mediana': 2800, 'p95': 5300,  'falha': 10504},
        {'inst': 3, 'usuarios': 10,   'req_s': 518,   'mediana': 250,  'p95': 660,   'falha': 0},
        {'inst': 3, 'usuarios': 100,  'req_s': 5232,  'mediana': 170,  'p95': 480,   'falha': 0},
        {'inst': 3, 'usuarios': 1000, 'req_s': 36112, 'mediana': 560,  'p95': 3200,  'falha': 26816},
    ]
}

# Cenário 3: Imagem 300KB - 2 minutos - Ramp up 2,10,50
cenario3 = {
    'nome': 'Cenário 3: Imagem 300KB',
    'dados': [
        {'inst': 1, 'usuarios': 10,   'req_s': 548,   'mediana': 160,  'p95': 370,   'falha': 0},
        {'inst': 1, 'usuarios': 100,  'req_s': 5465,  'mediana': 120,  'p95': 300,   'falha': 0},
        {'inst': 1, 'usuarios': 1000, 'req_s': 27901, 'mediana': 2800, 'p95': 4100,  'falha': 9777},
        {'inst': 2, 'usuarios': 10,   'req_s': 554,   'mediana': 160,  'p95': 350,   'falha': 0},
        {'inst': 2, 'usuarios': 100,  'req_s': 5307,  'mediana': 160,  'p95': 400,   'falha': 0},
        {'inst': 2, 'usuarios': 1000, 'req_s': 26846, 'mediana': 38,   'p95': 5600,  'falha': 14478},
        {'inst': 3, 'usuarios': 10,   'req_s': 513,   'mediana': 250,  'p95': 640,   'falha': 0},
        {'inst': 3, 'usuarios': 100,  'req_s': 5236,  'mediana': 180,  'p95': 570,   'falha': 0},
        {'inst': 3, 'usuarios': 1000, 'req_s': 36632, 'mediana': 620,  'p95': 2900,  'falha': 26747},
    ]
}

cenarios = [cenario1, cenario2, cenario3]

# ============================================================================
# FUNÇÃO AUXILIAR
# ============================================================================

def extrair_dados_por_instancia(cenario):
    """Extrai dados organizados por número de instâncias"""
    resultado = {}
    for ponto in cenario['dados']:
        inst = ponto['inst']
        if inst not in resultado:
            resultado[inst] = {'usuarios': [], 'req_s': [], 'mediana': [], 'p95': [], 'falha': []}
        resultado[inst]['usuarios'].append(ponto['usuarios'])
        resultado[inst]['req_s'].append(ponto['req_s'])
        resultado[inst]['mediana'].append(ponto['mediana'])
        resultado[inst]['p95'].append(ponto['p95'])
        resultado[inst]['falha'].append(ponto['falha'])
    return resultado

# ============================================================================
# GRÁFICOS PARA CADA CENÁRIO
# ============================================================================

for cenario in cenarios:
    dados_por_inst = extrair_dados_por_instancia(cenario)
    
    # --- Gráfico 1: Tempo Mediano vs Usuários (Barras) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    usuarios_unicos = sorted(set([d['usuarios'] for d in cenario['dados']]))
    instancias_uniques = sorted(dados_por_inst.keys())
    x = np.arange(len(usuarios_unicos))
    width = 0.25
    
    for idx, inst in enumerate(instancias_uniques):
        medianas = dados_por_inst[inst]['mediana']
        ax.bar(x + idx*width, medianas, width, label=f'{inst} instância(s)')
    
    ax.set_xlabel('Número de usuários', fontsize=12)
    ax.set_ylabel('Mediana de tempo de resposta (ms)', fontsize=12)
    ax.set_title(f"{cenario['nome']} - Tempo vs Usuários", fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(usuarios_unicos)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{cenario['nome'].replace(' ', '_').replace(':', '')}_tempo_vs_usuarios.png", dpi=150)
    plt.close()
    
    # --- Gráfico 2: Req/s vs Instâncias (Barras) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(instancias_uniques))
    width = 0.25
    
    for idx, usuarios in enumerate(usuarios_unicos):
        req_s_values = []
        for inst in instancias_uniques:
            for ponto in cenario['dados']:
                if ponto['inst'] == inst and ponto['usuarios'] == usuarios:
                    req_s_values.append(ponto['req_s'])
                    break
        ax.bar(x + idx*width, req_s_values, width, label=f'{usuarios} usuários')
    
    ax.set_xlabel('Número de instâncias', fontsize=12)
    ax.set_ylabel('Requisições por segundo', fontsize=12)
    ax.set_title(f"{cenario['nome']} - Req/s vs Instâncias", fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(instancias_uniques)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{cenario['nome'].replace(' ', '_').replace(':', '')}_req_s_vs_instancias.png", dpi=150)
    plt.close()
    
    # --- Gráfico 3: P95 vs Usuários (Barras) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(usuarios_unicos))
    
    for idx, inst in enumerate(instancias_uniques):
        p95_values = dados_por_inst[inst]['p95']
        ax.bar(x + idx*width, p95_values, width, label=f'{inst} instância(s)')
    
    ax.set_xlabel('Número de usuários', fontsize=12)
    ax.set_ylabel('P95 de tempo de resposta (ms)', fontsize=12)
    ax.set_title(f"{cenario['nome']} - P95 vs Usuários", fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(usuarios_unicos)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{cenario['nome'].replace(' ', '_').replace(':', '')}_p95_vs_usuarios.png", dpi=150)
    plt.close()
    
    # --- Gráfico 4: Falhas vs Usuários (Barras) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(usuarios_unicos))
    
    for idx, inst in enumerate(instancias_uniques):
        falhas = dados_por_inst[inst]['falha']
        ax.bar(x + idx*width, falhas, width, label=f'{inst} instância(s)')
    
    ax.set_xlabel('Número de usuários', fontsize=12)
    ax.set_ylabel('Falhas por segundo', fontsize=12)
    ax.set_title(f"{cenario['nome']} - Falhas vs Usuários", fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(usuarios_unicos)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{cenario['nome'].replace(' ', '_').replace(':', '')}_falhas_vs_usuarios.png", dpi=150)
    plt.close()

# ============================================================================
# GRÁFICOS COMPARATIVOS ENTRE CENÁRIOS
# ============================================================================

# Gráfico: Req/s com 1000 usuários - Comparação entre cenários
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(1, 4)
width = 0.25
for idx, cenario in enumerate(cenarios):
    dados_por_inst = extrair_dados_por_instancia(cenario)
    # Pegar dados com 1000 usuários
    req_1000 = [dados_por_inst[i]['req_s'][2] for i in sorted(dados_por_inst.keys())]
    ax.bar(x + idx*width, req_1000, width, label=cenario['nome'].split(':')[1].strip())

ax.set_xlabel('Número de instâncias', fontsize=12)
ax.set_ylabel('Requisições por segundo', fontsize=12)
ax.set_title('Comparação de Req/s com 1000 usuários', fontsize=14, fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels(['1', '2', '3'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('comparacao_req_s_1000usuarios.png', dpi=150)
plt.close()

# Gráfico: Falhas com 1000 usuários - Comparação entre cenários
fig, ax = plt.subplots(figsize=(10, 6))
for idx, cenario in enumerate(cenarios):
    dados_por_inst = extrair_dados_por_instancia(cenario)
    # Pegar dados com 1000 usuários
    falha_1000 = [dados_por_inst[i]['falha'][2] for i in sorted(dados_por_inst.keys())]
    ax.bar(x + idx*width, falha_1000, width, label=cenario['nome'].split(':')[1].strip())

ax.set_xlabel('Número de instâncias', fontsize=12)
ax.set_ylabel('Falhas por segundo', fontsize=12)
ax.set_title('Comparação de Falhas com 1000 usuários', fontsize=14, fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels(['1', '2', '3'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('comparacao_falhas_1000usuarios.png', dpi=150)
plt.close()

print("✓ Gráficos gerados com sucesso!")