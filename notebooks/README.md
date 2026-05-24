# Notebook Colab del Principia Novae Mathematicae

Questa cartella contiene i notebook interattivi (Google Colab) che accompagnano e dimostrano i risultati presentati nel **Principia Novae Mathematicae v1.3**.

Ogni notebook è autonomo: può essere aperto direttamente in Colab, eseguito cella per cella, e produce i risultati citati nel PDF.

---

## Elenco dei notebook

| Notebook | Descrizione | Capitolo di riferimento |
| :--- | :--- | :--- |
| **`novae_test.ipynb`** | Test della libreria Novae (addizione, moltiplicazione, conversione). Dimostra le tabelline e l'aritmetica formale. | Cap. 2 (Aritmetica) |
| **`chimica_novae.ipynb`** | Registro chimico formale: struttura di idrogeno, ossigeno, carbonio e molecole (H₂O, O₂). | Cap. 3 (Registro chimico) |
| **`stabilita_logistica.ipynb`** | Iterazione logistica caotica: dimostra che il sistema Novae previene l'overflow (NaN) che colpisce il calcolo classico. | Cap. 5 (Fisica computazionale) |
| **`alu_compilazione_test.ipynb`** | Compilazione dell'ALU Novae in C e test di tutte le operazioni aritmetiche (addizione, sottrazione, moltiplicazione, divisione). | Cap. 6 (Informatica e ALU) |
| **`benchmark_mappature.ipynb`** | Confronto delle prestazioni di diverse mappature binarie dei simboli Novae (lineare, Gray, complementare) in C puro. | Cap. 6, Sez. 6.3 |
| **`reti_neurali_widedeep.ipynb`** | Architettura Wide & Deep Novae con neuroni unipolari e multipolari icosaedrici, addestrata su MNIST. | Cap. 7 (Reti neurali) |

---

## Come eseguire i notebook

1. Vai su [Google Colab](https://colab.research.google.com/).
2. Clicca su **File → Apri da GitHub**.
3. Incolla l'URL del repository: `https://github.com/oppomariolevi-ai/novaebin`.
4. Seleziona il notebook che vuoi eseguire dalla cartella `notebooks/`.
5. Esegui le celle in ordine (**Runtime → Esegui tutto**).

**Nota:** I notebook che utilizzano codice C (`alu_compilazione_test.ipynb`, `benchmark_mappature.ipynb`) richiedono la compilazione tramite `gcc` e funzionano solo su Colab (non su Jupyter locale senza compilatore).

---

## Requisiti

- Python 3.8+
- Librerie Python: `torch`, `numpy`, `matplotlib`, `sympy`, `pandas`, `scikit-learn` (installate automaticamente su Colab).
- Compilatore `gcc` (solo per i notebook con codice C, già disponibile su Colab).

---

## Licenza

Tutti i notebook sono rilasciati sotto licenza **MIT**. Sentiti libero di modificarli, condividerli e utilizzarli per i tuoi progetti.

---

## Collegamenti

- [Repository principale](https://github.com/oppomariolevi-ai/novaebin)
- [Principia Novae Mathematicae v1.3 su Zenodo](https://doi.org/10.5281/zenodo.20338369)
- [Libreria Python `novae.py`](https://github.com/oppomariolevi-ai/novaebin/blob/main/novae.py)
