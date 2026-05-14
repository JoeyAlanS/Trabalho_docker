from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt

# Marcadores por linha (círculo, quadrado, losango, etc.) — evitamos ^ e v (triângulos).
MARKERS_LINE = ["o", "s", "D", "p", "P", "*", "X", "h", "8", "H", "d", "+", "x", "1", "2", "3", "4"]

# ============================================================================
# PASTA DE SAÍDA
# ============================================================================
OUTPUT_DIR = "output_graphs"
Path(OUTPUT_DIR).mkdir(exist_ok=True)


# ============================================================================
# DADOS — SUBSTITUA APÓS CADA BATERIA DE TESTES
# ============================================================================

cenario_python_cache = {
    "nome": "Cenário: Python + Redis (com cache)",
    "tipo": "Python + cache",
    "dados": [
        {"usuarios": 100, "req_s": 126133, "mediana": 130, "p95": 200, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 128455, "mediana": 220, "p95": 1300, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 132082, "mediana": 240, "p95": 3300, "falhas": 8, "taxa_falha": 0.0},
    ],
}

cenario_python_no_cache = {
    "nome": "Cenário: Python sem cache",
    "tipo": "Python sem cache",
    "dados": [
        {"usuarios": 100, "req_s": 5350, "mediana": 5200, "p95": 8400, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 4494, "mediana": 9300, "p95": 16000, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 6844, "mediana": 9300, "p95": 41000, "falhas": 451, "taxa_falha": 0.07},
    ],
}

cenario_ruby_cache = {
    "nome": "Cenário: Ruby + Redis (com cache)",
    "tipo": "Ruby + cache",
    "dados": [
        {"usuarios": 100, "req_s": 132922, "mediana": 160, "p95": 560, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 139673, "mediana": 160, "p95": 610, "falhas": 2445, "taxa_falha": 0.02},
        {"usuarios": 600, "req_s": 144886, "mediana": 170, "p95": 10000, "falhas": 8881, "taxa_falha": 0.06},
    ],
}

cenario_ruby_no_cache = {
    "nome": "Cenário: Ruby sem cache",
    "tipo": "Ruby sem cache",
    "dados": [
        {"usuarios": 100, "req_s": 9741, "mediana": 2400, "p95": 4700, "falhas": 51, "taxa_falha": 0.01},
        {"usuarios": 200, "req_s": 12716, "mediana": 2800, "p95": 10000, "falhas": 2671, "taxa_falha": 0.21},
        {"usuarios": 600, "req_s": 16254, "mediana": 3400, "p95": 15000, "falhas": 5827, "taxa_falha": 0.36},
    ],
}

# Agrupamentos solicitados
CENARIOS_COM_CACHE = [cenario_python_cache, cenario_ruby_cache]
CENARIOS_SEM_CACHE = [cenario_python_no_cache, cenario_ruby_no_cache]
TODOS_CENARIOS = [cenario_python_cache, cenario_ruby_cache, cenario_python_no_cache, cenario_ruby_no_cache]


def _plot_metrica_vs_usuarios(cenarios: list[dict], metrica_chave: str, eixo_y_label: str, titulo: str, nome_arquivo: str, converter_pct: bool = False) -> None:
    """Gera um gráfico de linha comparando uma métrica específica pela quantidade de usuários."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    todos_usuarios = set()
    
    for idx, cenario in enumerate(cenarios):
        dados = cenario["dados"]
        usuarios = sorted({d["usuarios"] for d in dados})
        todos_usuarios.update(usuarios)
        
        valores = []
        for u in usuarios:
            val = next((d[metrica_chave] for d in dados if d["usuarios"] == u), 0)
            if converter_pct:
                val *= 100
            valores.append(val)
            
        mk = MARKERS_LINE[idx % len(MARKERS_LINE)]
        ax.plot(
            usuarios,
            valores,
            marker=mk,
            linewidth=2.5,
            markersize=9,
            label=cenario['tipo']
        )
        
    ax.set_xlabel("Quantidade de Usuários", fontsize=12, fontweight="bold")
    ax.set_ylabel(eixo_y_label, fontsize=12, fontweight="bold")
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xticks(sorted(list(todos_usuarios))) # Força o eixo X a mostrar exatamente 100, 200, 600
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.4, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{nome_arquivo}.png", dpi=150)
    plt.close()


def _gerar_readme(graficos_gerados: list[dict]) -> None:
    """Gera o arquivo README.md com as imagens renderizadas organizadas por categorias."""
    caminho_readme = os.path.join(OUTPUT_DIR, "README.md")
    
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("# Resultados dos Testes de Carga (Link Extractor)\n\n")
        f.write("Abaixo estão os gráficos comparativos considerando a **Quantidade de Usuários**.\n\n")
        
        for secao in graficos_gerados:
            f.write(f"## {secao['grupo']}\n\n")
            for titulo, arquivo in secao['graficos']:
                f.write(f"### {titulo}\n")
                f.write(f"![{titulo}]({arquivo}.png)\n\n")
            f.write("---\n\n")


def main() -> None:
    print("Gerando gráficos...")
    
    configuracoes_graficos = []

    # ==========================================
    # 1. Gráficos COM CACHE
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_COM_CACHE, "taxa_falha", "Taxa de Falha (%)", "Taxa de Falha vs Usuários (Com Cache)", "falha_com_cache", converter_pct=True)
    _plot_metrica_vs_usuarios(CENARIOS_COM_CACHE, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (Com Cache)", "p95_com_cache")
    _plot_metrica_vs_usuarios(CENARIOS_COM_CACHE, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (Com Cache)", "rps_com_cache")
    
    configuracoes_graficos.append({
        "grupo": "1. Cenários COM Cache (Python vs Ruby)",
        "graficos": [
            ("Taxa de Falha", "falha_com_cache"),
            ("Tempo de Resposta (P95)", "p95_com_cache"),
            ("Requisições por Segundo (RPS)", "rps_com_cache")
        ]
    })

    # ==========================================
    # 2. Gráficos SEM CACHE
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_SEM_CACHE, "taxa_falha", "Taxa de Falha (%)", "Taxa de Falha vs Usuários (Sem Cache)", "falha_sem_cache", converter_pct=True)
    _plot_metrica_vs_usuarios(CENARIOS_SEM_CACHE, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (Sem Cache)", "p95_sem_cache")
    _plot_metrica_vs_usuarios(CENARIOS_SEM_CACHE, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (Sem Cache)", "rps_sem_cache")

    configuracoes_graficos.append({
        "grupo": "2. Cenários SEM Cache (Python vs Ruby)",
        "graficos": [
            ("Taxa de Falha", "falha_sem_cache"),
            ("Tempo de Resposta (P95)", "p95_sem_cache"),
            ("Requisições por Segundo (RPS)", "rps_sem_cache")
        ]
    })

    # ==========================================
    # 3. Gráficos GERAIS (Todos Juntos)
    # ==========================================
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "taxa_falha", "Taxa de Falha (%)", "Visão Geral: Taxa de Falha vs Usuários", "falha_geral", converter_pct=True)
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "p95", "Tempo de Resposta P95 (ms)", "Visão Geral: P95 vs Usuários", "p95_geral")
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "req_s", "Requisições por Segundo (RPS)", "Visão Geral: RPS vs Usuários", "rps_geral")

    configuracoes_graficos.append({
        "grupo": "3. Visão Geral (Com e Sem Cache)",
        "graficos": [
            ("Taxa de Falha", "falha_geral"),
            ("Tempo de Resposta (P95)", "p95_geral"),
            ("Requisições por Segundo (RPS)", "rps_geral")
        ]
    })

    # Gerar o README
    _gerar_readme(configuracoes_graficos)

    print(f"✅ Concluído! Foram gerados 9 gráficos na pasta '{OUTPUT_DIR}'.")
    print(f"O arquivo README.md foi criado e organizado com todas as imagens.")


if __name__ == "__main__":
    main()