"""
Registro chimico formale Novae con tabella comparativa.
Dimostra il Capitolo 3 del Principia Novae Mathematicae v1.3.
"""

import urllib.request
url = "https://raw.githubusercontent.com/oppomariolevi-ai/novaebin/main/novae.py"
urllib.request.urlretrieve(url, "novae.py")

from novae import NovaeInt

def somma_novae(*numeri):
    if not numeri:
        return '0'
    risultato = NovaeInt(numeri[0])
    for n in numeri[1:]:
        risultato = risultato + NovaeInt(n)
    return risultato.symbol

# --- Idrogeno ---
quark_h = '2'; gluoni_h = '0'; nucleo_h = somma_novae(quark_h, gluoni_h)
elettroni_h = '0'; totale_h = somma_novae(nucleo_h, elettroni_h)

# --- Ossigeno ---
quark_o = '37'; gluoni_o = '05'; nucleo_o = somma_novae(quark_o, gluoni_o)
shell_0 = '1'; shell_1 = '1'; shell_2 = '3'
totale_e = somma_novae(shell_0, shell_1, shell_2)
totale_o = somma_novae(nucleo_o, totale_e)

# --- Acqua ---
due_idrogeni = somma_novae(totale_h, totale_h)
totale_acqua = somma_novae(due_idrogeni, totale_o)

# --- Tabella comparativa ---
print("=" * 70)
print("REGISTRO CHIMICO NOVAE – CONFRONTO CON DECIMALE")
print("=" * 70)
print(f"{'Elemento':<12} {'Particella':<20} {'Decimale':<10} {'Novae':<10}")
print("-" * 70)

# Idrogeno
print(f"{'Idrogeno H⁰':<12} {'Quark':<20} {3:<10} {quark_h:<10}")
print(f"{'':<12} {'Gluoni':<20} {1:<10} {gluoni_h:<10}")
print(f"{'':<12} {'Nucleo (totale)':<20} {4:<10} {nucleo_h:<10}")
print(f"{'':<12} {'Elettroni':<20} {1:<10} {elettroni_h:<10}")
print(f"{'':<12} {'TOTALE':<20} {5:<10} {totale_h:<10}")
print("-" * 70)

# Ossigeno
print(f"{'Ossigeno O⁰⁵':<12} {'Quark':<20} {48:<10} {quark_o:<10}")
print(f"{'':<12} {'Gluoni':<20} {16:<10} {gluoni_o:<10}")
print(f"{'':<12} {'Nucleo (totale)':<20} {64:<10} {nucleo_o:<10}")
print(f"{'':<12} {'Elettroni (1s²)':<20} {2:<10} {shell_0:<10}")
print(f"{'':<12} {'Elettroni (2s²)':<20} {2:<10} {shell_1:<10}")
print(f"{'':<12} {'Elettroni (2p⁴)':<20} {4:<10} {shell_2:<10}")
print(f"{'':<12} {'Elettroni (totale)':<20} {8:<10} {totale_e:<10}")
print(f"{'':<12} {'TOTALE':<20} {72:<10} {totale_o:<10}")
print("-" * 70)

# Acqua
print(f"{'Acqua H₂O':<12} {'2 Idrogeni (4+4)':<20} {10:<10} {due_idrogeni:<10}")
print(f"{'':<12} {'1 Ossigeno':<20} {72:<10} {totale_o:<10}")
print(f"{'':<12} {'TOTALE MOLECOLA':<20} {82:<10} {totale_acqua:<10}")
print("=" * 70)
print("Nota: nella colonna 'Novae' ogni simbolo rappresenta la quantità.")
print("Es. '0' = 1, '1' = 2, '9' = 10, '00' = 11.")
print("La somma di simboli Novae segue le regole del sistema: 0+0=1, 0+1=2, ecc.")# Shell elettroniche: 1s² 2s² 2p⁴
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
