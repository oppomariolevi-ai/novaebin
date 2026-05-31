# Principia Novae Mathematicae

**Un nuovo linguaggio matematico fondato sulla pura successione e sulla geometria icosaedrica.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20338369.svg)](https://doi.org/10.5281/zenodo.20338369)

---

## Cos'è il Novae?

Il sistema decimale che usiamo ogni giorno non è l'unico modo di contare. Il Novae è un sistema di numerazione che elimina alla radice i concetti di zero assoluto e infinito, sostituendoli con la pura successione.

Nel Novae:
- Il vuoto è `∅`, non `0`
- `0` rappresenta l'unità, non il nulla
- L'addizione è successione pura: `0 + 0 = 1`
- Non esistono zeri posizionali, né infiniti, né singolarità

## Ipotesi fondante

Il continuo emerge dal discreto. Lo spazio è un reticolo tridimensionale che può essere mappato con un artificio logico: le Sfere di Planck, la cui aggregazione segue il kissing number icosaedrico (12). Le fluttuazioni del vuoto (`∅`) rappresentano la granularità ultima della realtà. Il tempo non è una dimensione aggiuntiva, ma un fenomeno che emerge dallo spazio: la luce percorre una Sfera di Planck per ogni istante, e la successione di questi istanti (`0 + 0 = 1`) genera il fluire del tempo.

In questo quadro, le singolarità e le divergenze che affliggono la fisica teorica (rinormalizzazione, costante cosmologica) non sono problemi della natura, ma artefatti del linguaggio decimale.

---

## Risultati sperimentali

| Ambito | Risultato | Notebook |
|--------|-----------|----------|
| **Reti neurali** | Wide & Deep Novae (98.0%) supera il classico (97.4%) su MNIST | [`reti_neurali_widedeep.py`](notebooks/reti_neurali_widedeep.py) |
| **Stabilità computazionale** | Iterazione logistica: 101 passi stabili vs 12 del classico | [`stabilita_logistica.py`](notebooks/stabilita_logistica.py) |
| **Informatica** | Eliminazione del null pointer: 0% errori vs 10% del classico | [`null_pointer_test.py`](notebooks/null_pointer_test.py) |
| **Hardware** | ALU Novae in C funzionante, benchmark di mappature binarie | [`alu_compilazione_test.py`](notebooks/alu_compilazione_test.py) |
| **Chimica** | Registro formale per atomi e molecole | [`chimica_novae.py`](notebooks/chimica_novae.py) |

---

## Documentazione

- 📄 [Principia Novae Mathematicae v1.3 (PDF)](https://zenodo.org/records/20338369)
- 📓 [Notebook Colab](notebooks/)
- 📚 [Libreria Python `novae.py`](novae.py)

---

## Installazione rapida

```bash
git clone https://github.com/oppomariolevi-ai/novaebin.git
cd novaebin
python3 novae.py
