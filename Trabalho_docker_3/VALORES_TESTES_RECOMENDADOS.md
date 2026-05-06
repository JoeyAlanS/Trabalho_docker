# Valores Recomendados para Testes - 3 Pontos por Instância

## Objetivo
Cada instância deve ter exatamente 3 pontos no gráfico P95 vs Usuários:
- **Esquerda (Carga Baixa)**: 0% de falha
- **Meio (Carga Média)**: 0% de falha  
- **Direita (Carga Alta)**: Até 10% de falha

---

## Cenário 1: Imagem 1MB

### Distribuição Recomendada
```
Instância 1: 400 usuários → 800 usuários → 1500 usuários
Instância 2: 400 usuários → 600 usuários → 1000 usuários
Instância 3: 400 usuários → 700 usuários → 1200 usuários
```

### Rationale
- **Esquerda**: 400 usuários (baixa carga, sem stress)
- **Meio**: 600-800 usuários (carga moderada, performance aceitável)
- **Direita**: 1200-1500 usuários (carga alta, perto do limite)

---

## Cenário 2: Texto 400KB - **DESTAQUE** ⭐

### Tabela Detalhada com Valores Específicos

| Instâncias | Teste | Usuários | Ramp-up | Duração | Alvo P95 (ms) | Falhas | Status |
|------------|-------|----------|---------|---------|--------------|--------|--------|
| **1** | Esquerda | 300 | 3s | 2 min | < 2000 | 0% ✅ | Baseline |
| **1** | Meio | 450 | 3s | 2 min | 2000-3500 | 0% ✅ | Confortável |
| **1** | Direita | 650 | 3s | 2 min | 4000-6000 | 5-10% ⚠️ | Limite |
| **2** | Esquerda | 300 | 3s | 2 min | < 1000 | 0% ✅ | Ótimo |
| **2** | Meio | 400 | 3s | 2 min | 1200-1800 | 0% ✅ | Confortável |
| **2** | Direita | 600 | 3s | 2 min | 3000-4500 | 5-10% ⚠️ | Limite |
| **3** | Esquerda | 300 | 3s | 2 min | < 800 | 0% ✅ | Ótimo |
| **3** | Meio | 450 | 3s | 2 min | 1000-1500 | 0% ✅ | Confortável |
| **3** | Direita | 650 | 3s | 2 min | 2500-3500 | 5-10% ⚠️ | Limite |

### Padrão Visual Esperado no Gráfico

```
P95 (ms) - Cenário 2: Texto 400KB
    │
 6000│                  ●  (1 inst, 650 usr)
    │                 /│
 5000│                / │
    │               /  │
 4000│              /   │
    │             /    │
 3000│            /     ●  (2 inst, 600 usr)
    │           /     /│
 2000│    ●     /    / │
    │   /│    /    /  │
 1500│  / │   /   /   │
    │ /  │  /   /    │
 1000│●   │ /   /     ●  (3 inst, 650 usr)
    │ \  │/   /     / 
  500│  \│   /    /   
    │   \│  /   /     
  0 ├────●─●──●──────●──
      300 450  300 400  600
      ◄─── Esquerda ────┼─── Direita ─►
```

### Padrão de Testes Recomendado

**Para Todas as 3 Instâncias:**
- Manter ramp-up **CONSTANTE em 3 segundos/usuário**
- Duração **sempre 2 minutos**
- Aumentar apenas a **quantidade de usuários**

### Checklist Cenário 2
- [ ] **Instância 1**: Execute 300 → 450 → 650 usuários (ramp 3s cada)
- [ ] **Instância 2**: Execute 300 → 400 → 600 usuários (ramp 3s cada)
- [ ] **Instância 3**: Execute 300 → 450 → 650 usuários (ramp 3s cada)
- [ ] Cada teste dura **exatamente 2 minutos**
- [ ] P95 cresce progressivamente: esquerda (baixo) → meio (médio) → direita (alto)
- [ ] Nenhuma falha nos primeiros 2 pontos
- [ ] Até 10% falha no terceiro ponto (direita)

---

## Cenário 3: Imagem 300KB

### Distribuição Recomendada
```
Instância 1: 350 usuários → 500 usuários → 700 usuários
Instância 2: 350 usuários → 450 usuários → 650 usuários
Instância 3: 350 usuários → 500 usuários → 750 usuários
```

### Rationale
- **Esquerda**: 350 usuários (carga leve, resposta rápida)
- **Meio**: 450-500 usuários (carga normal, performance estável)
- **Direita**: 700-750 usuários (carga pico, até 10% falha aceitável)

---

## Cenário 4: Híbrido

### Distribuição Recomendada
```
Instância 1: 500 usuários → 800 usuários → 1300 usuários
Instância 2: 600 usuários → 900 usuários → 1400 usuários
Instância 3: 800 usuários → 1200 usuários → 1600 usuários
```

### Rationale
- **Esquerda**: 500-800 usuários (carga base, operação normal)
- **Meio**: 800-1200 usuários (carga escalada, performance aceitável)
- **Direita**: 1300-1600 usuários (carga crítica, até 10% falha)

---

## Padrão Geral para Executar os Testes

### Template por Instância
```
Instância N:
  Teste 1 (Esquerda - 0% falha):    Ramp-up LENTO,  X usuários, duração 2-3 min
  Teste 2 (Meio - 0% falha):        Ramp-up MÉDIO,   Y usuários, duração 2-3 min
  Teste 3 (Direita - ~10% falha):   Ramp-up RÁPIDO,  Z usuários, duração 2-3 min
```

### Ramp-up Recomendado (Pode ser o MESMO para todos os 3 pontos)

**Opção 1 - Ramp-up CONSISTENTE (RECOMENDADO):**
```
Usar o MESMO ramp-up para todos os testes de uma instância
Exemplo: Ramp-up de 2 segundos por usuário para todos os 3 pontos
- Esquerda:  350 usuários com ramp-up 2s
- Meio:      500 usuários com ramp-up 2s
- Direita:   700 usuários com ramp-up 2s
```
✅ **Vantagem**: Isolá o efeito da QUANTIDADE de usuários, não da velocidade de ramp-up
✅ **Mais científico**: Comparação justa entre os 3 pontos

**Opção 2 - Ramp-up PROGRESSIVO (Menos recomendado):**
```
Variar o ramp-up conforme a carga
- Lento (Esquerda):   5-10 seg/usuário
- Médio (Meio):       2-5 seg/usuário
- Rápido (Direita):   1-2 seg/usuário
```
❌ **Desvantagem**: Mistura 2 variáveis (usuários + velocidade), dificulta análise

### RECOMENDAÇÃO FINAL
**Use ramp-up consistente (mesmo valor para os 3 pontos)**
```
Cenário 1 (1MB): Ramp-up = 2 seg/usuário
Cenário 2 (400KB): Ramp-up = 3 seg/usuário
Cenário 3 (300KB): Ramp-up = 3 seg/usuário
Cenário 4 (Híbrido): Ramp-up = 2 seg/usuário
```

---

## Checklist de Validação

- [ ] Ponto esquerda: Tempo mediano < 2s, 0% falha
- [ ] Ponto meio: Tempo mediano < 3s, 0% falha
- [ ] Ponto direita: Tempo mediano < 5s, 0-10% falha
- [ ] 3 pontos bem distribuídos no gráfico
- [ ] Cada série (1, 2, 3 instâncias) forma uma curva clara

---

## Dicas de Implementação

1. **Começar pelo ponto esquerda**: Encontre a carga mínima com 0% falha
2. **Ponto médio**: 1.5x a carga do ponto esquerda
3. **Ponto direita**: 2-2.5x a carga do ponto esquerda (deve gerar falhas)
4. **Testar incrementalmente**: Não salte de 400 para 1500 usuários
5. **Monitorar P95**: O que importa é a métrica P95, não apenas mediana

---
