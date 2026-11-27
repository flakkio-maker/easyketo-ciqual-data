#!/usr/bin/env python3
"""Aggiunge nome_en/nome_fr/nome_es/nome_de agli ingredienti di ricette_scoperta.json, dalle
traduzioni in ingredienti_traduzioni.json (chiave = nome italiano dell'ingrediente, `nome_it`).
Solo se il campo manca (non sovrascrive). Mantiene il formato del file (indent 2, a capo finale).

Uso: python3 -I unisci_traduzioni_ingredienti.py ricette_scoperta.json ingredienti_traduzioni.json
"""
import json
import sys

LINGUE = ["en", "fr", "es", "de"]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    ricette = json.load(open(sys.argv[1], encoding="utf-8"))
    tr = json.load(open(sys.argv[2], encoding="utf-8"))
    aggiunti = 0
    for r in ricette:
        nuovi = []
        for i in r.get("ingredienti", []):
            chiave = (i.get("nome_it") or i["nome"]).strip()
            t = tr.get(chiave)
            if t is None:
                sys.exit(f"ricetta {r['id']}: ingrediente senza traduzione: {chiave!r}")
            n = {}
            for k, v in i.items():
                n[k] = v
                if k == "nome_it":
                    for l in LINGUE:
                        if not i.get("nome_" + l):
                            n["nome_" + l] = t[l]
                            aggiunti += 1
            if "nome_en" not in n:  # ingrediente senza nome_it: aggiungi in coda
                for l in LINGUE:
                    n.setdefault("nome_" + l, t[l])
            nuovi.append(n)
        r["ingredienti"] = nuovi
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        f.write(json.dumps(ricette, ensure_ascii=False, indent=2) + "\n")
    print(f"{aggiunti} traduzioni aggiunte a {sum(len(r['ingredienti']) for r in ricette)} ingredienti")


if __name__ == "__main__":
    main()
