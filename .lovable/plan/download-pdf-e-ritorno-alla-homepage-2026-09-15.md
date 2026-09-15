# Download PDF e ritorno alla homepage

## Obiettivo

Aggiungere in fondo a ogni scheda modello due azioni chiare:

- scaricare un PDF completo del modello;
- tornare alla homepage con l’elenco di tutti i modelli.

## Contenuto del PDF

Il documento userà la lingua selezionata nell’app al momento del download (EN oppure RU) e includerà:

1. nome e ID del modello;
2. immagine principale;
3. descrizione;
4. varianti colore con codice e immagine;
5. tutte le schede di Styling & Combinations, ciascuna con il proprio testo e le sole immagini associate;
6. consigli di vendita;
7. domande e risposte della gestione obiezioni.

## Implementazione

1. Aggiungere una generazione PDF lato utente con supporto ai testi cirillici e paginazione automatica.
2. Creare un layout PDF pulito e coerente con l’identità Luisa Spagnoli, ottimizzato per fogli A4.
3. Gestire il caricamento delle immagini prima della creazione del documento; quando una foto non è disponibile, mostrare un segnaposto senza bloccare il download.
4. Aggiungere le etichette bilingui necessarie per “Scarica PDF”, stato di preparazione, eventuale errore e “Torna a tutti i modelli”.
5. Inserire in fondo alla scheda un pulsante principale con icona download e un secondo comando per tornare alla homepage.
6. Durante la preparazione, disabilitare il pulsante PDF e mostrare chiaramente lo stato, evitando download multipli.

## Verifica

- Provare il download in EN e RU su una scheda completa come Festone.
- Controllare visivamente tutte le pagine del PDF per testi tagliati, caratteri cirillici, immagini deformate e separazione corretta dei look.
- Verificare i due pulsanti su desktop e mobile e confermare che il ritorno apra la homepage.
- Controllare che l’app non presenti errori dopo l’aggiornamento.
