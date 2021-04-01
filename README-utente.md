# batch-mailer
batch-mailer è un sistema che consente di inviare in contemporanea più messaggi di Posta Elettronica Certificata (PEC). 

## Template e lista di dati
Per poter effettuare questo invio multiplo, occorrono 2 file:
1. un template in formato .docx che include una o più variabili nella forma "${variabile}";
2. una lista di dati in formato .xlsx (o .csv) che include i campi corrispondenti alle variabili del documento.

Le variabili del template verranno sostituite dai valori specificati all'interno della lista di dati. Esempi di template e di lista sono disponibili qui di seguito:

![docx](https://github.com/synapta/batch-mailer/blob/master/docs/docx.png)

![xlsx](https://github.com/synapta/batch-mailer/blob/master/docs/xlsx.png)

I 2 file verranno elaborati da batch-mailer che si occuperà di creare il contenuto delle email da inviare (1 email per ciascuna riga della lista). La lista dovrà necessariamente contenere tutte le variabili che sono presenti all'interno del template.

Oltre a questi, è richiesto di specificare 2 ulteriori campi obbligatori che non occorre definire all'interno del template:
* il campo `oggetto`, i cui valori verranno utilizzati da batch-mailer come oggetto (subject) delle email;
* il campo `pec`, i cui valori verranno utilizzati da batch-mailer come caselle di destinazione delle email.

E' possibile inoltre inserire nella lista dei campi facoltativi per gli allegati. Questi campi devono essere specificati nella forma `allegato1`, `allegato2`, `allegato3`, ecc. Per ciascun campo di tipo allegato, occorre inserire un link a un file pubblicamente accessibile e disponibile su next cloud. Batch-mailer si occuperà di caricare i link come allegati della email.

Di seguito sono riportate le istruzioni per l'invio massivo delle email.

## Accesso all'applicazione
Per poter utilizzare batch-mailer, occorre effettuare un doppio click su il file denominato `main.exe`.

A questo punto, l'utente accederà a 2 finestre differenti:
* Una schermata nera dalla quale è possibile monitorare le operazioni di batch-mailer.
* Un'interfaccia grafica che consente all'utente di utilizzare direttamente batch-mailer.

## Login sul server di posta
Per poter effettuare l'invio delle PEC, occorre collegarsi al proprio server di posta. 

![login](https://github.com/synapta/batch-mailer/blob/master/docs/login.png)

Questa operazione richiede di inserire 4 informazioni differenti:
* L'indirizzo email della propria casella PEC (mittente).
* La password di accesso della propria casella PEC.
* L'indirizzo del server di posta. Questo valore dipende dal proprio gestore. Nel caso di [Register](https://www.pec.net/), il valore da inserire nel campo è: `smtp.pec-email.com` (già inserito come valore di default).
* La porta del server, il cui valore di default è `465`.

Una volta inseriti i valori nei campi del form, è possibile cliccare sul bottone `Effettua l'accesso`.

## Caricamento del template e della lista
Se l'operazione precedente è andata a buon fine, sarà possibile effettuare il caricamento del template e della lista. Per il caricamento è possibile cliccare sui pannelli e selezionare il file desiderato, oppure trascinare direttamente il file sul pannello.

Il pannello in alto consente di caricare il template della email, mentre il pannello in basso consente di caricare la lista di dati. Una volta effettuato il caricamento, cliccare su `Controlla validità`.

![load](https://github.com/synapta/batch-mailer/blob/master/docs/load.png)

Batch-mailer effettuerà una serie di controlli sui file inseriti, tra cui ad esempio:
* Un controllo sull'esistenza dei campi obbligatori `oggetto` e `pec`.
* Un controllo di coerenza tra le variabili del template e i campi della lista. Se non c'è coerenza, all'utente verranno mostrati le variabili e i campi, così da aiutarlo a correggere gli errori.
* Un controllo sul formato dei file inserito.

![loaded](https://github.com/synapta/batch-mailer/blob/master/docs/loaded.png)

## Anteprima dei messaggi di posta
Se l'operazione precedente è andata a buon fine, l'utente accederà a una schermata con 2 tipologie di informazioni:
* Un'anteprima della email da inviare. In particolare, l'utente visualizzerà la mail contenente i dati della prima riga della lista.
* Una lista dei destinatari (con il dettaglio complessivo del numero di email che verranno inviate).

A questo punto sarà possibile effettuare 2 operazioni:
* Cliccare su `Modifica i file caricati` per correggere eventuali errori dell'utente.
* Cliccare su `Invia le mail` per poter effettuare l'invio massivo. Un'ulteriore richiesta di conferma apparirà di fronte all'utente per prevenire qualsiasi tipo di invio non voluto.

![preview](https://github.com/synapta/batch-mailer/blob/master/docs/preview.png)

## Esito dell'invio
Al termine dell'invio massivo, l'utente accederà alle informazioni relative all'esito di tale invio. Quest'ultimo si presenterà come una lista in cui, per ciascun destinatario, verrà mostrato l'esito positivo con l'etichetta `OK` oppure verranno visualizzati eventuali errori.

![results](https://github.com/synapta/batch-mailer/blob/master/docs/results.png)

*ATTENZIONE: attualmente il protocollo universale di funzionamento delle email non consente di identificare errori dell'invio dovuto a indirizzi mail non esistenti. Pertanto, batch-mailer indicherà esito positivo anche in questo caso. Tuttavia, per l'utente sarà possibile verificare questo tipo di errore direttamente sulla propria casella di posta*.

L'utente avrà la possibilità di stampare l'esito dell'invio, cliccando su `Stampa il resoconto`, oppure effettuando un nuovo invio cliccando su `Invia nuove mail`.
