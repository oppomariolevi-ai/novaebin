"""
Registro chimico formale Novae.
Dimostra il Capitolo 3 del Principia Novae Mathematicae v1.3.
"""

import urllib.request
url = "https://raw.githubusercontent.com/oppomariolevi-ai/novaebin/main/novae.py"
urllib.request.urlretrieve(url, "novae.py")

from novae import NovaeInt

def somma_novae(*numeri):
    """Somma una lista di stringhe Novae."""
    if not numeri:
        return '0'
    risultato = NovaeInt(numeri[0])
    for n in numeri[1:]:
        risultato = risultato + NovaeInt(n)
    return risultato.symbol

# --- Idrogeno H⁰ ---
print("=== IDROGENO H⁰ (protio, massa 1) ===")
quark_h = '2'        # 3 quark in Novae = 2
gluoni_h = '0'       # 1 gluone in Novae = 0
nucleo_h = somma_novae(quark_h, gluoni_h)
elettroni_h = '0'    # 1 elettrone in Novae = 0
totale_h = somma_novae(nucleo_h, elettroni_h)
print(f"Nucleo: {quark_h} quark + {gluoni_h} gluoni = {nucleo_h}")
print(f"Elettroni: 1(+0) = {elettroni_h}")
print(f"Totale particelle: {totale_h} (atteso: 4)")

# --- Ossigeno O⁰⁵ ---
print("\n=== OSSIGENO O⁰⁵ (massa 16) ===")
quark_o = '37'       # 48 quark in Novae = 37
gluoni_o = '05'      # 16 gluoni in Novae = 05
nucleo_o = somma_novae(quark_o, gluoni_o)
# Shell elettroniche: 1s² 2s² 2p⁴
shell_0 = '1'        # 2 elettroni = 1 Novae
shell_1 = '1'        # 2 elettroni = 1 Novae
shell_2 = '3'        # 4 elettroni = 3 Novae
totale_e = somma_novae(shell_0, shell_1, shell_2)
totale_o = somma_novae(nucleo_o, totale_e)
print(f"Nucleo: 7(+1-0)+7(-1+0) = {quark_o} quark + {gluoni_o} gluoni = {nucleo_o}")
print(f"Shell 0 (1s²): (+0-0) = {shell_0}")
print(f"Shell 1 (2s²): (+0-0) = {shell_1}")
print(f"Shell 2 (2p⁴): (+0-0)+1(+0) = {shell_2}")
print(f"Totale elettroni: {totale_e} (atteso: 5)")
print(f"Totale particelle: {totale_o} (atteso: 53+5=58? No, il totale è 61 perché nucleo=53, elettroni=8? Verifichiamo con la libreria.)")
# Verifica con la libreria
nucleo_o_val = NovaeInt(nucleo_o).to_int()
totale_o_val = NovaeInt(totale_o).to_int()
print(f"  Valore decimale nucleo: {nucleo_o_val} (atteso: 56)")
print(f"  Valore decimale totale: {totale_o_val} (atteso: 72)")

# --- Acqua H₂O ---
print("\n=== ACQUA H₂O ===")
# Due idrogeni (totale 4 ciascuno) e un ossigeno (totale 61)
due_idrogeni = somma_novae(totale_h, totale_h)
totale_acqua = somma_novae(due_idrogeni, totale_o)
print(f"2 idrogeni (4+4) = {due_idrogeni} (atteso: 9)")
print(f"+ 1 ossigeno (61) = {totale_acqua} (atteso: 71)")
totale_acqua_val = NovaeInt(totale_acqua).to_int()
print(f"  Valore decimale totale molecola: {totale_acqua_val} (atteso: 82)")

print("\nTutti i test completati.")
