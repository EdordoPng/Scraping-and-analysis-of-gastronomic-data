
# Reperimento automatico ed analisi di dati gastronomici 
        Scraping and analysis of gastronomic data  


## Note esplicative
Questo progetto fa uso di queste distinzioni per rendere più chiara la tetodologia di approccio :  
   - Portata : Un insieme di ricette attinenti alla stessa tipologia, es. primi piatti, contorni, dolci ...
   - Ricetta : Oggetto di analisi principale della quale vogliamo ottenere le informazioni dal sito
   - Ingredienti : insieme di alimenti necessari per la realizzazione della ricetta 


# WORKFLOW 
Per andare ad eseguire la attività, si tenga in considerazione questo workflow che mostra il corretto uso in sequenza dei programmi presenti nella cartella recipe-finder

# 1 ) Ottenere un file json con tutti i dettagli di una specifica portata desiderata
        
Esempio comando da terminale : python [Percorso]/webScraping-dissapore/scrapingPortata.py antipasti 1
    
Viene eseguito il programma scrapingPortata.py che prende in ingresso la portata desiderata ed il tempo (in secondi) didormienza che si desidera attendere tra l'analisi di una ricetta e la sucessiva. 

A tal proposito viene usato il file portata.conf in cui è possibile, per l'utente non programmatore, andare a visionare 
i link alle varie portate, come anche le portate disponibili all'analisi. 

Viene prodotto in output, nella cartella "cartella_portate" un file json rinominato con il nome della portata analizzata. 
Se "cartella_portate" non esistesse, viene auto generata dal programma. 

Esso contiene le relative ricette, con dati gestiti in questo modo :

    "title" : nome della ricetta
    "description" : desccrizione accurata della ricetta
    "instructions" : insieme di passi da svolgere per creare il piatto ompleto
    "ingredients" : array di ingredienti con i seguenti campi 
        "name" (str) 
        "amount" (str) 
    "details" : stringa contenente un insieme di informazioni utili


# 2 ) Collezione in file unico di tutti i dati raccolti

Esempio comando da terminale : python [Percorso]/dataCollector/dataCollector.py cartella_portate

Viene eseguito il programma dataCollector.py che prende in ingresso il nome della cartella contenente tutti
i file json ottenuti chiamando, ripetutamente e per varie portate, il programma 1 
Vengono analizzati i diversi json relativi alle diverse portate e vengono creati in output 2 file json,
i quali estrapolano ulteriori dati. Nota che i file presenti in cartella_portate, il cui nome 
è presente nel file to_skip.conf (presente in cartella_portate), saranno scartati dall' analisi. 

## Cookbook.json : 

Questo file contiene tutte le ricette analizzate. I dati son così presentati:

    "title" : nome della ricetta
    "description" : descrizione accurata della ricetta
    "instructions" : insieme di passi da svolgere per creare il piatto completo
    "ingredients" : array di ingredienti con i seguenti campi 
        "Nome" (str) 
        "Quantità" (str)
        "Unità di misura" (str)
    "portions" : numero di persone per cui è predisposta la ricetta
    "details" : stringa contenente un insieme di informazioni utili
    "acquisition time": timestamp in cui le informazioni sono state reperite
    "link": URL della pagina web in cui sono presenti le informazioni delle ricetta
    "portata_name": nome della portata a cui una ricetta fa riferimento

## Cookbook_SingleServing.json : 

Questo file contiene tutte le ricette analizzate, i dati sono stati rimodellati per ottenere le ricette in formato porzione singola, inoltre sono stati estratti ulteriori dati così da poterli usare in modo più semplice.
I dati son così presentati:
    
    "Titolo" : nome della ricetta
    "Descrizione" : descrizione accurata della ricetta
    "Istruzioni" : insieme di passi da svolgere per creare il piatto completo
    "Ingredienti" : array di ingredienti con i seguenti campi 
        "Nome" (str) 
        "Quantità" (str)
        "Unità di misura" (str)
    "Kcal" (int)
    "Cucina" (str)
    "Difficoltà" (str)
    "Tempo Cottura" (str)
    "Tempo Preparazione" (str)
    "Senza Glutine" (boolean)
    "Senza Lattosio" (boolean)
    "Senza Glutine" (boolean)
    "Data Acquisizione": timestamp in cui le informazioni sono state reperite
    "Link": URL della pagina web in cui sono presenti le informazioni delle ricetta
    "Portata di appartenenza": nome della portata a cui una ricetta fa riferimento

Nota che il file to_skip.conf presente nella cartella "cartella_portate" viene usato da dataCollector.py per andare a 
scartare determinati file da non considerare nell'analisi.
Dunque all'interno del file to_skip.conf l'utente non programmatore puyò andare a modificare il file settando i file che 
si desidera escludere dall'analisi, qualora presenti.


# 3 ) Analisi dei dati

Esempio comando da terminale : python [Percorso]/dataAnalysisCSV/dataAnalysis.py 

Viene eseguito il programma dataAnalysis.py che non prende in ingresso alcun parametro, ma si limita ad 
estrapolare il nome della cartella ed il nome del file da analizzare tramite il file dataAnalysis.conf. 
dataAnalysis.py produce in output diversi file, i quali che possono essere sfruttati indipendentemente :

- Viene creato il file "ingr_storage.csv" che contiene tutti gli ingredienti presenti nelle ricette analizzate, 
nota che vien settato di default una unità di misura = 0
I dati son inseriti con questo formato :                            Nome, Quantita, Unità di misura
    
- Viene creato il file "ingr_storage1.csv", il quale presenta gli stessi dati di ingr_storage.csv.
Vien creato per poter esser manualmente modificato cambiando l'attributo "Quantità" di determinati ingredienti. 
Questo file verrà poi usato nella futura esecuzione del programma "magazzino.py" per andare ad inizializzare il
contenuto del magazzino da uno stato di partenza (e non da vuoto).

- Viene creato il file "elenco_uso_ingredienti.csv" che contiene tutti gli ingredienti presenti nel cookbook analizzato,ordinati lessiograficamente, ognuno con un proprio contatore di uso. Il contatore indica quante volte l'ingrediente è stato usato all'interno delle ricette nel file Cookbook_SingleServing.json creato precedentemente. Per modificare il file da usare, modificare manualmente il file dataAnalysis.py.
I dati verranno forniti in una tabella con attributi :               Nome, Contatore uso, Unità di misura 

- Viene creato il file "elenco_ingredienti.txt" che contiene tutti gli ingredienti presenti nel cookbook analizzato


# 4 ) Computazione degli ingredienti genitori (primari)

Gli ingredienti primari vengono definiti in modo diverso per Dissapore e Planeat. 

Esempio comando da terminale : python [Percorso]/testAzienda/parentComputation.py 

Eseguito questo programma, vien creata cartella_genitori, una cartella che andrà a ontenere l'output prodotto. 

- Viene creato il file "all_dissapore_ing.txt" che contiene tutti i nomi di ingredienti del dataset Dissapore 

- Viene creato il file "all_planeat_ing.txt" che contiene tutti i nomi di ingredienti del dataset Planeat 

- Viene creato il file "genitore_1_mio.csv" che contiene tutti i nomi di ingredienti che sono considerati tali secondo 
il fatto che il nome dell' ingrediente sia incluso almeno una volta nel titolo delle ricette presenti nel file cookbook.

- Viene creato il file "genitore_1_loro.csv" che contiene tutti i nomi di ingredienti che sono considerati tali secondo 
il fatto che, per come sono definiti gli ingredienti nel dataBase Planeat, non abbiamo un ingrediente genitori all'interno
del campo prime_item_id. Per visionare ciò basta aprire il file ingredienti-planeat.csv (presente in test azienda)


# 5 ) Computazione similarità tra ingredienti

Esempio comando da terminale : python [Percorso]/testAzienda/completeFuzzy.py 

Questo programma serve per andare a confrontare tutti gli ingredienti Planeat con quelli Dissapore per cercare corrispondenze. Salva l'output in un file csv che avrà come prima colonna gli ingredienti Planeat e sulla seconda quelli Dissapore.
Vi sarà un indice da 0 a 100 che indica quanto è buona la similaritò tra le parole.
Poichè per svolere questo compito possono essere adoperate varie metodologie per ottenere il massimo risultato, sono 
stati creati metodi alternativi che adempiscono differentemente a questo scopo. I programmi : 

- completeFuzzy.py      (usa la funzione ratio base)

- completeFuzzy2.py     (ritorna 0 se prima parola dei due ingredienti diversa, ultima lettera troncata)

- completeFuzzy2B.py    (se prima parola dei due ingredienti diversa, con ultima lettera troncata, fuzzy base)

- completeFuzzy3.py     (controlla uguaglianza ed implementa un contributo moltiplicativo)

- completeFuzzy4.py     (controlla uguaglianza ed implementa un contributo additivo)

- completeFuzzy5.py     (controlla uguaglianza ed implementa contributo additivo e moltiplicativo)

- completeFuzzy6.py     (controlla uguaglianza ed implementa contributo additivo e moltiplicativo e requisiti di lunghezza)

Se eseguiti singolarmente, permettono di ottenere un file csv in output, che sarà inserito in testAzienda/cartella_matching.
Questi csv sono stati ottenuti impostando una soglia da 0 a 100 al di sotto della quale scartare una corrispondenza, ed inoltre
modificano in modo diverso il punteggio di fuzzy similarity.

E' stato inoltre eseguito il programma completeFuzzy.py con una soglia pari ad 1 per ottenere il matching base completo.
E' stato anche eseguito con una soglia pari ad 83 per avere una idea nel numero di matching


# 6 ) Estrazione set di validazione 
    
Esempio comando da terminale : python [Percorso]/testAzienda/validateFuzzy.py 

Per poter andare a valutare quale sia il miglior modello tra i 6 proposti al punto precedente, serve valutare i loro output.
Per svolgere ciò serve estrarre un insieme di tuple dal file complete_fuzzy_soglia_1.csv, il quale contiene 
matching tutti a tutti degli ingredienti dei due dataset. 

Nel codice proposto sono state estratte 1000 tuple dal file complete_fuzzy_soglia_1.csv seguendo la metodologia di 
scelta di 100 campioni negli intervalli di somiglianza [i*10, (i + 1) * 10] con i = 0, 1 , … ,9
L' output è posto nel file saggio_1000_righe_fuzzy.csv

In seguito è stata necessario un assegnamento manuale dell’output desiderato (ground truth) ponendo a 1 se vi è similarità, altrimenti 0 (nell' analisi della similaritò tra due ingredienti). Le scelte effettuate sono visibili nel file Ingredient_Validation_Set_(Prof).xlsx ed in validation_set.csv


# 7 ) Test ed Analisi funzioni di similarità 

Esempio comando da terminale : python [Percorso]/testAzienda/testFuzzy.py 

Uso del validation_set.csv per determinare le performance delle 7 funzioni di similarità.
I risultati sono stampati sul terminale, inoltre li ottengo anche nel file testFuzzy che è presente sia in formato csv che xlsx.
Questo programma controlla quante risposte corrette otteniamo analizzando validation_set.csv
Otteniamo questo valore e lo confrontiamo con la risposta che otteniamo in vari metodi cf1 ... cf6, definiti in modi diversi
Tramitre la matrice di confusione otteniamo, nei vario casi, i seguenti dati : 

- True Negative
- False Positive,
- False Negative,
- True Positive
- Precision
- Speificity
- Recall
- F1_score

Analizzando tali dati, il metodo 2 è risultato il più performante. 
Impostando in seguito la soglia ad 70 (su 100), uso testAzienda/completeFuzzy2.py per ottenere il matching completo tra le due liste di ingredienti, trovando 975 corrispondenze.


# 8 ) Computazione ricette realizzabili 

Esempio comando da terminale : python [Percorso]/dataAnalysisCSV/craftableRecipesPlaneat.py 

Questo programma trova le ricette che possono esser realizzate, controllando gli ingredienti e valutando eventuali sostituti
(degli ingredienti Dissapore nella ricetta) presenti nel file di fuzzy matching. 
Quello utilizzato in questo caso è testAzienda/cartella_matching/complete_fuzzy2.csv
Quel file viene prodotto dal programma che sfrutta il modello più performante tra i 7 creati in testAzienda (riferimento
a completeFuzzy.py , completeFuzzy2.py , ... , completeFuzzy6.py ), tra i quali il secondo è risultato il più performante.

Ricerchiamo inoltre la miglior corrispondenza (tupla che massimizza Fuzzy Score ) nel file csv, tra l’ingrediente Dissapore presente nella ricetta e uno Planeat.
Se l’ingrediente non viene trovato, ricetta non realizzabile e vengono forniti i nomi degli ingredienti mancanti.
Usando questo approccio su 2592 ricette Dissapore, 228 risultano esser realizzabili con gli ingredienti Planeat.

L'elenco dei nomi di tali ricette realizzabili non è posto in un file, ma viene stampato a schermo.
Nel caso si volesse ottenere in un file, basta aggiungere il codice nel main() di craftableRecipesPlaneat, andando a salvare in un file la variabile : "available_reipes"


# 9 ) Creazione tabelle di similarità tra ricette 

Esempio comando da terminale : python [Percorso]/recipeSimilarityChecker/similarityChecker.py 

Questo programma ha lo scopo di creare un dataframe di similarità per ogni Portata analizzata.
Il punteggio di somiglianza tra due diverse ricette, viene ottenuto controllando in primo luogo la similarità coseno
tra gli ingredienti di ciascuna ricetta con gli altri.
Quindi questo valore viene aggiornato utilizzando una logica che prevede di andare a :

- trovare: gli ingredienti primari di una ricetta (gli ingredienti con il nome o parte del loro nome sono contenuti nel nome della ricetta a cui appartengono)
- trovare: ingredienti primari in comune e non in comune tra due ricette
- calcolare: quanti sono gli ingredienti primari totali e ottienere il nuovo valore aggiornato

Per ogni portata analizzata, l'output viene salvato in : 

- CSV in recipeSimilarityChecker/similarity_csv  
- XLSX in recipeSimilarityChecker/similarity_xlsx

I file prodotti contengono i nomi delle ricette come attributi riga e colonna, l'intersezione tra le due indica il valore 
di similarità che è stato trovato in quel determinato caso. 


# Extra ) Ricerca ingredienti genitori in comune ai due dataSet

Esempio comando da terminale : python [Percorso]/testAzienda/compareData.py 

Questo programma da una idea degl numero di ingredienti in ingredienti_1_mio e ingredienti_1_loro.
Si ricercano dapprima dei nomi identici tra gli ingredienti primari di Dissapore e di Planeat.
In seguito si ricercano dei nomi simili tra gli ingredienti primari di Dissapore e di Planeat, usando una funzione 
che calcola la similaritò tra due stringhe come la distanza nelle operazioni da effettuare per trasformare una nell' altra.

- Viene creato il file "parent_ingr_fuzzy_matching.csv" che contiene coppie di ingredienti genitori provenienti dai due 
dataset diversi, con l'indice di similarità calcolato. Nota che questo file è inserito in testAzienda/cartella_matching


# Installation

Le libreie python, richieste per l'eseuzione del codice, sono presenti all'interno del file "requirement.txt" 


# Authors and acknowledgment

- Edoardo Diana (code author) https://github.com/EdordoPng
- Tullio Facchinetti (relatore Università di Pavia)