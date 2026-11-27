#!/usr/bin/env python3
"""Aggiunge nome_en/nome_it/nome_fr/nome_es/nome_de a taco_2011.json dalle traduzioni
in taco_traduzioni.json (chiave = food_code "taco-N"). Il nome canonico `nome` resta il
portoghese nativo della TACO. Va rilanciato dopo converti_taco.py (che rigenera il JSON
senza traduzioni). Controlla la copertura: nessuna voce senza le 5 lingue.

Uso: python3 -I unisci_traduzioni_taco.py taco_2011.json taco_traduzioni.json
"""
import json
import sys

LINGUE = ["en", "it", "fr", "es", "de"]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        dati = json.load(f)
    with open(sys.argv[2], encoding="utf-8") as f:
        tr = json.load(f)
    mancanti = [r["food_code"] for r in dati if r["food_code"] not in tr]
    if mancanti:
        sys.exit(f"voci senza traduzione: {mancanti[:10]} (totale {len(mancanti)})")
    out = []
    for r in dati:
        t = tr[r["food_code"]]
        nuova = {}
        for k, v in r.items():
            nuova[k] = v
            if k == "nome":
                for l in LINGUE:
                    testo = (t.get(l) or "").strip()
                    if not testo:
                        sys.exit(f"{r['food_code']}: manca {l}")
                    nuova[f"nome_{l}"] = testo
        out.append(nuova)
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(out)} voci con {len(LINGUE)} traduzioni -> {sys.argv[1]}")


if __name__ == "__main__":
    main()
