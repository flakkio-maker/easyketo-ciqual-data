#!/usr/bin/env python3
"""Aggiunge i campi micronutrienti a ciqual_2025.json (gia' esistente),
incrociando i file XML ufficiali ANSES (alim/compo/const) tramite
alim_code/const_code. Vedi DECISIONI.md "Nota backlog: micronutrienti" e
questa cartella per il dettaglio.

Fonte: Table Ciqual 2025 (ANSES), file XML ufficiali const/alim/compo.
Licence Ouverte Etalab 2.0 (stessa licenza gia' usata per ciqual_2025.json).

Join: alim.xml (alim_code <-> alim_nom_eng) <-> ciqual_2025.json (nome ==
alim_nom_eng, il campo "nome" e' sempre il nome inglese originale, vedi
Entities.kt CiqualAlimentoEntity) <-> compo.xml (alim_code + const_code ->
teneur) per i const_code elencati in CAMPI_MICRONUTRIENTI sotto.

Note sui valori:
- teneur puo' essere "< X" (sotto soglia di rilevamento, XML-escaped
  "&lt; X"): interpretato come X (stima per eccesso, piu' informativo di
  0 pur restando un'approssimazione — diverso dal trattamento CREA dove
  il CSV sorgente non distingue affatto i due casi).
- Nessun alimento/nutriente completamente assente da compo.xml per una
  coppia (alim_code, const_code) -> 0.0, stesso principio "non
  disponibile" gia' usato per CREA.
- Biotina (vitamina B7): CIQUAL non la include come nutriente (verificato
  cercando nel dizionario const.xml, nessun code corrispondente) —
  resta sempre 0.0 per tutti gli alimenti CIQUAL, a differenza di CREA
  che invece la riporta. Non un bug, e' un limite della fonte.
- Vitamina K: CIQUAL separa K1 (const 54101) e K2 (54104) — sommati per
  ottenere un valore "vitamina_k" comparabile alla colonna unica di CREA.
- Vitamina A: usato il code 51104 (retinol equivalent), coerente con la
  colonna CREA "vitamin_a_retinol_equivalent".
- Vitamina B9: usato il code 56700 (folati totali), non la variante DFE
  (56702) ne' l'acido folico da fortificazione da solo (56708) — stessa
  granularita' "folati totali" della colonna CREA "folate".
"""
import html
import json
import re

ALIM_PATH = "alim_2025_11_03.xml"
COMPO_PATH = "compo_2025_11_03.xml"
CIQUAL_JSON_PATH = "ciqual_2025.json"

# campo_output -> singolo const_code, oppure lista di const_code da sommare
# (solo vitamina_k: K1+K2)
CAMPI_MICRONUTRIENTI = {
    "sodio": "10110",
    "potassio": "10190",
    "calcio": "10200",
    "ferro": "10260",
    "magnesio": "10120",
    "zinco": "10300",
    "fosforo": "10150",
    "iodio": "10530",
    "selenio": "10340",
    "rame": "10290",
    "manganese": "10251",
    "vitamina_a": "51104",
    "vitamina_b1": "56100",
    "vitamina_b2": "56200",
    "vitamina_b3": "56310",
    "vitamina_b5": "56400",
    "vitamina_b6": "56500",
    "vitamina_b7": None,  # biotina non presente nella fonte CIQUAL
    "vitamina_b9": "56700",
    "vitamina_b12": "56600",
    "vitamina_c": "55100",
    "vitamina_d": "52100",
    "vitamina_e": "53100",
    "vitamina_k": ["54101", "54104"],
    "colesterolo": "75100",
    "grassi_saturi": "40302",
    "grassi_monoinsaturi": "40303",
    "grassi_polinsaturi": "40304",
    "omega3_ala": "41833",
    "omega3_epa": "42053",
    "omega3_dha": "42263",
    "omega6_linoleico": "41826",
}


def parse_teneur(raw: str) -> float:
    raw = html.unescape(raw.strip()).replace("<", "").strip()
    raw = raw.replace(",", ".")
    if not raw:
        return 0.0
    try:
        return float(raw)
    except ValueError:
        return 0.0


def carica_alim_code_per_nome() -> dict:
    content = open(ALIM_PATH, encoding="utf-8").read()
    mapping = {}
    for blocco in re.findall(r"<ALIM>(.*?)</ALIM>", content, re.S):
        code = re.search(r"<alim_code>\s*(\S+)\s*</alim_code>", blocco)
        eng = re.search(r"<alim_nom_eng>\s*(.*?)\s*</alim_nom_eng>", blocco, re.S)
        if code and eng:
            nome = html.unescape(eng.group(1).strip())
            if nome not in mapping:  # primo occorrenza vince sui rari duplicati
                mapping[nome] = code.group(1).strip()
    return mapping


def carica_compo() -> dict:
    """Ritorna {(alim_code, const_code): valore_float}."""
    content = open(COMPO_PATH, encoding="utf-8").read()
    compo = {}
    for blocco in re.findall(r"<COMPO>(.*?)</COMPO>", content, re.S):
        alim = re.search(r"<alim_code>\s*(\S+)\s*</alim_code>", blocco)
        const = re.search(r"<const_code>\s*(\S+)\s*</const_code>", blocco)
        teneur = re.search(r"<teneur[^>]*>([^<]*)</teneur>", blocco)
        if alim and const and teneur:
            compo[(alim.group(1).strip(), const.group(1).strip())] = parse_teneur(teneur.group(1))
    return compo


def main() -> None:
    alim_code_per_nome = carica_alim_code_per_nome()
    compo = carica_compo()

    with open(CIQUAL_JSON_PATH, encoding="utf-8") as f:
        alimenti = json.load(f)

    trovati = 0
    for alimento in alimenti:
        alim_code = alim_code_per_nome.get(alimento["nome"])
        if alim_code is None:
            for campo in CAMPI_MICRONUTRIENTI:
                alimento[campo] = 0.0
            continue
        trovati += 1
        for campo, const_code in CAMPI_MICRONUTRIENTI.items():
            if const_code is None:
                alimento[campo] = 0.0
            elif isinstance(const_code, list):
                alimento[campo] = sum(compo.get((alim_code, c), 0.0) for c in const_code)
            else:
                alimento[campo] = compo.get((alim_code, const_code), 0.0)

    with open(CIQUAL_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(alimenti, f, ensure_ascii=False, indent=None, separators=(",", ":"))

    print(f"Alimenti totali: {len(alimenti)}")
    print(f"Con alim_code trovato (micronutrienti reali): {trovati}")
    print(f"Senza match (micronutrienti a 0.0): {len(alimenti) - trovati}")


if __name__ == "__main__":
    main()
