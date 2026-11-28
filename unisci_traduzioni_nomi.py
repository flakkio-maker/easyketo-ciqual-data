#!/usr/bin/env python3
"""Aggiunge ai dataset alimentari le traduzioni dei nomi (nome_pt, nome_en, ...), da un file di
traduzioni `traduzioni_<db>.json` del tipo {"<indice riga>": {"fonte": "<nome originale>", "pt": "..."}}.

- La chiave e' la POSIZIONE della voce nel dataset (alcuni dataset non hanno un codice univoco).
- `fonte` e' il nome originale al momento della traduzione: se non coincide con `nome` della riga,
  l'unione si ferma (il dataset e' cambiato: ritradurre, non mescolare voci diverse).
- Aggiunge solo i campi mancanti (non sovrascrive); le nuove chiavi `nome_<lingua>` vengono inserite
  subito dopo l'ultimo campo `nome*` esistente. Formato del file invariato (JSON compatto).

Uso: python3 -I unisci_traduzioni_nomi.py ciqual_2025.json traduzioni_ciqual.json pt
     python3 -I unisci_traduzioni_nomi.py crea_2026.json traduzioni_crea.json en,fr,es,de,pt
"""
import json
import sys


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    dati = json.load(open(sys.argv[1], encoding="utf-8"))
    tr = json.load(open(sys.argv[2], encoding="utf-8"))
    lingue = sys.argv[3].split(",")
    if len(tr) != len(dati):
        sys.exit(f"traduzioni per {len(tr)} voci, dataset di {len(dati)}")
    aggiunti = 0
    out = []
    for i, r in enumerate(dati):
        t = tr.get(str(i))
        if t is None:
            sys.exit(f"voce {i} senza traduzione")
        if (t["fonte"] or "").strip() != (r["nome"] or "").strip():
            sys.exit(f"voce {i}: il nome originale e' cambiato ({t['fonte']!r} vs {r['nome']!r})")
        nuove = {}
        for l in lingue:
            testo = (t.get(l) or "").strip()
            if not testo:
                sys.exit(f"voce {i}: manca {l}")
            if not (r.get("nome_" + l) or "").strip():
                nuove["nome_" + l] = testo
        chiavi = list(r.keys())
        ultima = max(k for k, c in enumerate(chiavi) if c.startswith("nome"))
        n = {}
        for k, c in enumerate(chiavi):
            n[c] = r[c]
            if k == ultima:
                n.update(nuove)
        aggiunti += len(nuove)
        out.append(n)
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(out)} voci, {aggiunti} traduzioni aggiunte -> {sys.argv[1]}")


if __name__ == "__main__":
    main()
