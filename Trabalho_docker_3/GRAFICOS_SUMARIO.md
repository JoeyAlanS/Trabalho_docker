# 📊 Sumário dos Gráficos Gerados

## ✅ Gráficos Criados com Sucesso (16 arquivos)

### Cenário 1: Imagem 1MB - 2 minutos
1. **Cenário_1_Imagem_1MB__2_minutos_tempo_vs_usuarios.png**
   - Tempo mediano de resposta vs número de usuários
   - Mostra degradação severa com 1 instância

2. **Cenário_1_Imagem_1MB__2_minutos_req_s_vs_instancias.png**
   - Requisições por segundo vs instâncias
   - Escalabilidade horizontal visível

3. **Cenário_1_Imagem_1MB__2_minutos_taxa_falha_vs_instancias.png**
   - Taxa de falha vs instâncias
   - Até 13% de falhas com 2 instâncias

---

### Cenário 2: Texto 400KB - 2 minutos
4. **Cenário_2_Texto_400KB__2_minutos_tempo_vs_usuarios.png**
   - Tempo mediano mais estável que Cenário 1
   - Máximo de 4.5 segundos

5. **Cenário_2_Texto_400KB__2_minutos_req_s_vs_instancias.png**
   - Distribuição equilibrada de carga
   - Anomalia em 630 usuários com 3 instâncias

6. **Cenário_2_Texto_400KB__2_minutos_taxa_falha_vs_instancias.png**
   - Taxa de falha controlada (0-6%)
   - Melhor que Cenário 1

---

### Cenário 3: Imagem 300KB - 2 minutos
7. **Cenário_3_Imagem_300KB__2_minutos_tempo_vs_usuarios.png**
   - Performance similar a Cenário 2
   - Máximo de 4 segundos

8. **Cenário_3_Imagem_300KB__2_minutos_req_s_vs_instancias.png**
   - Throughput consistente
   - ~11-12k req/s em máxima carga

9. **Cenário_3_Imagem_300KB__2_minutos_taxa_falha_vs_instancias.png**
   - Taxa de falha otimizada (0-10%)
   - 3 instâncias reduzem falhas para 7%

---

### Cenário 4: Híbrido - 2 minutos
10. **Cenário_4_Híbrido__2_minutos_tempo_vs_usuarios.png**
    - Variação alta (1.3s a 26s)
    - Difícil de prever com conteúdo misto

11. **Cenário_4_Híbrido__2_minutos_req_s_vs_instancias.png**
    - Throughput inconsistente
    - Instância 2 com performance anômala

12. **Cenário_4_Híbrido__2_minutos_taxa_falha_vs_instancias.png**
    - Taxa de falha alta (até 12%)
    - Requer mais instâncias para estabilidade

---

### Gráficos Comparativos (Todos Cenários)
13. **comparacao_req_s_max_carga.png**
    - Comparação de throughput em máxima carga
    - Cenário 3 é mais eficiente

14. **comparacao_taxa_falha_max_carga.png**
    - Comparação de taxa de falha
    - Todos os cenários atingem 10-13% com 1 instância

15. **comparacao_mediana_max_carga.png**
    - Comparação de tempo mediano
    - Cenário 1 tem 59s; Cenários 2-3 têm ~4s

16. **comparacao_taxa_falha_vs_usuarios.png** (gerado anteriormente)
    - Referência histórica

---

## 📊 Como Visualizar os Gráficos

```bash
# Abrir a pasta com os gráficos
cd output_graphs

# Abrir um arquivo PNG específico (Windows)
start comparacao_req_s_max_carga.png
```

---

## 🎯 Insight Principal

| Métrica | Melhor | Pior |
|---------|--------|------|
| **Tempo Mediano** | Cenário 3 (2.3s com 3 inst) | Cenário 1 (59s com 1 inst) |
| **Throughput** | Cenário 2 (124.8k req/s - anomalia) | Cenário 4 (4.4k req/s) |
| **Taxa Falha** | Cenário 2 (0% com 2 inst) | Cenário 1 (13% com 2 inst) |
| **Escalabilidade** | Cenário 3 | Cenário 4 |

---

## ✨ Próximos Passos Recomendados

1. ✅ **Validar Anomalias**
   - Cenário 2, Inst. 3, 630 usuários: 124.840 req/s
   - Cenário 4, Inst. 2, 500 usuários: 22.000ms

2. 📊 **Analisar Logs**
   - Revisar logs de Locust para períodos de anomalia
   - Validar configuração de instâncias

3. 🔧 **Otimização**
   - Compressar arquivos para ≤300KB
   - Usar CDN para distribuição
   - Implementar cache agressivo

4. 📈 **Escalar**
   - Expandir para 4-5 instâncias
   - Teste com 1000+ usuários simultâneos
   - Monitorar limite real do sistema
