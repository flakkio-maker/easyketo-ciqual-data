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
- Nessuna traduzione italiana/francese/spagnola aggiunta in questo
  passaggio (a differenza di CIQUAL/CREA, che le hanno ricevute in un
  secondo momento) — BLS resta per ora DE (nativo) + EN (dalla fonte
  ufficiale) soltanto. Un'estensione futura è possibile con lo stesso
  procedimento già usato per CIQUAL/CREA (traduzione a blocchi via
  agenti in background), non fatta qui per restare nello scope della
  richiesta originale (aggiungere una fonte tedesca, non tradurla in
  altre 3 lingue).
- Nessun duplicato di nome trovato tra le 7.043 voci valide.

## Aggiornamento

Il BLS ha un meccanismo di download ufficiale in blocco
(https://blsdb.de/download, aggiornato periodicamente dal Max
Rubner-Institut) — un aggiornamento futuro richiede riscaricare lo ZIP e
rieseguire lo stesso script di conversione, non un refresh automatico
periodico integrato nell'app.
