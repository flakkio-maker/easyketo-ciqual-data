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
  "ingredienti": str | null         # idem, "nome qty, nome qty, ..."
}
"""
import csv
import json

CSV_PATH = "crea_food_composition_tables.csv"
RECIPES_PATH = "crea_recipes.json"
OUT_PATH = "crea_2026.json"


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
            alimenti.append({
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
            })

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
