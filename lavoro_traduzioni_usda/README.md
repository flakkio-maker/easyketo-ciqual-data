# Traduzioni nomi USDA (it, fr, es, de, pt-BR): lavoro SOSPESO il 28 novembre 2026

`usda_2026.json` (13.402 voci) ha ancora solo il nome inglese. Gli altri 5 database (CIQUAL, BLS, UK, CREA, TACO) sono gia' in 6 lingue.
I lotti sono di 298 voci: il lotto NN copre le righe (NN-1)*298 ... NN*298-1 (id = indice riga). L'ultimo (45) e' piu' corto.

## Stato
- **output/**: 25 lotti tradotti e validati (0 problemi): 01-15, 17, 18, 20, 21, 24-28, 35.
- **output_parziali/**: lotti 30, 31, 32, 34, incompleti (mancano 5, 4, 1, 5 voci). Non validi cosi': vanno completati.
- **Da fare del tutto**: 16, 19, 22, 23, 29, 33, 36-45.
- Mai rivisti da un madrelingua; controllati solo dal validatore e a campione a vista. Il controllo "per somiglianza" non e' affidabile tra lingue lontane.
- Il lavoro si e' fermato per il limite d'uso a 5 ore, poi per richiesta del titolare.

## Come proseguire
1. Per ogni lotto da fare: tradurre `input/in_usda_NN.json` (id, en, categoria, tipo) seguendo `ISTRUZIONI_DB.md` (glossario, regole di stile; pt = portoghese del Brasile). Output `output/out_usda_NN.json`: `{"<id>": {"it":"..","fr":"..","es":"..","de":"..","pt":".."}}` per OGNI id.
   Con gli agenti: un agente per lotto, ognuno con una cartella di lavoro propria (cartelle condivise hanno causato sovrascritture); massimo ~20 agenti in parallelo.
2. Validare ogni lotto: `python3 -I validate_names.py input/in_usda_NN.json output/out_usda_NN.json it,fr,es,de,pt` fino a "0 problemi".
   Per i parziali, completare solo gli id mancanti e unirli ai file gia' presenti.
3. Quando tutti i 45 lotti sono in `output/`: dalla radice del repo
   `python3 -I lavoro_traduzioni_usda/prepara_traduzioni_usda.py` (crea `traduzioni_usda.json`; senza tutti i lotti dice quali mancano), poi
   `python3 -I unisci_traduzioni_nomi.py usda_2026.json traduzioni_usda.json it,fr,es,de,pt`.
4. Controllare che i campi preesistenti non siano cambiati e aggiornare `README_USDA.md`. **Non assumere che l'app supporti già PT:** nel branch `main` di `flakkio-maker/EasyKeto`, verificato il 28 novembre 2026, `UsdaDownloadWorker` e le entity/DAO gestiscono IT/FR/ES/DE ma non `nome_pt`. Serve un branch applicativo separato per aggiungere il campo e i mapping, senza cambiare la lingua dell'interfaccia.
5. Le traduzioni arrivano agli utenti solo dopo due passaggi: pubblicazione del JSON aggiornato su `main` di questo repository (l'app scarica da `raw.githubusercontent.com/.../main`) **e** rilascio di una versione dell'app che sappia leggere `nome_pt`. La sola pubblicazione del JSON non basta.


## Verifica incrociata con il codice dell'app (28 novembre 2026)

La precedente nota che indicava già presenti le colonne `nome_pt` in `UsdaDownloadWorker`/entity/DAO non è corretta rispetto al branch `main` attuale di `flakkio-maker/EasyKeto`. La verifica dei file `UsdaDownloadWorker.kt`, `EntitiesDatasetNutrizionali.kt` e `TraduzioneAlimentoUseCase.kt` mostra supporto IT/FR/ES/DE, ma non PT. Inoltre `BancaDati` non contiene ancora TACO.

Non considerare quindi le traduzioni USDA PT-BR o TACO pronte per la produzione finché non sarà completata anche l'integrazione applicativa e verificata con build/test.
