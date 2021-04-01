# batch-mailer
batch-mailer è un sistema che consente di inviare in contemporanea più messaggi di Posta Elettronica Certificata (PEC). 

## Template e lista di dati
Per poter effettuare questo invio multiplo, occorrono 2 file:
1. un template in formato .docx che include una o più variabili nella forma "${esempio}";
2. una lista di dati in formato .xlsx (o .csv) che include i campi corrispondenti alle variabili del documento.

Le variabili del template verranno sostituite dai valori specificati all'interno della lista di dati. Un esempio di template e di lista sono disponibili qui di seguito:

INSERIMENTO DELLE 2 IMMAGINI

I 2 file verranno elaborati da batch-mailer che si occuperà di creare il contenuto delle email (1 per ciascuna riga della lista). La lista dovrà necessariamente contenere tutte le variabili che sono presenti all'interno del template.

Oltre a questi, è richiesto di specificare 2 ulteriori campi obbligatori che non occorre definire all'interno del template:
* il campo `oggetto`, i cui valori verranno utilizzati da batch-mailer come oggetto (subject) delle email;
* il campo `pec`, i cui valori verranno utilizzati da batch-mailer come inidirizzi di destinazione delle email.

E' possibile inoltre inserire nella lista dei campi facoltativi per gli allegati. Questi campi devono essere specificati nella forma `allegato1`, `allegato2`, `allegato3`, ecc. Per ciascun campo di tipo allegato, occorre inserire un link a un file pubblicamente accessibile e disponibile su next cloud. Batch-mailer si occuperà di caricare i link come allegati della mail.

Di seguito sono riportate le istruzioni per l'invio massivo delle mail.

## Accesso all'applicazione
Per poter utilizzare batch-mailer, occorre effettuare un doppio click su il file denominato `main.exe`.

A questo punto, si apriranno di fronte all'utente 2 nuove finestre:
* Una finestra nera dal quale è possibile monitorare le operazioni di batch-mailer.
* Un'interfaccia grafica che consente all'utente di utilizzare direttamente batch-mailer.

## Login sul server di posta
Per poter effettuare l'invio delle PEC, occorre collegarsi al proprio server di posta. Questa operazione richiede di inserire 4 informazioni differenti:
* L'indirizzo mail della propria casella PEC (mittente).
* La password di accesso della propria casella PEC.
* L'indirizzo del server di posta. Questo valore dipende dal proprio gestore. Nel caso di [Register](https://www.pec.net/), il valore da inserire nel campo è: `smtp.pec-email.com` (già inserito come valore di default).
* La porta del server, il cui valore di default è `465`.

Una volta inseriti i valori nei campi del form, è possibile cliccare sul bottone `Effettua l'accesso`.

## Caricamento del template e della lista
Se l'operazione precendente è andata a buon fine, sarà possibile effettuare il caricamento del template e della lista. Per il caricamento è possible cliccare sui pannelli e selezionare il file desiderato, oppure trascire direttamente il file.

Il pannello in alto consente di caricare il template, mentre il pannello in basso consente di caricare la lista di dati. Una volta effettuato il caricamento, cliccare su `Controlla validità`.

INSERIMENTO IMMAGINE LOAD

Batch-mailer effettuerà tutta una serie di controlli sui file inseriti, tra cui ad esempio:
* Un controllo sull'esistenza dei campi obbligatori `oggetto` e `pec`.
* Un controllo di coerenza tra le variabili del template e i campi della lista. Se non c'è coerenza, all'utente verranno mostrati le variabili e i campi, così da aiutarlo a correggere gli errori.
* Un controllo sul formato dei file inserito.

INSERIMENTO IMMAGINE LOADED

## Anteprima dei messaggi di posta
Se loperazione precedente è andata a buon fine, l'utente accederà a una schermata con 2 tipologie di informazioni:
* Un'anteprima della mail inviata. In particolare, l'utente visualizzerà la mail contenente i dati della prima riga della lista.
* Una lista dei destinatari (con il dettaglio del numero di mail che verranno inviate).

A questo punto sarà possibile effettuare 2 operazioni:
* Cliccare su `Modifica i file caricati` per correggere eventuali errori dell'utente (LINK ALLA SEZIONE PRECEDENTE).
* Cliccare su `Invia le mail` per poter effettuare l'invio massivo. Un'ulteriore richiesta di conferma apparirà di fronte all'utente per prevenire qualsiasi tipo di invio non voluto.

IMMAGINE DELL'ANTEPRIMA.

## Esito dell'invio
Una volta in cui le mail sono state inviate, l'utente accederà alle informazioni relative all'esito dell'invio. Tale esito si presenterà come una lista in cui, per ciascun destinatario, verrà mostrato l'esito positivo con l'etichetta `OK` oppure verranno visualizzati eventuali errori nell'invio.

IMMAGINE DELL'ESITO

*ATTENZIONE: attualmente il protocollo universale di funzionamento delle mail non consente di identiicare errori dell'invio dovuto a indirizzi mail non esistenti. Pertanto, batch-mailer indicherà esito positivo anche in questo caso. Tuttavia, per l'utente sarà possibile verificare questo tipo di errore direttamente sulla propria casella di posta*.

L'utente avrà la possibilità di stampare l'esito dell'invio, cliccando su `Stampa il resoconto`, oppure effettuando un nuovo invio cliccando su `Invia nuove mail`.










Questo strumento consente agli utenti di inviare più messaggi di posta, combinando un file modello (.docx) e un riempimento foglio (.csv o .xlsx) per riempire il modello. Pertanto, per poter utilizzare lo strumento, è necessario preparare due file diversi:

* un file .docx che include variabili nella forma di "$ {variabile}";
* un file .xlsx (o .csv), che include i campi corrispondenti alle variabili .docx.

Inoltre, i file .xlsx richiedono due campi obbligatori:
* `oggetto`: include la stringa per l'oggetto dell'email;
* `pec`: include un indirizzo email valido;

Il file .xlsx può anche includere campi allegati nella forma di `allegato1`,` allegato2`, `allegaton`. È possibile inserire collegamenti validi in questi campi, che verranno scaricati e allegati all'e-mail.