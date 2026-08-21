#!/usr/bin/env python3
"""Normalizza le tabelle di composizione CREA in un JSON analogo a ciqual_2025.json.

Fonte: CREA - Consiglio per la ricerca in agricoltura e l'analisi dell'economia
agraria, Centro di ricerca Alimenti e Nutrizione (ex INRAN) - Tabelle di
composizione degli alimenti, https://www.alimentinutrizione.it/
Uso libero confermato dal committente (citazione completa obbligatoria, vedi
attribuzione nel README del repo dati e nel badge in-app).

Schema di output, un oggetto per alimento:
{
  "nome": str,                    # gia' in italiano (CREA e' un dataset italiano)
  "food_code": str,               # codice CREA originale, stabile tra le versioni
  "categoria": str,                # una delle 19 categorie native CREA
  "carboidrati_disponibili": float,  # available_carbohydrates, gia' netto (std EU)
  "fibre": float,                  # total_fiber
  "grassi": float,                 # lipids
  "proteine": float,                # proteins
  "calorie": float,                 # energy_kcal
  "preparazione": str | null,       # solo per le 51 "Ricette Italiane" (crea_recipes.json)
  "ingredienti": str | null,        # idem, "nome qty, nome qty, ..."
  ...MICRONUTRIENTI_CAMPI (vedi sotto)  # minerali/vitamine/qualita' grassi, mg o g/100g
}

Micronutrienti aggiunti il 21 agosto 2026 (vedi DECISIONI.md, "Nota
backlog: micronutrienti"): stesso principio dei macro, mappatura diretta
1:1 dal CSV sorgente CREA (che li riporta gia' su 139 colonne totali),
nessuna conversione di unita' necessaria (il CSV e' gia' in mg o g per
100g, coerente con l'unita' usata per i macro). Selezionati solo i
campi discussi esplicitamente (minerali, vitamine, qualita' dei grassi
inclusi i singoli omega-3/6, colesterolo) — non tutte le 139 colonne
del CSV originale (es. amminoacidi, polifenoli/fitosteroli esclusi,
fuori dallo scope deciso).
"""
import csv
import json

CSV_PATH = "crea_food_composition_tables.csv"
RECIPES_PATH = "crea_recipes.json"
OUT_PATH = "crea_2026.json"

# Mappatura campo_output -> colonna_csv per i micronutrienti (mg/100g salvo
# indicato altrimenti). Chiave = nome campo nel JSON di output.
CAMPI_MICRONUTRIENTI = {
    # Minerali (mg/100g)
    "sodio": "sodium",
    "potassio": "potassium",
    "calcio": "calcium",
    "ferro": "iron",
    "magnesio": "magnesium",
    "zinco": "zinc",
    "fosforo": "phosphorus",
    "iodio": "iodine",
    "selenio": "selenium",
    "rame": "copper",
    "manganese": "manganese",
    # Vitamine (mg o µg/100g secondo la fonte, non convertito)
    "vitamina_a": "vitamin_a_retinol_equivalent",
    "vitamina_b1": "thiamine",
    "vitamina_b2": "riboflavin",
    "vitamina_b3": "niacin",
    "vitamina_b5": "pantothenic_acid",
    "vitamina_b6": "vitamin_b6",
    "vitamina_b7": "biotin",
    "vitamina_b9": "folate",
    "vitamina_b12": "vitamin_b12",
    "vitamina_c": "vitamin_c",
    "vitamina_d": "vitamin_d",
    "vitamina_e": "vitamin_e",
    "vitamina_k": "vitamin_k",
    # Qualita' dei grassi (g/100g)
    "colesterolo": "cholesterol",
    "grassi_saturi": "Saturated_fatty_acids",
    "grassi_monoinsaturi": "monounsaturated_fatty_acids",
    "grassi_polinsaturi": "polyunsaturated_fatty_acids",
    "omega3_ala": "C18:3_linolenic_acid",
    "omega3_epa": "C20:5_eicosapentaenoic_acid_EPA",
    "omega3_dha": "C22:6_docosahexaenoic_acid_DHA",
    "omega6_linoleico": "C18:2_linoleic_acid",
}


def parse_float(value: str) -> float:
    value = (value or "").strip()
    if not value:
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def carica_ricette() -> dict:
    ricette = {}
    with open(RECIPES_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            ingredienti = ", ".join(
                f"{ing['name']} {ing.get('quantity', '')}".strip()
                for ing in d.get("ingredients", [])
            )
            ricette[d["food_code"]] = {
                "preparazione": d.get("preparation") or None,
                "ingredienti": ingredienti or None,
            }
    return ricette


def main() -> None:
    ricette = carica_ricette()
    alimenti = []
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            food_code = row["food_code"].strip()
            ricetta = ricette.get(food_code, {})
            alimento = {
                "nome": row["name"].strip(),
                "food_code": food_code,
                "categoria": row["category"].strip(),
                "carboidrati_disponibili": parse_float(row["available_carbohydrates"]),
                "fibre": parse_float(row["total_fiber"]),
                "grassi": parse_float(row["lipids"]),
                "proteine": parse_float(row["proteins"]),
                "calorie": parse_float(row["energy_kcal"]),
                "preparazione": ricetta.get("preparazione"),
                "ingredienti": ricetta.get("ingredienti"),
            }
            for campo_output, colonna_csv in CAMPI_MICRONUTRIENTI.items():
                alimento[campo_output] = parse_float(row.get(colonna_csv, ""))
            alimenti.append(alimento)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(alimenti, f, ensure_ascii=False, indent=None, separators=(",", ":"))

    print(f"Scritti {len(alimenti)} alimenti in {OUT_PATH}")
    categorie = sorted({a["categoria"] for a in alimenti})
    print(f"Categorie ({len(categorie)}):")
    for c in categorie:
        print(f"  - {c}")
    con_ricetta = sum(1 for a in alimenti if a["preparazione"])
    print(f"Con ricetta/preparazione: {con_ricetta}")


if __name__ == "__main__":
    main()
