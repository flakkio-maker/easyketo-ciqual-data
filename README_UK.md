# Dataset UK (CoFID) — convertito per EasyKeto

`uk_2025.json` è ricavato dal **CoFID — McCance and Widdowson's
Composition of Foods Integrated Dataset**, edizione 2021, la banca dati
ufficiale britannica di composizione degli alimenti, pubblicata dal
governo del Regno Unito (Public Health England / gov.uk) —
https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid.
È l'edizione più recente di un dataset nato nel 1940 (McCance &
Widdowson), il più antico e più citato d'Europa dopo quello francese.

**Licenza:** Open Government Licence v3.0 (OGL v3.0) — confermata
direttamente sulla pagina di pubblicazione gov.uk. Permette uso
commerciale, copia, distribuzione e adattamento, con il solo obbligo di
citare la fonte — stesso livello di apertura di CC BY 4.0 (BLS) e
Licence Ouverte Etalab 2.0 (CIQUAL).

**Attribuzione (citazione):** Public Health England, McCance and
Widdowson's Composition of Foods Integrated Dataset (CoFID), 2021.
https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid
— Open Government Licence v3.0. Stesso meccanismo già usato per
CREA/BLS/OFF: badge "UK" su ogni alimento di questa fonte più
attribuzione completa a fondo schermata nella ricerca alimenti (vedi
`AlimentiScreen.kt` nel repo principale).

## Conversione

Fonte: `McCance_Widdowsons_Composition_of_Foods_Integrated_Dataset_2021..xlsx`
(workbook Excel ufficiale, 15 fogli), foglio `'1.3 Proximates'` (2.887
righe dati a partire dalla riga 4). Estratti i campi necessari all'app.

| Campo app | Colonna CoFID | Note |
|---|---|---|
| `nome` | `Food Name` | Inglese, nativo — nessun `nome_en` separato perché l'inglese È la lingua nativa qui |
| `nome_it` / `nome_fr` / `nome_es` / `nome_de` | — | Traduzioni statiche (20 agosto 2026, seguito — vedi `DECISIONI.md` nel repo principale "Traduzioni BLS/UK: parità di lingue con CIQUAL/CREA"), stesso principio delle colonne equivalenti di CIQUAL/CREA/BLS: traduzione naturale (non letterale) del nome inglese, non una rielaborazione dal dato nutrizionale |
| `food_code` | `Food Code` | Codice CoFID originale |
| `carboidrati_disponibili` | `Carbohydrate` | Convenzione "carboidrati disponibili" (già netti di fibra, standard EU/de-facto europeo) — mapping diretto, zero conversione, stesso principio di CIQUAL/CREA/BLS |
| `fibre` | `Fibre (NSP)` (Non-starch polysaccharide, metodo Englyst) | Scelta rispetto alla colonna alternativa AOAC per copertura dati nettamente migliore (vedi sotto) — non incide sui carboidrati, già netti a prescindere |
| `grassi` | `Fat` | |
| `proteine` | `Protein` | |
| `calorie` | `Energy (kcal)` | |
| `categoria` | — | `null` per tutte le voci — nessuna colonna categoria testuale utilizzabile in questo foglio, stessa scelta già fatta per BLS |

Note sulla conversione:
- 2.887 righe dati nel foglio sorgente, **2.537 convertite** — 350
  escluse perché almeno uno dei campi numerici richiesti non era un
  valore utilizzabile: `'N'` (dato non disponibile) o testo non
  interpretabile come numero. Stessa disciplina già seguita per
  CIQUAL/CREA/BLS: nessun valore indovinato per un campo mancante.
- Valori `'Tr'` (traccia, quantità presente ma non misurabile in modo
  affidabile) trattati come `0.0` — convenzione standard nella scienza
  della nutrizione per questo tipo di dataset, non un'invenzione.
- **Fibra: scelta NSP (Englyst) invece di AOAC.** Il foglio sorgente
  offre entrambe le colonne, ma NSP ha copertura dati nettamente
  migliore (2.538 righe utilizzabili contro 1.548 di AOAC, su 2.887
  totali) — scelta esclusivamente per completezza del dato, senza
  impatto sui carboidrati (che sono già "disponibili"/netti a
  prescindere da quale colonna fibra si scelga, la fibra qui è solo un
  dato informativo separato).
- 2 nomi duplicati legittimi mantenuti (varianti distinte con lo stesso
  nome commerciale, es. marche/preparazioni diverse con la stessa
  etichetta) — nessuna deduplicazione forzata, stesso principio già
  applicato a CIQUAL/CREA/BLS.
- Traduzioni italiano/francese/spagnolo/tedesco aggiunte in un secondo
  passaggio (20 agosto 2026) — tutte e 2.537 le voci, via agenti in
  batch paralleli, stesso procedimento già usato per CIQUAL/CREA. Vedi
  `DECISIONI.md` nel repo principale.

## Aggiornamento

Il CoFID viene aggiornato periodicamente da Public Health England/UK
Government (nuove edizioni pubblicate su gov.uk) — un aggiornamento
futuro richiede riscaricare il workbook Excel più recente e rieseguire
lo stesso procedimento di estrazione, non un refresh automatico
periodico integrato nell'app.
