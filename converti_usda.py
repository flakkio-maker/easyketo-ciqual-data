#!/usr/bin/env python3
"""Converte USDA FoodData Central (alimenti generici) in usda_2026.json,
nello stesso schema di uk_2025.json / bls_2025.json / ciqual_2025.json.

Fonti (scaricate da https://fdc.nal.usda.gov/download-datasets/, JSON):
  - Foundation Foods   FoodData_Central_foundation_food_json_2026-10-29.zip
  - SR Legacy          FoodData_Central_sr_legacy_food_json_2018-04.zip
  - Survey (FNDDS)     FoodData_Central_survey_food_json_2024-10-31.zip
NON incluso di proposito: Branded Foods (prodotti confezionati). Open Food
Facts li copre gia' nell'app e sarebbero un doppione.

Licenza: USDA FoodData Central e' di pubblico dominio (CC0 1.0). Citazione
consigliata dall'USDA: U.S. Department of Agriculture, Agricultural Research
Service. FoodData Central, 2026. fdc.nal.usda.gov.

Uso:
  python3 -I converti_usda.py CARTELLA_FOUNDATION CARTELLA_SR CARTELLA_SURVEY usda_2026.json
(ogni cartella contiene il .json estratto dal rispettivo zip)

Convenzioni (identiche alle altre fonti, vedi README_UK.md):
  - valori per 100 g di parte edibile; kcal, g, mg, ug come nella fonte USDA
  - carboidrati_disponibili = carboidrati totali (per differenza) - fibra,
    mai negativi; stessa convenzione "netti di fibra" di CIQUAL/CREA/BLS/UK
  - un valore mancante per un micronutriente -> 0.0; un valore mancante per
    uno dei 4 campi obbligatori (kcal, carboidrati, grassi, proteine) -> voce
    scartata, nessun valore indovinato
  - i micronutrienti uguali a 0 non sono scritti nel JSON (default 0.0 lato app)
  - nomi in inglese (lingua nativa della fonte): nome_it/fr/es/de assenti
  - duplicati per nome: si tiene la fonte piu' affidabile
    (Foundation > SR Legacy > Survey)
"""
import glob
import json
import os
import re
import sys

# campo app -> numero nutriente USDA (nutrient.number), in ordine di preferenza
NUTRIENTI = {
    "calorie": ["208", "957", "958"],
    "proteine": ["203"],
    "grassi": ["204"],
    "_carbo_totali": ["205", "205.2"],
    "fibre": ["291"],
    "sodio": ["307"], "potassio": ["306"], "calcio": ["301"], "ferro": ["303"],
    "magnesio": ["304"], "zinco": ["309"], "fosforo": ["305"], "iodio": ["314"],
    "selenio": ["317"], "rame": ["312"], "manganese": ["315"],
    "vitamina_a": ["320"], "vitamina_b1": ["404"], "vitamina_b2": ["405"],
    "vitamina_b3": ["406"], "vitamina_b5": ["410"], "vitamina_b6": ["415"],
    "vitamina_b7": ["416"], "vitamina_b9": ["417", "435"], "vitamina_b12": ["418"],
    "vitamina_c": ["401"], "vitamina_d": ["328"], "vitamina_e": ["323"],
    "vitamina_k": ["430"], "colesterolo": ["601"],
    "grassi_saturi": ["606"], "grassi_monoinsaturi": ["645"], "grassi_polinsaturi": ["646"],
    "omega3_ala": ["851"], "omega3_epa": ["629"], "omega3_dha": ["621"],
    "omega6_linoleico": ["618"],
}
OBBLIGATORI = ["calorie", "proteine", "grassi", "_carbo_totali"]
ORDINE_CAMPI = [
    "nome", "food_code", "carboidrati_disponibili", "fibre", "grassi", "proteine",
    "calorie", "categoria", "tipo_dato", "sodio", "potassio", "calcio", "magnesio",
    "fosforo", "ferro", "rame", "zinco", "manganese", "selenio", "iodio",
    "vitamina_a", "vitamina_d", "vitamina_e", "vitamina_k", "vitamina_b1",
    "vitamina_b2", "vitamina_b3", "vitamina_b6", "vitamina_b12", "vitamina_b9",
    "vitamina_b5", "vitamina_b7", "vitamina_c", "grassi_saturi",
    "grassi_monoinsaturi", "grassi_polinsaturi", "colesterolo", "omega3_ala",
    "omega3_epa", "omega3_dha", "omega6_linoleico",
]


CAMPI_SEMPRE = {"nome", "food_code", "carboidrati_disponibili", "fibre", "grassi", "proteine", "calorie", "categoria", "tipo_dato"}


def carica(cartella, chiave):
    percorsi = glob.glob(os.path.join(cartella, "*.json"))
    if len(percorsi) != 1:
        sys.exit(f"{cartella}: atteso un solo .json, trovati {len(percorsi)}")
    with open(percorsi[0], encoding="utf-8") as f:
        return json.load(f)[chiave]


def valori_nutrienti(alimento):
    per_numero = {}
    for fn in alimento.get("foodNutrients", []):
        numero = str((fn.get("nutrient") or {}).get("number", ""))
        amount = fn.get("amount")
        if numero and amount is not None and numero not in per_numero:
            per_numero[numero] = float(amount)
    out = {}
    for campo, numeri in NUTRIENTI.items():
        for n in numeri:
            if n in per_numero:
                out[campo] = per_numero[n]
                break
    return out


def converti(alimento, tipo_dato, categoria):
    nome = re.sub(r"\s+", " ", (alimento.get("description") or "")).strip()
    if not nome:
        return None
    v = valori_nutrienti(alimento)
    if any(c not in v for c in OBBLIGATORI):
        return None
    fibra = max(v.get("fibre", 0.0), 0.0)
    netti = max(v["_carbo_totali"] - fibra, 0.0)
    riga = {
        "nome": nome,
        "food_code": f"fdc-{alimento['fdcId']}",
        "carboidrati_disponibili": round(netti, 2),
        "fibre": round(fibra, 2),
        "grassi": round(max(v["grassi"], 0.0), 2),
        "proteine": round(max(v["proteine"], 0.0), 2),
        "calorie": round(max(v["calorie"], 0.0), 1),
        "categoria": categoria,
        "tipo_dato": tipo_dato,
    }
    for campo in ORDINE_CAMPI:
        if campo not in riga:
            riga[campo] = round(max(v.get(campo, 0.0), 0.0), 3)
    # Micronutrienti a zero omessi dal JSON (l'app li legge come 0.0 di
    # default): dimezza il file senza perdere informazione.
    return {k: riga[k] for k in ORDINE_CAMPI if k in CAMPI_SEMPRE or riga[k] != 0}


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    d_found, d_sr, d_survey, out = sys.argv[1:]
    sorgenti = [
        ("Foundation", carica(d_found, "FoundationFoods"),
         lambda a: (a.get("foodCategory") or {}).get("description")),
        ("SR Legacy", carica(d_sr, "SRLegacyFoods"),
         lambda a: (a.get("foodCategory") or {}).get("description")),
        ("Survey (FNDDS)", carica(d_survey, "SurveyFoods"),
         lambda a: (a.get("wweiaFoodCategory") or {}).get("wweiaFoodCategoryDescription")),
    ]
    risultato, visti, stats = [], set(), {}
    for tipo, lista, cat in sorgenti:
        tenuti = scartati_dati = duplicati = 0
        for a in lista:
            riga = converti(a, tipo, cat(a))
            if riga is None:
                scartati_dati += 1
                continue
            chiave = riga["nome"].lower()
            if chiave in visti:
                duplicati += 1
                continue
            visti.add(chiave)
            risultato.append(riga)
            tenuti += 1
        stats[tipo] = (len(lista), tenuti, scartati_dati, duplicati)
    risultato.sort(key=lambda r: r["nome"].lower())
    with open(out, "w", encoding="utf-8") as f:
        json.dump(risultato, f, ensure_ascii=False, separators=(",", ":"))
    for tipo, (tot, ok, sc, dup) in stats.items():
        print(f"{tipo}: {tot} in fonte, {ok} tenuti, {sc} scartati (dati mancanti), {dup} duplicati per nome")
    print(f"TOTALE {len(risultato)} alimenti -> {out} ({os.path.getsize(out)/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
