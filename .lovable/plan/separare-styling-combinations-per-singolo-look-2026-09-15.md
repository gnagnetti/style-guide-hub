# Separare Styling & Combinations per singolo look

## Obiettivo

Ogni combinazione distinta del testo sorgente diventerà una scheda autonoma. Sotto la descrizione di ciascuna scheda compariranno esclusivamente le immagini dei modelli citati in quella combinazione, mantenendo `url.xlsx` come fonte ufficiale delle immagini.

## Modifiche

1. Aggiornare la generazione dei dati per riconoscere come confini di una combinazione:
   - ogni voce `В lookbook (Look …)`;
   - ogni voce `На витрине (Vetrina …)`;
   - gli equivalenti già presenti negli altri testi;
   - i separatori `|` già supportati;
   - i separatori `-` quando introducono una nuova combinazione, senza dividere i trattini usati normalmente dentro una descrizione.
2. Conservare il testo introduttivo e il relativo `Вариант …` nella prima scheda pertinente; propagare il contesto della variante alle combinazioni successive quando serve a non perdere il colore di riferimento.
3. Estrarre articoli, codici e immagini separatamente da ogni nuova scheda, così nessuna scheda eredita immagini citate nelle altre.
4. Rigenerare tutti i 273 modelli usando i file Excel sorgente e mantenere i collegamenti alle schede dei modelli riconosciuti.
5. Verificare in particolare Festone (ID 389): il blocco attuale dovrà produrre sei schede, ciascuna con il proprio testo e i soli articoli associati. Controllare inoltre tutti i modelli interessati per evitare schede vuote o testi troncati.
6. Verificare la pagina su desktop e mobile, l’apertura delle immagini, i collegamenti ai modelli e l’assenza di errori.

## Dettagli tecnici

- La separazione avverrà durante l’importazione, non soltanto a livello grafico, per garantire una corretta relazione testo–immagini in tutta l’app.
- Il formato dati esistente (`looks[]` con `text` e `items[]`) resta invariato; la pagina mostrerà automaticamente una scheda per ogni elemento.
- Le URL non verranno dedotte dal testo: continueranno a essere risolte tramite `url.xlsx`, con segnaposto quando il file non contiene una foto.
