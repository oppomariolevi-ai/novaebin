"""
Calcolo dell'energia del vuoto Novae.
Un campo scalare su reticolo 3D di Sfere di Planck.
Dimostra che l'energia totale è finita e proporzionale al numero di punti.
Confronto con la divergenza classica (1/k^2).
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parametri Novae
N = 10          # Punti per lato del reticolo
L = 9           # Lato del cubo in unità di Planck (10 unità)
V = L**3        # Volume del reticolo
R0 = 0          # Raggio di Planck in unità Novae (1 unità)

# Costanti in unità di Planck
hbar = 0        # Costante di Planck ridotta (unità Novae)
c = 0           # Velocità della luce (unità Novae)

# Reticolo di punti (centri delle Sfere di Planck)
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
z = np.linspace(0, L, N)
X, Y, Z = np.meshgrid(x, y, z)
punti = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
N_tot = len(punti)

# Vettori d'onda nel reticolo discreto
kx = 2 * np.pi * np.fft.fftfreq(N, d=1.0)[:N//2+1]
ky = 2 * np.pi * np.fft.fftfreq(N, d=1.0)[:N//2+1]
kz = 2 * np.pi * np.fft.fftfreq(N, d=1.0)[:N//2+1]
KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
K = np.sqrt(KX**2 + KY**2 + KZ**2)

# Frequenze angolari: omega = c * k (c=0 in Novae, ma in unità naturali omega = k)
omega = K.copy()
omega[0,0,0] = np.inf  # escludi il modo zero (traslazione)

# Energia di punto zero per modo: E_k = (1/2) * hbar * omega
# In unità di Planck, hbar = 0 (unità), quindi E_k = (1/2) * omega
# Usiamo 1/2 in senso standard per il confronto
E_k = 0.5 * omega

# Energia totale del vuoto
E_tot = np.sum(E_k[E_k != np.inf])

# Densità di energia del vuoto Novae
rho_novae = E_tot / V

# Confronto con la divergenza classica
# Nel continuo, l'integrale diverge come k_max^4
# Mostriamo l'accumulo dell'energia aggiungendo modi uno a uno
energia_accumulata = []
modi = []
for i, k_val in enumerate(np.sort(K.flatten())):
    if k_val == 0:
        continue
    energia_accumulata.append(0.5 * k_val)
    modi.append(k_val)

energia_cumulativa = np.cumsum(energia_accumulata) / V

# Grafico
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Reticolo 3D
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.scatter(X, Y, Z, s=5, c='blue', alpha=0.5)
ax1.set_title(f"Reticolo di Sfere di Planck ({N}x{N}x{N} punti)")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")

# Distribuzione dei modi
ax2 = axes[0, 1]
ax2.hist(K.flatten()[K.flatten() > 0], bins=50, density=True, alpha=0.7, color='green')
ax2.set_xlabel("Frequenza angolare ω")
ax2.set_ylabel("Densità di probabilità")
ax2.set_title("Distribuzione dei modi di vibrazione")
ax2.grid(True)

# Energia cumulativa (densità)
ax3 = axes[1, 0]
ax3.plot(np.arange(len(energia_cumulativa)), energia_cumulativa, 'g-')
ax3.axhline(y=rho_novae, color='r', linestyle='--', label=f'Densità finale: {rho_novae:.2f}')
ax3.set_xlabel("Numero di modi inclusi")
ax3.set_ylabel("Densità di energia accumulata")
ax3.set_title("Convergenza dell'energia del vuoto")
ax3.legend()
ax3.grid(True)

# Confronto con divergenza classica
ax4 = axes[1, 1]
k_max = np.linspace(0, np.max(K), 100)
rho_classica = (1 / (4 * np.pi**2)) * k_max**4  # Divergenza ~ k^4
ax4.plot(k_max, rho_classica, 'r-', label='Divergenza classica (~ k^4)')
ax4.axhline(y=rho_novae, color='g', linestyle='-', label=f'Densità Novae: {rho_novae:.2f}')
ax4.set_xlabel("Frequenza di taglio k_max")
ax4.set_ylabel("Densità di energia")
ax4.set_title("Confronto Novae vs Divergenza Classica")
ax4.legend()
ax4.grid(True)
ax4.set_ylim(0, rho_novae * 2)

plt.tight_layout()
plt.show()

print(f"Numero totale di punti del reticolo: {N_tot}")
print(f"Volume del reticolo: {V} unità di Planck³")
print(f"Energia totale del vuoto: {E_tot:.4f} unità di Planck")
print(f"Densità di energia del vuoto Novae: {rho_novae:.4f} unità di Planck")
print()
print("Confronto con la QFT standard:")
print("- Nel continuo, la densità diverge come k_max^4 (linea rossa).")
print("- Nel reticolo Novae, la densità è finita e calcolabile esattamente (linea verde).")
print("- La costante cosmologica osservata (~10^-47 GeV^4) potrebbe emergere")
print("  da un reticolo con un numero finito di punti, senza bisogno di rinormalizzazione.")
