# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Nederlands: traduzione dei testi dell'interfaccia di EditSimple.

La chiave e' il testo italiano cosi' come compare nel codice (in tr() e N_()),
il valore la sua traduzione. I segnaposto tra graffe vanno lasciati identici.
Dopo ogni modifica:

    .venv\\Scripts\\python.exe scripts\\check_i18n.py nl
"""

from __future__ import annotations

NAME = "Nederlands"

CATALOG: dict[str, str] = {
    "Impossibile avviare l'interfaccia: {error}\n\nInstalla le dipendenze con:\n    {command}":
        "Kan de interface niet starten: {error}\n\nInstalleer de afhankelijkheden met:\n    {command}",
    "In alto a sinistra": "Linksboven",
    "In alto a destra": "Rechtsboven",
    "In basso a sinistra": "Linksonder",
    "In basso a destra": "Rechtsonder",
    "Progetto EditSimple": "EditSimple-project",
    "Tutti i file": "Alle bestanden",
    "Apertura (all'inizio)": "Opening (aan het begin)",
    "Chiusura (alla fine)": "Afsluiting (aan het einde)",
    "Apri progetto... (Ctrl+O)": "Project openen... (Ctrl+O)",
    "Progetto": "Project",
    "Nuovo": "Nieuw",
    "Nuovo progetto (Ctrl+N)": "Nieuw project (Ctrl+N)",
    "Apri": "Openen",
    "Apri progetto (Ctrl+O)": "Project openen (Ctrl+O)",
    "Salva": "Opslaan",
    "Salva progetto (Ctrl+S)": "Project opslaan (Ctrl+S)",
    "Annulla (Ctrl+Z)": "Ongedaan maken (Ctrl+Z)",
    "Ripeti (Ctrl+Y)": "Opnieuw (Ctrl+Y)",
    "Clip": "Clip",
    "Importa video": "Video importeren",
    "Importa un video in coda o al cursore (Ctrl+I)": "Importeert een video aan het einde of op de cursor (Ctrl+I)",
    "Audio": "Audio",
    "Aggiungi una traccia audio (commento, musica) al cursore":
        "Voegt een audiospoor (commentaar, muziek) toe op de cursor",
    "Taglia": "Knippen",
    "Taglia la clip al cursore (S)": "Knipt de clip op de cursor (S)",
    "Elimina": "Verwijderen",
    "Elimina la porzione IN-OUT o l'elemento selezionato (Canc)":
        "Verwijdert het deel IN-OUT of het geselecteerde element (Del)",
    "Fermo": "Stilstaand",
    "Fermo immagine del fotogramma al cursore (F)": "Stilstaand beeld van het frame op de cursor (F)",
    "Slide": "Dia",
    "Inserisci una slide": "Een dia invoegen",
    "Velocita'": "Snelheid",
    "Velocita' della porzione IN-OUT: piu' veloce o rallentata (V)":
        "Snelheid van het deel IN-OUT: sneller of vertraagd (V)",
    "Sovraimpressioni": "Overlays",
    "Testo": "Tekst",
    "Testo (T)": "Tekst (T)",
    "Immagine": "Afbeelding",
    "Immagine sopra il video, da spostare e ridimensionare":
        "Afbeelding boven de video, te verplaatsen en te schalen",
    "Logo": "Logo",
    "Logo e testo dell'operatore, fermi in un angolo (L)": "Logo en tekst van de operator, vast in een hoek (L)",
    "Riquadro": "Kader",
    "Riquadro (R): puo' seguire il soggetto": "Kader (R): kan het onderwerp volgen",
    "Ovale": "Ovaal",
    "Ovale (E): puo' seguire il soggetto": "Ovaal (E): kan het onderwerp volgen",
    "Freccia": "Pijl",
    "Freccia (A): puo' seguire il soggetto": "Pijl (A): kan het onderwerp volgen",
    "Zoom": "Zoom",
    "Zoom rettangolare: l'area scelta in un riquadro ingrandito (Z)":
        "Rechthoekige zoom: het gekozen gebied in een vergroot kader (Z)",
    "Zoom ovale: l'area scelta in un ovale ingrandito (Maiusc+Z)":
        "Ovale zoom: het gekozen gebied in een vergroot ovaal (Shift+Z)",
    "Pixel": "Pixel",
    "Pixelatura rettangolare che insegue il soggetto (P)": "Rechthoekige pixelering die het onderwerp volgt (P)",
    "Pixelatura ovale che insegue il soggetto (K)": "Ovale pixelering die het onderwerp volgt (K)",
    "Uscita": "Uitvoer",
    "Esporta MP4": "MP4 exporteren",
    "Esporta il video finale (Ctrl+E)": "Exporteert de uiteindelijke video (Ctrl+E)",
    "Inseguimento (VitTrack)": "Volgen (VitTrack)",
    "Esportazione": "Export",
    "Logo e testo dell'operatore": "Logo en tekst van de operator",
    "Angoli arrotondati": "Afgeronde hoeken",
    "Crediti": "Colofon",
    "Lingua": "Taal",
    "Impostazioni salvate.": "Instellingen opgeslagen.",
    "Download di ffmpeg": "Download van ffmpeg",
    "Download di VitTrack": "Download van VitTrack",
    "Progetto non salvato": "Project niet opgeslagen",
    "Salvare le modifiche al progetto?": "Wijzigingen in het project opslaan?",
    "Nuovo progetto.": "Nieuw project.",
    "Lettura del video...": "Video lezen...",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}":
        "{file} geïmporteerd: {width}x{height}, {fps:g} fps, {duration}",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}, senza audio":
        "{file} geïmporteerd: {width}x{height}, {fps:g} fps, {duration}, zonder audio",
    "Audio di questo pezzo eliminato (il video resta). Ctrl+Z per riaverlo.":
        "Audio van dit stuk verwijderd (de video blijft). Ctrl+Z om het terug te halen.",
    "Clip eliminata.": "Clip verwijderd.",
    "Fermo immagine": "Stilstaand beeld",
    "Nuovo testo": "Nieuwe tekst",
    "Testo aggiunto: trascinalo, ingrandiscilo dagli angoli, doppio clic per riscriverlo.":
        "Tekst toegevoegd: sleep hem, vergroot hem via de hoeken, dubbelklik om hem te herschrijven.",
    "Modifica testo": "Tekst bewerken",
    "Immagine aggiunta: trascinala per spostarla, dagli angoli per ridimensionarla.":
        "Afbeelding toegevoegd: sleep om haar te verplaatsen, via de hoeken om haar te schalen.",
    "Pixelatura con inseguimento": "Pixelering met volgen",
    "Cancellati {count} punti del percorso (il primo resta: e' la partenza della figura).":
        "{count} punten van het pad gewist (het eerste blijft: het is het vertrekpunt van de figuur).",
    "Cancellati {count} punti del percorso.": "{count} punten van het pad gewist.",
    "Inseguimento del soggetto": "Onderwerp volgen",
    "Esportazione in corso": "Export bezig",
    "montaggio video per presentazioni": "videomontage voor presentaties",
    "PROGETTO": "PROJECT",
    "nuovo": "nieuw",
    "Nessun video": "Geen video",
    "Montaggio": "Montage",
    "Configura": "Configuratie",
    "Riproduci / pausa (Spazio)": "Afspelen / pauze (Spatie)",
    "larghezza logo % del video": "logobreedte % van de video",
    "altezza testo % del lato corto": "teksthoogte % van de korte zijde",
    "distanza dai bordi % del lato corto": "afstand tot de randen % van de korte zijde",
    "opacita' %": "dekking %",
    "angoli arrotondati %": "afgeronde hoeken %",
    "sfondo del testo": "tekstachtergrond",
    "riquadro": "kader",
    "zoom rettangolare": "rechthoekige zoom",
    "pixel rettangolare": "rechthoekige pixel",
    "Colore del testo": "Tekstkleur",
    "Colore dello sfondo": "Achtergrondkleur",
    "Immagine del logo": "Logoafbeelding",
    "Questa immagine non si apre.": "Deze afbeelding kan niet worden geopend.",
    "Controllo in corso...": "Controleren...",
    "Pronto.": "Gereed.",
    "ffmpeg non e' stato trovato. Scaricalo dal riquadro FFmpeg della pagina Configurazione: senza, non si possono importare ne' esportare video.":
        "ffmpeg niet gevonden. Download het via het vak FFmpeg op de pagina Configuratie: zonder ffmpeg kunnen "
        "video's niet worden geïmporteerd of geëxporteerd.",
    "ffmpeg non e' stato trovato. Installalo con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) o copia un eseguibile ffmpeg in tools/ffmpeg/: senza, non si possono importare ne' esportare video.":
        "ffmpeg niet gevonden. Installeer het met de pakketbeheerder van het systeem (bijvoorbeeld sudo apt install ffmpeg) of kopieer een uitvoerbaar ffmpeg-bestand naar tools/ffmpeg/: zonder ffmpeg kunnen video's niet worden geïmporteerd of geëxporteerd.",
    "Non salvare": "Niet opslaan",
    "Niente da annullare.": "Niets om ongedaan te maken.",
    "inizio": "begin",
    "fine": "einde",
    "Apri progetto": "Project openen",
    "File mancanti": "Ontbrekende bestanden",
    "Salva progetto": "Project opslaan",
    "Dove inserire il video?": "Waar de video invoegen?",
    "Importazione": "Importeren",
    "Il file non contiene video. Per l'audio usa il pulsante Audio.":
        "Het bestand bevat geen video. Gebruik voor audio de knop Audio.",
    "Importa prima un video.": "Importeer eerst een video.",
    "Aggiungi traccia audio": "Audiospoor toevoegen",
    "Il file non contiene audio.": "Het bestand bevat geen audio.",
    "Il cursore e' gia' su un confine fra clip.": "De cursor staat al op een grens tussen clips.",
    "Importa prima un video: la slide prende la sua misura.":
        "Importeer eerst een video: de dia neemt de afmetingen ervan over.",
    "Al cursore ({time})": "Op de cursor ({time})",
    "Dove": "Waar",
    "Durata (secondi)": "Duur (seconden)",
    "Crea": "Maken",
    "La slide e' un fondo a tinta unita (il colore si sceglie nel pannello). Testi e immagini si aggiungono sopra con gli strumenti Testo e Immagine.":
        "De dia is een effen achtergrond (de kleur kies je in het paneel). Teksten en afbeeldingen voeg je erop toe "
        "met de gereedschappen Tekst en Afbeelding.",
    "Slide di chiusura aggiunta alla fine: regolala nel pannello a destra.":
        "Slotdia toegevoegd aan het einde: stel haar in via het paneel rechts.",
    "Inserisci": "Invoegen",
    "Applica": "Toepassen",
    "Effetti": "Effecten",
    "Pixel ovale": "Ovale pixel",
    "Pixel rettangolare": "Rechthoekige pixel",
    "Zoom ovale (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Ovale zoom (rechthoek op het object, dan klikken waar het kader moet komen)",
    "Zoom (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Zoom (rechthoek op het object, dan klikken waar het kader moet komen)",
    "Carica l'immagine del logo e scrivi il testo dell'operatore nella pagina Configura, poi premi di nuovo Logo.":
        "Laad de logoafbeelding en schrijf de tekst van de operator op de pagina Configuratie, druk dan opnieuw op Logo.",
    "Logo e operatore aggiunti per tutto il video: trascinali sull'anteprima o regolali nel pannello.":
        "Logo en operator toegevoegd voor de hele video: sleep ze in het voorbeeld of stel ze in via het paneel.",
    "Zoom aggiunto (fermo: sul fermo immagine non c'e' nulla da inseguire).":
        "Zoom toegevoegd (vast: op een stilstaand beeld valt niets te volgen).",
    "Insegui": "Volgen",
    "Keyframe": "Keyframe",
    "Porta il cursore dentro l'effetto.": "Zet de cursor binnen het effect.",
    "Nessun keyframe al cursore: usa Prec. / Succ. per andarci.":
        "Geen keyframe op de cursor: gebruik Vor. / Volg. om ernaartoe te gaan.",
    "Il primo punto del percorso non si cancella: e' la partenza della figura.":
        "Het eerste punt van het pad kan niet worden gewist: het is het vertrekpunt van de figuur.",
    "Seleziona prima dei punti sulla barra dell'effetto nella timeline (clic, Maiusc+clic per un intervallo, Ctrl+clic per aggiungerne).":
        "Selecteer eerst punten op de effectbalk in de tijdlijn (klik, Shift+klik voor een bereik, Ctrl+klik om "
        "punten toe te voegen).",
    "Nessun altro keyframe in quella direzione.": "Geen andere keyframe in die richting.",
    "Inseguimento": "Volgen",
    "L'inseguimento funziona solo su una clip video (non su un fermo immagine): la figura resta ferma.":
        "Volgen werkt alleen op een videoclip (niet op een stilstaand beeld): de figuur blijft stilstaan.",
    "Testo di prova": "Voorbeeldtekst",
    "La timeline e' vuota.": "De tijdlijn is leeg.",
    "Esportazione completata": "Export voltooid",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Scarica / Aggiorna prende il build ufficiale per Windows (release essentials) da gyan.dev e tiene solo ffmpeg.exe, LICENSE e README in tools/ffmpeg/. Nessuna installazione, nessuna modifica al PATH.":
        "ffmpeg zit niet in het programma: het is een apart programma met een eigen licentie. Downloaden / Bijwerken "
        "haalt de officiële Windows-build (release essentials) van gyan.dev en bewaart alleen ffmpeg.exe, LICENSE en "
        "README in tools/ffmpeg/. Geen installatie, geen wijzigingen aan het PATH.",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Su Linux e macOS si installa con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) oppure si mette un eseguibile ffmpeg in tools/ffmpeg/. Il download automatico vale solo per Windows.":
        "ffmpeg zit niet in het programma: het is een apart programma met een eigen licentie. Op Linux en macOS installeert u het met de pakketbeheerder van het systeem (bijvoorbeeld sudo apt install ffmpeg) of zet u een uitvoerbaar ffmpeg-bestand in tools/ffmpeg/. Automatisch downloaden is alleen beschikbaar op Windows.",
    "Scarica / Aggiorna": "Downloaden / Bijwerken",
    "Apri cartella tools": "Map tools openen",
    "VitTrack e' un modello addestrato per seguire oggetti e persone: ritrova il soggetto dopo un palo o un passante e capisce quando e' perso. Viene dal repository ufficiale opencv_zoo (licenza Apache 2.0, compatibile con la GPL 3), circa 0,7 MB, in tools/vittrack/ con la sua licenza. Senza, l'inseguimento usa il confronto a modello.":
        "VitTrack is een getraind model om objecten en personen te volgen: het vindt het onderwerp terug na een paal "
        "of een voorbijganger en herkent wanneer het kwijt is. Het komt uit de officiële repository opencv_zoo "
        "(licentie Apache 2.0, compatibel met de GPL 3), ongeveer 0,7 MB, in tools/vittrack/ met zijn licentie. "
        "Zonder VitTrack gebruikt het volgen sjabloonvergelijking.",
    "Scarica": "Downloaden",
    "Qualita' video (CRF, 15 = ottima, 28 = leggera)": "Videokwaliteit (CRF, 15 = uitstekend, 28 = licht)",
    "Velocita' di codifica (preset x264)": "Coderingssnelheid (preset x264)",
    "Audio (kbit/s)": "Audio (kbit/s)",
    "Durate proposte (secondi)": "Voorgestelde duur (seconden)",
    "Pixelatura: grandezza dei pixel e soglia dell'inseguimento (0.2-0.9)":
        "Pixelering: pixelgrootte en drempel voor het volgen (0.2-0.9)",
    "Salva impostazioni": "Instellingen opslaan",
    "Carica immagine del logo...": "Logoafbeelding laden...",
    "Togli logo": "Logo verwijderen",
    "Testo dell'operatore (nome, qualifica, data...)": "Tekst van de operator (naam, functie, datum...)",
    "Il pulsante Logo (tasto L) mette logo e testo nell'angolo scelto, fermi per tutto il video (o solo nella porzione IN-OUT, se e' segnata). Nel progetto si possono poi spostare, ridimensionare e cambiare dal pannello a destra.":
        "De knop Logo (toets L) zet logo en tekst in de gekozen hoek, vast voor de hele video (of alleen in het deel "
        "IN-OUT, als dat is gemarkeerd). In het project kun je ze daarna verplaatsen, schalen en wijzigen via het "
        "paneel rechts.",
    "Proposti ai nuovi effetti, in % del lato corto (0 = angoli vivi, 50 = estremita' tonde); ogni effetto poi si regola nel suo pannello":
        "Voorgesteld voor nieuwe effecten, in % van de korte zijde (0 = scherpe hoeken, 50 = ronde uiteinden); elk "
        "effect stel je daarna in via zijn paneel",
    "nessun logo": "geen logo",
    "La lingua dell'interfaccia cambia subito, senza riavviare.":
        "De taal van de interface verandert meteen, zonder herstart.",
    "Valore non valido": "Ongeldige waarde",
    "Controlla i numeri inseriti.": "Controleer de ingevoerde getallen.",
    "ffmpeg scaricato in tools/ffmpeg.": "ffmpeg gedownload naar tools/ffmpeg.",
    "VitTrack non scaricato: l'inseguimento usa il confronto a modello, che puo' perdere il soggetto dietro un ostacolo.":
        "VitTrack niet gedownload: het volgen gebruikt sjabloonvergelijking, die het onderwerp achter een obstakel "
        "kan verliezen.",
    "Modello scaricato in tools/vittrack: l'inseguimento ora lo usa.":
        "Model gedownload naar tools/vittrack: het volgen gebruikt het nu.",
    "Cartella": "Map",
    "Progetto aperto: {file}": "Project geopend: {file}",
    "Salvataggio": "Opslaan",
    "Progetto salvato: {path}": "Project opgeslagen: {path}",
    "In coda": "Aan het einde",
    "Al cursore": "Op de cursor",
    "Traccia audio aggiunta: {name} ({duration})": "Audiospoor toegevoegd: {name} ({duration})",
    "Clip tagliata a {time}.": "Clip geknipt op {time}.",
    "Audio originale tolto fra {start} e {end} (il video resta).":
        "Originele audio verwijderd tussen {start} en {end} (de video blijft).",
    "Slide di apertura aggiunta all'inizio: regolala nel pannello a destra.":
        "Openingsdia toegevoegd aan het begin: stel haar in via het paneel rechts.",
    "Fermo immagine di {seconds:g} s inserito.": "Stilstaand beeld van {seconds:g} s ingevoegd.",
    "Segna prima la porzione con IN e OUT (tasti I e O), oppure seleziona una clip.":
        "Markeer eerst het deel met IN en OUT (toetsen I en O), of selecteer een clip.",
    "Mostra l'icona dell'orologio con le lancette e la velocita' sotto":
        "Toont het klokpictogram met wijzers en de snelheid eronder",
    "Velocita' {speed} applicata fra {start} e {end}.": "Snelheid {speed} toegepast tussen {start} en {end}.",
    "{effect} aggiunto: regola i valori nel pannello a destra o trascina sull'anteprima.":
        "{effect} toegevoegd: stel de waarden in via het paneel rechts of sleep in het voorbeeld.",
    "Fino all'istante (secondi della timeline)": "Tot het tijdstip (seconden van de tijdlijn)",
    "Grandezza dei pixel": "Pixelgrootte",
    "Keyframe a {time}: trascina la figura per correggerla.":
        "Keyframe op {time}: sleep de figuur om haar te corrigeren.",
    "Inseguimento annullato.": "Volgen geannuleerd.",
    "Inseguimento completato: {frames} fotogrammi, {points} punti":
        "Volgen voltooid: {frames} frames, {points} punten",
    "Esportazione annullata.": "Export geannuleerd.",
    "Esportazione fallita": "Export mislukt",
    "Esportazione fallita.": "Export mislukt.",
    "Apri cartella": "Map openen",
    "Chiudi": "Sluiten",
    "PAGINE": "PAGINA'S",
    "Inizio (Home)": "Begin (Home)",
    "Fotogramma precedente (Sinistra)": "Vorig frame (Links)",
    "Fotogramma successivo (Destra)": "Volgend frame (Rechts)",
    "Fine (Fine)": "Einde (End)",
    "Adatta la timeline": "Tijdlijn passend maken",
    "Ingrandisci la timeline (Ctrl+rotellina). Per spostarla: Alt+trascina, tasto centrale o rotellina":
        "Tijdlijn inzoomen (Ctrl+scrollwiel). Verschuiven: Alt+slepen, middelste knop of scrollwiel",
    "Riduci la timeline": "Tijdlijn uitzoomen",
    "Configurazione": "Configuratie",
    "fermo immagine": "stilstaand beeld",
    "effetti": "effecten",
    "angolo": "hoek",
    "disposizione": "indeling",
    "colore testo": "tekstkleur",
    "sfondo sotto logo e scritta": "achtergrond onder logo en tekst",
    "colore": "kleur",
    "Nessun logo: carica un'immagine (PNG con trasparenza, JPG...).":
        "Geen logo: laad een afbeelding (PNG met transparantie, JPG...).",
    "Immagini": "Afbeeldingen",
    "ffmpeg NON trovato: scaricalo con il pulsante qui sotto.": "ffmpeg NIET gevonden: download het met de knop hieronder.",
    "{label}: {done:.1f} MB / {total:.1f} MB": "{label}: {done:.1f} MB / {total:.1f} MB",
    "{label}: {done:.1f} MB": "{label}: {done:.1f} MB",
    "Download fallito": "Download mislukt",
    "{label}: {done:.2f} MB / {total:.2f} MB": "{label}: {done:.2f} MB / {total:.2f} MB",
    "{label}: {done:.2f} MB": "{label}: {done:.2f} MB",
    "Spazio riproduci  ·  ← → fotogramma  ·  I / O segna  ·  S taglia  ·  Canc elimina  ·  Ctrl+Z annulla  ·  Esc annulla disegno":
        "Spatie afspelen  ·  ← → frame  ·  I / O markeren  ·  S knippen  ·  Del verwijderen  ·  Ctrl+Z ongedaan maken  ·  "
        "Esc tekenen annuleren",
    "Fotogramma non leggibile: {file}": "Frame niet leesbaar: {file}",
    "Questi file non si trovano piu':\n\n{files}": "Deze bestanden zijn niet meer te vinden:\n\n{files}",
    "Video": "Video",
    "{file}\n\nAggiungerlo in coda alla timeline oppure inserirlo al cursore ({time})?":
        "{file}\n\nAan het einde van de tijdlijn toevoegen of op de cursor ({time}) invoegen?",
    "Eliminata la porzione {start} - {end}.": "Deel {start} - {end} verwijderd.",
    "Audio originale spento (il video resta): riaccendilo dal pannello o con Ctrl+Z.":
        "Originele audio uitgeschakeld (de video blijft): zet hem weer aan via het paneel of met Ctrl+Z.",
    "Porzione {start} - {end}. Da 2x in su accelera, 0.5x e 0.25x rallentano (la porzione dura il doppio o il quadruplo); con 1x si torna alla velocita' normale.":
        "Deel {start} - {end}. Vanaf 2x versnelt het, 0.5x en 0.25x vertragen (het deel duurt twee of vier keer zo "
        "lang); met 1x keer je terug naar de normale snelheid.",
    "Disegna: {effect}  (Esc annulla)": "Tekenen: {effect}  (Esc annuleert)",
    "Logo e operatore aggiunti fra {start} e {end}: trascinali sull'anteprima o regolali nel pannello.":
        "Logo en operator toegevoegd tussen {start} en {end}: sleep ze in het voorbeeld of stel ze in via het paneel.",
    "Keyframe a {time}.": "Keyframe op {time}.",
    "; soggetto uscito dall'inquadratura: l'effetto finisce a {time}":
        "; onderwerp buiten beeld: het effect eindigt op {time}",
    "; soggetto perso: l'effetto finisce a {time}": "; onderwerp kwijt: het effect eindigt op {time}",
    "Video MP4": "MP4-video",
    "Esportato {path} ({size:.1f} MB in {seconds:.0f} s).": "{path} geëxporteerd ({size:.1f} MB in {seconds:.0f} s).",
    "{path}\n\n{size:.1f} MB in {seconds:.0f} secondi.\n\nAprire la cartella?":
        "{path}\n\n{size:.1f} MB in {seconds:.0f} seconden.\n\nDe map openen?",
    "{app} {version}. Montaggio video semplice per presentazioni: timeline, tagli, fermo immagine, avanzamento veloce, sovraimpressioni, zoom e pixelatura con inseguimento; esportazione mp4 con ffmpeg. Progetti in formato JSON.":
        "{app} {version}. Eenvoudige videomontage voor presentaties: tijdlijn, knippen, stilstaand beeld, versneld "
        "afspelen, overlays, zoom en pixelering met volgen; export naar mp4 met ffmpeg. Projecten in JSON-formaat.",
    "{copyright}. Software libero: GNU General Public License versione 3 con termini aggiuntivi (attribuzione dell'autore, nome e logo), vedi i file LICENSE e NOTICE. Nessuna garanzia. Usa librerie e programmi di terze parti con le loro licenze (elencati in NOTICE).":
        "{copyright}. Vrije software: GNU General Public License versie 3 met aanvullende voorwaarden "
        "(naamsvermelding van de auteur, naam en logo), zie de bestanden LICENSE en NOTICE. Geen garantie. Gebruikt "
        "bibliotheken en programma's van derden met hun eigen licenties (vermeld in NOTICE).",
    "cartella tools/ffmpeg": "map tools/ffmpeg",
    "PATH di sistema": "systeem-PATH",
    "VitTrack presente: l'inseguimento lo usa.\n{model}": "VitTrack aanwezig: het volgen gebruikt het.\n{model}",
    "{width}x{height}  {fps:g} fps  {clips} clip  {duration}": "{width}x{height}  {fps:g} fps  {clips} clips  {duration}",
    "Anteprima: {error}": "Voorbeeld: {error}",
    "Audio dell'anteprima non disponibile: {error}": "Audio van het voorbeeld niet beschikbaar: {error}",
    "Impossibile aprire il progetto:\n{error}": "Kan het project niet openen:\n{error}",
    "Slide aggiunta a {time}: regolala nel pannello a destra.":
        "Dia toegevoegd op {time}: stel haar in via het paneel rechts.",
    "Il fotogramma a {time} resta fermo per questo tempo; cio' che segue scorre in avanti.":
        "Het frame op {time} blijft zo lang stilstaan; wat volgt schuift naar achteren.",
    "L'inseguimento parte dal cursore ({start}) e segue il soggetto fino a questo istante (al massimo la fine della clip: {clip_end}).":
        "Het volgen begint bij de cursor ({start}) en volgt het onderwerp tot dit tijdstip (hoogstens het einde van "
        "de clip: {clip_end}).",
    "File non trovato: {path}": "Bestand niet gevonden: {path}",
    "ffmpeg trovato ({where})\n{path}\nversione {version}": "ffmpeg gevonden ({where})\n{path}\nversie {version}",
    "Segna IN e OUT (tasti I e O) oppure seleziona un elemento da eliminare.":
        "Markeer IN en OUT (toetsen I en O) of selecteer een element om te verwijderen.",
    "Fotogramma {done} / {total}": "Frame {done} / {total}",
    "; soggetto non trovato da {time} al keyframe": "; onderwerp niet gevonden van {time} tot de keyframe",
    ", non trovato in {frames} fotogrammi": ", niet gevonden in {frames} frames",
    "formato audio inatteso": "onverwacht audioformaat",
    "Scegli il carattere": "Lettertype kiezen",
    "Cerca carattere...": "Lettertype zoeken...",
    "{shown} / {total}  - caricamento...": "{shown} / {total}  - laden...",
    "Caratteri della cartella font/ e di Windows, mostrati con il testo «{sample}». Clicca per scegliere.":
        "Lettertypen uit de map font/ en van Windows, getoond met de tekst «{sample}». Klik om te kiezen.",
    "ffmpeg non trovato: scaricalo dalla pagina Configurazione.":
        "ffmpeg niet gevonden: download het via de pagina Configuratie.",
    "Durata sconosciuta (file danneggiato o non riconosciuto).":
        "Onbekende duur (beschadigd of niet herkend bestand).",
    "Il file non contiene ne' video ne' audio riconoscibili.":
        "Het bestand bevat geen herkenbare video of audio.",
    "ffmpeg non ha scritto il fotogramma.": "ffmpeg heeft het frame niet geschreven.",
    "ffmpeg: codice di uscita {code}": "ffmpeg: exitcode {code}",
    "Impossibile aprire il video: {path}": "Kan de video niet openen: {path}",
    "Testo a destra del logo": "Tekst rechts van het logo",
    "Testo a sinistra del logo": "Tekst links van het logo",
    "Testo sotto il logo": "Tekst onder het logo",
    "Riempi (taglia i bordi)": "Vullen (randen bijsnijden)",
    "Intera (bande del colore)": "Volledig (balken in de kleur)",
    "Stira": "Uitrekken",
    "Al centro": "In het midden",
    "Sinistra": "Links",
    "Centro": "Midden",
    "Destra": "Rechts",
    "Nessun elemento selezionato.\n\nClicca una clip, un effetto o una traccia audio nella timeline per vederne le proprieta'.\n\nFlusso di lavoro:\n1. Importa un video (Ctrl+I)\n2. Segna IN e OUT (tasti I e O) e taglia o elimina\n3. Aggiungi fermo immagine, velocita', testi, frecce, riquadri, zoom, pixelatura\n4. Esporta in mp4 (Ctrl+E)":
        "Geen element geselecteerd.\n\nKlik op een clip, een effect of een audiospoor in de tijdlijn om de "
        "eigenschappen te zien.\n\nWerkwijze:\n1. Importeer een video (Ctrl+I)\n2. Markeer IN en OUT (toetsen I en "
        "O) en knip of verwijder\n3. Voeg stilstaand beeld, snelheid, teksten, pijlen, kaders, zoom, pixelering "
        "toe\n4. Exporteer naar mp4 (Ctrl+E)",
    "Proprieta'": "Eigenschappen",
    "File": "Bestand",
    "Durata": "Duur",
    "Posizione": "Positie",
    "Elimina clip": "Clip verwijderen",
    "Transizioni": "Overgangen",
    "Dal nero (s)": "Uit zwart (s)",
    "Al nero (s)": "Naar zwart (s)",
    "Durata (s)": "Duur (s)",
    "Colore sfondo": "Achtergrondkleur",
    "nessuna": "geen",
    "Elimina slide": "Dia verwijderen",
    "Tempo": "Tijd",
    "Inizio (s)": "Begin (s)",
    "Fine (s)": "Einde (s)",
    "Elimina effetto": "Effect verwijderen",
    "Stato": "Status",
    "Keyframe qui (fissa la posizione)": "Keyframe hier (positie vastleggen)",
    "Audio originale attivo": "Originele audio aan",
    "Volume": "Volume",
    "Dissolvenze": "Faden",
    "All'inizio (s)": "Aan het begin (s)",
    "Alla fine (s)": "Aan het einde (s)",
    "Elimina l'audio originale": "Originele audio verwijderen",
    "Pezzo": "Stuk",
    "Audio di questo pezzo": "Audio van dit stuk",
    "Volume di questo pezzo": "Volume van dit stuk",
    "Entrata (s)": "Fade-in (s)",
    "Uscita (s)": "Fade-out (s)",
    "Elimina audio di questo pezzo": "Audio van dit stuk verwijderen",
    "Nome": "Naam",
    "Porzione del file": "Deel van het bestand",
    "Dall'istante (s)": "Vanaf tijdstip (s)",
    "All'istante (s)": "Tot tijdstip (s)",
    "Muta": "Dempen",
    "Elimina traccia": "Spoor verwijderen",
    "video": "video",
    "Istante sorgente (s)": "Brontijdstip (s)",
    "Taglio nel video sorgente": "Knip in de bronvideo",
    "Audio originale di questa clip": "Originele audio van deze clip",
    "Volume audio originale (tutto il progetto)": "Volume originele audio (hele project)",
    "Velocita' (sotto 1x rallenta)": "Snelheid (onder 1x vertraagd)",
    "Mostra orologio con la velocita'": "Klok met de snelheid tonen",
    "Orologio (tutto il progetto)": "Klok (hele project)",
    "Dimensione (px)": "Grootte (px)",
    "Colore": "Kleur",
    "Opacita' sfondo": "Dekking achtergrond",
    "Fusione con la succ. (s)": "Overvloeien met volg. (s)",
    "Slide di apertura": "Openingsdia",
    "Adattamento": "Aanpassing",
    "Allineamento": "Uitlijning",
    "Ombra": "Schaduw",
    "Opacita' del testo": "Dekking van de tekst",
    "Sfondo dietro il testo": "Achtergrond achter de tekst",
    "Modifica testo...": "Tekst bewerken...",
    "fermo": "vast",
    "Ripeti inseguimento dal cursore": "Volgen opnieuw vanaf de cursor",
    "Segui il soggetto": "Onderwerp volgen",
    "Non seguire piu'": "Niet meer volgen",
    "nessuno": "geen",
    "Togli keyframe al cursore": "Keyframe op de cursor verwijderen",
    "Cancella i punti selezionati": "Geselecteerde punten wissen",
    "il file non ha audio": "het bestand heeft geen audio",
    "= cursore": "= cursor",
    "Dal nero: la clip compare dal nero. Al nero: sparisce nel nero. Fusione: la clip sfuma nella successiva, a cavallo del taglio (la durata del video non cambia). Anche l'audio sale e scende. 0 = taglio netto.":
        "Uit zwart: de clip verschijnt uit het zwart. Naar zwart: hij verdwijnt in het zwart. Overvloeien: de clip "
        "vloeit over in de volgende, rond de knip (de duur van de video verandert niet). Ook de audio gaat omhoog en "
        "omlaag. 0 = harde knip.",
    "La slide e' un fondo a tinta unita o un'immagine adattata alla misura del video. Testi e immagini si mettono sopra con gli strumenti Testo e Immagine: con il cursore sulla slide durano quanto lei.":
        "De dia is een effen achtergrond of een afbeelding aangepast aan de afmetingen van de video. Teksten en "
        "afbeeldingen zet je erop met de gereedschappen Tekst en Afbeelding: met de cursor op de dia duren ze even "
        "lang als de dia.",
    "Larghezza (px)": "Breedte (px)",
    "Opacita'": "Dekking",
    "Dove l'inseguimento sbaglia: porta il cursore li' e trascina la figura sul soggetto (dagli angoli per la misura). Diventa un keyframe: il tratto prima viene corretto e l'inseguimento riparte da li' fino al keyframe successivo.\nNella timeline, sulla barra dell'effetto, i keyframe sono rombi e i punti dell'inseguimento pallini. Clic: seleziona e porta il cursore; Maiusc+clic: intervallo; Ctrl+clic: aggiunge o toglie. Canc o tasto destro: cancella i selezionati (li' la figura va dritta fra i punti rimasti).":
        "Waar het volgen fout gaat: zet de cursor daar en sleep de figuur op het onderwerp (via de hoeken voor de "
        "grootte). Het wordt een keyframe: het stuk ervoor wordt gecorrigeerd en het volgen begint daar opnieuw tot "
        "de volgende keyframe.\nIn de tijdlijn, op de effectbalk, zijn keyframes ruitjes en de volgpunten bolletjes. "
        "Klik: selecteert en verplaatst de cursor; Shift+klik: bereik; Ctrl+klik: toevoegen of weghalen. Del of "
        "rechtermuisknop: wist de geselecteerde (daar gaat de figuur recht tussen de overgebleven punten).",
    "< Prec.": "< Vor.",
    "Succ. >": "Volg. >",
    "Centra orizz.": "Horiz. centreren",
    "Centra vert.": "Vert. centreren",
    "Valgono per l'audio originale di tutto il video: sale all'inizio e scende alla fine. Canc spegne tutto l'audio originale (il video resta). Per un solo pezzo clicca la sua barra nella riga dell'audio.":
        "Gelden voor de originele audio van de hele video: hij gaat omhoog aan het begin en omlaag aan het einde. "
        "Del schakelt alle originele audio uit (de video blijft). Voor één stuk klik je op zijn balk in de "
        "audioregel.",
    "Per togliere solo un tratto d'audio: segna IN e OUT (tasti I e O) e premi Canc con l'audio selezionato: il video resta. Oppure taglia con S e seleziona il pezzo d'audio: Canc lo elimina, qui ne regoli volume e dissolvenze.":
        "Om alleen een stuk audio weg te halen: markeer IN en OUT (toetsen I en O) en druk op Del met de audio "
        "geselecteerd: de video blijft. Of knip met S en selecteer het audiostuk: Del verwijdert het, hier stel je "
        "volume en faden in.",
    "Il volume sale da zero all'inizio della traccia e scende a zero alla fine.":
        "Het volume gaat aan het begin van het spoor omhoog vanaf nul en aan het einde omlaag naar nul.",
    "slide": "dia",
    "Clip: {kind}": "Clip: {kind}",
    "Traccia audio": "Audiospoor",
    "Slide di chiusura": "Slotdia",
    "Togli": "Verwijderen",
    "Sull'anteprima: trascina per spostare, dagli angoli per ingrandire, doppio clic per riscriverlo.":
        "In het voorbeeld: sleep om te verplaatsen, via de hoeken om te vergroten, dubbelklik om te herschrijven.",
    "Largh.": "Br.",
    "  Alt.": "  H.",
    "Spessore bordo": "Randdikte",
    "Riempimento": "Vulling",
    "Opacita' riempimento": "Dekking vulling",
    "Il contenuto della figura fa da modello: la figura segue il soggetto nei fotogrammi successivi; quando esce dall'inquadratura l'effetto finisce.":
        "De inhoud van de figuur dient als sjabloon: de figuur volgt het onderwerp in de volgende frames; wanneer het "
        "buiten beeld gaat, eindigt het effect.",
    "segue il soggetto ({points} punti)": "volgt het onderwerp ({points} punten)",
    "Effetto: {name}": "Effect: {name}",
    "Audio originale (un pezzo)": "Originele audio (één stuk)",
    "Carattere": "Lettertype",
    "Sull'anteprima: trascina per spostarla, dagli angoli per ridimensionarla (le proporzioni restano quelle dell'immagine).":
        "In het voorbeeld: sleep om haar te verplaatsen, via de hoeken om haar te schalen (de verhoudingen van de "
        "afbeelding blijven behouden).",
    "Coda X": "Staart X",
    "Punta X": "Punt X",
    "Spessore": "Dikte",
    "Audio originale (tutto)": "Originele audio (alles)",
    "Area da ingrandire": "Te vergroten gebied",
    "Forma": "Vorm",
    "Angoli (rettangolare)": "Hoeken (rechthoekig)",
    "Contorno colorato sull'area ingrandita": "Gekleurde omtrek rond het vergrote gebied",
    "Linea fra l'area e il riquadro": "Lijn tussen het gebied en het kader",
    "Riquadro ingrandito": "Vergroot kader",
    "L'area fa da modello: lo zoom segue l'oggetto nei fotogrammi successivi, il riquadro ingrandito resta dove l'hai messo. Se l'oggetto esce dall'inquadratura lo zoom finisce.":
        "Het gebied dient als sjabloon: de zoom volgt het object in de volgende frames, het vergrote kader blijft waar "
        "je het hebt gezet. Als het object buiten beeld gaat, eindigt de zoom.",
    "Rettangolare": "Rechthoekig",
    "Ingrandimento": "Vergroting",
    "Larghezza": "Breedte",
    "Per tutto il video": "Voor de hele video",
    "Largh. logo (px)": "Logobreedte (px)",
    "Dimensione testo": "Tekstgrootte",
    "Colore testo": "Tekstkleur",
    "Disposizione": "Indeling",
    "Ombra sotto il testo": "Schaduw onder de tekst",
    "Sfondo": "Achtergrond",
    "Sfondo sotto logo e scritta": "Achtergrond onder logo en tekst",
    "Opacita' di tutto": "Dekking van alles",
    "Angolo": "Hoek",
    "Il colore vale per il bordo del riquadro, il contorno dell'area e la linea. L'area scelta viene mostrata ingrandita nel riquadro, sopra il video, per la durata dell'effetto. Sull'anteprima: trascina l'area o il riquadro, ridimensiona l'area dagli angoli.":
        "De kleur geldt voor de rand van het kader, de omtrek van het gebied en de lijn. Het gekozen gebied wordt "
        "vergroot getoond in het kader, boven de video, zolang het effect duurt. In het voorbeeld: sleep het gebied "
        "of het kader, schaal het gebied via de hoeken.",
    "Pixelatura": "Pixelering",
    "Grandezza pixel": "Pixelgrootte",
    "Resta fermo nel punto scelto. Sull'anteprima trascinalo per spostarlo, tira un angolo per ingrandire o rimpicciolire logo e testo insieme. I valori proposti per i prossimi si cambiano in Configurazione.":
        "Blijft vast op de gekozen plek. Sleep in het voorbeeld om te verplaatsen, trek aan een hoek om logo en tekst "
        "samen te vergroten of te verkleinen. De voorgestelde waarden voor de volgende wijzig je in Configuratie.",
    "fisso": "vast",
    "Soggetto perso": "Onderwerp kwijt",
    "Ripeti l'inseguimento dopo aver cambiato inizio o fine.":
        "Herhaal het volgen na het wijzigen van begin of einde.",
    "{points} punti": "{points} punten",
    "{frames} fotogrammi": "{frames} frames",
    "Trascina sull'anteprima per disegnare il riquadro": "Sleep in het voorbeeld om het kader te tekenen",
    "Trascina sull'anteprima per disegnare l'ovale": "Sleep in het voorbeeld om het ovaal te tekenen",
    "Trascina sull'anteprima un rettangolo sull'oggetto da ingrandire":
        "Sleep in het voorbeeld een rechthoek over het te vergroten object",
    "Clicca dove far apparire il riquadro ingrandito  -  {factor}x  (rotellina o tasti 2, 3, 4, 6, 8)":
        "Klik waar het vergrote kader moet verschijnen  -  {factor}x  (scrollwiel of toetsen 2, 3, 4, 6, 8)",
    "Clicca sull'anteprima dove mettere il tempo trascorso": "Klik in het voorbeeld waar de verstreken tijd moet komen",
    "Trascina sull'anteprima l'area da pixelare: verra' inseguita nei fotogrammi successivi":
        "Sleep in het voorbeeld het te pixeleren gebied: het wordt gevolgd in de volgende frames",
    "Trascina dalla coda alla punta della freccia": "Sleep van de staart naar de punt van de pijl",
    "Clicca sull'anteprima dove mettere il testo": "Klik in het voorbeeld waar de tekst moet komen",
    "Importa un video per vedere l'anteprima": "Importeer een video om het voorbeeld te zien",
    "segue il soggetto": "volgt het onderwerp",
    "Logo e operatore": "Logo en operator",
    "Slide di apertura: {text}": "Openingsdia: {text}",
    "Slide di chiusura: {text}": "Slotdia: {text}",
    "Slide: {text}": "Dia: {text}",
    "Fermo immagine ({name})": "Stilstaand beeld ({name})",
    "Percorso del progetto mancante": "Pad van het project ontbreekt",
    "La timeline e' vuota: importa almeno un video.": "De tijdlijn is leeg: importeer minstens één video.",
    "Preparazione dei segmenti": "Segmenten voorbereiden",
    "Disegno delle sovraimpressioni": "Overlays tekenen",
    "Preparazione": "Voorbereiding",
    "Completato": "Voltooid",
    "ffmpeg non ha scritto il file di uscita.": "ffmpeg heeft het uitvoerbestand niet geschreven.",
    "Disegno del contorno dello zoom": "Omtrek van de zoom tekenen",
    "Disegno dell'orologio {speed}": "Klok {speed} tekenen",
    "Codifica: {done} / {total}": "Coderen: {done} / {total}",
    "Audio originale": "Originele audio",
    "muto": "gedempt",
    "immagine": "afbeelding",
    "orologio": "klok",
    "senza audio": "zonder audio",
    "audio": "audio",
    "{name} ({points} punti)": "{name} ({points} punten)",
    "{name} (fisso)": "{name} (vast)",
    "{name} (segue)": "{name} (volgt)",
    "audio {volume:.0f} %": "audio {volume:.0f} %",
    "Risposta inattesa dal sito di download di ffmpeg.": "Onverwacht antwoord van de downloadsite van ffmpeg.",
    "Il download automatico e' disponibile solo su Windows: installa ffmpeg con il gestore di pacchetti del sistema.":
        "Automatisch downloaden is alleen beschikbaar op Windows: installeer ffmpeg met de pakketbeheerder van het "
        "systeem.",
    "licenza di VitTrack": "licentie van VitTrack",
    "Il file scaricato non e' un archivio zip valido.": "Het gedownloade bestand is geen geldig zip-archief.",
    "Estrazione di ffmpeg": "ffmpeg uitpakken",
    "L'ffmpeg scaricato non si avvia su questo PC.": "De gedownloade ffmpeg werkt niet op deze pc.",
    "Il modello scaricato non corrisponde a quello atteso (impronta SHA-256 diversa).":
        "Het gedownloade model komt niet overeen met het verwachte (andere SHA-256-vingerafdruk).",
    "Il pacchetto scaricato non contiene {file}.": "Het gedownloade pakket bevat geen {file}.",
    "{file} manca dopo l'estrazione.": "{file} ontbreekt na het uitpakken.",
    "Impossibile controllare l'ultima versione di ffmpeg: {error}":
        "Kan de nieuwste ffmpeg-versie niet controleren: {error}",
    "Download di {name} fallito: {error}": "Download van {name} mislukt: {error}",
    "Impossibile aggiornare '{folder}': file in uso. Aspetta la fine dell'esportazione e riprova.":
        "Kan ‘{folder}’ niet bijwerken: bestanden in gebruik. Wacht tot de export klaar is en probeer opnieuw.",
    "OpenCV non riesce a caricare il modello: {error}": "OpenCV kan het model niet laden: {error}",
    "Archivio non valido: percorso sospetto '{path}'.": "Ongeldig archief: verdacht pad ‘{path}’.",
    "Download di {name}": "{name} downloaden",
    "Nessun fotogramma all'istante di partenza.": "Geen frame op het starttijdstip.",
    "INFO": "INFO",
    "CONFERMA": "BEVESTIGEN",
    "ATTENZIONE": "WAARSCHUWING",
    "ERRORE": "FOUT",
    "OK": "OK",
    "Annulla": "Annuleren",
    "Si'": "Ja",
    "No": "Nee",
    "Interruzione...": "Onderbreken...",
    "Invio va a capo, Ctrl+Invio conferma.": "Enter voor een nieuwe regel, Ctrl+Enter bevestigt.",
    "Allineamento delle righe": "Uitlijning van de regels",
    "Scrivi il testo.": "Schrijf de tekst.",
    "Fondo scuro": "Donkere achtergrond",
    "Centra nel video": "Centreren in de video",
    "Dimensione non valida.": "Ongeldige grootte.",
    "{field}: valore fra {min:g} e {max:g}.": "{field}: waarde tussen {min:g} en {max:g}.",
    "{field}: inserisci un numero.": "{field}: voer een getal in.",
    # ------------------------------------------------------- tempo trascorso
    "Tempo trascorso dall'inizio del video: clic dove metterlo, poi si sposta":
        "Verstreken tijd sinds het begin van de video: klik waar hij moet komen, daarna kun je hem verplaatsen",
    "Tempo trascorso aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.":
        "Verstreken tijd toegevoegd: sleep hem waar je wilt, stel hem in via het paneel rechts.",
    "minuti:secondi (01:23)": "minuten:seconden (01:23)",
    "ore:minuti:secondi (00:01:23)": "uren:minuten:seconden (00:01:23)",
    "con i decimi (01:23.4)": "met tienden (01:23.4)",
    "dall'inizio del video": "vanaf het begin van de video",
    "dall'inizio dell'effetto": "vanaf het begin van het effect",
    "Tempo trascorso": "Verstreken tijd",
    "Formato": "Formaat",
    "Conta": "Telt",
    "Testo davanti": "Tekst ervoor",
    "Sfondo dietro il tempo": "Achtergrond achter de tijd",
    "Sull'anteprima: trascinalo dove vuoi, dagli angoli per ingrandirlo.":
        "In het voorbeeld: sleep hem waar je wilt, via de hoeken om hem te vergroten.",
    "Disegno del tempo trascorso": "Verstreken tijd tekenen",

    # ------------------------------------------------------- riproduzione
    '10 fotogrammi indietro (Ctrl+Sinistra)': '10 frames terug (Ctrl+Links)',
    "Riproduci all'indietro / pausa (Maiusc+Spazio), senza audio": 'Achteruit afspelen / pauze (Shift+Spatie), zonder geluid',
    '10 fotogrammi avanti (Ctrl+Destra)': '10 frames vooruit (Ctrl+Rechts)',
    'Allunga fino al cursore': 'Verlengen tot de cursor',
    'Interrompi al cursore': 'Stoppen bij de cursor',
    '{effect} allungato fino a {t:.2f} s.': '{effect} verlengd tot {t:.2f} s.',
    '{effect} interrotto a {t:.2f} s.': '{effect} gestopt op {t:.2f} s.',
    "{effect} nascosto: non compare in anteprima ne' nel video esportato.": '{effect} verborgen: niet zichtbaar in de voorvertoning en in de geëxporteerde video.',
    '{effect} di nuovo visibile.': '{effect} weer zichtbaar.',
    '{zoom}% - trascina per spostarti, doppio clic centrale: adatta': '{zoom}% - sleep om te verschuiven, dubbelklik middelste knop: passend',
    'Fotogrammi': 'Frames',
    "Numero del fotogramma dall'inizio del video: clic dove metterlo, poi si sposta": 'Framenummer vanaf het begin van de video: klik waar het moet komen, daarna verplaatsen',
    'Numero del fotogramma aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.': 'Framenummer toegevoegd: sleep het waar je wilt, pas het aan in het paneel rechts.',
    'Numero del fotogramma': 'Framenummer',
    'Primo fotogramma': 'Eerste frame',
    "Clicca sull'anteprima dove mettere il numero del fotogramma": 'Klik in de voorvertoning waar het framenummer moet komen',
    'Anteprima': 'Voorvertoning',
    'Anteprima riattaccata.': 'Voorvertoning weer vastgezet.',
    "Riattacca l'anteprima alla finestra principale": 'Voorvertoning terugzetten in het hoofdvenster',
    "Stacca l'anteprima in una finestra a parte (piu' spazio per la timeline)": 'Voorvertoning losmaken in een apart venster (meer ruimte voor de tijdlijn)',
    'Anteprima in una finestra a parte: chiudila o usa il pulsante in alto a destra per riattaccarla.': 'Voorvertoning in een apart venster: sluit het of gebruik de knop rechtsboven om het terug te zetten.',
    "Trascina un rettangolo attorno al soggetto: la freccia lo seguira' tenendo la punta dov'e'.": 'Sleep een rechthoek rond het onderwerp: de pijl volgt het en de punt blijft waar hij is.',
    'soggetto della freccia': 'onderwerp van de pijl',
    "Si disegna un rettangolo attorno al soggetto: la freccia lo segue nei fotogrammi successivi tenendo la punta su di lui; quando esce dall'inquadratura l'effetto finisce.": 'Teken een rechthoek rond het onderwerp: de pijl volgt het in de volgende frames met de punt erop; als het uit beeld gaat, stopt het effect.',
    'Scegli un altro soggetto': 'Ander onderwerp kiezen',
    'Trascina un rettangolo attorno al soggetto che la freccia deve seguire': 'Sleep een rechthoek rond het onderwerp dat de pijl moet volgen',
}
