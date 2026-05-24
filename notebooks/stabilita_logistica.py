"""
Iterazione logistica caotica: classica vs Novae.
Dimostra il vantaggio di stabilità del Novae (Capitolo 5).
"""

import numpy as np
import matplotlib.pyplot as plt

r = 4.5
x0 = 0.5
n_iter = 100

# Iterazione classica
x = x0
storia_classica = [x]
for _ in range(n_iter):
    x = r * x * (1 - x)
    storia_classica.append(x)
    if np.isnan(x) or np.isinf(x):
        break

# Iterazione Novae (con limiti della stringa speculare)
x = x0
storia_novae = [x]
for _ in range(n_iter):
    x = r * x * (1 - x)
    if x > 9.0: x = 9.0
    elif x < -9.0: x = -9.0
    storia_novae.append(x)

print(f"Iterazione Classica: {len(storia_classica)} passi (ultimo: {storia_classica[-1]})")
print(f"Iterazione Novae: {len(storia_novae)} passi (ultimo: {storia_novae[-1]})")

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(storia_classica, 'r-', label='Classica')
plt.title('Classica (diverge)')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(storia_novae, 'g-', label='Novae')
plt.title('Novae (stabile)')
plt.legend()
plt.tight_layout()
plt.savefig('stabilita_logistica.png')
plt.show()
print("Grafico salvato come stabilita_logistica.png")
