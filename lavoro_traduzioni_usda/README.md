# Traduzioni nomi USDA (it, fr, es, de, pt-BR): avanzamento aggiornato il 28 novembre 2026

`usda_2026.json` (13.402 voci) ha ancora solo il nome inglese. Gli altri 5 database (CIQUAL, BLS, UK, CREA, TACO) sono gia' in 6 lingue.
I lotti sono di 298 voci: il lotto NN copre le righe (NN-1)*298 ... NN*298-1 (id = indice riga). L'ultimo (45) e' piu' corto.

## Stato
- **output/**: 30 lotti completi sul piano strutturale: 01-17, 18, 20, 21, 24-28, 30-32, 34-35.
- **output_parziali/**: nessun lotto parziale residuo. Il lotto 16 è stato tradotto integralmente nelle cinque lingue, controllato per copertura esatta degli ID e trasferito in `output/`; i lotti 30, 31, 32 e 34 sono stati completati integrando gli ID mancanti e trasferiti in `output/`.
- **Da fare del tutto**: 19, 22, 23, 29, 33, 36-45 (15 lotti).
- I lotti appena completati hanno superato un controllo strutturale di copertura ID e presenza dei cinque campi lingua, coerente con `validate_names.py`. Non sono stati eseguiti localmente gli script Python del repository né una revisione madrelingua: non considerarli validati linguisticamente.
- Il README precedente riportava conteggi di mancanti non coerenti con gli input effettivi: i mancanti rilevati erano 25 nel lotto 30, 4 nel 31, 1 nel 32 e 9 nel 34.

## Come proseguire
1. Per ogni lotto da fare: tradurre `input/in_usda_NN.json` (id, en, categoria, tipo) seguendo `ISTRUZIONI_DB.md` (glossario, regole di stile; pt = portoghese del Brasile). Output `output/out_usda_NN.json`: `{"<id>": {"it":"..","fr":"..","es":"..","de":"..","pt":".."}}` per OGNI id.
   Con gli agenti: un agente per lotto, ognuno con una cartella di lavoro propria (cartelle condivise hanno causato sovrascritture); massimo ~20 agenti in parallelo.
2. Validare ogni lotto: `python3 -I validate_names.py input/in_usda_NN.json output/out_usda_NN.json it,fr,es,de,pt` fino a "0 problemi".
   Per i parziali, completare solo gli id mancanti e unirli ai file gia' presenti.
3. Quando tutti i 45 lotti sono in `output/`: dalla radice del repo
   `python3 -I lavoro_traduzioni_usda/prepara_traduzioni_usda.py` (crea `traduzioni_usda.json`; senza tutti i lotti dice quali mancano), poi
   `python3 -I unisci_traduzioni_nomi.py usda_2026.json traduzioni_usda.json it,fr,es,de,pt`.
4. Controllare che i campi preesistenti non siano cambiati, aggiornare `README_USDA.md` e `DECISIONI.md` dell'app, committare. Nell'app `UsdaDownloadWorker`/entity/DAO hanno gia' le colonne nome_it/fr/es/de/pt: dopo l'unione verificare solo che compili.
5. I nomi arrivano agli utenti solo dopo il merge del branch dati su `main` (l'app scarica da raw.githubusercontent.com/.../main).
