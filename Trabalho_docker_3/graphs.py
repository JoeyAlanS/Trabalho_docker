import matplotlib.pyplot as plt
import numpy as np

# --- Gráfico 1: Eixo X = Número de usuários ---
usuarios = [10, 100, 1000]
tempo_1inst = [2.5, 6.5, 13.5]   # seus dados reais
tempo_2inst = [4.8, 7.5, 20.5]
tempo_3inst = [7.5, 9.0, 15.5]

x = np.arange(len(usuarios))
width = 0.25

fig, ax = plt.subplots()
ax.bar(x - width, tempo_1inst, width, label='1 instância', color='lightblue')
ax.bar(x,         tempo_2inst, width, label='2 instâncias', color='moccasin')
ax.bar(x + width, tempo_3inst, width, label='3 instâncias', color='lightpink')

ax.set_xlabel('Número de usuários')
ax.set_ylabel('Tempo de resposta (s)')
ax.set_xticks(x)
ax.set_xticklabels(usuarios)
ax.legend()
plt.tight_layout()
plt.savefig('grafico_usuarios.png')
plt.show()

# --- Gráfico 2: Eixo X = Número de instâncias ---
instancias = [1, 2, 3]
rps_10u  = [2.5, 6.5, 13.5]
rps_100u = [4.8, 7.5, 20.5]
rps_1000u= [7.5, 9.0, 15.5]

x = np.arange(len(instancias))

fig, ax = plt.subplots()
ax.bar(x - width, rps_10u,   width, label='10 usuários',   color='lightgreen')
ax.bar(x,         rps_100u,  width, label='100 usuários',  color='lightblue')
ax.bar(x + width, rps_1000u, width, label='1000 usuários', color='lightyellow')

ax.set_xlabel('Número de instâncias')
ax.set_ylabel('Requisições por segundo (s)')
ax.set_xticks(x)
ax.set_xticklabels(instancias)
ax.legend()
plt.tight_layout()
plt.savefig('grafico_instancias.png')
plt.show()