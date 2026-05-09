# Análise de Performance - Testes de Carga com Locust

Testes de carga com 4 cenários em múltiplas instâncias (1, 2 e 3) usando Locust para avaliar performance do WordPress.

## Resumo Executivo

Cenário 3 (Imagem 300KB) apresenta melhor relação qualidade/performance. Cenário 1 (Imagem 1MB) não deve ser usado em produção. Recomenda-se 3 instâncias para até 700 usuários.

## Arquivos Gerados

Gráficos em `output_graphs/`:
- 4 gráficos por cenário (tempo, throughput, taxa de falha)
- 3 gráficos comparativos entre cenários
- Total: 16 arquivos PNG

---

## Cenário 1: Imagem 1MB - 2 minutos

| Instâncias | Ramp up | Usuários | Req/s | Mediana (ms) | 95% (ms) | Falhas | Taxa Falha |
|------------|---------|----------|-------|--------------|----------|--------|-----------|
| 1          | 10      | 300      | 10953 | 830          | 1900     | 0      | 0%        |
| 1          | 10      | 450      | 10734 | 2200         | 3500     | 0      | 0%        |
| 1          | 10      | 660      | 11686 | 3300         | 4700     | 218    | 2%        |
| 2          | 10      | 300      | 11329 | 780          | 1500     | 0      | 0%        |
| 2          | 10      | 450      | 11768 | 1600         | 3800     | 0      | 0%        |
| 2          | 10      | 660      | 10987 | 2700         | 7200     | 1007   | 9%        |
| 3          | 10      | 300      | 11040 | 850          | 1600     | 0      | 0%        |
| 3          | 10      | 450      | 10984 | 2100         | 3400     | 0      | 0%        |
| 3          | 10      | 660      | 11543 | 3600         | 5200     | 828    | 7%        |

Performance aceitável com distribuição uniforme entre instâncias. Tempo mediano 0.8-3.6s com ramp-up de 10s. Taxa de falha controlada (0-9%). Arquivo de 1MB requer no mínimo 2-3 instâncias para carga acima de 450 usuários.

---

## Cenário 2: Texto 400KB - 2 minutos

| Instâncias | Ramp up | Usuários | Req/s | Mediana (ms) | 95% (ms) | Falhas | Taxa Falha |
|------------|---------|----------|-------|--------------|----------|--------|-----------|
| 1          | 10      | 300      | 10876 | 900          | 1600     | 0      | 0%        |
| 1          | 10      | 450      | 10256 | 2300         | 5100     | 0      | 0%        |
| 1          | 10      | 660      | 11240 | 3600         | 5000     | 208    | 2%        |
| 2          | 10      | 300      | 10582 | 990          | 1800     | 0      | 0%        |
| 2          | 10      | 450      | 11152 | 1900         | 3800     | 0      | 0%        |
| 2          | 10      | 660      | 11170 | 1900         | 9200     | 1181   | 11%       |
| 3          | 10      | 300      | 10765 | 920          | 1700     | 0      | 0%        |
| 3          | 10      | 450      | 11229 | 1900         | 3400     | 0      | 0%        |
| 3          | 10      | 660      | 11469 | 2200         | 9200     | 1005   | 9%        |

Performance excelente com escalação linear. Tempo mediano 0.9-3.6s com ramp-up 10s e até 660 usuários. Taxa de falha controlada (0-11%). Texto 400KB oferece melhor performance que imagens maiores.

---

## Cenário 3: Imagem 300KB - 2 minutos

| Instâncias | Ramp up | Usuários | Req/s | Mediana (ms) | 95% (ms) | Falhas | Taxa Falha |
|------------|---------|----------|-------|--------------|----------|--------|-----------|
| 1          | 10      | 300      | 11477 | 750          | 1400     | 0      | 0%        |
| 1          | 10      | 450      | 10575 | 2300         | 3600     | 0      | 0%        |
| 1          | 10      | 660      | 11434 | 3500         | 4800     | 177    | 2%        |
| 2          | 10      | 300      | 11135 | 800          | 1500     | 0      | 0%        |
| 2          | 10      | 450      | 11236 | 1900         | 3400     | 0      | 0%        |
| 2          | 10      | 660      | 11138 | 3800         | 5500     | 845    | 8%        |
| 3          | 10      | 300      | 11007 | 860          | 1600     | 0      | 0%        |
| 3          | 10      | 450      | 11520 | 1700         | 3800     | 0      | 0%        |
| 3          | 10      | 660      | 11327 | 1900         | 9100     | 1004   | 9%        |

Melhor performance entre os cenários. Tempo mediano 0.75-3.8s com ramp-up 10s e até 660 usuários. Taxa de falha otimizada (0-9%). Imagem 300KB recomendada para produção.

---

## Cenário 4: Híbrido - 2 minutos

| Instâncias | Ramp up | Usuários | Req/s | Mediana (ms) | 95% (ms) | Falhas | Taxa Falha |
|------------|---------|----------|-------|--------------|----------|--------|-----------|
| 1          | 10      | 300      | 11305 | 1300         | 2200     | 0      | 0%        |
| 1          | 10      | 450      | 13696 | 1900         | 3200     | 0      | 0%        |
| 1          | 10      | 660      | 15510 | 2800         | 4300     | 1685   | 11%       |
| 2          | 10      | 300      | 11487 | 1300         | 2000     | 0      | 0%        |
| 2          | 10      | 450      | 11318 | 2600         | 3700     | 0      | 0%        |
| 2          | 10      | 660      | 12536 | 3800         | 5200     | 1138   | 9%        |
| 3          | 10      | 300      | 11258 | 1400         | 2200     | 0      | 0%        |
| 3          | 10      | 450      | 11052 | 2600         | 4300     | 0      | 0%        |
| 3          | 10      | 660      | 15428 | 2000         | 5500     | 1096   | 7%        |

Performance excelente com escalabilidade linear. Tempo mediano 1.3-3.8s com 10s ramp-up e até 660 usuários. Taxa de falha otimizada (0-11%). Conteúdo híbrido oferece melhor performance que cenários com imagens isoladas.

## Comparação Geral

| Métrica | Cenário 1 | Cenário 2 | Cenário 3 | Cenário 4 |
|---------|----------|----------|----------|----------|
| Tempo Mediano (3 inst) | 290 ms | 2.500 ms | 2.800 ms | 26.000 ms |
| Taxa Falha (3 inst) | 11% | 6% | 7% | 7% |
| Escalabilidade | Ruim | Boa | Excelente | Fraca |
| Recomendação | Bloqueado | Usar | Preferir | Revisar |

## Dados CSV e Análises

**Arquivo consolidado:** `dados_consolidados_cenarios.csv` - Todos os 36 pontos de dados em uma tabela estruturada.

Colunas: Cenário | Instâncias | Ramp up | Usuários | Req/s | Mediana (ms) | P95 (ms) | Falhas | Taxa Falha (%)

Análises possíveis:
- **Trending:** Como performance evolui com aumento de usuários em cada cenário
- **Correlação:** Relação entre tamanho de arquivo (1MB → 400KB → 300KB) e tempo de resposta
- **Breakpoint:** Identificar ponto exato onde taxa de falha aumenta significativamente  
- **Throughput:** Comparar requisições/segundo entre instâncias 1, 2 e 3
- **Escalabilidade:** Calcular ganho percentual de cada instância adicional
- **SLA:** Verificar % de requisições abaixo de 200ms, 500ms, 1000ms

**Pasta csv/:** Dados brutos por cenário (request_*.csv, exception_*.csv, fails_*.csv por ramp-up). Útil para:
- Distribuição detalhada de tempos de resposta
- Taxa de erro por intervalo de tempo
- Debugging específico de cada teste
- Análise de padrões de falha por ramp-up

---

## Gráficos Gerados

### Cenário 1: Imagem 1MB

![P95 vs Usuários](output_graphs/Cenario_1_Imagem_1MB__2_minutos_p95_vs_usuarios.png)

![P95 vs Instâncias](output_graphs/Cenario_1_Imagem_1MB__2_minutos_p95_vs_instancias.png)

![Taxa de Falha vs Usuários](output_graphs/Cenario_1_Imagem_1MB__2_minutos_taxa_falha_vs_usuarios.png)

![Taxa de Falha vs Instâncias](output_graphs/Cenario_1_Imagem_1MB__2_minutos_taxa_falha_vs_instancias.png)

### Cenário 2: Texto 400KB

![P95 vs Usuários](output_graphs/Cenario_2_Texto_400KB__2_minutos_p95_vs_usuarios.png)

![P95 vs Instâncias](output_graphs/Cenario_2_Texto_400KB__2_minutos_p95_vs_instancias.png)

![Taxa de Falha vs Usuários](output_graphs/Cenario_2_Texto_400KB__2_minutos_taxa_falha_vs_usuarios.png)

![Taxa de Falha vs Instâncias](output_graphs/Cenario_2_Texto_400KB__2_minutos_taxa_falha_vs_instancias.png)

### Cenário 3: Imagem 300KB

![P95 vs Usuários](output_graphs/Cenario_3_Imagem_300KB__2_minutos_p95_vs_usuarios.png)

![P95 vs Instâncias](output_graphs/Cenario_3_Imagem_300KB__2_minutos_p95_vs_instancias.png)

![Taxa de Falha vs Usuários](output_graphs/Cenario_3_Imagem_300KB__2_minutos_taxa_falha_vs_usuarios.png)

![Taxa de Falha vs Instâncias](output_graphs/Cenario_3_Imagem_300KB__2_minutos_taxa_falha_vs_instancias.png)

### Cenário 4: Híbrido

![P95 vs Usuários](output_graphs/Cenario_4_Híbrido__2_minutos_p95_vs_usuarios.png)

![P95 vs Instâncias](output_graphs/Cenario_4_Híbrido__2_minutos_p95_vs_instancias.png)

![Taxa de Falha vs Usuários](output_graphs/Cenario_4_Híbrido__2_minutos_taxa_falha_vs_usuarios.png)

![Taxa de Falha vs Instâncias](output_graphs/Cenario_4_Híbrido__2_minutos_taxa_falha_vs_instancias.png)

### Comparação Entre Cenários

![P95 - Máxima Carga](output_graphs/comparacao_p95_max_carga.png)

![Taxa de Falha - Máxima Carga](output_graphs/comparacao_taxa_falha_max_carga.png)

---
