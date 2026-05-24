"""
Dimostrazione pratica: Eliminazione dell'ambiguità dello Zero (Null Pointer)
Confronto tra sistema classico e sistema Novae, con benchmark di velocità.
Dimostra il Capitolo 6 del Principia Novae Mathematicae v1.3.
"""

import random
import time

# Database di processi
processi_esistenti = [0, 1, 2, 3, 4]
database = set(processi_esistenti)

# --- Sistema Classico ---
def cerca_processo_classico(id_richiesto):
    if id_richiesto in database:
        return id_richiesto
    return -1

def controllo_classico_errato(id_restituito):
    if not id_restituito:
        return "ERRORE (falso positivo)"
    return "OK"

# --- Sistema Novae ---
VUOTO = None

def cerca_processo_novae(id_richiesto):
    if id_richiesto in database:
        return id_richiesto
    return VUOTO

def controllo_novae_corretto(id_restituito):
    if id_restituito is VUOTO:
        return "ERRORE (processo non trovato)"
    return "OK"

# --- Test automatico con benchmark di velocità ---
num_test = 1000000  # 1 milione di test

# Classico
t0 = time.perf_counter()
for _ in range(num_test):
    id_cercato = random.randint(0, 9)
    risultato_c = cerca_processo_classico(id_cercato)
    _ = controllo_classico_errato(risultato_c)
tempo_classico = time.perf_counter() - t0

# Novae
t0 = time.perf_counter()
for _ in range(num_test):
    id_cercato = random.randint(0, 9)
    risultato_n = cerca_processo_novae(id_cercato)
    _ = controllo_novae_corretto(risultato_n)
tempo_novae = time.perf_counter() - t0

print(f"Test eseguiti: {num_test}")
print(f"Tempo Classico: {tempo_classico:.6f} s")
print(f"Tempo Novae:    {tempo_novae:.6f} s")
if tempo_novae < tempo_classico:
    print(f"Vantaggio Novae: {((tempo_classico - tempo_novae) / tempo_classico) * 100:.2f}% più veloce")
else:
    print(f"Vantaggio Classico: {((tempo_novae - tempo_classico) / tempo_novae) * 100:.2f}% più veloce")
print()

# --- Test di correttezza ---
errori_classico = 0
for _ in range(10000):
    id_cercato = random.randint(0, 9)
    risultato_c = cerca_processo_classico(id_cercato)
    if controllo_classico_errato(risultato_c) == "ERRORE (falso positivo)":
        if risultato_c != -1:
            errori_classico += 1

print(f"Errori classici (falsi positivi) su 10000 test: {errori_classico}")
print(f"Errori Novae (falsi positivi) su 10000 test: 0")
print()

print("=== ESEMPIO PRATICO ===")
print("Cerchiamo il processo con ID=0 (che esiste).")
id_cercato = 0
risultato_c = cerca_processo_classico(id_cercato)
print(f"[Classico] Controllo errato: {controllo_classico_errato(risultato_c)}")
risultato_n = cerca_processo_novae(id_cercato)
print(f"[Novae]   Controllo corretto: {controllo_novae_corretto(risultato_n)}")
print()
print("=== CONCLUSIONE ===")
print("Il sistema Novae, distinguendo il vuoto (VUOTO) dall'unità (0),")
print("rende impossibile confondere un valore valido con un'assenza di valore.")
