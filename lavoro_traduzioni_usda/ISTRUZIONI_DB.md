# Traduzione dei nomi alimenti delle banche dati Ketorbit

Banche dati nutrizionali (CIQUAL francese, BLS tedesca, CoFID britannica, CREA italiana, USDA americana) usate in un'app di diario alimentare. Ogni voce e' il NOME DI UN ALIMENTO come in una tabella di composizione (es. "Chicken, broilers or fryers, breast, meat only, cooked, roasted"). Devi produrre i nomi nelle lingue mancanti, nello stile delle traduzioni GIA' presenti nelle altre lingue dell'app: guarda a campione `/home/user/easyketo-ciqual-data/ciqual_2025.json` (campi `nome`, `nome_it`, `nome_fr`, `nome_es`, `nome_de`) per il tono e la struttura prima di cominciare.

## Formato
Input `in_<db>_NN.json`: lista di oggetti con `id` e il nome nelle lingue gia' disponibili (`en`, `it`, `fr`, `de`, `categoria`...). Output `out_<db>_NN.json`: `{"<id>": {"<lingua>": "...", ...}}` con SOLO le lingue richieste dal tuo prompt, per OGNI id.

## Regole generali (tutte le lingue)
- MANTIENI la struttura del nome: segmenti separati da virgola nello stesso ordine ("Alimento, variante, parte, stato, preparazione"), maiuscola solo sul primo segmento (i nomi propri e in tedesco i sostantivi mantengono la loro maiuscola). Non riordinare in "frase naturale": la forma e' quella delle tabelle di composizione (es. it "Pollo, petto, solo carne, cotto, arrosto"; es "Pollo, pechuga, solo carne, cocida, asada").
- Traduci TUTTO il senso, comprese specifiche (percentuali, "NFS", "ns as to ...", "with/without salt", marche). Percentuali e numeri restano identici. Marchi registrati e nomi propri (McDonald's, Kellogg's, Worcestershire, Parmesan DOP...) invariati.
- Alimenti tipici di un paese senza equivalente (haggis, pierogi, tamales, mochi, Yorkshire pudding...): mantieni il nome originale e traduci solo gli altri segmenti; aggiungi una breve spiegazione tra parentesi SOLO se il nome non e' comprensibile in quella lingua.
- Niente newline, niente spazi iniziali/finali, niente virgolette tipografiche.
- Stesse parole sempre per la stessa cosa in tutto il tuo lotto (usa il glossario sotto e resta coerente).

## Glossario obbligatorio (stati e specifiche piu' frequenti)
| EN | it | fr | es | de | pt-BR |
|---|---|---|---|---|---|
| raw | crudo/a | cru(e) | crudo/a | roh | cru(a) |
| cooked | cotto/a | cuit(e) | cocido/a | gekocht | cozido/a |
| boiled | bollito/a | bouilli(e) | hervido/a | gekocht | cozido(a) em água |
| roasted | arrosto | rôti(e) | asado/a | gebraten (im Ofen) | assado/a |
| baked | al forno | cuit(e) au four | al horno | gebacken | assado/a no forno |
| fried | fritto/a | frit(e) | frito/a | frittiert | frito/a |
| grilled/broiled | alla griglia | grillé(e) | a la parrilla | gegrillt | grelhado/a |
| steamed | al vapore | cuit(e) à la vapeur | al vapor | gedämpft | cozido(a) no vapor |
| stewed/braised | brasato/stufato | braisé(e)/mijoté(e) | estofado/a | geschmort | refogado/a ou ensopado/a |
| dried | secco/a | séché(e) | seco/a | getrocknet | seco/a |
| dehydrated | disidratato/a | déshydraté(e) | deshidratado/a | dehydriert | desidratado/a |
| canned | in scatola | en conserve | en conserva | aus der Dose | enlatado/a |
| frozen | surgelato/a | surgelé(e) | congelado/a | tiefgekühlt | congelado/a |
| fresh | fresco/a | frais (fraîche) | fresco/a | frisch | fresco/a |
| drained | sgocciolato/a | égoutté(e) | escurrido/a | abgetropft | escorrido/a |
| solids and liquids | solidi e liquidi | solides et liquides | sólidos y líquidos | feste und flüssige Bestandteile | sólidos e líquidos |
| with salt / without salt | con sale / senza sale | avec sel / sans sel | con sal / sin sal | mit Salz / ohne Salz | com sal / sem sal |
| unsalted | non salato | non salé | sin sal | ungesalzen | sem sal |
| salted | salato | salé | salado | gesalzen | salgado |
| sweetened / unsweetened | zuccherato / non zuccherato | sucré / non sucré | azucarado / sin azúcar | gezuckert / ungezuckert | adoçado / sem açúcar |
| low fat | a basso contenuto di grassi | allégé / pauvre en matières grasses | bajo en grasa | fettarm | com baixo teor de gordura |
| nonfat / fat free | senza grassi | sans matières grasses | sin grasa | fettfrei | sem gordura |
| whole (milk, grain) | intero / integrale | entier / complet | entero / integral | Voll- / Vollkorn- | integral |
| skim | scremato | écrémé | desnatado | entrahmt | desnatado |
| lean | magro | maigre | magro | mager | magro |
| lean and fat | magro e grasso | maigre et gras | magro y grasa | mager und fett | magro e gordura |
| separable lean only | solo parte magra | partie maigre seulement | solo parte magra | nur magerer Anteil | apenas parte magra |
| trimmed to 1/4" fat | grasso rifilato a 6 mm | gras paré à 6 mm | grasa recortada a 6 mm | Fett auf 6 mm getrimmt | gordura aparada a 6 mm |
| boneless | disossato | désossé | deshuesado | ohne Knochen | sem osso |
| bone-in | con osso | avec os | con hueso | mit Knochen | com osso |
| skinless | senza pelle | sans peau | sin piel | ohne Haut | sem pele |
| with skin | con pelle | avec peau | con piel | mit Haut | com pele |
| meat only | solo carne | viande seule | solo carne | nur Fleisch | apenas carne |
| meat and skin | carne e pelle | viande et peau | carne y piel | Fleisch und Haut | carne e pele |
| ground | macinato | haché | picado/molido | gehackt/Hack- | moído |
| chopped | tritato | haché | picado | gehackt | picado |
| sliced | a fette | tranché | en lonchas/rodajas | in Scheiben | fatiado |
| diced | a cubetti | en dés | en dados | gewürfelt | em cubos |
| shredded | grattugiato/sfilacciato | râpé/effiloché | rallado/deshebrado | geraspelt/gezupft | ralado/desfiado |
| pitted | snocciolato | dénoyauté | sin hueso | entsteint | sem caroço |
| peeled | sbucciato | pelé | pelado | geschält | descascado |
| with/without peel (skin, "with skin") for fruit | con/senza buccia | avec/sans peau | con/sin piel | mit/ohne Schale | com/sem casca |
| seedless | senza semi | sans pépins | sin semillas | kernlos | sem sementes |
| enriched | arricchito | enrichi | enriquecido | angereichert | enriquecido |
| fortified | fortificato | fortifié | fortificado | angereichert | fortificado |
| unenriched | non arricchito | non enrichi | sin enriquecer | nicht angereichert | não enriquecido |
| commercially prepared | di produzione industriale | préparé industriellement | de preparación industrial | handelsüblich zubereitet | industrializado |
| homemade / home-prepared | fatto in casa | fait maison | casero | hausgemacht | caseiro |
| restaurant | da ristorante | de restaurant | de restaurante | aus dem Restaurant | de restaurante |
| fast food | fast food | fast-food | comida rápida | Fast Food | fast food |
| ready-to-eat | pronto da mangiare | prêt à consommer | listo para comer | verzehrfertig | pronto para consumo |
| instant | istantaneo | instantané | instantáneo | Instant- | instantâneo |
| prepared with water / with milk | preparato con acqua / latte | préparé avec de l'eau / du lait | preparado con agua / leche | mit Wasser / Milch zubereitet | preparado com água / leite |
| not further specified (NFS) | non specificato | non spécifié | no especificado | nicht näher bezeichnet | não especificado |
| NS as to ... | non specificato se ... | non précisé si ... | sin especificar si ... | nicht angegeben ob ... | não especificado se ... |
| with / without (generic) | con / senza | avec / sans | con / sin | mit / ohne | com / sem |
| and / or | e / o | et / ou | y / o | und / oder | e / ou |
| juice | succo | jus | zumo | Saft | suco |
| sauce | salsa/sugo | sauce | salsa | Sauce | molho |
| soup | zuppa | soupe | sopa | Suppe | sopa |
| bread | pane | pain | pan | Brot | pão |
| cheese | formaggio | fromage | queso | Käse | queijo |
| milk | latte | lait | leche | Milch | leite |
| butter | burro | beurre | mantequilla | Butter | manteiga |
| oil | olio | huile | aceite | Öl | óleo (azeite se oliva) |
| egg(s) | uovo/uova | œuf(s) | huevo(s) | Ei/Eier | ovo(s) |
| beef / pork / lamb / veal | manzo / maiale / agnello / vitello | bœuf / porc / agneau / veau | vacuno (res) / cerdo / cordero / ternera | Rind / Schwein / Lamm / Kalb | carne bovina / carne suína / cordeiro / vitela |
| chicken / turkey | pollo / tacchino | poulet / dinde | pollo / pavo | Huhn / Pute | frango / peru |
| shrimp / prawn | gambero | crevette | gamba/camarón | Garnele | camarão |
| ham / bacon / sausage | prosciutto / pancetta / salsiccia | jambon / lard (bacon) / saucisse | jamón / beicon / salchicha | Schinken / Speck / Wurst | presunto / bacon / salsicha |
| corn / potato / tomato | mais / patata / pomodoro | maïs / pomme de terre / tomate | maíz / patata / tomate | Mais / Kartoffel / Tomate | milho / batata / tomate |
| candy / cookie / cake | caramella / biscotto / torta | bonbon / biscuit / gâteau | caramelo / galleta / pastel | Bonbon / Keks / Kuchen | bala / biscoito / bolo |

pt-BR: portoghese del BRASILE (suco, café da manhã, abobrinha, mandioca, cenoura, presunto, bacon, geladeira...), mai europeo (sumo, pequeno-almoço, courgette).
Tedesco: sostantivi con maiuscola; composti normali ("Hähnchenbrust"). Spagnolo: neutro internazionale (preferisci i termini di uso comune in America Latina e Spagna; "carne de res" o "vacuno" per manzo: usa "vacuno" per i tagli, "res" se la fonte dice beef generico, ma resta coerente nel lotto).

## Procedura
1. Leggi il file di input e il file `ciqual_2025.json` a campione per lo stile.
2. Traduci TUTTE le voci a blocchi di ~60-100, scrivi `out_...json` (JSON UTF-8, ensure_ascii=False). Usa uno script Python per assemblare l'output se serve, ma controlla che nessun id manchi.
3. Esegui `python3 -I /tmp/claude-0/-home-user/465a224a-64ac-5730-bdf5-6719801e5d69/scratchpad/validate_names.py <input> <output> <lingue_csv>` fino a "0 problemi".
4. Non toccare altri file. Rispondi con 1-2 righe: voci tradotte, esito, fino a 5 dubbi.
