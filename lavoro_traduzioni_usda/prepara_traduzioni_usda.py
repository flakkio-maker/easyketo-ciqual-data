#!/usr/bin/env python3
"""Assembla output/out_usda_NN.json (chiave = indice riga di usda_2026.json) in traduzioni_usda.json,
nel formato richiesto da ../unisci_traduzioni_nomi.py: {"<indice>": {"fonte": nome, "it":..,"fr":..,"es":..,"de":..,"pt":..}}.
Uso (dalla radice del repo): python3 -I lavoro_traduzioni_usda/prepara_traduzioni_usda.py
Si ferma se manca qualche voce (per verificare lo stato senza unire: stampa i lotti mancanti)."""
import glob, json, os, sys
base = os.path.dirname(os.path.abspath(__file__))
usda = json.load(open(os.path.join(base, "..", "usda_2026.json"), encoding="utf-8"))
tr = {}
for f in sorted(glob.glob(os.path.join(base, "output", "out_usda_*.json"))):
    for k, v in json.load(open(f, encoding="utf-8")).items():
        tr[k] = v
manca = [i for i in range(len(usda)) if str(i) not in tr]
if manca:
    lotti = sorted({i // 298 + 1 for i in manca})
    sys.exit(f"mancano {len(manca)} voci, lotti: {lotti}")
out = {}
for i, r in enumerate(usda):
    out[str(i)] = {"fonte": r["nome"], **{l: tr[str(i)][l].strip() for l in ("it", "fr", "es", "de", "pt")}}
json.dump(out, open(os.path.join(base, "..", "traduzioni_usda.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("scritto traduzioni_usda.json:", len(out), "voci")
