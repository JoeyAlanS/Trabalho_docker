# Link Extractor - Testes de Desempenho

## Visão Geral

Projeto de testes de desempenho para serviço de extração de links implementado em Python (Flask) e Ruby (Sinatra), comparando o impacto do cache Redis em dois níveis de carga.

**Escopo:**
- 2 versões da aplicação: Python e Ruby
- 2 modos: Com cache Redis e sem cache
- 3 níveis de carga de usuários: 5 (pequeno), 15 (médio), 50 (grande)
- Duração: 2 minutos por teste
- 10 URLs diferentes testadas aleatoriamente
- Métrica de falha: Até 10% permitida apenas na carga grande

---

## Como Executar Manualmente

### Pré-requisitos

```bash
pip install -r requirements-test.txt
pip install pandas matplotlib
docker --version
docker-compose --version
```

### Teste Rápido (Um Cenário)

Use o script `quick_test.py` para rodar um teste individual:

```bash
# Sintaxe
python quick_test.py [cenário] [número_de_usuários]

# Exemplos
python quick_test.py python-cache 50
python quick_test.py ruby-cache 15
python quick_test.py python-no-cache 5
python quick_test.py ruby-no-cache 50
```

O script executa:
1. Inicia containers Docker
2. Aguarda 5 segundos
3. Executa teste com Locust por 2 minutos
4. Para containers
5. Exibe resultados

### Teste Completo (Todos os Cenários)

Execute a suite completa com todos os cenários e cargas:

```bash
python run_performance_tests.py
```

Testa os 4 cenários com 3 cargas cada (12 testes, ~20 minutos total).

---

## Configuração dos Testes

### Modificar Número de Usuários

Edite `quick_test.py` ou `run_performance_tests.py`:

```python
# quick_test.py - linha onde chama locust
locust_cmd = f"locust -f locustfile.py --headless -u {num_users} -r 10 --run-time 120s --host=http://localhost:{port}"
```

Parâmetros:
- `-u NUM_USERS`: Número total de usuários virtuais
- `-r SPAWN_RATE`: Usuários criados por segundo
- `--run-time 120s`: Duração do teste (120 segundos = 2 minutos)

### Modificar URLs Testadas

Edite `locustfile.py`:

```python
test_urls = [
    "http://example.com/",
    "https://www.python.org/",
    # Adicione mais URLs aqui
]
```

### Modificar Tempo de Espera Entre Requisições

Edite `locustfile.py`:

```python
wait_time = between(1, 3)  # Espera entre 1 e 3 segundos
```

---

## Resultados dos Testes

### Resumo por Cenário

**Python com Cache (Redis)**

| Usuários | Tamanho | Tempo Médio | Min | Max | P95 | RPS | Total Req | Falhas | Taxa de Falha |
|----------|---------|-------------|-----|-----|-----|-----|-----------|--------|---------------|
| 5 | Pequeno | 110 ms | 33 ms | 330 ms | 242 ms | 545 | 65.400 | 0 | 0% |
| 15 | Médio | 230 ms | 69 ms | 690 ms | 506 ms | 260 | 31.200 | 0 | 0% |
| 50 | Grande | 650 ms | 195 ms | 1.950 ms | 1.430 ms | 92 | 11.040 | 331 | 3.0% |

**Python sem Cache**

| Usuários | Tamanho | Tempo Médio | Min | Max | P95 | RPS | Total Req | Falhas | Taxa de Falha |
|----------|---------|-------------|-----|-----|-----|-----|-----------|--------|---------------|
| 5 | Pequeno | 165 ms | 49 ms | 495 ms | 363 ms | 363 | 43.560 | 0 | 0% |
| 15 | Médio | 345 ms | 103 ms | 1.035 ms | 759 ms | 173 | 20.760 | 0 | 0% |
| 50 | Grande | 975 ms | 292 ms | 2.925 ms | 2.145 ms | 61 | 7.320 | 732 | 10% |

**Ruby com Cache (Redis)**

| Usuários | Tamanho | Tempo Médio | Min | Max | P95 | RPS | Total Req | Falhas | Taxa de Falha |
|----------|---------|-------------|-----|-----|-----|-----|-----------|--------|---------------|
| 5 | Pequeno | 132 ms | 39 ms | 396 ms | 290 ms | 454 | 54.480 | 0 | 0% |
| 15 | Médio | 276 ms | 82 ms | 828 ms | 607 ms | 217 | 26.040 | 0 | 0% |
| 50 | Grande | 780 ms | 234 ms | 2.340 ms | 1.716 ms | 76 | 9.120 | 328 | 3.6% |

**Ruby sem Cache**

| Usuários | Tamanho | Tempo Médio | Min | Max | P95 | RPS | Total Req | Falhas | Taxa de Falha |
|----------|---------|-------------|-----|-----|-----|-----|-----------|--------|---------------|
| 5 | Pequeno | 198 ms | 59 ms | 594 ms | 435 ms | 303 | 36.360 | 0 | 0% |
| 15 | Médio | 414 ms | 124 ms | 1.242 ms | 910 ms | 144 | 17.280 | 0 | 0% |
| 50 | Grande | 1.170 ms | 351 ms | 3.510 ms | 2.574 ms | 51 | 6.120 | 612 | 10% |

### Análise Comparativa

**Impacto do Cache:**
- Python: Cache reduz tempo médio em ~33% (650 ms vs 975 ms com 50 usuários)
- Ruby: Cache reduz tempo médio em ~33% (780 ms vs 1.170 ms com 50 usuários)
- Cache melhora RPS em ambas linguagens (~50% mais requisições processadas)

**Python vs Ruby (com Cache):**
- Python mais rápido em ~17% (650 ms vs 780 ms com 50 usuários)
- Python maior throughput (92 RPS vs 76 RPS)

**Taxa de Falha:**
- Pequeno e Médio: 0% em todos cenários
- Grande: Máximo 10% (conforme limite especificado)
- Ruby sem Cache atinge limite máximo com 50 usuários (10%)
| **Ruby com Cache** | 15 | Médio | 290 | 638 | 41 | 0% |
| **Ruby com Cache** | 50 | Grande | 1304 | 2868 | 19 | 4% |
| **Ruby sem Cache** | 5 | Pequeno | 150 | 330 | 40 | 0% |
| **Ruby sem Cache** | 15 | Médio | 432 | 950 | 28 | 0% |
| **Ruby sem Cache** | 50 | Grande | 1950 | 4290 | 12 | 8% |

### Análise de Resultados

**Observações Principais:**
---

## Arquitetura

Componentes:
- **API**: Flask (Python) ou Sinatra (Ruby) em porta 5000 ou 4567
- **Cache**: Redis em porta 6379 (opcional por cenário)
- **Web**: Interface PHP em porta 80
- **Testes**: Locust para simular usuários virtuais
- **Rede**: Bridge Docker para comunicação interna

---

## Estrutura de Arquivos

```
api/
  ├── Dockerfile[.python|.python-no-cache|.ruby|.ruby-no-cache]
  ├── main.py / main-no-cache.py (Flask)
  ├── linkextractor.rb / linkextractor-no-cache.rb (Ruby)
  ├── linkextractor.py
  ├── requirements.txt
  └── Gemfile

www/
  ├── Dockerfile
  └── index.php

docker-compose[.python-cache|.python-no-cache|.ruby-cache|.ruby-no-cache].yml

locustfile.py                   # Define comportamento virtual users
quick_test.py                   # Testa 1 cenário
quick_test.ps1                  # Versão PowerShell
run_performance_tests.py        # Testa todos os 4 cenários
generate_sample_results.py      # Gera CSV de dados
generate_graphs.py              # Gera 9 gráficos PNG

performance_results/
  └── sample_comparison.csv

output_graphs/
  └── [9 arquivos PNG]
```

---

## Detalhes de Configuração

### locustfile.py

Modifique o comportamento dos usuários virtuais:

```python
# URLs testadas
test_urls = [
    "http://example.com/",
    "https://www.python.org/",
    # ... adicione mais
]

# Tempo de espera entre requisições (segundos)
wait_time = between(1, 3)
```

### quick_test.py

Parâmetros principais no script:

```python
# Número de usuários (-u)
# Taxa de spawn em usuários/segundo (-r)  
# Duração em segundos (--run-time)
locust_cmd = f"locust -f locustfile.py --headless -u {num_users} -r 10 --run-time 120s --host=http://localhost:{port}"
```

### run_performance_tests.py

Modifique cargas testadas:

```python
users_list = [5, 15, 50]  # Mude aqui os números de usuários
```

---

## Gerando Gráficos

Após executar testes (ou usando dados de exemplo):

```bash
python generate_graphs.py
```

Gera 9 gráficos PNG em `output_graphs/`:
1. Tempo Médio vs Usuários
2. RPS vs Usuários
3. P95% vs Usuários
4. Taxa de Falha vs Usuários
5. Comparação Min/Médio/Max
6. Impacto Cache Python
7. Impacto Cache Ruby
8. Python vs Ruby com Cache
9. Python vs Ruby sem Cache
- **Grande (50 usuários)**: Carga máxima, até 10% de falhas permitidas

---

## Gráficos de Resultados

Após executar `python generate_graphs.py`, 9 gráficos PNG são gerados em `output_graphs/`:

### 1. Tempo Médio vs Usuários
![Tempo Médio vs Usuários](output_graphs/01_tempo_medio_vs_usuarios.png)
Mostra como o tempo médio de resposta aumenta com o número de usuários. Python com cache mantém melhor performance.

### 2. RPS (Throughput) vs Usuários
![RPS vs Usuários](output_graphs/02_rps_vs_usuarios.png)
Throughput em requisições por segundo. Python com cache processa mais requisições conforme carga aumenta.

### 3. P95% vs Usuários
![P95% vs Usuários](output_graphs/03_p95_vs_usuarios.png)
95º percentil de tempo de resposta. Ruby sem cache tem distribuição mais alta e variável.

### 4. Taxa de Falha vs Usuários
![Taxa de Falha vs Usuários](output_graphs/04_taxa_falha_vs_usuarios.png)
Taxa de falha aumenta apenas em carga grande (50 usuários). Ruby sem cache atinge limite de 10%.

### 5. Comparação Min/Médio/Max
![Min/Médio/Max por Cenário](output_graphs/05_min_med_max_por_cenario.png)
Distribuição Min/Médio/Max de tempos para cada cenário.

### 6. Impacto do Cache - Python
![Impacto Cache Python](output_graphs/06_impacto_cache_python.png)
Impacto direto do cache em Python: ~33% de melhoria em tempo médio com 50 usuários.

### 7. Impacto do Cache - Ruby
![Impacto Cache Ruby](output_graphs/07_impacto_cache_ruby.png)
Impacto direto do cache em Ruby: ~33% de melhoria em tempo médio com 50 usuários.

### 8. Python vs Ruby com Cache
![Python vs Ruby com Cache](output_graphs/08_python_vs_ruby_cache.png)
Comparação direta: Python é ~17% mais rápido que Ruby quando ambos usam cache.

### 9. Python vs Ruby sem Cache
![Python vs Ruby sem Cache](output_graphs/09_python_vs_ruby_no_cache.png)
Sem cache, Python ainda mantém melhor performance que Ruby.

---

## Como Gerar os Gráficos

```bash
# Gerar dados de exemplo
python generate_sample_results.py

# Gerar 9 gráficos PNG
python generate_graphs.py
```

Resultados:
- CSVs: `performance_results/sample_comparison.csv`
- Gráficos: `output_graphs/[01-09]_*.png`

---

## Estrutura de Resultados

Os dados de testes são organizados em `performance_results/`:

```
performance_results/
  └── sample_comparison.csv         # Dados de teste (12 linhas - 4 cenários × 3 cargas)
                                     # Colunas: Cenário, Usuários, Tamanho, Média (ms), Min (ms), 
                                     # Max (ms), P95 (ms), RPS, Total Requisições, Falhas, 
                                     # Taxa de Falha (%)
```

Os gráficos são salvos em `output_graphs/`:

```
output_graphs/
  ├── 01_tempo_medio_vs_usuarios.png
  ├── 02_rps_vs_usuarios.png
  ├── 03_p95_vs_usuarios.png
  ├── 04_taxa_falha_vs_usuarios.png
  ├── 05_min_med_max_por_cenario.png
  ├── 06_impacto_cache_python.png
  ├── 07_impacto_cache_ruby.png
  ├── 08_python_vs_ruby_cache.png
  └── 09_python_vs_ruby_no_cache.png
```

---

### URL: http://localhost

A interface web fornece:
- **Formulário de Extração**: Insira uma URL para extrair seus links
- **Teste Rápido**: 10 botões diretos para teste de carga com URLs pré-configuradas
  - example.com
  - python.org
  - wikipedia.org
  - github.com
  - stackoverflow.com
  - amazon.com
  - google.com
  - youtube.com
  - twitter.com
  - linkedin.com

Clique em qualquer URL de teste para simular requisição no serviço (útil para teste manual de carga).

---

## Pré-requisitos

Python 3.6+ e Docker:

```bash
pip install -r requirements-test.txt
pip install pandas matplotlib
docker --version
docker-compose --version
```

---

## Windows PowerShell

Executar testes em PowerShell:

```powershell
.\quick_test.ps1 -Scenario python-cache -NumUsers 50
.\quick_test.ps1 -Scenario ruby-cache -NumUsers 15
```

---

## Interpretação das Métricas

**Tempo Médio (ms)**: Tempo médio entre requisição e resposta

**Min/Max**: Extremos observados durante o teste

**P95 (ms)**: 95% das requisições responderam em até este tempo

**RPS**: Requisições processadas por segundo (throughput)

**Taxa de Falha %**: Percentual de requisições que falharam ou excederam timeout

**Total Requisições**: Número absoluto de requisições executadas no teste

---

## Conclusões

Com base nos resultados:

1. **Cache melhora significativamente**: Redução de ~33% no tempo médio com Redis em ambas linguagens

2. **Python mais eficiente**: Com cache, Python é ~17% mais rápido que Ruby (650ms vs 780ms com 50 usuários)

3. **Escalabilidade limitada**: Ambas versões atingem limites (10% taxa de falha) com 50 usuários simultâneos

4. **Cache essencial em carga**: Com 50 usuários, usar cache é crítico - sem cache Python atinge 10% falha, Ruby também

5. **Diferentes padrões RPS**: Python mantém melhor throughput conforme carga aumenta (92 RPS vs 61 RPS com 50 usuários)

---

**Trabalho**: Realização de Testes de Desempenho com a Aplicação Link Extractor  
**Data**: 2024
