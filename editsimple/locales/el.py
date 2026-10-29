# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Ελληνικά: traduzione dei testi dell'interfaccia di EditSimple.

La chiave e' il testo italiano cosi' come compare nel codice (in tr() e N_()),
il valore la sua traduzione. I segnaposto tra graffe vanno lasciati identici.
Dopo ogni modifica:

    .venv\\Scripts\\python.exe scripts\\check_i18n.py el
"""

from __future__ import annotations

NAME = "Ελληνικά"

CATALOG: dict[str, str] = {
    "Impossibile avviare l'interfaccia: {error}\n\nInstalla le dipendenze con:\n    {command}":
        "Δεν είναι δυνατή η εκκίνηση της διεπαφής: {error}\n\nΕγκαταστήστε τις εξαρτήσεις με:\n    {command}",
    "In alto a sinistra":
        "Πάνω αριστερά",
    "In alto a destra":
        "Πάνω δεξιά",
    "In basso a sinistra":
        "Κάτω αριστερά",
    "In basso a destra":
        "Κάτω δεξιά",
    "Progetto EditSimple":
        "Έργο EditSimple",
    "Tutti i file":
        "Όλα τα αρχεία",
    "Apertura (all'inizio)":
        "Άνοιγμα (στην αρχή)",
    "Chiusura (alla fine)":
        "Κλείσιμο (στο τέλος)",
    "Apri progetto... (Ctrl+O)":
        "Άνοιγμα έργου... (Ctrl+O)",
    "Progetto":
        "Έργο",
    "Nuovo":
        "Νέο",
    "Nuovo progetto (Ctrl+N)":
        "Νέο έργο (Ctrl+N)",
    "Apri":
        "Άνοιγμα",
    "Apri progetto (Ctrl+O)":
        "Άνοιγμα έργου (Ctrl+O)",
    "Salva":
        "Αποθήκευση",
    "Salva progetto (Ctrl+S)":
        "Αποθήκευση έργου (Ctrl+S)",
    "Annulla (Ctrl+Z)":
        "Αναίρεση (Ctrl+Z)",
    "Ripeti (Ctrl+Y)":
        "Επανάληψη (Ctrl+Y)",
    "Clip":
        "Κλιπ",
    "Importa video":
        "Εισαγωγή βίντεο",
    "Importa un video in coda o al cursore (Ctrl+I)":
        "Εισαγωγή βίντεο στο τέλος ή στον δρομέα (Ctrl+I)",
    "Audio":
        "Ήχος",
    "Aggiungi una traccia audio (commento, musica) al cursore":
        "Προσθήκη κομματιού ήχου (σχόλιο, μουσική) στον δρομέα",
    "Taglia":
        "Κοπή",
    "Taglia la clip al cursore (S)":
        "Κοπή του κλιπ στον δρομέα (S)",
    "Elimina":
        "Διαγραφή",
    "Elimina la porzione IN-OUT o l'elemento selezionato (Canc)":
        "Διαγραφή του τμήματος IN-OUT ή του επιλεγμένου στοιχείου (Delete)",
    "Fermo":
        "Πάγωμα",
    "Fermo immagine del fotogramma al cursore (F)":
        "Πάγωμα του καρέ στον δρομέα (F)",
    "Slide":
        "Διαφάνεια",
    "Inserisci una slide":
        "Εισαγωγή διαφάνειας",
    "Velocita'":
        "Ταχύτητα",
    "Velocita' della porzione IN-OUT: piu' veloce o rallentata (V)":
        "Ταχύτητα του τμήματος IN-OUT: γρηγορότερα ή πιο αργά (V)",
    "Sovraimpressioni":
        "Επικαλύψεις",
    "Testo":
        "Κείμενο",
    "Testo (T)":
        "Κείμενο (T)",
    "Immagine":
        "Εικόνα",
    "Immagine sopra il video, da spostare e ridimensionare":
        "Εικόνα πάνω στο βίντεο, για μετακίνηση και αλλαγή μεγέθους",
    "Logo":
        "Λογότυπο",
    "Logo e testo dell'operatore, fermi in un angolo (L)":
        "Λογότυπο και κείμενο χειριστή, σταθερά σε μια γωνία (L)",
    "Riquadro":
        "Πλαίσιο",
    "Riquadro (R): puo' seguire il soggetto":
        "Πλαίσιο (R): μπορεί να ακολουθεί το θέμα",
    "Ovale":
        "Οβάλ",
    "Ovale (E): puo' seguire il soggetto":
        "Οβάλ (E): μπορεί να ακολουθεί το θέμα",
    "Freccia":
        "Βέλος",
    "Freccia (A): puo' seguire il soggetto":
        "Βέλος (A): μπορεί να ακολουθεί το θέμα",
    "Zoom":
        "Ζουμ",
    "Zoom rettangolare: l'area scelta in un riquadro ingrandito (Z)":
        "Ορθογώνιο ζουμ: η επιλεγμένη περιοχή μεγεθυμένη σε πλαίσιο (Z)",
    "Zoom ovale: l'area scelta in un ovale ingrandito (Maiusc+Z)":
        "Οβάλ ζουμ: η επιλεγμένη περιοχή μεγεθυμένη σε οβάλ (Shift+Z)",
    "Pixel":
        "Pixel",
    "Pixelatura rettangolare che insegue il soggetto (P)":
        "Ορθογώνιο ψηφιδωτό που ακολουθεί το θέμα (P)",
    "Pixelatura ovale che insegue il soggetto (K)":
        "Οβάλ ψηφιδωτό που ακολουθεί το θέμα (K)",
    "Uscita":
        "Έξοδος",
    "Esporta MP4":
        "Εξαγωγή MP4",
    "Esporta il video finale (Ctrl+E)":
        "Εξαγωγή του τελικού βίντεο (Ctrl+E)",
    "Inseguimento (VitTrack)":
        "Παρακολούθηση (VitTrack)",
    "Esportazione":
        "Εξαγωγή",
    "Logo e testo dell'operatore":
        "Λογότυπο και κείμενο χειριστή",
    "Angoli arrotondati":
        "Στρογγυλεμένες γωνίες",
    "Crediti":
        "Συντελεστές",
    "Lingua":
        "Γλώσσα",
    "Impostazioni salvate.":
        "Οι ρυθμίσεις αποθηκεύτηκαν.",
    "Download di ffmpeg":
        "Λήψη του ffmpeg",
    "Download di VitTrack":
        "Λήψη του VitTrack",
    "Progetto non salvato":
        "Μη αποθηκευμένο έργο",
    "Salvare le modifiche al progetto?":
        "Αποθήκευση των αλλαγών στο έργο;",
    "Nuovo progetto.":
        "Νέο έργο.",
    "Lettura del video...":
        "Ανάγνωση του βίντεο...",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}":
        "Εισήχθη το {file}: {width}x{height}, {fps:g} fps, {duration}",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}, senza audio":
        "Εισήχθη το {file}: {width}x{height}, {fps:g} fps, {duration}, χωρίς ήχο",
    "Audio di questo pezzo eliminato (il video resta). Ctrl+Z per riaverlo.":
        "Ο ήχος αυτού του κομματιού διαγράφηκε (το βίντεο μένει). Ctrl+Z για επαναφορά.",
    "Clip eliminata.":
        "Το κλιπ διαγράφηκε.",
    "Fermo immagine":
        "Πάγωμα καρέ",
    "Nuovo testo":
        "Νέο κείμενο",
    "Testo aggiunto: trascinalo, ingrandiscilo dagli angoli, doppio clic per riscriverlo.":
        "Το κείμενο προστέθηκε: σύρετέ το, μεγαλώστε το από τις γωνίες, διπλό κλικ για να το ξαναγράψετε.",
    "Modifica testo":
        "Επεξεργασία κειμένου",
    "Immagine aggiunta: trascinala per spostarla, dagli angoli per ridimensionarla.":
        "Η εικόνα προστέθηκε: σύρετέ τη για μετακίνηση, από τις γωνίες για αλλαγή μεγέθους.",
    "Pixelatura con inseguimento":
        "Ψηφιδωτό με παρακολούθηση",
    "Cancellati {count} punti del percorso (il primo resta: e' la partenza della figura).":
        "Διαγράφηκαν {count} σημεία της διαδρομής (το πρώτο μένει: είναι η αφετηρία του σχήματος).",
    "Cancellati {count} punti del percorso.":
        "Διαγράφηκαν {count} σημεία της διαδρομής.",
    "Inseguimento del soggetto":
        "Παρακολούθηση θέματος",
    "Esportazione in corso":
        "Εξαγωγή σε εξέλιξη",
    "montaggio video per presentazioni":
        "μοντάζ βίντεο για παρουσιάσεις",
    "PROGETTO":
        "ΕΡΓΟ",
    "nuovo":
        "νέο",
    "Nessun video":
        "Χωρίς βίντεο",
    "Montaggio":
        "Μοντάζ",
    "Configura":
        "Διαμόρφωση",
    "Riproduci / pausa (Spazio)":
        "Αναπαραγωγή / παύση (Διάστημα)",
    "larghezza logo % del video":
        "πλάτος λογότυπου % του βίντεο",
    "altezza testo % del lato corto":
        "ύψος κειμένου % της μικρής πλευράς",
    "distanza dai bordi % del lato corto":
        "απόσταση από τα άκρα % της μικρής πλευράς",
    "opacita' %":
        "αδιαφάνεια %",
    "angoli arrotondati %":
        "στρογγυλεμένες γωνίες %",
    "sfondo del testo":
        "φόντο κειμένου",
    "riquadro":
        "πλαίσιο",
    "zoom rettangolare":
        "ορθογώνιο ζουμ",
    "pixel rettangolare":
        "ορθογώνιο pixel",
    "Colore del testo":
        "Χρώμα κειμένου",
    "Colore dello sfondo":
        "Χρώμα φόντου",
    "Immagine del logo":
        "Εικόνα λογότυπου",
    "Questa immagine non si apre.":
        "Αυτή η εικόνα δεν ανοίγει.",
    "Controllo in corso...":
        "Έλεγχος...",
    "Pronto.":
        "Έτοιμο.",
    "ffmpeg non e' stato trovato. Scaricalo dal riquadro FFmpeg della pagina Configurazione: senza, non si possono importare ne' esportare video.":
        "Το ffmpeg δεν βρέθηκε. Κατεβάστε το από το πλαίσιο FFmpeg της σελίδας Διαμόρφωση: χωρίς αυτό δεν μπορείτε να εισαγάγετε ούτε να εξαγάγετε βίντεο.",
    "Non salvare":
        "Χωρίς αποθήκευση",
    "Niente da annullare.":
        "Τίποτα για αναίρεση.",
    "inizio":
        "αρχή",
    "fine":
        "τέλος",
    "Apri progetto":
        "Άνοιγμα έργου",
    "File mancanti":
        "Αρχεία που λείπουν",
    "Salva progetto":
        "Αποθήκευση έργου",
    "Dove inserire il video?":
        "Πού να εισαχθεί το βίντεο;",
    "Importazione":
        "Εισαγωγή",
    "Il file non contiene video. Per l'audio usa il pulsante Audio.":
        "Το αρχείο δεν περιέχει βίντεο. Για ήχο χρησιμοποιήστε το κουμπί Ήχος.",
    "Importa prima un video.":
        "Εισαγάγετε πρώτα ένα βίντεο.",
    "Aggiungi traccia audio":
        "Προσθήκη κομματιού ήχου",
    "Il file non contiene audio.":
        "Το αρχείο δεν περιέχει ήχο.",
    "Il cursore e' gia' su un confine fra clip.":
        "Ο δρομέας βρίσκεται ήδη σε όριο μεταξύ κλιπ.",
    "Importa prima un video: la slide prende la sua misura.":
        "Εισαγάγετε πρώτα ένα βίντεο: η διαφάνεια παίρνει τις διαστάσεις του.",
    "Al cursore ({time})":
        "Στον δρομέα ({time})",
    "Dove":
        "Πού",
    "Durata (secondi)":
        "Διάρκεια (δευτερόλεπτα)",
    "Crea":
        "Δημιουργία",
    "La slide e' un fondo a tinta unita (il colore si sceglie nel pannello). Testi e immagini si aggiungono sopra con gli strumenti Testo e Immagine.":
        "Η διαφάνεια είναι ένα μονόχρωμο φόντο (το χρώμα επιλέγεται στον πίνακα). Κείμενα και εικόνες προστίθενται από πάνω με τα εργαλεία Κείμενο και Εικόνα.",
    "Slide di chiusura aggiunta alla fine: regolala nel pannello a destra.":
        "Η διαφάνεια κλεισίματος προστέθηκε στο τέλος: ρυθμίστε τη στον πίνακα δεξιά.",
    "Inserisci":
        "Εισαγωγή",
    "Applica":
        "Εφαρμογή",
    "Effetti":
        "Εφέ",
    "Pixel ovale":
        "Οβάλ pixel",
    "Pixel rettangolare":
        "Ορθογώνιο pixel",
    "Zoom ovale (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Οβάλ ζουμ (ορθογώνιο στο αντικείμενο, μετά κλικ εκεί όπου θα μπει το πλαίσιο)",
    "Zoom (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Ζουμ (ορθογώνιο στο αντικείμενο, μετά κλικ εκεί όπου θα μπει το πλαίσιο)",
    "Carica l'immagine del logo e scrivi il testo dell'operatore nella pagina Configura, poi premi di nuovo Logo.":
        "Φορτώστε την εικόνα του λογότυπου και γράψτε το κείμενο του χειριστή στη σελίδα Διαμόρφωση, μετά πατήστε ξανά Λογότυπο.",
    "Logo e operatore aggiunti per tutto il video: trascinali sull'anteprima o regolali nel pannello.":
        "Λογότυπο και χειριστής προστέθηκαν για όλο το βίντεο: σύρετέ τα στην προεπισκόπηση ή ρυθμίστε τα στον πίνακα.",
    "Zoom aggiunto (fermo: sul fermo immagine non c'e' nulla da inseguire).":
        "Το ζουμ προστέθηκε (σταθερό: στο πάγωμα καρέ δεν υπάρχει τίποτα για παρακολούθηση).",
    "Insegui":
        "Παρακολούθηση",
    "Keyframe":
        "Καρέ-κλειδί",
    "Porta il cursore dentro l'effetto.":
        "Φέρτε τον δρομέα μέσα στο εφέ.",
    "Nessun keyframe al cursore: usa Prec. / Succ. per andarci.":
        "Κανένα καρέ-κλειδί στον δρομέα: χρησιμοποιήστε Προηγ. / Επόμ. για να πάτε εκεί.",
    "Il primo punto del percorso non si cancella: e' la partenza della figura.":
        "Το πρώτο σημείο της διαδρομής δεν διαγράφεται: είναι η αφετηρία του σχήματος.",
    "Seleziona prima dei punti sulla barra dell'effetto nella timeline (clic, Maiusc+clic per un intervallo, Ctrl+clic per aggiungerne).":
        "Επιλέξτε πρώτα σημεία στη μπάρα του εφέ στη χρονογραμμή (κλικ, Shift+κλικ για διάστημα, Ctrl+κλικ για προσθήκη).",
    "Nessun altro keyframe in quella direzione.":
        "Κανένα άλλο καρέ-κλειδί προς αυτή την κατεύθυνση.",
    "Inseguimento":
        "Παρακολούθηση",
    "L'inseguimento funziona solo su una clip video (non su un fermo immagine): la figura resta ferma.":
        "Η παρακολούθηση λειτουργεί μόνο σε κλιπ βίντεο (όχι σε πάγωμα καρέ): το σχήμα μένει σταθερό.",
    "Testo di prova":
        "Δοκιμαστικό κείμενο",
    "La timeline e' vuota.":
        "Η χρονογραμμή είναι κενή.",
    "Esportazione completata":
        "Η εξαγωγή ολοκληρώθηκε",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Scarica / Aggiorna prende il build ufficiale per Windows (release essentials) da gyan.dev e tiene solo ffmpeg.exe, LICENSE e README in tools/ffmpeg/. Nessuna installazione, nessuna modifica al PATH.":
        "Το ffmpeg δεν περιλαμβάνεται στο πρόγραμμα: είναι ξεχωριστό πρόγραμμα με δική του άδεια. Η Λήψη / Ενημέρωση παίρνει την επίσημη έκδοση για Windows (release essentials) από το gyan.dev και κρατά μόνο τα ffmpeg.exe, LICENSE και README στο tools/ffmpeg/. Καμία εγκατάσταση, καμία αλλαγή στο PATH.",
    "Scarica / Aggiorna":
        "Λήψη / Ενημέρωση",
    "Apri cartella tools":
        "Άνοιγμα φακέλου tools",
    "VitTrack e' un modello addestrato per seguire oggetti e persone: ritrova il soggetto dopo un palo o un passante e capisce quando e' perso. Viene dal repository ufficiale opencv_zoo (licenza Apache 2.0, compatibile con la GPL 3), circa 0,7 MB, in tools/vittrack/ con la sua licenza. Senza, l'inseguimento usa il confronto a modello.":
        "Το VitTrack είναι ένα εκπαιδευμένο μοντέλο για την παρακολούθηση αντικειμένων και προσώπων: ξαναβρίσκει το θέμα μετά από μια κολόνα ή έναν περαστικό και καταλαβαίνει πότε χάθηκε. Προέρχεται από το επίσημο αποθετήριο opencv_zoo (άδεια Apache 2.0, συμβατή με τη GPL 3), περίπου 0,7 MB, στο tools/vittrack/ με την άδειά του. Χωρίς αυτό, η παρακολούθηση χρησιμοποιεί σύγκριση με πρότυπο.",
    "Scarica":
        "Λήψη",
    "Qualita' video (CRF, 15 = ottima, 28 = leggera)":
        "Ποιότητα βίντεο (CRF, 15 = άριστη, 28 = ελαφριά)",
    "Velocita' di codifica (preset x264)":
        "Ταχύτητα κωδικοποίησης (preset x264)",
    "Audio (kbit/s)":
        "Ήχος (kbit/s)",
    "Durate proposte (secondi)":
        "Προτεινόμενες διάρκειες (δευτερόλεπτα)",
    "Pixelatura: grandezza dei pixel e soglia dell'inseguimento (0.2-0.9)":
        "Ψηφιδωτό: μέγεθος pixel και κατώφλι παρακολούθησης (0.2-0.9)",
    "Salva impostazioni":
        "Αποθήκευση ρυθμίσεων",
    "Carica immagine del logo...":
        "Φόρτωση εικόνας λογότυπου...",
    "Togli logo":
        "Αφαίρεση λογότυπου",
    "Testo dell'operatore (nome, qualifica, data...)":
        "Κείμενο χειριστή (όνομα, ιδιότητα, ημερομηνία...)",
    "Il pulsante Logo (tasto L) mette logo e testo nell'angolo scelto, fermi per tutto il video (o solo nella porzione IN-OUT, se e' segnata). Nel progetto si possono poi spostare, ridimensionare e cambiare dal pannello a destra.":
        "Το κουμπί Λογότυπο (πλήκτρο L) βάζει λογότυπο και κείμενο στην επιλεγμένη γωνία, σταθερά για όλο το βίντεο (ή μόνο στο τμήμα IN-OUT, αν έχει οριστεί). Στο έργο μπορείτε μετά να τα μετακινήσετε, να αλλάξετε το μέγεθός τους και να τα τροποποιήσετε από τον πίνακα δεξιά.",
    "Proposti ai nuovi effetti, in % del lato corto (0 = angoli vivi, 50 = estremita' tonde); ogni effetto poi si regola nel suo pannello":
        "Προτείνονται στα νέα εφέ, σε % της μικρής πλευράς (0 = κοφτές γωνίες, 50 = στρογγυλά άκρα)· κάθε εφέ ρυθμίζεται μετά στον πίνακά του",
    "nessun logo":
        "κανένα λογότυπο",
    "La lingua dell'interfaccia cambia subito, senza riavviare.":
        "Η γλώσσα της διεπαφής αλλάζει αμέσως, χωρίς επανεκκίνηση.",
    "Valore non valido":
        "Μη έγκυρη τιμή",
    "Controlla i numeri inseriti.":
        "Ελέγξτε τους αριθμούς που εισαγάγατε.",
    "ffmpeg scaricato in tools/ffmpeg.":
        "Το ffmpeg κατέβηκε στο tools/ffmpeg.",
    "VitTrack non scaricato: l'inseguimento usa il confronto a modello, che puo' perdere il soggetto dietro un ostacolo.":
        "Το VitTrack δεν έχει κατέβει: η παρακολούθηση χρησιμοποιεί σύγκριση με πρότυπο, που μπορεί να χάσει το θέμα πίσω από ένα εμπόδιο.",
    "Modello scaricato in tools/vittrack: l'inseguimento ora lo usa.":
        "Το μοντέλο κατέβηκε στο tools/vittrack: η παρακολούθηση το χρησιμοποιεί πλέον.",
    "Cartella":
        "Φάκελος",
    "Progetto aperto: {file}":
        "Άνοιξε το έργο: {file}",
    "Salvataggio":
        "Αποθήκευση",
    "Progetto salvato: {path}":
        "Το έργο αποθηκεύτηκε: {path}",
    "In coda":
        "Στο τέλος",
    "Al cursore":
        "Στον δρομέα",
    "Traccia audio aggiunta: {name} ({duration})":
        "Προστέθηκε κομμάτι ήχου: {name} ({duration})",
    "Clip tagliata a {time}.":
        "Το κλιπ κόπηκε στο {time}.",
    "Audio originale tolto fra {start} e {end} (il video resta).":
        "Ο αρχικός ήχος αφαιρέθηκε μεταξύ {start} και {end} (το βίντεο μένει).",
    "Slide di apertura aggiunta all'inizio: regolala nel pannello a destra.":
        "Η διαφάνεια έναρξης προστέθηκε στην αρχή: ρυθμίστε τη στον πίνακα δεξιά.",
    "Fermo immagine di {seconds:g} s inserito.":
        "Εισήχθη πάγωμα καρέ {seconds:g} s.",
    "Segna prima la porzione con IN e OUT (tasti I e O), oppure seleziona una clip.":
        "Ορίστε πρώτα το τμήμα με IN και OUT (πλήκτρα I και O) ή επιλέξτε ένα κλιπ.",
    "Mostra l'icona dell'orologio con le lancette e la velocita' sotto":
        "Εμφάνιση του εικονιδίου ρολογιού με δείκτες και της ταχύτητας από κάτω",
    "Velocita' {speed} applicata fra {start} e {end}.":
        "Ταχύτητα {speed} εφαρμόστηκε μεταξύ {start} και {end}.",
    "{effect} aggiunto: regola i valori nel pannello a destra o trascina sull'anteprima.":
        "Προστέθηκε: {effect}. Ρυθμίστε τις τιμές στον πίνακα δεξιά ή σύρετε στην προεπισκόπηση.",
    "Fino all'istante (secondi della timeline)":
        "Έως τη στιγμή (δευτερόλεπτα της χρονογραμμής)",
    "Grandezza dei pixel":
        "Μέγεθος pixel",
    "Keyframe a {time}: trascina la figura per correggerla.":
        "Καρέ-κλειδί στο {time}: σύρετε το σχήμα για να το διορθώσετε.",
    "Inseguimento annullato.":
        "Η παρακολούθηση ακυρώθηκε.",
    "Inseguimento completato: {frames} fotogrammi, {points} punti":
        "Η παρακολούθηση ολοκληρώθηκε: {frames} καρέ, {points} σημεία",
    "Esportazione annullata.":
        "Η εξαγωγή ακυρώθηκε.",
    "Esportazione fallita":
        "Η εξαγωγή απέτυχε",
    "Esportazione fallita.":
        "Η εξαγωγή απέτυχε.",
    "Apri cartella":
        "Άνοιγμα φακέλου",
    "Chiudi":
        "Κλείσιμο",
    "PAGINE":
        "ΣΕΛΙΔΕΣ",
    "Inizio (Home)":
        "Αρχή (Home)",
    "Fotogramma precedente (Sinistra)":
        "Προηγούμενο καρέ (Αριστερά)",
    "Fotogramma successivo (Destra)":
        "Επόμενο καρέ (Δεξιά)",
    "Fine (Fine)":
        "Τέλος (End)",
    "Adatta la timeline":
        "Προσαρμογή χρονογραμμής",
    "Ingrandisci la timeline (Ctrl+rotellina). Per spostarla: Alt+trascina, tasto centrale o rotellina":
        "Μεγέθυνση χρονογραμμής (Ctrl+ροδέλα). Για μετακίνηση: Alt+σύρσιμο, μεσαίο πλήκτρο ή ροδέλα",
    "Riduci la timeline":
        "Σμίκρυνση χρονογραμμής",
    "Configurazione":
        "Διαμόρφωση",
    "fermo immagine":
        "πάγωμα καρέ",
    "effetti":
        "εφέ",
    "angolo":
        "γωνία",
    "disposizione":
        "διάταξη",
    "colore testo":
        "χρώμα κειμένου",
    "sfondo sotto logo e scritta":
        "φόντο κάτω από λογότυπο και κείμενο",
    "colore":
        "χρώμα",
    "Nessun logo: carica un'immagine (PNG con trasparenza, JPG...).":
        "Κανένα λογότυπο: φορτώστε μια εικόνα (PNG με διαφάνεια, JPG...).",
    "Immagini":
        "Εικόνες",
    "ffmpeg NON trovato: scaricalo con il pulsante qui sotto.":
        "Το ffmpeg ΔΕΝ βρέθηκε: κατεβάστε το με το παρακάτω κουμπί.",
    "{label}: {done:.1f} MB / {total:.1f} MB":
        "{label}: {done:.1f} MB / {total:.1f} MB",
    "{label}: {done:.1f} MB":
        "{label}: {done:.1f} MB",
    "Download fallito":
        "Η λήψη απέτυχε",
    "{label}: {done:.2f} MB / {total:.2f} MB":
        "{label}: {done:.2f} MB / {total:.2f} MB",
    "{label}: {done:.2f} MB":
        "{label}: {done:.2f} MB",
    "Spazio riproduci  ·  ← → fotogramma  ·  I / O segna  ·  S taglia  ·  Canc elimina  ·  Ctrl+Z annulla  ·  Esc annulla disegno":
        "Διάστημα αναπαραγωγή  ·  ← → καρέ  ·  I / O όριο  ·  S κοπή  ·  Delete διαγραφή  ·  Ctrl+Z αναίρεση  ·  Esc ακύρωση σχεδίου",
    "Fotogramma non leggibile: {file}":
        "Μη αναγνώσιμο καρέ: {file}",
    "Questi file non si trovano piu':\n\n{files}":
        "Αυτά τα αρχεία δεν βρίσκονται πια:\n\n{files}",
    "Video":
        "Βίντεο",
    "{file}\n\nAggiungerlo in coda alla timeline oppure inserirlo al cursore ({time})?":
        "{file}\n\nΠροσθήκη στο τέλος της χρονογραμμής ή εισαγωγή στον δρομέα ({time});",
    "Eliminata la porzione {start} - {end}.":
        "Διαγράφηκε το τμήμα {start} - {end}.",
    "Audio originale spento (il video resta): riaccendilo dal pannello o con Ctrl+Z.":
        "Ο αρχικός ήχος απενεργοποιήθηκε (το βίντεο μένει): ενεργοποιήστε τον ξανά από τον πίνακα ή με Ctrl+Z.",
    "Porzione {start} - {end}. Da 2x in su accelera, 0.5x e 0.25x rallentano (la porzione dura il doppio o il quadruplo); con 1x si torna alla velocita' normale.":
        "Τμήμα {start} - {end}. Από 2x και πάνω επιταχύνει, τα 0.5x και 0.25x επιβραδύνουν (το τμήμα διαρκεί το διπλάσιο ή το τετραπλάσιο)· με 1x επιστρέφει στην κανονική ταχύτητα.",
    "Disegna: {effect}  (Esc annulla)":
        "Σχεδίαση: {effect}  (Esc ακύρωση)",
    "Logo e operatore aggiunti fra {start} e {end}: trascinali sull'anteprima o regolali nel pannello.":
        "Λογότυπο και χειριστής προστέθηκαν μεταξύ {start} και {end}: σύρετέ τα στην προεπισκόπηση ή ρυθμίστε τα στον πίνακα.",
    "Keyframe a {time}.":
        "Καρέ-κλειδί στο {time}.",
    "; soggetto uscito dall'inquadratura: l'effetto finisce a {time}":
        "· το θέμα βγήκε από το κάδρο: το εφέ τελειώνει στο {time}",
    "; soggetto perso: l'effetto finisce a {time}":
        "· το θέμα χάθηκε: το εφέ τελειώνει στο {time}",
    "Video MP4":
        "Βίντεο MP4",
    "Esportato {path} ({size:.1f} MB in {seconds:.0f} s).":
        "Εξήχθη το {path} ({size:.1f} MB σε {seconds:.0f} s).",
    "{path}\n\n{size:.1f} MB in {seconds:.0f} secondi.\n\nAprire la cartella?":
        "{path}\n\n{size:.1f} MB σε {seconds:.0f} δευτερόλεπτα.\n\nΆνοιγμα του φακέλου;",
    "{app} {version}. Montaggio video semplice per presentazioni: timeline, tagli, fermo immagine, avanzamento veloce, sovraimpressioni, zoom e pixelatura con inseguimento; esportazione mp4 con ffmpeg. Progetti in formato JSON.":
        "{app} {version}. Απλό μοντάζ βίντεο για παρουσιάσεις: χρονογραμμή, κοπές, πάγωμα καρέ, γρήγορη κίνηση, επικαλύψεις, ζουμ και ψηφιδωτό με παρακολούθηση· εξαγωγή mp4 με το ffmpeg. Έργα σε μορφή JSON.",
    "{copyright}. Software libero: GNU General Public License versione 3 con termini aggiuntivi (attribuzione dell'autore, nome e logo), vedi i file LICENSE e NOTICE. Nessuna garanzia. Usa librerie e programmi di terze parti con le loro licenze (elencati in NOTICE).":
        "{copyright}. Ελεύθερο λογισμικό: GNU General Public License έκδοση 3 με πρόσθετους όρους (απόδοση στον δημιουργό, όνομα και λογότυπο), δείτε τα αρχεία LICENSE και NOTICE. Καμία εγγύηση. Χρησιμοποιεί βιβλιοθήκες και προγράμματα τρίτων με τις άδειές τους (αναφέρονται στο NOTICE).",
    "cartella tools/ffmpeg":
        "φάκελος tools/ffmpeg",
    "PATH di sistema":
        "PATH συστήματος",
    "VitTrack presente: l'inseguimento lo usa.\n{model}":
        "Το VitTrack υπάρχει: η παρακολούθηση το χρησιμοποιεί.\n{model}",
    "{width}x{height}  {fps:g} fps  {clips} clip  {duration}":
        "{width}x{height}  {fps:g} fps  {clips} κλιπ  {duration}",
    "Anteprima: {error}":
        "Προεπισκόπηση: {error}",
    "Audio dell'anteprima non disponibile: {error}":
        "Ο ήχος της προεπισκόπησης δεν είναι διαθέσιμος: {error}",
    "Impossibile aprire il progetto:\n{error}":
        "Δεν είναι δυνατό το άνοιγμα του έργου:\n{error}",
    "Slide aggiunta a {time}: regolala nel pannello a destra.":
        "Η διαφάνεια προστέθηκε στο {time}: ρυθμίστε τη στον πίνακα δεξιά.",
    "Il fotogramma a {time} resta fermo per questo tempo; cio' che segue scorre in avanti.":
        "Το καρέ στο {time} μένει σταθερό για αυτό το διάστημα· ό,τι ακολουθεί μετατίθεται μπροστά.",
    "L'inseguimento parte dal cursore ({start}) e segue il soggetto fino a questo istante (al massimo la fine della clip: {clip_end}).":
        "Η παρακολούθηση ξεκινά από τον δρομέα ({start}) και ακολουθεί το θέμα έως αυτή τη στιγμή (το πολύ έως το τέλος του κλιπ: {clip_end}).",
    "File non trovato: {path}":
        "Το αρχείο δεν βρέθηκε: {path}",
    "ffmpeg trovato ({where})\n{path}\nversione {version}":
        "Το ffmpeg βρέθηκε ({where})\n{path}\nέκδοση {version}",
    "Segna IN e OUT (tasti I e O) oppure seleziona un elemento da eliminare.":
        "Ορίστε IN και OUT (πλήκτρα I και O) ή επιλέξτε ένα στοιχείο για διαγραφή.",
    "Fotogramma {done} / {total}":
        "Καρέ {done} / {total}",
    "; soggetto non trovato da {time} al keyframe":
        "· το θέμα δεν βρέθηκε από το {time} έως το καρέ-κλειδί",
    ", non trovato in {frames} fotogrammi":
        ", δεν βρέθηκε σε {frames} καρέ",
    "formato audio inatteso":
        "μη αναμενόμενη μορφή ήχου",
    "Scegli il carattere":
        "Επιλογή γραμματοσειράς",
    "Cerca carattere...":
        "Αναζήτηση γραμματοσειράς...",
    "{shown} / {total}  - caricamento...":
        "{shown} / {total}  - φόρτωση...",
    "Caratteri della cartella font/ e di Windows, mostrati con il testo «{sample}». Clicca per scegliere.":
        "Γραμματοσειρές του φακέλου font/ και των Windows, με το κείμενο «{sample}». Κάντε κλικ για επιλογή.",
    "ffmpeg non trovato: scaricalo dalla pagina Configurazione.":
        "Το ffmpeg δεν βρέθηκε: κατεβάστε το από τη σελίδα Διαμόρφωση.",
    "Durata sconosciuta (file danneggiato o non riconosciuto).":
        "Άγνωστη διάρκεια (κατεστραμμένο ή μη αναγνωρισμένο αρχείο).",
    "Il file non contiene ne' video ne' audio riconoscibili.":
        "Το αρχείο δεν περιέχει αναγνωρίσιμο βίντεο ούτε ήχο.",
    "ffmpeg non ha scritto il fotogramma.":
        "Το ffmpeg δεν έγραψε το καρέ.",
    "ffmpeg: codice di uscita {code}":
        "ffmpeg: κωδικός εξόδου {code}",
    "Impossibile aprire il video: {path}":
        "Δεν είναι δυνατό το άνοιγμα του βίντεο: {path}",
    "Testo a destra del logo":
        "Κείμενο δεξιά του λογότυπου",
    "Testo a sinistra del logo":
        "Κείμενο αριστερά του λογότυπου",
    "Testo sotto il logo":
        "Κείμενο κάτω από το λογότυπο",
    "Riempi (taglia i bordi)":
        "Γέμισμα (κόβει τα άκρα)",
    "Intera (bande del colore)":
        "Ολόκληρη (λωρίδες χρώματος)",
    "Stira":
        "Τέντωμα",
    "Al centro":
        "Στο κέντρο",
    "Sinistra":
        "Αριστερά",
    "Centro":
        "Κέντρο",
    "Destra":
        "Δεξιά",
    "Nessun elemento selezionato.\n\nClicca una clip, un effetto o una traccia audio nella timeline per vederne le proprieta'.\n\nFlusso di lavoro:\n1. Importa un video (Ctrl+I)\n2. Segna IN e OUT (tasti I e O) e taglia o elimina\n3. Aggiungi fermo immagine, velocita', testi, frecce, riquadri, zoom, pixelatura\n4. Esporta in mp4 (Ctrl+E)":
        "Κανένα επιλεγμένο στοιχείο.\n\nΚάντε κλικ σε ένα κλιπ, ένα εφέ ή ένα κομμάτι ήχου στη χρονογραμμή για να δείτε τις ιδιότητές του.\n\nΡοή εργασίας:\n1. Εισαγάγετε ένα βίντεο (Ctrl+I)\n2. Ορίστε IN και OUT (πλήκτρα I και O) και κόψτε ή διαγράψτε\n3. Προσθέστε πάγωμα καρέ, ταχύτητα, κείμενα, βέλη, πλαίσια, ζουμ, ψηφιδωτό\n4. Εξαγάγετε σε mp4 (Ctrl+E)",
    "Proprieta'":
        "Ιδιότητες",
    "File":
        "Αρχείο",
    "Durata":
        "Διάρκεια",
    "Posizione":
        "Θέση",
    "Elimina clip":
        "Διαγραφή κλιπ",
    "Transizioni":
        "Μεταβάσεις",
    "Dal nero (s)":
        "Από μαύρο (s)",
    "Al nero (s)":
        "Σε μαύρο (s)",
    "Durata (s)":
        "Διάρκεια (s)",
    "Colore sfondo":
        "Χρώμα φόντου",
    "nessuna":
        "καμία",
    "Elimina slide":
        "Διαγραφή διαφάνειας",
    "Tempo":
        "Χρόνος",
    "Inizio (s)":
        "Αρχή (s)",
    "Fine (s)":
        "Τέλος (s)",
    "Elimina effetto":
        "Διαγραφή εφέ",
    "Stato":
        "Κατάσταση",
    "Keyframe qui (fissa la posizione)":
        "Καρέ-κλειδί εδώ (σταθεροποιεί τη θέση)",
    "Audio originale attivo":
        "Αρχικός ήχος ενεργός",
    "Volume":
        "Ένταση",
    "Dissolvenze":
        "Σβησίματα",
    "All'inizio (s)":
        "Στην αρχή (s)",
    "Alla fine (s)":
        "Στο τέλος (s)",
    "Elimina l'audio originale":
        "Διαγραφή του αρχικού ήχου",
    "Pezzo":
        "Κομμάτι",
    "Audio di questo pezzo":
        "Ήχος αυτού του κομματιού",
    "Volume di questo pezzo":
        "Ένταση αυτού του κομματιού",
    "Entrata (s)":
        "Εμφάνιση (s)",
    "Uscita (s)":
        "Σβήσιμο (s)",
    "Elimina audio di questo pezzo":
        "Διαγραφή ήχου αυτού του κομματιού",
    "Nome":
        "Όνομα",
    "Porzione del file":
        "Τμήμα του αρχείου",
    "Dall'istante (s)":
        "Από τη στιγμή (s)",
    "All'istante (s)":
        "Έως τη στιγμή (s)",
    "Muta":
        "Σίγαση",
    "Elimina traccia":
        "Διαγραφή κομματιού",
    "video":
        "βίντεο",
    "Istante sorgente (s)":
        "Στιγμή πηγής (s)",
    "Taglio nel video sorgente":
        "Κοπή στο αρχικό βίντεο",
    "Audio originale di questa clip":
        "Αρχικός ήχος αυτού του κλιπ",
    "Volume audio originale (tutto il progetto)":
        "Ένταση αρχικού ήχου (όλο το έργο)",
    "Velocita' (sotto 1x rallenta)":
        "Ταχύτητα (κάτω από 1x επιβραδύνει)",
    "Mostra orologio con la velocita'":
        "Εμφάνιση ρολογιού με την ταχύτητα",
    "Orologio (tutto il progetto)":
        "Ρολόι (όλο το έργο)",
    "Dimensione (px)":
        "Μέγεθος (px)",
    "Colore":
        "Χρώμα",
    "Opacita' sfondo":
        "Αδιαφάνεια φόντου",
    "Fusione con la succ. (s)":
        "Διάλυση στο επόμ. (s)",
    "Slide di apertura":
        "Διαφάνεια έναρξης",
    "Adattamento":
        "Προσαρμογή",
    "Allineamento":
        "Στοίχιση",
    "Ombra":
        "Σκιά",
    "Opacita' del testo":
        "Αδιαφάνεια κειμένου",
    "Sfondo dietro il testo":
        "Φόντο πίσω από το κείμενο",
    "Modifica testo...":
        "Επεξεργασία κειμένου...",
    "fermo":
        "σταθερό",
    "Ripeti inseguimento dal cursore":
        "Επανάληψη παρακολούθησης από τον δρομέα",
    "Segui il soggetto":
        "Παρακολούθηση θέματος",
    "Non seguire piu'":
        "Διακοπή παρακολούθησης",
    "nessuno":
        "κανένα",
    "Togli keyframe al cursore":
        "Αφαίρεση καρέ-κλειδιού στον δρομέα",
    "Cancella i punti selezionati":
        "Διαγραφή επιλεγμένων σημείων",
    "il file non ha audio":
        "το αρχείο δεν έχει ήχο",
    "= cursore":
        "= δρομέας",
    "Dal nero: la clip compare dal nero. Al nero: sparisce nel nero. Fusione: la clip sfuma nella successiva, a cavallo del taglio (la durata del video non cambia). Anche l'audio sale e scende. 0 = taglio netto.":
        "Από μαύρο: το κλιπ εμφανίζεται από το μαύρο. Σε μαύρο: χάνεται στο μαύρο. Διάλυση: το κλιπ σβήνει μέσα στο επόμενο, γύρω από την κοπή (η διάρκεια του βίντεο δεν αλλάζει). Και ο ήχος ανεβαίνει και κατεβαίνει. 0 = απότομη κοπή.",
    "La slide e' un fondo a tinta unita o un'immagine adattata alla misura del video. Testi e immagini si mettono sopra con gli strumenti Testo e Immagine: con il cursore sulla slide durano quanto lei.":
        "Η διαφάνεια είναι ένα μονόχρωμο φόντο ή μια εικόνα προσαρμοσμένη στις διαστάσεις του βίντεο. Κείμενα και εικόνες μπαίνουν από πάνω με τα εργαλεία Κείμενο και Εικόνα: με τον δρομέα στη διαφάνεια διαρκούν όσο αυτή.",
    "Larghezza (px)":
        "Πλάτος (px)",
    "Opacita'":
        "Αδιαφάνεια",
    "Dove l'inseguimento sbaglia: porta il cursore li' e trascina la figura sul soggetto (dagli angoli per la misura). Diventa un keyframe: il tratto prima viene corretto e l'inseguimento riparte da li' fino al keyframe successivo.\nNella timeline, sulla barra dell'effetto, i keyframe sono rombi e i punti dell'inseguimento pallini. Clic: seleziona e porta il cursore; Maiusc+clic: intervallo; Ctrl+clic: aggiunge o toglie. Canc o tasto destro: cancella i selezionati (li' la figura va dritta fra i punti rimasti).":
        "Όπου η παρακολούθηση κάνει λάθος: φέρτε τον δρομέα εκεί και σύρετε το σχήμα πάνω στο θέμα (από τις γωνίες για το μέγεθος). Γίνεται καρέ-κλειδί: το προηγούμενο τμήμα διορθώνεται και η παρακολούθηση ξαναρχίζει από εκεί έως το επόμενο καρέ-κλειδί.\nΣτη χρονογραμμή, στη μπάρα του εφέ, τα καρέ-κλειδιά είναι ρόμβοι και τα σημεία της παρακολούθησης κουκκίδες. Κλικ: επιλογή και μετακίνηση του δρομέα· Shift+κλικ: διάστημα· Ctrl+κλικ: προσθήκη ή αφαίρεση. Delete ή δεξί κλικ: διαγραφή των επιλεγμένων (εκεί το σχήμα πηγαίνει ευθεία ανάμεσα στα σημεία που μένουν).",
    "< Prec.":
        "< Προηγ.",
    "Succ. >":
        "Επόμ. >",
    "Centra orizz.":
        "Οριζ. κέντρο",
    "Centra vert.":
        "Κάθ. κέντρο",
    "Valgono per l'audio originale di tutto il video: sale all'inizio e scende alla fine. Canc spegne tutto l'audio originale (il video resta). Per un solo pezzo clicca la sua barra nella riga dell'audio.":
        "Ισχύουν για τον αρχικό ήχο όλου του βίντεο: ανεβαίνει στην αρχή και κατεβαίνει στο τέλος. Το Delete απενεργοποιεί όλο τον αρχικό ήχο (το βίντεο μένει). Για ένα μόνο κομμάτι κάντε κλικ στη μπάρα του στη γραμμή του ήχου.",
    "Per togliere solo un tratto d'audio: segna IN e OUT (tasti I e O) e premi Canc con l'audio selezionato: il video resta. Oppure taglia con S e seleziona il pezzo d'audio: Canc lo elimina, qui ne regoli volume e dissolvenze.":
        "Για να αφαιρέσετε μόνο ένα τμήμα ήχου: ορίστε IN και OUT (πλήκτρα I και O) και πατήστε Delete με τον ήχο επιλεγμένο: το βίντεο μένει. Ή κόψτε με S και επιλέξτε το κομμάτι ήχου: το Delete το διαγράφει, εδώ ρυθμίζετε την ένταση και τα σβησίματά του.",
    "Il volume sale da zero all'inizio della traccia e scende a zero alla fine.":
        "Η ένταση ανεβαίνει από το μηδέν στην αρχή του κομματιού και πέφτει στο μηδέν στο τέλος.",
    "slide":
        "διαφάνεια",
    "Clip: {kind}":
        "Κλιπ: {kind}",
    "Traccia audio":
        "Κομμάτι ήχου",
    "Slide di chiusura":
        "Διαφάνεια κλεισίματος",
    "Togli":
        "Αφαίρεση",
    "Sull'anteprima: trascina per spostare, dagli angoli per ingrandire, doppio clic per riscriverlo.":
        "Στην προεπισκόπηση: σύρετε για μετακίνηση, από τις γωνίες για μεγέθυνση, διπλό κλικ για να το ξαναγράψετε.",
    "Largh.":
        "Πλάτ.",
    "  Alt.":
        "  Ύψ.",
    "Spessore bordo":
        "Πάχος περιγράμματος",
    "Riempimento":
        "Γέμισμα",
    "Opacita' riempimento":
        "Αδιαφάνεια γεμίσματος",
    "Il contenuto della figura fa da modello: la figura segue il soggetto nei fotogrammi successivi; quando esce dall'inquadratura l'effetto finisce.":
        "Το περιεχόμενο του σχήματος γίνεται πρότυπο: το σχήμα ακολουθεί το θέμα στα επόμενα καρέ· όταν βγει από το κάδρο, το εφέ τελειώνει.",
    "segue il soggetto ({points} punti)":
        "ακολουθεί το θέμα ({points} σημεία)",
    "Effetto: {name}":
        "Εφέ: {name}",
    "Audio originale (un pezzo)":
        "Αρχικός ήχος (ένα κομμάτι)",
    "Carattere":
        "Γραμματοσειρά",
    "Sull'anteprima: trascina per spostarla, dagli angoli per ridimensionarla (le proporzioni restano quelle dell'immagine).":
        "Στην προεπισκόπηση: σύρετε για μετακίνηση, από τις γωνίες για αλλαγή μεγέθους (οι αναλογίες μένουν αυτές της εικόνας).",
    "Coda X":
        "Ουρά X",
    "Punta X":
        "Αιχμή X",
    "Spessore":
        "Πάχος",
    "Audio originale (tutto)":
        "Αρχικός ήχος (όλος)",
    "Area da ingrandire":
        "Περιοχή μεγέθυνσης",
    "Forma":
        "Σχήμα",
    "Angoli (rettangolare)":
        "Γωνίες (ορθογώνιο)",
    "Contorno colorato sull'area ingrandita":
        "Χρωματιστό περίγραμμα στη μεγεθυμένη περιοχή",
    "Linea fra l'area e il riquadro":
        "Γραμμή μεταξύ περιοχής και πλαισίου",
    "Riquadro ingrandito":
        "Μεγεθυμένο πλαίσιο",
    "L'area fa da modello: lo zoom segue l'oggetto nei fotogrammi successivi, il riquadro ingrandito resta dove l'hai messo. Se l'oggetto esce dall'inquadratura lo zoom finisce.":
        "Η περιοχή γίνεται πρότυπο: το ζουμ ακολουθεί το αντικείμενο στα επόμενα καρέ, το μεγεθυμένο πλαίσιο μένει εκεί που το βάλατε. Αν το αντικείμενο βγει από το κάδρο, το ζουμ τελειώνει.",
    "Rettangolare":
        "Ορθογώνιο",
    "Ingrandimento":
        "Μεγέθυνση",
    "Larghezza":
        "Πλάτος",
    "Per tutto il video":
        "Για όλο το βίντεο",
    "Largh. logo (px)":
        "Πλάτ. λογότυπου (px)",
    "Dimensione testo":
        "Μέγεθος κειμένου",
    "Colore testo":
        "Χρώμα κειμένου",
    "Disposizione":
        "Διάταξη",
    "Ombra sotto il testo":
        "Σκιά κάτω από το κείμενο",
    "Sfondo":
        "Φόντο",
    "Sfondo sotto logo e scritta":
        "Φόντο κάτω από λογότυπο και κείμενο",
    "Opacita' di tutto":
        "Συνολική αδιαφάνεια",
    "Angolo":
        "Γωνία",
    "Il colore vale per il bordo del riquadro, il contorno dell'area e la linea. L'area scelta viene mostrata ingrandita nel riquadro, sopra il video, per la durata dell'effetto. Sull'anteprima: trascina l'area o il riquadro, ridimensiona l'area dagli angoli.":
        "Το χρώμα ισχύει για το περίγραμμα του πλαισίου, το περίγραμμα της περιοχής και τη γραμμή. Η επιλεγμένη περιοχή εμφανίζεται μεγεθυμένη στο πλαίσιο, πάνω στο βίντεο, για τη διάρκεια του εφέ. Στην προεπισκόπηση: σύρετε την περιοχή ή το πλαίσιο, αλλάξτε το μέγεθος της περιοχής από τις γωνίες.",
    "Pixelatura":
        "Ψηφιδωτό",
    "Grandezza pixel":
        "Μέγεθος pixel",
    "Resta fermo nel punto scelto. Sull'anteprima trascinalo per spostarlo, tira un angolo per ingrandire o rimpicciolire logo e testo insieme. I valori proposti per i prossimi si cambiano in Configurazione.":
        "Μένει σταθερό στο επιλεγμένο σημείο. Στην προεπισκόπηση σύρετέ το για μετακίνηση, τραβήξτε μια γωνία για να μεγαλώσετε ή να μικρύνετε μαζί λογότυπο και κείμενο. Οι προτεινόμενες τιμές για τα επόμενα αλλάζουν στη Διαμόρφωση.",
    "fisso":
        "σταθερό",
    "Soggetto perso":
        "Το θέμα χάθηκε",
    "Ripeti l'inseguimento dopo aver cambiato inizio o fine.":
        "Επαναλάβετε την παρακολούθηση αφού αλλάξετε αρχή ή τέλος.",
    "{points} punti":
        "{points} σημεία",
    "{frames} fotogrammi":
        "{frames} καρέ",
    "Trascina sull'anteprima per disegnare il riquadro":
        "Σύρετε στην προεπισκόπηση για να σχεδιάσετε το πλαίσιο",
    "Trascina sull'anteprima per disegnare l'ovale":
        "Σύρετε στην προεπισκόπηση για να σχεδιάσετε το οβάλ",
    "Trascina sull'anteprima un rettangolo sull'oggetto da ingrandire":
        "Σύρετε στην προεπισκόπηση ένα ορθογώνιο πάνω στο αντικείμενο που θα μεγεθυνθεί",
    "Trascina sull'anteprima l'area da pixelare: verra' inseguita nei fotogrammi successivi":
        "Σύρετε στην προεπισκόπηση την περιοχή για ψηφιδωτό: θα παρακολουθείται στα επόμενα καρέ",
    "Trascina dalla coda alla punta della freccia":
        "Σύρετε από την ουρά προς την αιχμή του βέλους",
    "Clicca sull'anteprima dove mettere il testo":
        "Κάντε κλικ στην προεπισκόπηση εκεί όπου θα μπει το κείμενο",
    "Importa un video per vedere l'anteprima":
        "Εισαγάγετε ένα βίντεο για να δείτε την προεπισκόπηση",
    "segue il soggetto":
        "ακολουθεί το θέμα",
    "Logo e operatore":
        "Λογότυπο και χειριστής",
    "Slide di apertura: {text}":
        "Διαφάνεια έναρξης: {text}",
    "Slide di chiusura: {text}":
        "Διαφάνεια κλεισίματος: {text}",
    "Slide: {text}":
        "Διαφάνεια: {text}",
    "Fermo immagine ({name})":
        "Πάγωμα καρέ ({name})",
    "Percorso del progetto mancante":
        "Λείπει η διαδρομή του έργου",
    "La timeline e' vuota: importa almeno un video.":
        "Η χρονογραμμή είναι κενή: εισαγάγετε τουλάχιστον ένα βίντεο.",
    "Preparazione dei segmenti":
        "Προετοιμασία των τμημάτων",
    "Disegno delle sovraimpressioni":
        "Σχεδίαση των επικαλύψεων",
    "Preparazione":
        "Προετοιμασία",
    "Completato":
        "Ολοκληρώθηκε",
    "ffmpeg non ha scritto il file di uscita.":
        "Το ffmpeg δεν έγραψε το αρχείο εξόδου.",
    "Disegno del contorno dello zoom":
        "Σχεδίαση του περιγράμματος του ζουμ",
    "Disegno dell'orologio {speed}":
        "Σχεδίαση του ρολογιού {speed}",
    "Codifica: {done} / {total}":
        "Κωδικοποίηση: {done} / {total}",
    "Audio originale":
        "Αρχικός ήχος",
    "muto":
        "σίγαση",
    "immagine":
        "εικόνα",
    "orologio":
        "ρολόι",
    "senza audio":
        "χωρίς ήχο",
    "audio":
        "ήχος",
    "{name} ({points} punti)":
        "{name} ({points} σημεία)",
    "{name} (fisso)":
        "{name} (σταθερό)",
    "{name} (segue)":
        "{name} (ακολουθεί)",
    "audio {volume:.0f} %":
        "ήχος {volume:.0f} %",
    "Risposta inattesa dal sito di download di ffmpeg.":
        "Μη αναμενόμενη απάντηση από τον ιστότοπο λήψης του ffmpeg.",
    "Il download automatico e' disponibile solo su Windows: installa ffmpeg con il gestore di pacchetti del sistema.":
        "Η αυτόματη λήψη είναι διαθέσιμη μόνο στα Windows: εγκαταστήστε το ffmpeg με τον διαχειριστή πακέτων του συστήματος.",
    "licenza di VitTrack":
        "άδεια του VitTrack",
    "Il file scaricato non e' un archivio zip valido.":
        "Το αρχείο που κατέβηκε δεν είναι έγκυρο αρχείο zip.",
    "Estrazione di ffmpeg":
        "Αποσυμπίεση του ffmpeg",
    "L'ffmpeg scaricato non si avvia su questo PC.":
        "Το ffmpeg που κατέβηκε δεν εκτελείται σε αυτόν τον υπολογιστή.",
    "Il modello scaricato non corrisponde a quello atteso (impronta SHA-256 diversa).":
        "Το μοντέλο που κατέβηκε δεν είναι το αναμενόμενο (διαφορετικό αποτύπωμα SHA-256).",
    "Il pacchetto scaricato non contiene {file}.":
        "Το πακέτο που κατέβηκε δεν περιέχει το {file}.",
    "{file} manca dopo l'estrazione.":
        "Το {file} λείπει μετά την αποσυμπίεση.",
    "Impossibile controllare l'ultima versione di ffmpeg: {error}":
        "Δεν είναι δυνατός ο έλεγχος της τελευταίας έκδοσης του ffmpeg: {error}",
    "Download di {name} fallito: {error}":
        "Η λήψη του {name} απέτυχε: {error}",
    "Impossibile aggiornare '{folder}': file in uso. Aspetta la fine dell'esportazione e riprova.":
        "Δεν είναι δυνατή η ενημέρωση του '{folder}': αρχεία σε χρήση. Περιμένετε να τελειώσει η εξαγωγή και δοκιμάστε ξανά.",
    "OpenCV non riesce a caricare il modello: {error}":
        "Το OpenCV δεν μπορεί να φορτώσει το μοντέλο: {error}",
    "Archivio non valido: percorso sospetto '{path}'.":
        "Μη έγκυρο αρχείο: ύποπτη διαδρομή '{path}'.",
    "Download di {name}":
        "Λήψη του {name}",
    "Nessun fotogramma all'istante di partenza.":
        "Κανένα καρέ στη στιγμή εκκίνησης.",
    "INFO":
        "ΠΛΗΡΟΦΟΡΙΕΣ",
    "CONFERMA":
        "ΕΠΙΒΕΒΑΙΩΣΗ",
    "ATTENZIONE":
        "ΠΡΟΕΙΔΟΠΟΙΗΣΗ",
    "ERRORE":
        "ΣΦΑΛΜΑ",
    "OK":
        "OK",
    "Annulla":
        "Ακύρωση",
    "Si'":
        "Ναι",
    "No":
        "Όχι",
    "Interruzione...":
        "Διακοπή...",
    "Invio va a capo, Ctrl+Invio conferma.":
        "Το Enter αλλάζει γραμμή, το Ctrl+Enter επιβεβαιώνει.",
    "Allineamento delle righe":
        "Στοίχιση γραμμών",
    "Scrivi il testo.":
        "Γράψτε το κείμενο.",
    "Fondo scuro":
        "Σκούρο φόντο",
    "Centra nel video":
        "Κεντράρισμα στο βίντεο",
    "Dimensione non valida.":
        "Μη έγκυρο μέγεθος.",
    "{field}: valore fra {min:g} e {max:g}.":
        "{field}: τιμή μεταξύ {min:g} και {max:g}.",
    "{field}: inserisci un numero.":
        "{field}: εισαγάγετε έναν αριθμό.",
    "Clicca dove far apparire il riquadro ingrandito  -  {factor}x  (rotellina o tasti 2, 3, 4, 6, 8)":
        "Κάντε κλικ εκεί όπου θα εμφανιστεί το μεγεθυμένο πλαίσιο  -  {factor}x  (ροδέλα ή πλήκτρα 2, 3, 4, 6, 8)",
    "Tempo trascorso dall'inizio del video: clic dove metterlo, poi si sposta":
        "Χρόνος που πέρασε από την αρχή του βίντεο: κλικ εκεί όπου θα μπει, μετά μετακινείται",
    "Tempo trascorso aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.":
        "Ο χρόνος που πέρασε προστέθηκε: σύρετέ τον όπου θέλετε, ρυθμίστε τον στον πίνακα δεξιά.",
    "minuti:secondi (01:23)":
        "λεπτά:δευτερόλεπτα (01:23)",
    "ore:minuti:secondi (00:01:23)":
        "ώρες:λεπτά:δευτερόλεπτα (00:01:23)",
    "con i decimi (01:23.4)":
        "με δέκατα (01:23.4)",
    "dall'inizio del video":
        "από την αρχή του βίντεο",
    "dall'inizio dell'effetto":
        "από την αρχή του εφέ",
    "Tempo trascorso":
        "Χρόνος που πέρασε",
    "Formato":
        "Μορφή",
    "Conta":
        "Μέτρηση",
    "Testo davanti":
        "Κείμενο μπροστά",
    "Sfondo dietro il tempo":
        "Φόντο πίσω από τον χρόνο",
    "Sull'anteprima: trascinalo dove vuoi, dagli angoli per ingrandirlo.":
        "Στην προεπισκόπηση: σύρετέ τον όπου θέλετε, από τις γωνίες για μεγέθυνση.",
    "Clicca sull'anteprima dove mettere il tempo trascorso":
        "Κάντε κλικ στην προεπισκόπηση εκεί όπου θα μπει ο χρόνος που πέρασε",
    "Disegno del tempo trascorso":
        "Σχεδίαση του χρόνου που πέρασε",

    # ------------------------------------------------------- riproduzione
    '10 fotogrammi indietro (Ctrl+Sinistra)': '10 καρέ πίσω (Ctrl+Αριστερά)',
    "Riproduci all'indietro / pausa (Maiusc+Spazio), senza audio": 'Αναπαραγωγή προς τα πίσω / παύση (Shift+Διάστημα), χωρίς ήχο',
    '10 fotogrammi avanti (Ctrl+Destra)': '10 καρέ μπροστά (Ctrl+Δεξιά)',
    'Allunga fino al cursore': 'Επέκταση έως τον δρομέα',
    'Interrompi al cursore': 'Διακοπή στον δρομέα',
    '{effect} allungato fino a {t:.2f} s.': '{effect}: επεκτάθηκε έως {t:.2f} s.',
    '{effect} interrotto a {t:.2f} s.': '{effect}: διακόπηκε στα {t:.2f} s.',
    "{effect} nascosto: non compare in anteprima ne' nel video esportato.": '{effect}: κρυφό, δεν εμφανίζεται ούτε στην προεπισκόπηση ούτε στο βίντεο που εξάγεται.',
    '{effect} di nuovo visibile.': '{effect}: ξανά ορατό.',
    '{zoom}% - trascina per spostarti, doppio clic centrale: adatta': '{zoom}% - σύρετε για μετακίνηση, διπλό κλικ με το μεσαίο: προσαρμογή',
    'Fotogrammi': 'Καρέ',
    "Numero del fotogramma dall'inizio del video: clic dove metterlo, poi si sposta": 'Αριθμός καρέ από την αρχή του βίντεο: κλικ όπου θα μπει, μετά μετακινείται',
    'Numero del fotogramma aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.': 'Προστέθηκε ο αριθμός καρέ: σύρετέ τον όπου θέλετε και ρυθμίστε τον στο πλαίσιο δεξιά.',
    'Numero del fotogramma': 'Αριθμός καρέ',
    'Primo fotogramma': 'Πρώτο καρέ',
    "Clicca sull'anteprima dove mettere il numero del fotogramma": 'Κάντε κλικ στην προεπισκόπηση όπου θα μπει ο αριθμός καρέ',
    'Anteprima': 'Προεπισκόπηση',
    'Anteprima riattaccata.': 'Η προεπισκόπηση επανασυνδέθηκε.',
    "Riattacca l'anteprima alla finestra principale": 'Επανασύνδεση της προεπισκόπησης στο κύριο παράθυρο',
    "Stacca l'anteprima in una finestra a parte (piu' spazio per la timeline)": 'Αποσύνδεση της προεπισκόπησης σε ξεχωριστό παράθυρο (περισσότερος χώρος για τη γραμμή χρόνου)',
    'Anteprima in una finestra a parte: chiudila o usa il pulsante in alto a destra per riattaccarla.': 'Προεπισκόπηση σε ξεχωριστό παράθυρο: κλείστε το ή πατήστε το κουμπί πάνω δεξιά για επανασύνδεση.',
    "Trascina un rettangolo attorno al soggetto: la freccia lo seguira' tenendo la punta dov'e'.": 'Σύρετε ένα ορθογώνιο γύρω από το θέμα: το βέλος θα το ακολουθεί κρατώντας τη μύτη εκεί που είναι.',
    'soggetto della freccia': 'θέμα του βέλους',
    "Si disegna un rettangolo attorno al soggetto: la freccia lo segue nei fotogrammi successivi tenendo la punta su di lui; quando esce dall'inquadratura l'effetto finisce.": 'Σχεδιάζεται ένα ορθογώνιο γύρω από το θέμα: το βέλος το ακολουθεί στα επόμενα καρέ κρατώντας τη μύτη πάνω του· όταν βγει από το κάδρο, το εφέ τελειώνει.',
    'Scegli un altro soggetto': 'Επιλογή άλλου θέματος',
    'Trascina un rettangolo attorno al soggetto che la freccia deve seguire': 'Σύρετε ένα ορθογώνιο γύρω από το θέμα που πρέπει να ακολουθεί το βέλος',
}
