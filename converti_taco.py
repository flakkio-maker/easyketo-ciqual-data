#!/usr/bin/env python3
"""Converte la TACO (Tabela Brasileira de Composicao de Alimentos, 4a ed. rev. e
ampliada, NEPA/UNICAMP, 2011) in taco_2011.json, nello stesso schema di
usda_2026.json / crea_2026.json.

Fonte: PDF ufficiale della 4a edizione (copia ospitata dal Conselho Federal de
Nutricionistas), https://www.cfn.org.br/wp-content/uploads/2017/03/taco_4_edicao_ampliada_e_revisada.pdf
Il NEPA non offre un file di dati: la tabella esiste solo come PDF, quindi si
estrae il testo con `pdftotext -layout` (poppler) e lo si interpreta qui.

Licenza/uso: la pubblicazione dichiara (frontespizio): "E permitida a
reproducao total ou parcial do material, desde que seja citada a fonte."
Nessuna licenza formale (non e' CC0/CC BY), nessun divieto esplicito di uso
commerciale. Citazione obbligatoria: NEPA/UNICAMP. Tabela Brasileira de
Composicao de Alimentos - TACO. 4a edicao revisada e ampliada. Campinas, 2011.
Vedi README_TACO.md e NOTICE.md dell'app.

Uso:
  pdftotext -layout taco_4_edicao_ampliada_e_revisada.pdf taco.txt
  python3 -I converti_taco.py taco.txt taco_2011.json

Convenzioni (identiche alle altre fonti, vedi README_USDA.md):
  - valori per 100 g di parte edibile
  - carboidrati_disponibili = carboidrati totali (per differenza) - fibra,
    mai negativi (stessa convenzione "netti di fibra" di CIQUAL/CREA/BLS/UK/USDA)
  - "Tr" (traccia, valore arrotondato tra 0 e la soglia) -> 0.0
  - "NA" (non applicabile), "*" (analisi in rivalutazione) o cella vuota ->
    valore assente: per i 4 campi obbligatori (kcal, carboidrati, grassi,
    proteine) la voce e' scartata, nessun valore indovinato; per i
    micronutrienti il campo non e' scritto (l'app lo legge come 0.0)
  - lettere di nota a margine di un valore ("20a") ignorate
  - nomi in portoghese (lingua nativa): niente nome_it/en/fr/es/de
  - vitamina_a = RAE; se manca, retinolo (per gli alimenti animali coincidono);
    mai RE (equivalenti di retinolo: sovrastima i carotenoidi rispetto a RAE)
"""
import json
import os
import re
import sys

OBBLIGATORI = ["calorie", "proteine", "grassi", "_carbo_totali"]
ORDINE_CAMPI = [
    "nome", "food_code", "carboidrati_disponibili", "fibre", "grassi", "proteine",
    "calorie", "categoria", "sodio", "potassio", "calcio", "magnesio", "fosforo",
    "ferro", "rame", "zinco", "manganese", "vitamina_a", "vitamina_b1",
    "vitamina_b2", "vitamina_b3", "vitamina_b6", "vitamina_c", "grassi_saturi",
    "grassi_monoinsaturi", "grassi_polinsaturi", "colesterolo",
]
CAMPI_SEMPRE = {"nome", "food_code", "carboidrati_disponibili", "fibre", "grassi",
                "proteine", "calorie", "categoria"}

# Tabella 1, blocco A: colonne dopo la descrizione, nell'ordine di stampa.
COL_A = ["umidade", "calorie", "_kj", "proteine", "grassi", "colesterolo",
         "_carbo_totali", "fibre", "_cinzas", "calcio", "magnesio"]
# Tabella 1, blocco B: etichette di intestazione -> campo.
COL_B = {
    "Manganês": "manganese", "Fósforo": "fosforo", "Ferro": "ferro",
    "Sódio": "sodio", "Potássio": "potassio", "Cobre": "rame", "Zinco": "zinco",
    "Retinol": "_retinol", "RE": "_re", "RAE": "_rae", "Tiamina": "vitamina_b1",
    "Riboflavina": "vitamina_b2", "Piridoxina": "vitamina_b6",
    "Niacina": "vitamina_b3", "C": "vitamina_c",
}
# Tabella 2: i primi tre valori dopo la descrizione.
COL_T2 = ["grassi_saturi", "grassi_monoinsaturi", "grassi_polinsaturi"]

RIGA_CON_NOME = re.compile(r"^\s*(\d{1,3})\s{2,}(\S.*?)\s{2,}(\S.*)$")
RIGA_SOLO_NUMERO = re.compile(r"^\s*(\d{1,3})\s{2,}(\S.*)$")
TOKEN = re.compile(r"\S+")
VALORE = re.compile(r"^(\d+(?:,\d+)?|Tr|NA|\*)[a-z]?$")


NA = "NA"  # "nao aplicavel": il nutriente non e' presente nell'alimento


def valore(tok):
    """Numero float, 0.0 per traccia, NA per non applicabile, None per assente."""
    m = VALORE.match(tok)
    if not m:
        return None
    t = m.group(1)
    if t == "Tr":
        return 0.0
    if t == "NA":
        return NA
    if t == "*":
        return None
    return float(t.replace(",", "."))


def tipo_blocco(riga):
    if "Umidade" in riga:
        return "A"
    if "Manganês" in riga:
        return "B"
    if "turados" in riga:
        return "T2"
    return None


def centri_colonne(intestazione):
    """Centro orizzontale di ogni etichetta della riga 'Numero do ...' (blocco B)."""
    out = []
    for m in TOKEN.finditer(intestazione):
        if m.group(0) in COL_B:
            out.append((COL_B[m.group(0)], (m.start() + m.end()) / 2))
    return out


def centri_unita(righe):
    """Centri delle 11 unita' '(%) (kcal) (kJ) (g) ...' del blocco A."""
    for r in righe:
        if "(kcal)" in r:
            un = [((m.start() + m.end()) / 2) for m in re.finditer(r"\(\S+?\)", r)]
            if len(un) == len(COL_A):
                return list(zip(COL_A, un))
    sys.exit("intestazione unita' del blocco A non trovata")


def analizza(testo):
    righe = testo.splitlines()
    nomi, categorie = {}, {}
    campi = {}  # numero -> dict campo -> valore
    stat = {"b_ambigue": 0, "b_righe": 0}
    blocco = None
    centri, centri_a = [], []
    categoria = None
    for i, r in enumerate(righe):
        if "Número do" in r or "Numero do" in r:
            # il tipo si legge dalla riga stessa (A: Umidade, B: Manganes) o
            # dalle 2 precedenti/seguenti (T2: 'Sa-/turados')
            vicine = " ".join(righe[max(0, i - 2): i + 2])
            blocco = tipo_blocco(r) or tipo_blocco(vicine)
            if blocco == "B":
                centri = centri_colonne(r)
            if blocco == "A":
                centri_a = centri_unita(righe[i: i + 4])
            continue
        if blocco is None:
            continue
        if r.startswith("Tabela 3") or "Aminoácidos" in r and "Tabela" in r:
            blocco = None
            continue
        if blocco == "A":
            m = RIGA_CON_NOME.match(r)
            if m and VALORE.match(m.group(3).split()[0]):
                num = int(m.group(1))
                resto = m.group(3)
                off = r.index(resto, r.index(m.group(2)) + len(m.group(2)))
                toks = [(t.start() + off, t.end() + off, t.group(0)) for t in TOKEN.finditer(resto)]
                nomi[num] = re.sub(r"\s+", " ", m.group(2)).strip()
                categorie[num] = categoria
                d = campi.setdefault(num, {})
                if len(toks) == len(COL_A):
                    assegn = [(COL_A[k], toks[k][2]) for k in range(len(toks))]
                else:
                    stat["a_per_posizione"] = stat.get("a_per_posizione", 0) + 1
                    usati, collisione, assegn = set(), False, []
                    for (a, b, t) in toks:
                        c = (a + b) / 2
                        campo, _ = min(centri_a, key=lambda x: abs(x[1] - c))
                        collisione |= campo in usati
                        usati.add(campo)
                        assegn.append((campo, t))
                    if collisione:
                        stat.setdefault("a_collisioni", []).append(num)
                        assegn = []
                for campo, t in assegn:
                    d[campo] = valore(t)
                continue
            s = r.strip()
            # riga di categoria: testo senza cifre iniziali, non intestazione/nota
            if s and not s[0].isdigit() and "Tabela" not in s and "Abrevia" not in s \
                    and "(" not in s[:2] and not re.search(r"\d,\d|^\d", s) \
                    and len(s) < 70 and s != "Vitamina" and not s.startswith(("†", "*", "Fonte", "Nota")):
                categoria = s
        elif blocco == "B":
            m = RIGA_SOLO_NUMERO.match(r)
            if not m:
                continue
            num = int(m.group(1))
            resto = m.group(2)
            off = r.index(resto, r.index(m.group(1)) + len(m.group(1)))
            d = campi.setdefault(num, {})
            toks = [(t.start() + off, t.end() + off, t.group(0)) for t in TOKEN.finditer(resto)]
            stat["b_righe"] += 1
            if len(toks) == len(centri):
                assegn = [(centri[k][0], toks[k][2]) for k in range(len(toks))]
            else:
                assegn = []
                usati = set()
                ambiguo = False
                for (a, b, t) in toks:
                    c = (a + b) / 2
                    campo, _ = min(centri, key=lambda x: abs(x[1] - c))
                    if campo in usati:
                        ambiguo = True
                    usati.add(campo)
                    assegn.append((campo, t))
                if ambiguo:
                    stat["b_ambigue"] += 1
                    # in caso di collisione si tiene solo la parte certa: i primi 7
                    # (minerali, sempre tutti presenti), niente vitamine
                    assegn = [(centri[k][0], toks[k][2]) for k in range(min(7, len(toks)))]
            for campo, t in assegn:
                d[campo] = valore(t)
        elif blocco == "T2":
            m = RIGA_CON_NOME.match(r)
            if not m:
                continue
            num = int(m.group(1))
            toks = m.group(3).split()
            d = campi.setdefault(num, {})
            for nome_col, tok in zip(COL_T2, toks):
                d[nome_col] = valore(tok)
    return nomi, categorie, campi, stat


def converti(num, nome, categoria, v):
    if not isinstance(v.get("calorie"), float):
        return None
    # NA = "non applicabile": il nutriente non c'e' (es. proteine e carboidrati
    # in un olio), quindi 0.0 sui macro e sulla fibra quando le calorie ci sono.
    v = dict(v)
    for c in ("proteine", "grassi", "_carbo_totali", "fibre"):
        if v.get(c) == NA:
            v[c] = 0.0
    if any(not isinstance(v.get(c), float) for c in OBBLIGATORI):
        return None
    fibra = max(v["fibre"] if isinstance(v.get("fibre"), float) else 0.0, 0.0)
    netti = max(v["_carbo_totali"] - fibra, 0.0)
    riga = {
        "nome": nome,
        "food_code": f"taco-{num}",
        "carboidrati_disponibili": round(netti, 2),
        "fibre": round(fibra, 2),
        "grassi": round(max(v["grassi"], 0.0), 2),
        "proteine": round(max(v["proteine"], 0.0), 2),
        "calorie": round(max(v["calorie"], 0.0), 1),
        "categoria": categoria,
    }
    vit_a = v.get("_rae")
    if not isinstance(vit_a, float):
        vit_a = v.get("_retinol")
    v = dict(v, vitamina_a=vit_a)
    for campo in ORDINE_CAMPI:
        if campo in riga:
            continue
        x = v.get(campo)
        if isinstance(x, float) and x > 0:
            riga[campo] = round(x, 3)
    return {k: riga[k] for k in ORDINE_CAMPI if k in riga}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        testo = f.read()
    nomi, categorie, campi, stat = analizza(testo)
    risultato, scartati, visti = [], [], set()
    for num in sorted(nomi):
        riga = converti(num, nomi[num], categorie.get(num), campi.get(num, {}))
        if riga is None:
            scartati.append((num, nomi[num]))
            continue
        chiave = riga["nome"].lower()
        if chiave in visti:
            scartati.append((num, nomi[num] + " [duplicato]"))
            continue
        visti.add(chiave)
        risultato.append(riga)
    risultato.sort(key=lambda r: r["nome"].lower())
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(risultato, f, ensure_ascii=False, separators=(",", ":"))
    print(f"voci lette: {len(nomi)}; tenute: {len(risultato)}; scartate: {len(scartati)}")
    for s in scartati:
        print("  scartata:", s)
    print("righe blocco B:", stat["b_righe"], "con colonne ambigue:", stat["b_ambigue"])
    print("righe blocco A assegnate per posizione:", stat.get("a_per_posizione", 0),
          "collisioni:", stat.get("a_collisioni", []))
    print(f"-> {sys.argv[2]} ({os.path.getsize(sys.argv[2]) / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
