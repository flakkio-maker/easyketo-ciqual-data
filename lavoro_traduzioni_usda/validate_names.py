#!/usr/bin/env python3
"""Uso: python3 -I validate_names.py in.json out.json LINGUE(csv)  -> exit 0 solo se completo."""
import json,sys
src=json.load(open(sys.argv[1],encoding="utf-8")); out=json.load(open(sys.argv[2],encoding="utf-8")); langs=sys.argv[3].split(",")
ids=[r["id"] for r in src]; bad=[]
if set(out)!=set(ids): bad.append(f"id: mancano {sorted(set(ids)-set(out))[:5]} extra {sorted(set(out)-set(ids))[:5]}")
for r in src:
    o=out.get(r["id"])
    if not isinstance(o,dict): continue
    for l in langs:
        t=o.get(l)
        if not isinstance(t,str) or not t.strip(): bad.append(f"{r['id']}: manca {l}")
        elif "\n" in t or t!=t.strip(): bad.append(f"{r['id']}: {l} con spazi/newline")
print(f"{len(ids)} voci, {len(out)} tradotte, {len(bad)} problemi")
for b in bad[:40]: print(" -",b)
sys.exit(1 if bad else 0)
