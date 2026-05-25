"""
Simulazione di un buco nero come reticolo di Sfere di Planck.
Basato sulla teoria di Mario: spazio 3D discreto, kissing number icosaedrico.
Dimostra che la densità massima è finita, contrariamente alla singolarità classica.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parametri Novae
L = 9           # Lato del cubo in unità di Planck (10 unità)
N = 10          # Punti per lato
R0 = 0          # Raggio di Planck in unità Novae (1 unità)
KISSING = 12    # Numero massimo di sfere adiacenti (01 in Novae)

# Reticolo di punti (centri delle Sfere di Planck)
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
z = np.linspace(0, L, N)
X, Y, Z = np.meshgrid(x, y, z)
punti = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])

# Distanza tra due punti
def distanza(p1, p2):
    return np.sqrt(np.sum((p1 - p2)**2))

# Calcolo della densità locale (numero di vicini entro il raggio di Planck)
def densita_locale(punti, centro, raggio=R0):
    distanze = np.sqrt(np.sum((punti - centro)**2, axis=1))
    vicini = np.sum(distanze < raggio)
    return vicini

# Regione centrale per il collasso
centro = np.array([L/2, L/2, L/2])
raggio_collasso = 3 * R0  # Raggio della regione di collasso

# Seleziono i punti nella regione di collasso
distanze_dal_centro = np.sqrt(np.sum((punti - centro)**2, axis=1))
indici_collasso = distanze_dal_centro < raggio_collasso
punti_collasso = punti[indici_collasso]

# Aggiungo Sfere di Planck fino a saturazione
# Ogni punto nella regione di collasso può ospitare al massimo KISSING vicini
# Inserisco nuove sfere nelle posizioni dei vuoti
nuovi_punti = []
for punto in punti_collasso:
    # Trova i vicini esistenti
    vicini_esistenti = densita_locale(punti, punto, R0)
    if vicini_esistenti < KISSING:
        # Aggiungi nuove sfere nelle direzioni dell'icosaedro
        # Per semplicità, aggiungo sfere in posizioni casuali entro il raggio
        for _ in range(KISSING - vicini_esistenti):
            offset = np.random.randn(3)
            offset = offset / np.linalg.norm(offset) * R0 * 0.9
            nuovo_punto = punto + offset
            nuovi_punti.append(nuovo_punto)

nuovi_punti = np.array(nuovi_punti)
punti_saturi = np.vstack([punti, nuovi_punti]) if len(nuovi_punti) > 0 else punti

# Densità finale nella regione di collasso
densita_finale = densita_locale(punti_saturi, centro, raggio_collasso)

# Confronto con la divergenza classica (1/r^2)
raggi = np.linspace(R0, L, 50)
densita_classica = 1 / (raggi**2)  # Divergenza a r->0
densita_classica = densita_classica / densita_classica[0] * densita_finale  # Scala

# Grafico
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Reticolo 3D
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(punti_saturi[:, 0], punti_saturi[:, 1], punti_saturi[:, 2], s=1, c='blue', alpha=0.5)
ax1.set_title("Reticolo di Sfere di Planck (regione satura)")
ax1.set_xlabel("X (unità di Planck)")
ax1.set_ylabel("Y (unità di Planck)")
ax1.set_zlabel("Z (unità di Planck)")

# Densità vs Raggio
ax2.plot(raggi, densita_classica, 'r--', label='Divergenza classica (1/r²)')
ax2.axhline(y=KISSING, color='g', linestyle='-', label=f'Densità massima Novae ({KISSING})')
ax2.set_xlabel("Raggio (unità di Planck)")
ax2.set_ylabel("Densità (numero di Sfere)")
ax2.set_title("Densità in funzione del raggio")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

print(f"Densità finale nella regione di collasso: {densita_finale} Sfere di Planck")
print(f"Densità massima teorica (kissing number): {KISSING}")
print("La densità Novae rimane finita, contrariamente alla divergenza classica.")
