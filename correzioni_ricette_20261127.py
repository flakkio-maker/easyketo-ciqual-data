#!/usr/bin/env python3
"""Correzioni a ricette_scoperta.json (27 novembre 2026), emerse dalla traduzione in portoghese.

Una tantum, con controllo dello stato di partenza (se la ricetta e' gia' corretta non fa nulla).
Per ogni ricetta i macro per porzione sono RICALCOLATI dai database (grammi x valori per 100 g di
CIQUAL/CREA, divisi per le porzioni), come nel resto del catalogo; i tag dieta non si toccano.

- 333 Manzo brasato alla birra: la birra non c'era. Aggiunti 200 g di birra chiara (CREA) e brodo da
  300 a 100 g; passo 5 aggiornato in 6 lingue.
- 337 Sgombro alla griglia: l'ingrediente era salmone. Ora sgombro (CREA "Sgombro o maccarello").
- 266 Sgombro al limone: idem, e tolta la nota "in sostituzione dello sgombro" dal passo 1.
- 254 Petto di tacchino con funghi: l'ingrediente era petto di pollo. Ora fesa di tacchino (CREA).
- 265 Fesa di tacchino con spinaci: idem, e tolta la nota "in sostituzione della fesa di tacchino".
- 204 Milky Way Shine Treatment: trattamento per capelli, non e' cibo: rimossa dal catalogo.

Uso: python3 -I correzioni_ricette_20261127.py ricette_scoperta.json ciqual_2025.json crea_2026.json
"""
import json
import sys

# Traduzioni degli ingredienti nuovi/cambiati (it, pt dal catalogo; en/fr/es/de aggiunte)
ING = {
    "birra": {"nome": "birra chiara", "nome_it": "birra chiara", "nome_en": "light beer", "nome_fr": "bière blonde",
              "nome_es": "cerveza rubia", "nome_de": "helles Bier", "nome_pt": "cerveja clara",
              "fonte_macro": "CREA", "voce_matchata": "Bevanda alcolica, Birra chiara"},
    "sgombro": {"nome": "sgombro crudo", "nome_it": "sgombro crudo", "nome_en": "raw mackerel", "nome_fr": "maquereau cru",
                "nome_es": "caballa cruda", "nome_de": "Makrele, roh", "nome_pt": "cavala crua",
                "fonte_macro": "CREA", "voce_matchata": "Sgombro o maccarello"},
    "tacchino": {"nome": "tacchino fesa cruda", "nome_it": "tacchino fesa cruda", "nome_en": "raw turkey breast",
                 "nome_fr": "blanc de dinde cru", "nome_es": "pechuga de pavo cruda", "nome_de": "Putenbrust, roh",
                 "nome_pt": "peito de peru cru", "fonte_macro": "CREA", "voce_matchata": "Tacchino, fesa, crudo"},
}

# (lingua) -> (vecchio, nuovo) sostituzioni di testo nei passi
POLLO_TACCHINO = {
    "it": [("petto di pollo", "petto di tacchino")],
    "en": [("chicken breast", "turkey breast")],
    "fr": [("blanc de poulet", "blanc de dinde")],
    "es": [("pechuga de pollo", "pechuga de pavo")],
    "de": [("Hähnchenbrust", "Putenbrust")],
    "pt": [("peito de frango", "peito de peru")],
}
NOTA_265 = {
    "it": " (in sostituzione della fesa di tacchino)", "en": " (used in place of the turkey escalope)",
    "fr": " (à la place de l'escalope de dinde)", "es": " (en sustitución de la pechuga de pavo)",
    "de": " (als Ersatz für die Putenoberschale)", "pt": " (usado no lugar do filé de peru)",
}
PASSO_266 = {
    "it": ("il filetto di pesce (in sostituzione dello sgombro)", "il filetto di sgombro"),
    "en": ("the fish fillet (used in place of the mackerel)", "the mackerel fillet"),
    "fr": ("le filet de poisson (à la place du maquereau)", "le filet de maquereau"),
    "es": ("el filete de pescado (en sustitución de la caballa)", "el filete de caballa"),
    "de": ("Fischfilet (als Ersatz für die Makrele)", "Makrelenfilet"),
    "pt": ("o filé de peixe (usado no lugar da cavala)", "o filé de cavala"),
}
PASSO_333 = {  # indice 4 in tutte le lingue
    "it": "Bagnare con la birra e il brodo di carne e verdure fino quasi a coprire, salare, coprire con un coperchio.",
    "en": "Pour in the beer and the meat and vegetable broth until almost covered, season with salt, cover with a lid.",
    "fr": "Mouillez avec la bière et le bouillon de viande et légumes jusqu'à presque couvrir, salez, couvrez avec un couvercle.",
    "es": "Regar con la cerveza y el caldo de carne y verduras hasta casi cubrir, salar, tapar con una tapa.",
    "de": "Mit dem Bier und der Fleisch-Gemüse-Brühe fast bedeckend aufgießen, salzen, mit einem Deckel abdecken.",
    "pt": "Despeje a cerveja e o caldo de carne e legumes até quase cobrir tudo, tempere com sal e tampe a panela.",
}
LINGUE = ["it", "en", "fr", "es", "de", "pt"]


def macro(ricetta, cat):
    k = c = g = p = 0.0
    for i in ricetta["ingredienti"]:
        if not i.get("fonte_macro"):
            continue
        r = cat[(i["fonte_macro"], i["voce_matchata"])]
        f = i["grammi"] / 100.0
        k += r["calorie"] * f
        c += r["carboidrati_disponibili"] * f
        g += r["grassi"] * f
        p += r["proteine"] * f
    n = ricetta["porzioni"] or 1.0
    return [round(x / n, 1) for x in (k, c, g, p)]


def applica_macro(r, cat):
    r["kcal_porzione"], r["carbo_porzione"], r["grassi_porzione"], r["proteine_porzione"] = macro(r, cat)


def sostituisci_ingrediente(r, indice, nuovo):
    vecchio = r["ingredienti"][indice]
    r["ingredienti"][indice] = dict(nuovo, grammi=vecchio["grammi"])


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        ricette = json.load(f)
    cat = {}
    for r in json.load(open(sys.argv[2], encoding="utf-8")):
        cat[("CIQUAL", r["nome_it"])] = r
    for r in json.load(open(sys.argv[3], encoding="utf-8")):
        cat[("CREA", r["nome"])] = r
    by = {r["id"]: r for r in ricette}
    fatte = []

    # 333: birra
    r = by[333]
    if not any("birra" in (i.get("nome_it") or "") for i in r["ingredienti"]):
        for i in r["ingredienti"]:
            if (i.get("nome_it") or "").startswith("brodo"):
                i["grammi"] = 100.0
        idx = next(n for n, i in enumerate(r["ingredienti"]) if (i.get("nome_it") or "").startswith("brodo"))
        r["ingredienti"].insert(idx, dict(ING["birra"], grammi=200.0))
        for l in LINGUE:
            r["procedimento_" + l][4] = PASSO_333[l]
        applica_macro(r, cat)
        fatte.append(333)

    # 337 / 266: salmone -> sgombro
    for rid in (337, 266):
        r = by[rid]
        for n, i in enumerate(r["ingredienti"]):
            if "salmone" in (i.get("nome_it") or ""):
                sostituisci_ingrediente(r, n, ING["sgombro"])
                if rid == 266:
                    for l in LINGUE:
                        vecchio, nuovo = PASSO_266[l]
                        r["procedimento_" + l][0] = r["procedimento_" + l][0].replace(vecchio, nuovo)
                applica_macro(r, cat)
                fatte.append(rid)

    # 254 / 265: pollo -> tacchino
    for rid in (254, 265):
        r = by[rid]
        for n, i in enumerate(r["ingredienti"]):
            if "pollo petto" in (i.get("nome_it") or ""):
                sostituisci_ingrediente(r, n, ING["tacchino"])
                for l in LINGUE:
                    passi = r["procedimento_" + l]
                    for k, s in enumerate(passi):
                        if rid == 265:
                            s = s.replace(NOTA_265[l], "")
                        for vecchio, nuovo in POLLO_TACCHINO[l]:
                            s = s.replace(vecchio, nuovo)
                        passi[k] = s
                applica_macro(r, cat)
                fatte.append(rid)

    # 204: non e' cibo
    prima = len(ricette)
    ricette = [r for r in ricette if r["id"] != 204]
    if len(ricette) != prima:
        fatte.append("204 rimossa")

    with open(sys.argv[1], "w", encoding="utf-8") as f:
        f.write(json.dumps(ricette, ensure_ascii=False, indent=2) + "\n")
    print("corrette:", fatte or "nessuna (gia' applicate)", "| ricette in catalogo:", len(ricette))


if __name__ == "__main__":
    main()
