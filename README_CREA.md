# Dataset CREA — convertito per EasyKeto

`crea_2026.json` è ricavato dalle Tabelle di composizione degli alimenti del
**CREA** (Consiglio per la ricerca in agricoltura e l'analisi dell'economia
agraria — Centro di ricerca Alimenti e Nutrizione, ex INRAN), pubblicate su
https://www.alimentinutrizione.it/.

**Attribuzione (citazione completa):** CREA — Consiglio per la ricerca in
agricoltura e l'analisi dell'economia agraria, Centro di ricerca Alimenti e
Nutrizione. *Tabelle di composizione degli alimenti*. https://www.alimentinutrizione.it/

Uso confermato liberamente disponibile dal titolare del progetto (12 agosto
2026): CREA consente l'utilizzo dei dati pubblicati sul proprio sito citando
la fonte per intero come sopra — il solo utilizzo esplicitamente vietato è lo
scraping automatico del sito, non applicabile qui (dataset ottenuto già in
forma strutturata). Vedi `DECISIONI.md` nel repo principale (blocco "Banca
dati CREA — chiarimento licenza") per il dettaglio della conferma.

A differenza di CIQUAL (Licence Ouverte Etalab 2.0, riuso libero anche
commerciale senza altro obbligo che la menzione fonte), la citazione CREA va
mostrata per intero, non solo nel footer di questo README: l'app mostra un
badge "CREA" su ogni alimento di questa fonte più l'attribuzione completa a
fondo schermata nella ricerca alimenti, stesso meccanismo già usato per
l'attribuzione ODbL di Open Food Facts (vedi `RicercaAlimentiRepositoryImpl`
e `AlimentiScreen.kt` nel repo principale).

## Conversione

Fonte: `crea_food_composition_tables.csv` (900 alimenti, incluse 51 voci
"Ricette Italiane" con codice `PC00xx`) + `crea_recipes.json` (56 ricette con
preparazione/ingredienti, collegate per `food_code`). Script:
`normalizza_crea.py` in questo repo.

| Campo app | Campo CREA | Note |
|---|---|---|
| `nome` | `name` | Già in italiano — CREA è un dataset nativo italiano, resta il campo canonico/fallback |
| `nome_en` / `nome_fr` / `nome_es` / `nome_de` | — | Traduzioni aggiunte il 12 agosto 2026 (task #236 dell'app, stesso principio di `nome_it` in CIQUAL — a differenza di CIQUAL, qui non esisteva alcuna colonna tradotta prima). La lingua mostrata all'utente segue quella di sistema del dispositivo, con fallback su `nome` (vedi `scegliTraduzioneAlimento`, `TraduzioneAlimentoUseCase.kt` nel repo principale) |
| `food_code` | `food_code` | Codice CREA originale, stabile tra le versioni |
| `categoria` | `category` | 19 categorie native (elenco sotto) |
| `carboidrati_disponibili` | `available_carbohydrates` | Standard EU, già netto di fibre — mapping diretto, stesso principio di CIQUAL |
| `fibre` | `total_fiber` | |
| `grassi` | `lipids` | |
| `proteine` | `proteins` | |
| `calorie` | `energy_kcal` | |
| `preparazione` | `crea_recipes.json: preparation` | Solo per le 56 voci con ricetta collegata, altrimenti `null` |
| `ingredienti` | `crea_recipes.json: ingredients` | Idem, stringa `"nome qty, nome qty, ..."` |

Note sulla conversione:
- Valori numerici mancanti/vuoti nel CSV sorgente sono mappati a `0.0`
  (nessun alimento escluso per campo mancante, a differenza di CIQUAL: il
  dataset CREA non ha valori "-"/"traces" da distinguere, solo celle vuote).
- Categorie (19, elenco nativo CREA, nessuna traduzione necessaria):
  Alimenti Etnici, Bevande alcoliche, Carni fresche, Carni trasformate e
  conservate, Cereali e derivati, Dolci, Fast-food a base di carne, Formaggi
  e latticini, Frattaglie, Frutta, Frutta secca a guscio e semi oleaginosi,
  Latte e yogurt, Legumi, Oli e grassi, Prodotti della pesca, Prodotti vari,
  Ricette Italiane, Uova, Verdure e ortaggi.
- La categoria "Ricette Italiane" è il differenziale principale rispetto a
  CIQUAL (dataset francese, debole sui piatti regionali italiani) — vedi
  `DECISIONI.md` nel repo principale.

## Aggiornamento

Il dataset CREA di origine non ha un meccanismo di download/API in blocco
(consultazione libera scheda per scheda sul sito); un aggiornamento futuro
richiede ripetere l'estrazione manuale e rigenerare questo file con lo stesso
script — non è previsto un refresh automatico periodico.
