# Resumo Executivo - Ramp-up e Valores para Testes

## ❓ Pergunta: O Ramp-up Deve Ser o Mesmo?

### ✅ SIM - Recomendação Oficial

**Use o MESMO ramp-up para os 3 pontos de cada cenário**

**Benefícios:**
- Isolá o impacto da **quantidade de usuários** (variável independente)
- Facilita análise do gráfico P95 vs Usuários
- Comparação científica e válida
- Mais realista (operação normal com velocidade constante)

---

## 📊 Valores de Ramp-up por Cenário

| Cenário | Conteúdo | Ramp-up | Aplicar em |
|---------|----------|---------|-----------|
| **1** | Imagem 1MB | **2 seg/usuário** | Todos 3 pontos (esquerda, meio, direita) |
| **2** | Texto 400KB | **3 seg/usuário** | Todos 3 pontos (esquerda, meio, direita) |
| **3** | Imagem 300KB | **3 seg/usuário** | Todos 3 pontos (esquerda, meio, direita) |
| **4** | Híbrido | **2 seg/usuário** | Todos 3 pontos (esquerda, meio, direita) |

---

## 🎯 Cenário 2 - Destaque Completo

### Por que é "Destaque"?
- ✅ Performance mais previsível
- ✅ Curva mais suave no gráfico
- ✅ Transição clara entre baixa/média/alta carga
- ✅ Melhor para análise de SLA

### Plano de Testes Completo

#### **Instância 1 (1 servidor)**
```
Teste 1 (Esquerda):   300 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~1500ms, 0% falha
Teste 2 (Meio):       450 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~2500ms, 0% falha
Teste 3 (Direita):    650 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~4500ms, 5-10% falha
```

#### **Instância 2 (2 servidores)**
```
Teste 1 (Esquerda):   300 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~800ms, 0% falha
Teste 2 (Meio):       400 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~1500ms, 0% falha
Teste 3 (Direita):    600 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~3500ms, 5-10% falha
```

#### **Instância 3 (3 servidores)**
```
Teste 1 (Esquerda):   300 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~600ms, 0% falha
Teste 2 (Meio):       450 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~1200ms, 0% falha
Teste 3 (Direita):    650 usuários, ramp-up 3s, 2 minutos → Esperado: P95 ~2800ms, 5-10% falha
```

### Resultado Visual no Gráfico

```
P95 (ms)
 5000 ┤
      ├       ●(1,650)
 4000 ┤      ╱│
      ├     ╱ │
 3000 ┤    ╱  ●(2,600)
      ├   ╱  ╱│
 2000 ┤  ●(1,450)  
      ├ ╱│  ╱ │
 1000 ┤●  │ ●(2,400)  
      ├ \│╱  ╱●(3,650)
  500 ┤  ●───●(2,300)
      ├    ╱│╱╱
  100 ├───●──●
      └────────────────── Usuários
        300 450 300 400 600 300 450 650
```

### Checklist de Execução

- [ ] **Cenário 2 - Instância 1:**
  - [ ] 300 usuários (ramp 3s)
  - [ ] 450 usuários (ramp 3s)
  - [ ] 650 usuários (ramp 3s)

- [ ] **Cenário 2 - Instância 2:**
  - [ ] 300 usuários (ramp 3s)
  - [ ] 400 usuários (ramp 3s)
  - [ ] 600 usuários (ramp 3s)

- [ ] **Cenário 2 - Instância 3:**
  - [ ] 300 usuários (ramp 3s)
  - [ ] 450 usuários (ramp 3s)
  - [ ] 650 usuários (ramp 3s)

---

## 💡 Dica Pro

Use este comando Locust para ramp-up de 3 seg/usuário:
```python
# locustfile.py
class MyUser(HttpUser):
    wait_time = between(1, 2)  # Time entre requests
    
# Linha de comando:
# locust -f locustfile.py -u 300 -r 100 (100 usuários/minuto = ~1.67/seg)
# Para 3 seg/usuário: -r 20 (20 usuários/minuto = ~3 segundos/usuário)
```

---
