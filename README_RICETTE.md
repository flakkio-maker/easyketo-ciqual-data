# Dataset ricette — scoperta (`ricette_scoperta.json`)

Catalogo di ricette per la funzione "Ricette — scoperta" di EasyKeto
(`FeatureFlags.RICETTE_SCOPERTA_ABILITATA`). **I macro di ogni ricetta sono
sempre calcolati dai database CIQUAL/CREA usati dall'app, mai presi dalla
fonte esterna** — indipendentemente dalla fonte, ogni ingrediente è
matchato uno per uno contro CIQUAL/CREA con un matcher testuale a soglia di
confidenza (nessun uso di IA/Gemini per il matching), e i grammi sono
sempre quantità reali dichiarate (mai stimate).

## Fonti combinate (448 ricette al 15 agosto 2026)

| Fonte (`fonte`) | N. ricette | Licenza | Note |
|---|---|---|---|
| `kaggle-foodcom` | 246 | Dataset Kaggle Food.com, licenza aperta | Estratte da un dataset di ~500k ricette, filtrate per plausibilità macro e bilancio massa (`peso_porzione_dichiarato_g` vs `serving_size` dichiarato) |
| `wikibooks-it` | 8 | CC BY-SA 4.0 (it.wikibooks.org, "Libro di cucina") | API pubblica MediaWiki, non scraping |
| `wikibooks-en` | 25 | CC BY-SA 4.0 (en.wikibooks.org, "Cookbook") | Categorie Italian/French/Spanish/German/English recipes |
| `originale` | 202 | — (autorship originale) | 20 ricette generiche + 182 ispirate a piatti reali e riconoscibili (es. Coq au vin, Gulasch, Tortilla española, Ossobuco alla milanese, Shepherd's pie, Butter chicken, Pad thai, Ramen, Tandoori), scritte una per una da conoscenza culinaria di dominio pubblico — non generate combinatoriamente, non estratte da alcun testo/dataset di terzi |

Cucine coperte: italiana, francese, tedesca, spagnola, inglese (prima
infornata), più cinese, giapponese, indiana, thailandese, americana, greca
ed europea/asiatica generiche (seconda e terza infornata, su richiesta
esplicita dell'utente di estendere a cucine asiatiche principali, USA e
altre europee).

**Perché non da Giallo Zafferano o simili:** valutato e rifiutato più volte
(vedi `DECISIONI.md` nel repo principale) — il diritto sui generis sulle
banche dati (Direttiva 96/9/CE) protegge la compilazione (quali ricette
esistono + ingredienti/quantità) indipendentemente dalla riformulazione del
testo. Solo fonti con licenza che permette esplicitamente l'estrazione
(CC BY-SA, licenze aperte) o dati di autorship originale.

**Nota sul volume:** una prima versione generava ricette "originali" in
modo combinatorio (pool di ingredienti × metodo di cottura × variante
dieta) per raggiungere ~5000 ricette — approccio scartato su richiesta
esplicita dell'utente ("non deve essere combinatorio, devi ispirarti a
cose reali", volume finale accettato più basso). Tutte le ricette
"originali" attuali (202, in tre infornate successive) sono scritte
singolarmente ispirandosi a piatti riconoscibili, non assemblate
meccanicamente.

**Copertura filtri:** verificata esplicitamente su richiesta dell'utente
("controlla che tutte le combinazioni di filtri diano almeno 1 risultato")
enumerando ogni combinazione pasto × cucina × tipo_dieta (14 cucine × 4
pasti × 4 diete = 224 combinazioni): 0/224 vuote nella versione attuale.
La terza infornata di ricette originali è stata scritta apposta per
colmare le 29 combinazioni ancora vuote dopo la seconda (soprattutto
colazione/spuntino ad alto contenuto proteico, e piatti chetogenici senza
riso per indiana/thailandese) — sempre piatti reali con quantità dosate
intenzionalmente per centrare quella fascia macro, non generazione
combinatoria.

## Schema (un oggetto per ricetta)

| Campo | Tipo | Note |
|---|---|---|
| `id` | Long | Intero progressivo, univoco nel file — il DTO Android (`RicetteScopertaDownloadWorker.kt`) richiede `Long`, non stringa |
| `nome` | String | |
| `fonte` | String | Uno dei valori in tabella sopra |
| `licenza_fonte` | String? | Testo di attribuzione da mostrare in UI, `null` per autorship originale |
| `tipo_pasto` | [String] | `colazione` / `pranzo` / `cena` / `spuntino` — una ricetta può averne più di uno |
| `cucina` | [String] | `italiana` / `francese` / `tedesca` / `spagnola` / `inglese` / altre (dedotte da tag/categoria per le fonti esterne) |
| `tipo_dieta` | [String] | `chetogenica` / `ipocalorica` / `bassa_glicemia` / `iperproteica` — euristica su macro già calcolati, non validazione clinica |
| `porzioni` | Double | |
| `peso_porzione_dichiarato_g` | Double | |
| `kcal_porzione` / `carbo_porzione` / `grassi_porzione` / `proteine_porzione` | Double | Per porzione |
| `ingredienti` | [{nome, grammi, fonte_macro, voce_matchata}] | `fonte_macro` è `"CIQUAL"`/`"CREA"`/`null` (ingredienti a impatto trascurabile) |
| `prompt_immagine` | String? | Testo descrittivo per un futuro tool di generazione immagini — non ancora usato in app |
| `procedimento_it` | [String] | Passi di preparazione in italiano, uno step per elemento — sempre presente per tutte le 448 ricette. Recuperato dalla fonte originale reale quando disponibile (tradotto in italiano se la fonte era in inglese) e scritto da zero, in base a conoscenza culinaria reale del piatto e agli ingredienti registrati, solo per le ricette senza fonte testuale recuperabile (perlopiù `fonte: "originale"`) — nessuna invenzione quando esiste un testo originale. Vedi `DECISIONI.md` nel repo principale, blocco "Procedimento ricette: fonte reale + multi-lingua" |
| `procedimento_en` | [String]? | Presente **solo** quando la fonte originale della ricetta era già in inglese (`kaggle-foodcom`, `wikibooks-en`) — in quel caso è il testo originale inglese, non una ritraduzione. `null` per le ricette con fonte italiana o senza fonte testuale. L'app Android mostra `procedimento_en` al posto di `procedimento_it` solo se la lingua di sistema del dispositivo è inglese |

## Pipeline di generazione

Script Python (non versionati in questo repo, vivono nell'ambiente di
sviluppo): downloader/estrattore per Wikibooks IT/EN (API MediaWiki
pubblica), pipeline Kaggle Food.com, tre moduli di ricette originali
scritte singolarmente (`ricette_reali.py`, `ricette_reali2.py`,
`ricette_reali3.py`), modulo di classificazione condiviso
(`tipo_pasto`/`cucina`/`tipo_dieta`/`prompt_immagine`) applicato in fase
di merge finale. Dettaglio delle decisioni prese in `DECISIONI.md` nel
repo principale, blocco "Ricette — scoperta".
