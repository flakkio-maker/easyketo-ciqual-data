# Dataset CIQUAL 2025 — convertito per App Cheto

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
- Nomi alimenti in **inglese** (`alim_nom_eng`), non in francese né tradotti
  in italiano: sono le traduzioni ufficiali fornite da ANSES nello stesso
  file sorgente, per evitare il rischio di una traduzione italiana
  approssimativa fatta a mano su 3.484 voci senza revisione umana.
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

Script di conversione non incluso in questo commit (girato una tantum in
locale); la logica è documentata qui per riproducibilità futura se il
dataset dovesse essere rigenerato per un aggiornamento CIQUAL successivo.
