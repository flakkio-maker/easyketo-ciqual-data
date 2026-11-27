#!/usr/bin/env python3
"""Aggiunge il portoghese brasiliano a ricette_scoperta.json: nome_pt, procedimento_pt e
nome_pt su ogni ingrediente, dalle traduzioni in ricette_traduzioni_pt.json (chiave = id
ricetta). Controlla che ogni ricetta abbia lo stesso numero di ingredienti e di passi
dell'originale. Mantiene il formato del file (indent 2, a capo finale).

Uso: python3 -I unisci_traduzioni_ricette_pt.py ricette_scoperta.json ricette_traduzioni_pt.json
"""
import json
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        ricette = json.load(f)
    with open(sys.argv[2], encoding="utf-8") as f:
        tr = json.load(f)
    out = []
    for r in ricette:
        t = tr.get(str(r["id"]))
        if t is None:
            sys.exit(f"ricetta {r['id']} senza traduzione")
        ing = r.get("ingredienti", [])
        if len(t["ingredienti"]) != len(ing):
            sys.exit(f"ricetta {r['id']}: {len(t['ingredienti'])} ingredienti tradotti su {len(ing)}")
        base = r.get("procedimento_en") or r.get("procedimento_it") or []
        if len(t["procedimento"]) != len(base):
            sys.exit(f"ricetta {r['id']}: {len(t['procedimento'])} passi tradotti su {len(base)}")
        nuova = {}
        for k, v in r.items():
            if k == "ingredienti":
                v = [dict(i, nome_pt=t["ingredienti"][n]) for n, i in enumerate(v)]
            nuova[k] = v
            if k == "nome_de":
                nuova["nome_pt"] = t["nome"]
            if k == "procedimento_de":
                nuova["procedimento_pt"] = t["procedimento"]
        if "nome_pt" not in nuova:
            nuova["nome_pt"] = t["nome"]
        if "procedimento_pt" not in nuova:
            nuova["procedimento_pt"] = t["procedimento"]
        out.append(nuova)
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(out)} ricette con portoghese -> {sys.argv[1]}")


if __name__ == "__main__":
    main()
