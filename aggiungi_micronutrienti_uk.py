#!/usr/bin/env python3
"""Aggiunge i campi micronutrienti a uk_2025.json (gia' esistente),
leggendo il file ufficiale CoFID (McCance and Widdowson's Composition of
Foods Integrated Dataset, Public Health England / gov.uk). Vedi
DECISIONI.md "Nota backlog: micronutrienti".

Fonte: cofid_main.xlsx, tre fogli separati (non uno solo come BLS):
"1.4 Inorganics" (minerali), "1.5 Vitamins" (vitamine), "1.3 Proximates"
(macro + qualita' grassi + colesterolo — stesso foglio dei macro gia'
usati per uk_2025.json). Ogni foglio ha "Food Code" in colonna 0,
formato "13-146" — stesso food_code gia' presente in uk_2025.json.

Note sui valori:
- Celle con 'N' (non misurato/non presente), 'Tr' (tracce) o vuote ->
  0.0, stesso principio "non disponibile" delle altre tre fonti.
- **Nessun omega-3/omega-6 individuale**: a differenza di CIQUAL/CREA/
  BLS (che riportano singolarmente ALA/EPA/DHA e acido linoleico),
  CoFID nel foglio Proximates riporta solo i TOTALI "n-3 poly /100g
  food" e "n-6 poly /100g food" (somma di tutti gli acidi grassi n-3 o
  n-6, EPA/DHA/ALA inclusi insieme). Non e' la stessa granularita' dei
  campi omega3_ala/omega3_epa/omega3_dha/omega6_linoleico delle altre
  fonti: mappare il totale in uno solo di questi campi (es. "ala")
  sarebbe fuorviante (implicherebbe che sia solo ALA, quando include
  anche EPA/DHA). Lasciati tutti e 4 a 0.0 per CoFID — limite di
  granularita' della fonte, non un errore di estrazione.
- Grassi saturi/monoinsaturi/polinsaturi: usate le colonne "/100g food"
  (non "/100g FA", che sono percentuali relative alla frazione lipidica
  totale, non valori assoluti per 100g di alimento) — "Satd FA /100g
  fd", "Mono FA /100g food" (variante totale, non "cis-Mono" che
  esclude i trans), "Poly FA /100g food" (variante totale, stesso
  criterio).
- Vitamina K: solo K1 (fillochinone) disponibile nella fonte, nessuna
  colonna K2 — diverso da CIQUAL (K1+K2 sommati) e BLS (gia'
  aggregato). Sotto-stima possibile rispetto alle altre fonti per
  alimenti ricchi di K2 (es. formaggi fermentati, natto).
- Niacina: usato "Niacin equivalent" (include la conversione da
  triptofano), non "Niacin" grezzo — stessa scelta di BLS (NIAEQU).
"""
import json

XLSX_PATH = "cofid_main.xlsx"
UK_JSON_PATH = "uk_2025.json"

# Indici di colonna (0-based) nei rispettivi fogli, identificati dagli
# header ufficiali del file. Non letti a runtime dall'header per
# semplicita' (il file e' un vendor file esterno non versionato qui).
COLONNE_INORGANICS = {
    "sodio": 7, "potassio": 8, "calcio": 9, "magnesio": 10, "fosforo": 11,
    "ferro": 12, "rame": 13, "zinco": 14, "manganese": 16, "selenio": 17,
    "iodio": 18,
}
COLONNE_VITAMINS = {
    "vitamina_a": 9, "vitamina_d": 10, "vitamina_e": 11, "vitamina_k": 12,
    "vitamina_b1": 13, "vitamina_b2": 14, "vitamina_b3": 17,
    "vitamina_b6": 18, "vitamina_b12": 19, "vitamina_b9": 20,
    "vitamina_b5": 21, "vitamina_b7": 22, "vitamina_c": 23,
}
COLONNE_PROXIMATES = {
    "grassi_saturi": 27, "grassi_monoinsaturi": 35, "grassi_polinsaturi": 39,
    "colesterolo": 46,
}
# Campi senza fonte nella granularita' richiesta (vedi nota sopra) —
# sempre 0.0 per tutti gli alimenti CoFID.
CAMPI_SEMPRE_ZERO = ["omega3_ala", "omega3_epa", "omega3_dha", "omega6_linoleico"]


def to_float(v) -> float:
    if v is None:
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if not s or s in ("N", "Tr", "-"):
        return 0.0
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def leggi_foglio(wb, nome_foglio: str, colonne: dict) -> dict:
    ws = wb[nome_foglio]
    rows = ws.iter_rows(values_only=True)
    next(rows)  # intestazione riga 1
    risultato = {}
    for row in rows:
        if not row or not row[0]:
            continue
        food_code = str(row[0]).strip()
        risultato[food_code] = {
            campo: to_float(row[idx]) for campo, idx in colonne.items()
        }
    return risultato


def main() -> None:
    import openpyxl

    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    inorganics = leggi_foglio(wb, "1.4 Inorganics", COLONNE_INORGANICS)
    vitamins = leggi_foglio(wb, "1.5 Vitamins", COLONNE_VITAMINS)
    proximates = leggi_foglio(wb, "1.3 Proximates", COLONNE_PROXIMATES)

    with open(UK_JSON_PATH, encoding="utf-8") as f:
        alimenti = json.load(f)

    trovati = 0
    for alimento in alimenti:
        food_code = alimento["food_code"]
        valori = {}
        valori.update(inorganics.get(food_code, {}))
        valori.update(vitamins.get(food_code, {}))
        valori.update(proximates.get(food_code, {}))
        for campo in CAMPI_SEMPRE_ZERO:
            valori[campo] = 0.0
        # Riempie eventuali campi mancanti (foglio senza quel food_code)
        for campo in list(COLONNE_INORGANICS) + list(COLONNE_VITAMINS) + list(COLONNE_PROXIMATES):
            valori.setdefault(campo, 0.0)
        if food_code in inorganics or food_code in vitamins or food_code in proximates:
            trovati += 1
        alimento.update(valori)

    with open(UK_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(alimenti, f, ensure_ascii=False, indent=None, separators=(",", ":"))

    print(f"Alimenti totali: {len(alimenti)}")
    print(f"Con almeno un match nei fogli dati: {trovati}")
    print(f"Senza alcun match: {len(alimenti) - trovati}")


if __name__ == "__main__":
    main()
