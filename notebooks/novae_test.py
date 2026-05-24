"""
Test della libreria Novae (addizione, moltiplicazione, conversione).
Dimostra il Capitolo 2 del Principia Novae Mathematicae v1.3.
"""

# Scarica la libreria ufficiale
import urllib.request
url = "https://raw.githubusercontent.com/oppomariolevi-ai/novaebin/main/novae.py"
urllib.request.urlretrieve(url, "novae.py")

from novae import NovaeInt

# Test addizione
print("=== ADDIZIONE ===")
a = NovaeInt('0')
b = NovaeInt('1')
print(f"0 + 0 = {a + a}  (atteso: 1)")
print(f"0 + 1 = {a + b}  (atteso: 2)")
print(f"1 + 1 = {b + b}  (atteso: 3)")

# Test moltiplicazione (valori attesi corretti)
print("\n=== MOLTIPLICAZIONE ===")
print(f"0 * 0 = {a * a}  (atteso: 0)")
print(f"0 * 1 = {a * b}  (atteso: 1)")
print(f"1 * 1 = {b * b}  (atteso: 3)")

# Test conversione (valori attesi corretti)
print("\n=== CONVERSIONE ===")
n = NovaeInt('5')
print(f"'5' in decimale: {n.to_int()}  (atteso: 6)")
m = NovaeInt.from_int(10)
print(f"10 decimale in Novae: {m}  (atteso: 9)")

print("\nTutti i test completati.")
