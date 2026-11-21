# Dataset USDA FoodData Central — convertito per Ketorbit

`usda_2026.json` e' ricavato da **USDA FoodData Central**, la banca dati
ufficiale statunitense di composizione degli alimenti (U.S. Department of
Agriculture, Agricultural Research Service) — https://fdc.nal.usda.gov/.

**Licenza:** pubblico dominio, CC0 1.0 (dichiarata dall'USDA sulla pagina dei
download). Nessun obbligo di attribuzione; l'app cita comunque la fonte come
fa per le altre banche dati.

**Citazione consigliata dall'USDA:** U.S. Department of Agriculture,
Agricultural Research Service. FoodData Central, 2026. fdc.nal.usda.gov.

## Fonti usate (JSON ufficiali, scaricati il 21 novembre 2026)

| Dataset | File | Voci in fonte | Voci tenute |
|---|---|---|---|
| Foundation Foods | `FoodData_Central_foundation_food_json_2026-10-29.zip` | 424 | 373 |
| SR Legacy (ultima edizione, 2018) | `FoodData_Central_sr_legacy_food_json_2018-04.zip` | 7.793 | 7.703 |
| Survey (FNDDS 2021-2023) | `FoodData_Central_survey_food_json_2024-10-31.zip` | 5.432 | 5.326 |

**Totale: 13.402 alimenti.** **NON incluso: Branded Foods** (prodotti
confezionati, ~450 MB): Open Food Facts li copre gia' nell'app, sarebbero un
doppione.

- Foundation: alimenti generici analizzati in laboratorio, il dato piu'
  affidabile.
- SR Legacy: il riferimento storico (alimenti generici, anche fast food e
  prodotti di uso comune USA).
- Survey / FNDDS: alimenti e piatti **come vengono mangiati** negli USA
  (hamburger, pizza, burrito, piatti misti), utile per il diario.

## Conversione

Script: `converti_usda.py` (Python 3, solo libreria standard).
Ogni voce e' per **100 g** di parte edibile, nello stesso schema di
`uk_2025.json`:

| Campo app | Nutriente USDA (numero) | Note |
|---|---|---|
| `calorie` | Energy kcal (208; ripiego Atwater 957/958) | |
| `proteine` | Protein (203) | |
| `grassi` | Total lipid (fat) (204) | |
| `carboidrati_disponibili` | Carbohydrate by difference (205) **meno** Fiber (291) | mai negativi; stessa convenzione "netti di fibra" di CIQUAL/CREA/BLS/UK |
| `fibre` | Fiber, total dietary (291) | |
| minerali | 301 Ca, 303 Fe, 304 Mg, 305 P, 306 K, 307 Na, 309 Zn, 312 Cu, 314 I, 315 Mn, 317 Se | mg (iodio e selenio in ug) |
| vitamine | A RAE 320, B1 404, B2 405, B3 406, B5 410, B6 415, B7 416, B9 417 (ripiego 435), B12 418, C 401, D 328, E 323, K 430 | vitamina A/D/K/B9/B12/B7 in ug, le altre in mg |
| grassi | saturi 606, monoinsaturi 645, polinsaturi 646, colesterolo 601 | |
| omega | ALA 851, EPA 629, DHA 621, linoleico 618 | a differenza di CoFID (UK) USDA li riporta singolarmente |
| `categoria` | categoria USDA (food category / WWEIA category) | testo inglese nativo |
| `tipo_dato` | Foundation / SR Legacy / Survey (FNDDS) | informativo |
| `food_code` | `fdc-<fdcId>` | identificativo stabile USDA |

Regole (stesse delle altre fonti):
- una voce senza uno dei 4 campi obbligatori (kcal, carboidrati, grassi,
  proteine) e' scartata: nessun valore indovinato (50 Foundation, 1 Survey);
- un micronutriente mancante vale 0.0 e **non e' scritto** nel JSON (l'app lo
  legge come 0.0 di default): dimezza il file (8,5 MB invece di 10,7 MB);
- duplicati per nome (case-insensitive): si tiene la fonte piu' affidabile,
  Foundation > SR Legacy > Survey (196 voci);
- nomi **in inglese** (lingua nativa della fonte): niente `nome_it/fr/es/de`
  per ora. L'app ripiega sul nome inglese quando la traduzione manca.

## Aggiornamento

Per rigenerare: scaricare i tre zip dalla pagina dei download USDA, estrarli
in tre cartelle separate e lanciare
`python3 -I converti_usda.py CART_FOUNDATION CART_SR CART_SURVEY usda_2026.json`.
Foundation e Survey vengono ripubblicati da USDA (due volte l'anno circa);
SR Legacy e' fermo al 2018.
