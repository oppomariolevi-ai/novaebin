# Novae: Il Sistema di Numerazione Non-Decimato

**Novae** è un sistema di numerazione posizionale che elimina la "decimazione" del sistema decimale classico. Invece di avere un simbolo (0) che rappresenta sia l'assenza di quantità che una posizione numerica, Novae distingue il **Vuoto** (`∅`) dall'**Unità** (`0`).

## Perché Novae?

Il sistema decimale e binario che usiamo oggi sono versioni "decimate" di un sistema più naturale, il Novae. La decimazione (dal latino *decimatio*, l'uccisione di un soldato ogni dieci) è l'atto di sacrificare un'unità ad ogni ciclo per generare un riporto. Novae elimina questo sacrificio, conservando ogni posizione sempre piena.

## Binario Novae: Vantaggi Immediati

Il **Binario Novae** è la trasposizione di questo principio nel sistema a due cifre (0, 1). I vantaggi sono misurabili:

### 1. Maggiore Densità di Informazione

| Lunghezza max bit | Binario Classico (valori) | Binario Novae (valori) |
| :--- | :--- | :--- |
| 1 bit | 2 | 2 |
| 2 bit | 4 | 6 |
| 3 bit | 8 | 14 |
| n bit | 2ⁿ | 2ⁿ⁺¹ - 2 |

Con stringhe fino a 3 bit, il Novae rappresenta il **75% in più** di valori.

### 2. Eliminazione del Null Pointer

Nel binario classico, `0` è ambiguo: è sia il primo indirizzo valido, sia il puntatore nullo.
Nel Binario Novae:
- `∅` (nessun segnale) = puntatore non inizializzato.
- `0` = primo indirizzo valido.

**Fine dei NullPointerException a livello hardware.**

### 3. Addizione come Successione Pura

L'addizione Novae è semplicemente l'applicazione ripetuta della funzione **successore**. Non servono complessi circuiti aritmetici, ma solo contatori e comparatori.

## Esecuzione Rapida

```bash
git clone https://github.com/oppomariolevi-ai/Novae.git
cd Novae
python3 binario_novae.py
