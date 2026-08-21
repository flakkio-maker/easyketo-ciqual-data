# Dataset BLS — convertito per EasyKeto

`bls_2025.json` è ricavato dal **Bundeslebensmittelschlüssel (BLS)**,
versione 4.0 (2025), la banca dati ufficiale tedesca di composizione degli
alimenti, mantenuta dal **Max Rubner-Institut** (MRI — Bundesforschungsinstitut
für Ernährung und Lebensmittel), pubblicata su https://www.blsdb.de/.

**Licenza:** CC BY 4.0 (Creative Commons Attribution 4.0 International) —
confermata nel catalogo open data ufficiale del governo tedesco
(https://www.govdata.de/, dataset "Bundeslebensmittelschlüssel (BLS),
Version 4.0"). A differenza delle versioni precedenti (3.x, a pagamento su
licenza), la 4.0 è pubblicata "senza barriere di licenza" dal 16 dicembre
2025 — permette uso commerciale, redistribuzione e derivati, con l'unico
obbligo di citare la fonte.

**Attribuzione (citazione):** Max Rubner-Institut (MRI), Bundeslebensmittelschlüssel
(BLS), Version 4.0, 2025. https://www.blsdb.de/ — CC BY 4.0. Stesso
meccanismo già usato per CREA/OFF: badge "BLS" su ogni alimento di questa
fonte più attribuzione completa a fondo schermata nella ricerca alimenti
(vedi `AlimentiScreen.kt` nel repo principale).

## Conversione

Fonte: `BLS_4_0_Daten_2025_DE.xlsx` (foglio unico, 7.140 alimenti, 418
colonne — un valore + fonte-dato + riferimento bibliografico per ogni
nutriente). Estratti solo i 5 costituenti necessari all'app.

| Campo app | Colonna BLS | Codice componente | Note |
|---|---|---|---|
| `nome` | `Lebensmittelbezeichnung` | — | Tedesco, nativo — campo canonico/fallback (BLS è un dataset nativo tedesco, come CREA lo è per l'italiano) |
| `nome_en` | `Food name` | — | Inglese, già incluso nella fonte ufficiale (non una traduzione aggiunta da noi, a differenza di CIQUAL/CREA) |
| `nome_it` | — | — | Traduzione italiana, aggiunta in un secondo passaggio partendo da `nome_en` (non da `nome` tedesco) — presente per tutte le 7.043 voci |
| `nome_fr` | — | — | Traduzione francese, stesso procedimento |
| `nome_es` | — | — | Traduzione spagnola, stesso procedimento |
| `food_code` | `BLS Code` | — | Codice BLS originale, stabile tra le versioni |
| `carboidrati_disponibili` | `CHO Kohlenhydrate, verfügbar` | CHO | Già "disponibili" (standard EU, netti di fibre) — mapping diretto, stesso principio di CIQUAL/CREA |
| `fibre` | `FIBT Ballaststoffe, gesamt` | FIBT | |
| `grassi` | `FAT Fett` | FAT | |
| `proteine` | `PROT625 Protein (Nx6,25)` | PROT625 | |
| `calorie` | `ENERCC Energie (Kilokalorien)` | ENERCC | |
| `categoria` | — | — | `null` per tutte le voci — BLS non ha una colonna categoria testuale nel file dati (solo un prefisso di 1 lettera nel `BLS Code`, es. `C`=cereali, `M`=latte/formaggi, non ancora mappato a una tassonomia utilizzabile). Nessuna disambiguazione per categoria stimata da Gemini per questa fonte, per ora — vedi `DECISIONI.md` nel repo principale |

Note sulla conversione:
- 7.140 righe nel file sorgente, **7.043 convertite** — 97 escluse perché
  almeno uno dei 5 campi numerici richiesti aveva un valore non numerico
  (`<LOD`/`<LOD or <LOQ` = sotto il limite di rilevabilità/quantificazione,
  o `-` = non determinato) invece di un numero: stessa disciplina già
  seguita per CIQUAL/CREA, nessun valore indovinato per un campo mancante.
- Nessun duplicato di nome trovato tra le 7.043 voci valide.
- Traduzioni IT/FR/ES aggiunte in un secondo passaggio (20 agosto 2026),
  con lo stesso procedimento già usato per CIQUAL/CREA/UK: traduzione a
  blocchi (250 voci per volta) via agenti in background, sequenziali (mai
  in parallelo), poi consolidate e verificate (nessun id mancante/duplicato,
  nessun campo vuoto) prima di essere fuse nel dataset. Traduzione fatta
  dall'inglese `nome_en` (fonte ufficiale), non dal tedesco `nome` — stesso
  criterio già usato per UK (da `nome`, essendo l'inglese la lingua
  canonica di quel dataset). Vedi `DECISIONI.md` nel repo principale,
  "Regola standard: traduzione dei dataset locali".

## Micronutrienti (aggiunti il 21 agosto 2026)

Vedi `DECISIONI.md` nel repo principale, "Nota backlog: micronutrienti".
Script incluso: `aggiungi_micronutrienti_bls.py`, legge direttamente
`BLS_4_0_Daten_2025_DE.xlsx` (formato largo: 3 colonne per nutriente,
"CODICE nome [unità]" / "CODICE Datenherkunft" / "CODICE Referenz") e
incrocia per `BLS Code` == `food_code` già presente in `bls_2025.json`.
Match: 7043/7043 (100%), il foglio dati copre tutti gli alimenti già
convertiti.

32 campi aggiunti, stessa struttura di `crea_2026.json`/`ciqual_2025.json`
(vedi `README_CREA.md`). Note specifiche BLS:

- **Selenio sempre 0.0**: BLS non lo traccia come nutriente (verificato
  cercando "Selen"/"selenium" nel dizionario componenti ufficiale,
  nessun codice trovato) — a differenza di CIQUAL/CREA che ce l'hanno.
  Limite della fonte, non un errore di estrazione.
- **Conversione unità µg→mg per rame, manganese, vitamina B6**: il
  foglio dati BLS riporta questi 3 campi in µg/100g, mentre CIQUAL/CREA
  li riportano in mg/100g per lo stesso nutriente (verificato negli
  header colonna, es. "CU Kupfer [µg/100g]") — senza la conversione i
  valori sarebbero risultati 1000 volte troppo alti rispetto alle altre
  due fonti (bug individuato e corretto prima del commit, verificando
  un campione: salmone reale crudo dava rame=180mg invece di 0.041mg
  prima del fix). Tutti gli altri 29 campi sono già nella stessa unità
  delle altre fonti, nessun'altra conversione necessaria.
- Codici usati per l'aggregazione dove BLS distingue più varianti:
  `VITA` (retinol equivalents, non `VITAA` RAE), `FOL` (folati
  equivalenti aggregati, non `FOLFD` grezzo né `FOLAC` sintetico) —
  stessa granularità delle altre due fonti. `VITK` è già un codice
  aggregato in BLS (a differenza di CIQUAL che va sommato da K1+K2).

File sorgente `BLS_4_0_Daten_2025_DE.xlsx` NON committato in questo
repo (vendor, ~30MB) — va riottenuto da blsdb.de per una rigenerazione
futura, stessa scelta già presa per gli altri file sorgente grezzi.

## Aggiornamento

Il BLS ha un meccanismo di download ufficiale in blocco
(https://blsdb.de/download, aggiornato periodicamente dal Max
Rubner-Institut) — un aggiornamento futuro richiede riscaricare lo ZIP e
rieseguire lo stesso script di conversione, non un refresh automatico
periodico integrato nell'app.
