# Dataset TACO — Tabela Brasileira de Composição de Alimentos, convertito per Ketorbit

`taco_2011.json` e' ricavato dalla **TACO, 4ª edição revisada e ampliada
(2011)**, la tabella di composizione degli alimenti brasiliani del **NEPA**
(Núcleo de Estudos e Pesquisas em Alimentação, **UNICAMP**, Campinas).

**Citazione obbligatoria:** NEPA/UNICAMP. *Tabela Brasileira de Composição de
Alimentos – TACO*. 4ª edição revisada e ampliada. Campinas: NEPA-UNICAMP, 2011.

**Licenza/uso:** non esiste una licenza formale (non e' CC0 ne' CC BY). Il
frontespizio e la pagina dei diritti dicono, testualmente: *"É permitida a
reprodução total ou parcial do material, desde que seja citada a fonte."* Non
c'e' nessun divieto esplicito di uso commerciale, ma non c'e' neppure una
dichiarazione esplicita che lo consenta. Per questo motivo la voce e' trattata
come "uso libero con obbligo di citazione" (come il CREA) e **va confermata per
iscritto dal NEPA** prima di distribuire l'app con questo dataset in
Produzione (vedi DECISIONI.md dell'app, 27 novembre 2026).

## Fonte e come e' stata letta

Il NEPA **non pubblica un file di dati**: la TACO esiste solo come PDF
(164 pagine; Tabela 1: composizione centesimale, minerali, vitamine e
colesterolo; Tabela 2: acidi grassi; Tabela 3: aminoacidi). Il PDF e' stato
scaricato il 27 novembre 2026 dalla copia ospitata dal Conselho Federal de
Nutricionistas:
https://www.cfn.org.br/wp-content/uploads/2017/03/taco_4_edicao_ampliada_e_revisada.pdf

Il testo si estrae con `pdftotext -layout` (poppler) e `converti_taco.py`
(Python 3, solo libreria standard) lo interpreta. Le colonne vuote spostano
l'allineamento: per le righe con meno valori del previsto l'assegnazione alle
colonne e' fatta **per posizione** rispetto all'intestazione di ogni pagina,
non per ordine (19 righe del blocco macro, nessuna ambigua).

**Verifica fatta:** 597 voci lette (tutte quelle della TACO); su 590 tenute il
confronto tra le calorie dichiarate e `4*(proteine+carboidrati)+9*grassi`
torna entro il 25% (o 40 kcal) per 589; l'unica fuori e' il lievito chimico,
dove l'incoerenza e' gia' nei dati della fonte.

## Conversione

Ogni voce e' per **100 g** di parte edibile, stesso schema di `usda_2026.json`:

| Campo app | Colonna TACO | Note |
|---|---|---|
| `calorie` | Energia (kcal) | |
| `proteine` | Proteína (g) | |
| `grassi` | Lipídeos (g) | |
| `carboidrati_disponibili` | Carboidrato (g) **meno** Fibra Alimentar | la TACO riporta i carboidrati totali; stessa convenzione "netti di fibra" di CIQUAL/CREA/BLS/UK/USDA, mai negativi |
| `fibre` | Fibra Alimentar (g) | |
| minerali | Cálcio, Magnésio, Manganês, Fósforo, Ferro, Sódio, Potássio, Cobre, Zinco | mg |
| vitamine | Tiamina (B1), Riboflavina (B2), Niacina (B3), Piridoxina (B6), Vitamina C | mg |
| `vitamina_a` | RAE (µg); se manca, Retinol | mai RE (equivalenti di retinolo: sovrastima i carotenoidi) |
| `colesterolo` | Colesterol (mg) | |
| `grassi_saturi/monoinsaturi/polinsaturi` | Tabela 2 | g; la TACO non include i trans |
| `categoria` | uno dei 15 gruppi della TACO | testo portoghese nativo |
| `food_code` | `taco-<numero>` | numero dell'alimento nella tabella (1-597), stabile |

Non presenti nella TACO (campi omessi): iodio, selenio, vitamine A/D/E/K
(a parte A), B5, B7, B9, B12 e omega-3/6 individuali.

Regole (stesse delle altre fonti, con un adattamento):
- `Tr` (traccia) -> 0.0; i micronutrienti a zero **non sono scritti** (l'app li
  legge come 0.0);
- `NA` (non applicabile) su proteine, grassi, carboidrati e fibra significa
  che il nutriente non c'e' (es. proteine e carboidrati in un olio): 0.0 se le
  calorie sono presenti. Sui micronutrienti `NA` = valore assente;
- `*` (analisi in rivalutazione, dichiarata dal NEPA) o cella vuota = valore
  assente: sui 4 campi obbligatori la voce e' **scartata**, nessun valore
  indovinato;
- lettere di nota a margine ("20a") ignorate;
- nomi **in portoghese** (lingua nativa): niente `nome_it/en/fr/es/de`. L'app
  mostra il nome portoghese quando la traduzione manca;
- duplicati per nome: nessuno.

**Totale: 590 alimenti** su 597 della TACO. Scartate 7 voci senza dati
pubblicati: Iogurte sabor abacaxi (450), Leite de vaca desnatado UHT (457),
Leite de vaca integral (458), Cana aguardente (472), Sal dietético (516),
Sal grosso (517), Coco verde cru (591). Il latte intero resta fuori finche'
il NEPA non pubblica i valori rivalutati.

## Aggiornamento

`pdftotext -layout taco_4_edicao_ampliada_e_revisada.pdf taco.txt` e poi
`python3 -I converti_taco.py taco.txt taco_2011.json`. Se il NEPA pubblicasse
una nuova edizione o un file di dati, rifare la verifica sopra.
