# Dataset CIQUAL 2025 — convertito per EasyKeto

`ciqual_2025.json` è ricavato dalla Table Ciqual 2025 (ANSES, Agence
nationale de sécurité sanitaire de l'alimentation, de l'environnement et du
travail), pubblicata con Licence Ouverte / Open Licence Etalab 2.0.

Fonte ufficiale: https://ciqual.anses.fr/ (dataset anche su
https://entrepot.recherche.data.gouv.fr/, DOI 10.57745/RDMHWY).

## Conversione

Partendo dai file XML ufficiali (`alim`, `alim_grp`, `compo`, `const`), per
ogni alimento sono stati estratti i cinque costituenti necessari all'app:

| Campo app | Costituente CIQUAL | Codice |
|---|---|---|
| `carboidrati_disponibili` | Glucides (g/100 g) | 31000 |
| `fibre` | Fibres alimentaires (g/100 g) | 34100 |
| `grassi` | Lipides (g/100 g) | 40000 |
| `proteine` | Protéines, N x facteur de Jones (g/100 g), fallback N x 6.25 | 25000 / 25003 |
| `calorie` | Energie, Règlement UE N° 1169/2011 (kcal/100 g) | 328 |

Note sulla conversione:
- Nomi alimenti in **inglese** (`nome`, da `alim_nom_eng`): sono le traduzioni
  ufficiali fornite da ANSES nello stesso file sorgente, usate come nome
  canonico/fallback per tutte le lingue.
- Nomi alimenti in **italiano** (`nome_it`): traduzione manuale di tutti i
  3.323 nomi inglesi sopra, aggiunta successivamente su richiesta esplicita
  (nessuna traduzione ufficiale ANSES disponibile in italiano). Usata in UI
  quando la lingua del dispositivo è italiano, con fallback su `nome` se
  mancante (vedi `RemoteRepositories.kt`, `nomeVisualizzato`). Non è una
  traduzione certificata ANSES: qualità "best effort", da rivedere se emergono
  imprecisioni in uso reale.
- Nomi alimenti in **inglese curato** (`nome_en`), **francese** (`nome_fr`),
  **spagnolo** (`nome_es`) e **tedesco** (`nome_de`): stessa logica di
  `nome_it` sopra, aggiunti insieme (12 agosto 2026, task #236 dell'app) per
  coprire tutte le lingue di sistema supportate. `nome_en` è DISTINTO dal
  campo `nome`: quest'ultimo resta il nome ufficiale ANSES grezzo (a volte
  tecnico/asciutto, usato come fallback ultimo se manca tutto il resto),
  mentre `nome_en` è una traduzione curata con lo stesso stile naturale delle
  altre lingue — per la maggior parte delle voci coincide con `nome` quando
  quest'ultimo era già naturale, ma non sempre (alcuni refusi/imprecisioni del
  dato sorgente ANSES sono stati corretti solo in `nome_en`, mai in `nome`).
  La lingua mostrata all'utente segue la lingua di sistema del dispositivo,
  con fallback su `nome` se mancano sia la lingua richiesta sia l'inglese
  (vedi `scegliTraduzioneAlimento`, `TraduzioneAlimentoUseCase.kt`).
- Valori "traces" (quantità rilevata ma non quantificabile con precisione)
  sono mappati a `0.0`. Diverso da "-" (dato non determinato per
  quell'alimento), che resta un valore assente e fa scartare l'alimento se
  riguarda uno dei 5 campi obbligatori.
- Valori "< X" (sotto soglia di rilevazione) sono mappati al valore numerico
  stesso (approssimazione accettabile per un valore già vicino a zero).
- Alimenti a cui manca uno dei 4 campi obbligatori (carboidrati, grassi,
  proteine, calorie) sono esclusi dal dataset finale, invece di comparire
  con un valore inventato: su 3.484 alimenti originali, **3.323** sono
  passati nel file finale (161 esclusi, perlopiù frutti esotici rari e
  varianti di formaggio poco comuni).
- `fibre` è opzionale nel dataset di origine ma non nel modello dati
  dell'app: se assente viene impostata a `0.0`.
- `categoria` è il gruppo alimentare di primo livello (11 gruppi, es.
  "meat, egg and fish", "cereal products").

Script di conversione originale (macro) non incluso in questo commit
(girato una tantum in locale); la logica è documentata qui per
riproducibilità futura se il dataset dovesse essere rigenerato per un
aggiornamento CIQUAL successivo.

## Micronutrienti (aggiunti il 21 agosto 2026)

Vedi `DECISIONI.md` nel repo principale, "Nota backlog: micronutrienti" e
il blocco "Micronutrienti CIQUAL implementati". A differenza della
conversione macro sopra, lo script per questo passaggio **è incluso**:
`aggiungi_micronutrienti_ciqual.py`, che incrocia `alim_2025_11_03.xml`
(alim_code ↔ nome inglese) e `compo_2025_11_03.xml` (alim_code +
const_code → valore) contro `ciqual_2025.json` già esistente, senza
toccare i campi macro/traduzioni già presenti.

32 campi aggiunti, stessa struttura di `crea_2026.json` (vedi
`README_CREA.md` per la tabella completa dei nomi campo): 11 minerali,
13 vitamine, 8 di qualità dei grassi. Note specifiche CIQUAL (diverse da
CREA):

- **Biotina (`vitamina_b7`) sempre 0.0**: CIQUAL non include questo
  nutriente nella sua tabella ufficiale (verificato cercando nel
  dizionario `const_2025_11_03.xml` — nessun codice corrispondente).
  Non è un bug di estrazione, è un limite della fonte.
- **`vitamina_k`** è la somma di K1 (`const_code` 54101) e K2 (54104):
  CIQUAL li separa, CREA no — sommati per restare comparabili.
- **Copertura match**: 3.322 alimenti su 3.323 hanno trovato un
  `alim_code` corrispondente per nome (99,97%); un solo alimento
  ("Biscuit (cookie), snack with chocolate filling, whole wheat") non ha
  trovato corrispondenza esatta nel nome inglese XML — resta a 0.0 su
  tutti i 32 campi micronutrienti, macro invariati.
- Stesso trattamento "< X" già usato per i macro (vedi sopra): valore
  numerico preso come approssimazione.

File sorgente XML (`alim_2025_11_03.xml`, `compo_2025_11_03.xml`) NON
committati in questo repo (troppo grandi/vendor, stessa scelta già presa
per `crea_food_composition_tables.csv` — vedi `README_CREA.md`): vanno
riottenuti dal sito ANSES per una futura rigenerazione.
