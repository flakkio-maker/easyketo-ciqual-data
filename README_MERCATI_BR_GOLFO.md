# Estensione mercati — Brasile e Golfo

**Verifica:** 28 novembre 2026  
**Branch dati di partenza:** `ccr-820dac60-h69k63` — commit `1ecefc62e69d8a07bc0b28db1f1c7fee8c0fec6d`  
**Branch di prosecuzione:** `codex/br-gulf-market-readiness-2026-11`

Questo documento consolida la verifica delle fonti alimentari per i mercati approvati: **Brasile, Emirati Arabi Uniti, Arabia Saudita, Qatar, Kuwait e Bahrain**. Non amplia il perimetro ad altri Paesi.

## 1. Decisioni di prodotto da mantenere

- Catalogo nutrizionale **unico e condiviso**, non sei database separati per Paese.
- Ogni voce deve conservare codice, fonte, Paese/origine del dato, versione, licenza e riferimento bibliografico.
- Le banche dati nazionali servono soprattutto per alimenti generici e piatti tradizionali; Open Food Facts resta utile per prodotti confezionati, marche e barcode.
- Le priorità nazionali devono ordinare i risultati, non escludere le altre fonti.
- Interfaccia invariata: IT/EN/FR/ES/DE. **PT-BR riguarda i nomi degli alimenti e i contenuti delle ricette, non una nuova lingua dell'interfaccia.** Per le altre lingue non disponibili resta il fallback inglese.
- Nessuna traduzione araba dell'interfaccia in questa fase. Nessuna nuova lingua asiatica o russa.
- Canada, Australia e Nuova Zelanda non fanno parte di questa estensione: sono già nel perimetro esistente.

## 2. Stato reale dei dati già presenti nel branch

Le traduzioni portoghesi sono effettivamente presenti nel repository dati. Ho eseguito controlli strutturali sui JSON disponibili nel branch:

| Dataset / file | Copertura verificata | Esito strutturale |
|---|---:|---|
| `traduzioni_ciqual.json` | 3.323 voci PT | 0 traduzioni PT mancanti |
| `traduzioni_bls.json` | 7.043 voci PT | 0 traduzioni PT mancanti |
| `traduzioni_crea.json` | 900 voci PT | 0 traduzioni PT mancanti |
| `traduzioni_uk.json` | 2.537 voci PT | 0 traduzioni PT mancanti |
| `taco_2011.json` + `taco_traduzioni.json` | 590 alimenti | PT nativo + EN/IT/FR/ES/DE presenti |
| `ricette_traduzioni_pt.json` | 443 ricette | nomi, ingredienti e passaggi non vuoti |
| USDA | 25 lotti completi su 45 | lavoro ancora parziale |

La verifica delle 443 traduzioni ricette ha trovato chiavi presenti, nomi non vuoti, ingredienti e passaggi non vuoti e nessuna stringa con newline. È un controllo strutturale, **non una revisione linguistica madrelingua**.

Altre osservazioni:
- `ingredienti_traduzioni.json` contiene 520 voci, ma nessuna ha ancora il campo `pt`. Le traduzioni degli ingredienti delle 443 ricette sono invece presenti nella struttura specifica di ciascuna ricetta.
- USDA: 25 lotti risultano completi e validati secondo il README del lavoro; quattro lotti sono parziali e venti devono ancora essere prodotti. Le traduzioni sono ancora separate in `lavoro_traduzioni_usda/output/` e non costituiscono una traduzione completa del dataset finale.
- La presenza dei JSON in questo branch non significa che l'app li stia già mostrando.

## 3. Gap tra repository dati e applicazione

Verifica effettuata sul branch `main` di `flakkio-maker/EasyKeto` il 28 novembre 2026.

**Il codice dell'app non è ancora allineato ai dati PT-BR e TACO.** In particolare:

1. `BancaDati` contiene CIQUAL, CREA, BLS, USDA, Open Food Facts e UK; non contiene ancora TACO.
2. La priorità Paese attuale include il Brasile nel gruppo con affinità USDA. Non esiste ancora una priorità TACO per il Brasile.
3. `UsdaDownloadWorker` e le entity nutrizionali gestiscono le traduzioni IT/FR/ES/DE, ma non `nome_pt`.
4. Non risultano ancora worker, entity, DAO, repository, migrazione Room e ricerca per TACO.
5. `RicetteScopertaDownloadWorker`, `ModelsRicette.kt` ed `EntitiesRicette.kt` non contengono ancora i campi PT per nome, procedimento e ingredienti.
6. La selezione delle traduzioni usa la lingua di sistema e poi il fallback inglese. Aggiungere i campi PT ai DTO/entity permetterebbe di mostrare i nomi PT quando il dispositivo usa il portoghese, senza aggiungere una traduzione dell'interfaccia.

Di conseguenza, **non dichiarare TACO o PT-BR già integrati nell'app**. Serve un branch separato nel repository applicativo, con migrazione Room, worker, repository, priorità di ricerca, stringhe UI nelle cinque lingue attuali e test. I dati pubblici vengono scaricati dall'app dal branch `main` di questo repository: i contenuti presenti in un branch di lavoro non raggiungono gli utenti finché non vengono pubblicati nel percorso previsto.

## 4. Brasile

### TACO — fonte locale principale candidata

La TACO del NEPA/UNICAMP, quarta edizione 2011, è una fonte brasiliana pertinente e già convertita nel branch:

- 597 alimenti nella pubblicazione originale;
- 590 voci utilizzabili nel JSON, sette escluse perché prive di dati sufficienti;
- nome originale in portoghese brasiliano;
- traduzioni EN/IT/FR/ES/DE in `taco_traduzioni.json`;
- valori per 100 g di parte edibile;
- codici stabili `taco-<numero>`.

Controlli eseguiti sul JSON:
- 590 record;
- 590 codici univoci;
- nessun campo macro obbligatorio mancante o negativo;
- tutti i nomi PT/EN/IT/FR/ES/DE presenti.

**Licenza:** la pubblicazione TACO afferma che la riproduzione totale o parziale è consentita citando la fonte. Non ho trovato una licenza standard CC0/CC BY né una clausola che chiarisca espressamente l'uso commerciale in un'app. La posizione prudente già riportata in `README_TACO.md` resta valida: chiedere conferma scritta al NEPA/UNICAMP prima della distribuzione commerciale. La fonte non va presentata come CC0.

La TACO è del 2011: è utile per gli alimenti brasiliani e i piatti locali, ma non sostituisce una banca dati aggiornata dei prodotti confezionati.

### TBCA/USP

La TBCA è più recente e più ampia, ma le condizioni pubblicate per l'uso commerciale e la riproduzione/modifica non la rendono una fonte da importare liberamente in un'app commerciale. Non copiarne i dati senza una licenza o autorizzazione specifica.

### Priorità proposta per il Brasile

Dopo autorizzazione TACO e integrazione applicativa:
1. TACO per alimenti generici e piatti brasiliani;
2. USDA come fallback per alimenti generici non coperti;
3. Open Food Facts per prodotti confezionati, marche e barcode.

La priorità deve riguardare la ricerca testuale; il barcode deve continuare a identificare il prodotto specifico quando presente.

## 5. Mercati del Golfo

### Arabia Saudita — SFDA

La SFDA ha annunciato nel 2026 il lancio della prima Saudi Food Composition Database nazionale, con dati su alimenti locali e piatti tradizionali, energia, macro e micronutrienti. La comunicazione ufficiale dichiara che i dati sono resi accessibili anche agli sviluppatori per creare strumenti digitali.

La piattaforma e la documentazione sono quindi il candidato più promettente per l'Arabia Saudita. Tuttavia:
- non ho verificato un'API pubblica o un export strutturato riutilizzabile;
- non ho trovato una licenza open data che autorizzi chiaramente la redistribuzione commerciale;
- i termini SFDA limitano il download di materiali/dati non posseduti o per i quali non si dispone di autorizzazione.

**Decisione:** chiedere alla SFDA accesso tecnico, formato strutturato e condizioni di riutilizzo. Non effettuare scraping o importazione massiva prima di aver chiarito i diritti.

### Bahrain — Bahrain Food Composition Tables 2025

La prima edizione 2025 del Ministry of Health presenta:
- 82 piatti tradizionali;
- 113 prodotti di mercato;
- analisi dirette per i prodotti di mercato e per parte dei piatti;
- dati presi anche da fonti regionali per alcuni alimenti.

Il documento dichiara che alcuni valori sono stati presi da Kuwait, Libano, Emirati, Giordania e Pakistan. È quindi essenziale conservare la provenienza del dato e non attribuire automaticamente ogni valore al Bahrain.

Il PDF è pubblicamente accessibile e compare anche nel catalogo FAO/INFOODS, ma non ho trovato nel PDF una licenza che autorizzi la redistribuzione commerciale. La Bahrain Government Open Data License riguarda i dataset pubblicati sul relativo Open Data Portal: non va applicata automaticamente a un PDF del Ministero pubblicato nella sezione pubblicazioni.

**Decisione:** candidato forte, ma chiedere autorizzazione scritta al Ministry of Health prima di incorporare e ridistribuire i valori.

### Emirati Arabi Uniti

Non ho individuato una banca dati nazionale completa, strutturata e pubblicamente riutilizzabile paragonabile a TACO o alla nuova banca dati saudita.

Il National Nutrition Guide del MOHAP è una guida nutrizionale, non un dataset completo di composizione alimentare. Studi e strumenti di valutazione dietetica locali fanno riferimento a USDA e a un numero limitato di piatti/ricette emiratine, ma non ho trovato un dataset aperto con licenza commerciale che possa essere importato direttamente.

**Decisione:** mantenere USDA per gli alimenti generici e Open Food Facts per prodotti confezionati. In una seconda fase chiedere al MOHAP o ai gruppi di ricerca locali se esiste un export autorizzabile di piatti e ricette emiratine.

### Qatar

Nelle fonti ufficiali e nel catalogo FAO/INFOODS consultati non ho individuato una banca dati nazionale recente, completa e riutilizzabile di composizione degli alimenti. I dataset pubblici del Qatar individuati riguardano anche importazioni e controlli alimentari, non valori nutrizionali per alimento.

**Decisione:** USDA + Open Food Facts. Non creare un dataset nazionale artificiale traducendo piatti generici o copiando ricette da siti commerciali.

### Kuwait

Esistono fonti storiche e scientifiche, tra cui tabelle di composizione del 1982 e 1998 e lavori KISR sui piatti compositi. Non ho verificato un dataset aggiornato, strutturato e con licenza aperta per la redistribuzione commerciale.

Il Bahrain FCT 2025 dichiara anche di aver preso alcuni valori da tabelle kuwaitiane: questi record possono essere utili solo mantenendo la fonte originaria e senza duplicarli come se fossero misurazioni del Bahrain.

**Decisione:** USDA + Open Food Facts finché KISR o il soggetto titolare non fornisce accesso e diritti di riutilizzo.

## 6. Architettura consigliata per il Golfo

Non creare cinque database separati né un unico blocco indistinto chiamato "Gulf foods".

Quando saranno disponibili autorizzazioni e dati, usare un catalogo condiviso con almeno:
- `food_code` stabile;
- `source_id` e nome della tabella;
- `country_origin` del dato;
- `source_country` quando il valore è stato preso da un altro Paese;
- versione/data della fonte;
- licenza e attribuzione;
- metodo (analisi diretta, ricetta standardizzata, valore preso da altra tabella);
- definizione dei carboidrati e unità.

Una ricetta o un alimento condiviso tra Paesi può essere cercato in più mercati, ma non deve essere duplicato o attribuito al Paese sbagliato.

Per il Golfo, la prima integrazione locale da valutare è **Saudi SFDA**, seguita da **Bahrain FCT 2025**. UAE, Qatar e Kuwait restano su USDA + Open Food Facts fino a quando non emerge una fonte locale riutilizzabile.

## 7. Normalizzazione nutrizionale — punto da non sbagliare

Le fonti non usano sempre la stessa definizione di carboidrati.

- TACO riporta carboidrati totali che includono la fibra. Il JSON normalizza `carboidrati_disponibili` sottraendo la fibra, in linea con la convenzione netta già usata nel progetto.
- Per controllare le calorie TACO bisogna usare i carboidrati totali originali, ricostruibili come `carboidrati_disponibili + fibre`; confrontare le kcal con i soli carboidrati netti genera falsi allarmi. La TACO usa coefficienti Atwater specifici: la formula 4-4-9 è solo un controllo di plausibilità, non una ricalcolazione esatta.
- Per SFDA e Bahrain non sottrarre automaticamente la fibra finché la definizione del campo carboidrati non è stata verificata nella metodologia della fonte.
- Valori mancanti restano mancanti/assenti secondo lo schema della fonte: non inventare micronutrienti o quantità.

## 8. MyFitnessPal come benchmark

La documentazione ufficiale MyFitnessPal dichiara che il suo database combina alimenti inseriti da MyFitnessPal e alimenti aggiunti dagli utenti, che possono essere condivisi con la community.

Questo suggerisce un benchmark utile, ma non una lista di dataset nazionali da replicare:
- copertura pratica dei cibi realmente cercati;
- barcode e prodotti confezionati;
- possibilità di aggiungere alimenti mancanti;
- qualità e distinguibilità delle voci;
- risultati locali e nomi comprensibili.

MyFitnessPal non pubblica in quella pagina un inventario verificabile delle banche dati ufficiali per ciascun Paese. Non usare dati o ricette copiati da MyFitnessPal: il confronto deve riguardare esperienza e copertura, non estrazione dei suoi contenuti.

La differenziazione sostenibile di Ketorbit è un catalogo più curato e con provenienza verificabile, affiancato da Open Food Facts, non la rincorsa al volume di voci generate dagli utenti.

## 9. Sequenza operativa raccomandata

1. **Consolidare i dati già presenti:** mantenere le traduzioni PT-BR verificate e TACO nel branch dati, senza dichiarare che siano già disponibili nell'app.
2. **Chiudere le autorizzazioni:** NEPA/UNICAMP per TACO; SFDA per Saudi; Ministry of Health Bahrain per BFCT; KISR per eventuali tabelle Kuwait.
3. **Completare USDA:** finire i 20 lotti mancanti e i quattro parziali; validare tutti i 45 lotti prima di unirli al dataset finale.
4. **Preparare l'app su branch separato:** supporto `nome_pt` per i database esistenti, ricette PT-BR, TACO worker/entity/DAO/repository, migrazione Room, priorità Brasile e test.
5. **Golfo:** integrare Saudi e Bahrain solo dopo autorizzazione; mantenere UAE/Qatar/Kuwait su USDA + OFF fino a dati locali riutilizzabili.
6. **Revisione linguistica:** far controllare a un madrelingua PT-BR un campione rappresentativo di nomi, ricette e termini alimentari prima di promuovere la traduzione come definitiva.

## 10. Fonti consultate

### Brasile
- NEPA/UNICAMP, TACO 4ª edizione 2011: https://nepa.unicamp.br/wp-content/uploads/sites/27/2023/10/taco_4_edicao_ampliada_e_revisada.pdf
- TBCA/USP: https://fcf.usp.br/tbca/

### Arabia Saudita
- SFDA, annuncio database nazionale (30 agosto 2026): https://sfda.gov.sa/en/news/19370
- Saudi Food Composition Database: https://fd.sfda.gov.sa/
- Termini di utilizzo SFDA: https://sfda.gov.sa/en/terms-of-use
- PDF SFCT: https://www.sfda.gov.sa/sites/default/files/2026-04/SFCT-E.pdf

### Bahrain
- Ministry of Health, Bahrain Food Composition Tables 2025: https://www.health.gov.bh/Content/Upload/File/638916394660950229-FCT-book-final-2025_en.pdf
- Catalogo FAO/INFOODS: https://www.fao.org/food-composition/tables-and-databases/detail/%28bahrain--2025%29-bahrain-food-composition-tables/en
- Bahrain Government Open Data: https://www.bahrain.bh/wps/portal/en/BNP/BahrainAtAGlance/OpenGovernmentData

### Emirati, Qatar e Kuwait
- MOHAP UAE, National Nutrition Guide: https://mohap.gov.ae/en/w/national-nutrition-guide
- FAO/INFOODS, directory tabelle e database: https://www.fao.org/infoods/infoods/tables-and-databases/en/
- FAO/INFOODS, tabelle Kuwait e Bahrain: https://www.fao.org/infoods/infoods/tables-and-databases/bahrain/
- EuroFIR, database di composizione alimentare: https://www.eurofir.org/food-information/food-composition-databases/

### Benchmark
- MyFitnessPal, “Where does MyFitnessPal get its food data?” (aggiornato 4 marzo 2026): https://support.myfitnesspal.com/hc/en-us/articles/360032271252-Where-does-MyFitnessPal-get-its-food-data

---

**Conclusione:** il Brasile è il mercato con il dataset locale già preparato (TACO), ma l'autorizzazione commerciale e l'integrazione nell'app restano da chiudere. Per il Golfo, Saudi e Bahrain hanno fonti nazionali promettenti ma diritti di riutilizzo non ancora chiariti; per UAE, Qatar e Kuwait è più corretto usare USDA + Open Food Facts piuttosto che inventare o redistribuire dati non autorizzati.
