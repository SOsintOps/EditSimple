# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Shqip: përkthimi i teksteve të ndërfaqes së EditSimple.

Çelësi është teksti italisht ashtu siç shfaqet në kod (në tr() dhe N_()),
vlera është përkthimi i tij. Vendmbajtësit në kllapa gjarpërore mbeten të pandryshuar.
Pas çdo ndryshimi:

    .venv\\Scripts\\python.exe scripts\\check_i18n.py sq
"""

from __future__ import annotations

NAME = "Shqip"

CATALOG: dict[str, str] = {
    # ---------------------------------------------------------------- avvio
    "Impossibile avviare l'interfaccia: {error}\n\nInstalla le dipendenze con:\n    {command}":
        "Ndërfaqja nuk mund të niset: {error}\n\nInstaloni varësitë me:\n    {command}",

    # ---------------------------------------------------------------- angoli e tipi
    "In alto a sinistra": "Lart majtas",
    "In alto a destra": "Lart djathtas",
    "In basso a sinistra": "Poshtë majtas",
    "In basso a destra": "Poshtë djathtas",
    "Progetto EditSimple": "Projekt EditSimple",
    "Tutti i file": "Të gjithë skedarët",
    "Apertura (all'inizio)": "Hapja (në fillim)",
    "Chiusura (alla fine)": "Mbyllja (në fund)",

    # ---------------------------------------------------------------- barra strumenti
    "Apri progetto... (Ctrl+O)": "Hap projektin... (Ctrl+O)",
    "Progetto": "Projekti",
    "Nuovo": "I ri",
    "Nuovo progetto (Ctrl+N)": "Projekt i ri (Ctrl+N)",
    "Apri": "Hap",
    "Apri progetto (Ctrl+O)": "Hap projektin (Ctrl+O)",
    "Salva": "Ruaj",
    "Salva progetto (Ctrl+S)": "Ruaj projektin (Ctrl+S)",
    "Annulla (Ctrl+Z)": "Zhbëj (Ctrl+Z)",
    "Ripeti (Ctrl+Y)": "Ribëj (Ctrl+Y)",
    "Clip": "Klipi",
    "Importa video": "Importo video",
    "Importa un video in coda o al cursore (Ctrl+I)": "Importon një video në fund ose te kursori (Ctrl+I)",
    "Audio": "Audio",
    "Aggiungi una traccia audio (commento, musica) al cursore":
        "Shton një gjurmë audio (koment, muzikë) te kursori",
    "Taglia": "Prit",
    "Taglia la clip al cursore (S)": "Pret klipin te kursori (S)",
    "Elimina": "Fshi",
    "Elimina la porzione IN-OUT o l'elemento selezionato (Canc)":
        "Fshin pjesën IN-OUT ose elementin e zgjedhur (Delete)",
    "Fermo": "Ngrij",
    "Fermo immagine del fotogramma al cursore (F)": "Ngrin kuadrin te kursori (F)",
    "Slide": "Slajd",
    "Inserisci una slide": "Fut një slajd",
    "Velocita'": "Shpejtësia",
    "Velocita' della porzione IN-OUT: piu' veloce o rallentata (V)":
        "Shpejtësia e pjesës IN-OUT: më e shpejtë ose e ngadalësuar (V)",
    "Sovraimpressioni": "Mbivendosje",
    "Testo": "Tekst",
    "Testo (T)": "Tekst (T)",
    "Immagine": "Imazh",
    "Immagine sopra il video, da spostare e ridimensionare":
        "Imazh mbi videon, për ta lëvizur dhe ndryshuar përmasat",
    "Logo": "Logo",
    "Logo e testo dell'operatore, fermi in un angolo (L)":
        "Logoja dhe teksti i operatorit, të palëvizshëm në një qoshe (L)",
    "Riquadro": "Kornizë",
    "Riquadro (R): puo' seguire il soggetto": "Kornizë (R): mund të ndjekë subjektin",
    "Ovale": "Oval",
    "Ovale (E): puo' seguire il soggetto": "Oval (E): mund të ndjekë subjektin",
    "Freccia": "Shigjetë",
    "Freccia (A): puo' seguire il soggetto": "Shigjetë (A): mund të ndjekë subjektin",
    "Zoom": "Zmadhim",
    "Zoom rettangolare: l'area scelta in un riquadro ingrandito (Z)":
        "Zmadhim drejtkëndor: zona e zgjedhur në një kornizë të zmadhuar (Z)",
    "Zoom ovale: l'area scelta in un ovale ingrandito (Maiusc+Z)":
        "Zmadhim oval: zona e zgjedhur në një oval të zmadhuar (Shift+Z)",
    "Pixel": "Piksel",
    "Pixelatura rettangolare che insegue il soggetto (P)": "Pikselim drejtkëndor që ndjek subjektin (P)",
    "Pixelatura ovale che insegue il soggetto (K)": "Pikselim oval që ndjek subjektin (K)",
    "Uscita": "Dalja",
    "Esporta MP4": "Eksporto MP4",
    "Esporta il video finale (Ctrl+E)": "Eksporton videon përfundimtare (Ctrl+E)",

    # ---------------------------------------------------------------- configurazione
    "Inseguimento (VitTrack)": "Ndjekja (VitTrack)",
    "Esportazione": "Eksportimi",
    "Logo e testo dell'operatore": "Logoja dhe teksti i operatorit",
    "Angoli arrotondati": "Qoshe të rrumbullakosura",
    "Crediti": "Kredite",
    "Lingua": "Gjuha",
    "Impostazioni salvate.": "Cilësimet u ruajtën.",
    "Download di ffmpeg": "Shkarkimi i ffmpeg",
    "Download di VitTrack": "Shkarkimi i VitTrack",

    # ---------------------------------------------------------------- messaggi
    "Progetto non salvato": "Projekt i paruajtur",
    "Salvare le modifiche al progetto?": "Të ruhen ndryshimet në projekt?",
    "Nuovo progetto.": "Projekt i ri.",
    "Lettura del video...": "Po lexohet videoja...",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}":
        "U importua {file}: {width}x{height}, {fps:g} fps, {duration}",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}, senza audio":
        "U importua {file}: {width}x{height}, {fps:g} fps, {duration}, pa audio",
    "Audio di questo pezzo eliminato (il video resta). Ctrl+Z per riaverlo.":
        "Audioja e kësaj pjese u fshi (videoja mbetet). Ctrl+Z për ta rikthyer.",
    "Clip eliminata.": "Klipi u fshi.",
    "Fermo immagine": "Kuadër i ngrirë",
    "Nuovo testo": "Tekst i ri",
    "Testo aggiunto: trascinalo, ingrandiscilo dagli angoli, doppio clic per riscriverlo.":
        "Teksti u shtua: zvarriteni, zmadhojeni nga qoshet, klik i dyfishtë për ta rishkruar.",
    "Modifica testo": "Ndrysho tekstin",
    "Immagine aggiunta: trascinala per spostarla, dagli angoli per ridimensionarla.":
        "Imazhi u shtua: zvarriteni për ta lëvizur, nga qoshet për t'i ndryshuar përmasat.",
    "Pixelatura con inseguimento": "Pikselim me ndjekje",
    "Cancellati {count} punti del percorso (il primo resta: e' la partenza della figura).":
        "U fshinë {count} pika të shtegut (e para mbetet: është nisja e figurës).",
    "Cancellati {count} punti del percorso.": "U fshinë {count} pika të shtegut.",
    "Inseguimento del soggetto": "Ndjekja e subjektit",
    "Esportazione in corso": "Eksportimi në vazhdim",
    "montaggio video per presentazioni": "montazh video për prezantime",
    "PROGETTO": "PROJEKTI",
    "nuovo": "i ri",
    "Nessun video": "Asnjë video",
    "Montaggio": "Montazhi",
    "Configura": "Konfiguro",
    "Riproduci / pausa (Spazio)": "Luaj / pauzë (Hapësirë)",
    "larghezza logo % del video": "gjerësia e logos % e videos",
    "altezza testo % del lato corto": "lartësia e tekstit % e anës së shkurtër",
    "distanza dai bordi % del lato corto": "largësia nga skajet % e anës së shkurtër",
    "opacita' %": "opaciteti %",
    "angoli arrotondati %": "qoshe të rrumbullakosura %",
    "sfondo del testo": "sfondi i tekstit",
    "riquadro": "kornizë",
    "zoom rettangolare": "zmadhim drejtkëndor",
    "pixel rettangolare": "piksel drejtkëndor",
    "Colore del testo": "Ngjyra e tekstit",
    "Colore dello sfondo": "Ngjyra e sfondit",
    "Immagine del logo": "Imazhi i logos",
    "Questa immagine non si apre.": "Ky imazh nuk hapet.",
    "Controllo in corso...": "Po kontrollohet...",
    "Pronto.": "Gati.",
    "ffmpeg non e' stato trovato. Scaricalo dal riquadro FFmpeg della pagina Configurazione: senza, non si possono importare ne' esportare video.":
        "ffmpeg nuk u gjet. Shkarkojeni nga kutia FFmpeg e faqes Konfigurimi: pa të, videot nuk mund "
        "të importohen as të eksportohen.",
    "ffmpeg non e' stato trovato. Installalo con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) o copia un eseguibile ffmpeg in tools/ffmpeg/: senza, non si possono importare ne' esportare video.":
        "ffmpeg nuk u gjet. Instalojeni me menaxherin e paketave të sistemit (për shembull sudo apt install ffmpeg) ose kopjoni një skedar ekzekutues ffmpeg në tools/ffmpeg/: pa të, videot nuk mund të importohen as të eksportohen.",
    "Non salvare": "Mos ruaj",
    "Niente da annullare.": "Asgjë për të zhbërë.",
    "inizio": "fillimi",
    "fine": "fundi",
    "Apri progetto": "Hap projektin",
    "File mancanti": "Skedarë që mungojnë",
    "Salva progetto": "Ruaj projektin",
    "Dove inserire il video?": "Ku të futet videoja?",
    "Importazione": "Importimi",
    "Il file non contiene video. Per l'audio usa il pulsante Audio.":
        "Skedari nuk përmban video. Për audion përdorni butonin Audio.",
    "Importa prima un video.": "Importoni fillimisht një video.",
    "Aggiungi traccia audio": "Shto gjurmë audio",
    "Il file non contiene audio.": "Skedari nuk përmban audio.",
    "Il cursore e' gia' su un confine fra clip.": "Kursori është tashmë në një kufi midis klipeve.",
    "Importa prima un video: la slide prende la sua misura.":
        "Importoni fillimisht një video: slajdi merr përmasat e saj.",
    "Al cursore ({time})": "Te kursori ({time})",
    "Dove": "Ku",
    "Durata (secondi)": "Kohëzgjatja (sekonda)",
    "Crea": "Krijo",
    "La slide e' un fondo a tinta unita (il colore si sceglie nel pannello). Testi e immagini si aggiungono sopra con gli strumenti Testo e Immagine.":
        "Slajdi është një sfond me ngjyrë të njëtrajtshme (ngjyra zgjidhet në panel). Tekstet dhe imazhet "
        "shtohen sipër me mjetet Tekst dhe Imazh.",
    "Slide di chiusura aggiunta alla fine: regolala nel pannello a destra.":
        "Slajdi i mbylljes u shtua në fund: rregullojeni në panelin djathtas.",
    "Inserisci": "Fut",
    "Applica": "Zbato",
    "Effetti": "Efektet",
    "Pixel ovale": "Piksel oval",
    "Pixel rettangolare": "Piksel drejtkëndor",
    "Zoom ovale (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Zmadhim oval (drejtkëndësh mbi objektin, pastaj klik ku të vendoset korniza)",
    "Zoom (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Zmadhim (drejtkëndësh mbi objektin, pastaj klik ku të vendoset korniza)",
    "Carica l'immagine del logo e scrivi il testo dell'operatore nella pagina Configura, poi premi di nuovo Logo.":
        "Ngarkoni imazhin e logos dhe shkruani tekstin e operatorit në faqen Konfiguro, pastaj shtypni "
        "përsëri Logo.",
    "Logo e operatore aggiunti per tutto il video: trascinali sull'anteprima o regolali nel pannello.":
        "Logoja dhe operatori u shtuan për gjithë videon: zvarritini mbi parapamje ose rregullojini në panel.",
    "Zoom aggiunto (fermo: sul fermo immagine non c'e' nulla da inseguire).":
        "Zmadhimi u shtua (i palëvizshëm: në kuadrin e ngrirë nuk ka asgjë për të ndjekur).",
    "Insegui": "Ndiq",
    "Keyframe": "Kuadër kyç",
    "Porta il cursore dentro l'effetto.": "Çojeni kursorin brenda efektit.",
    "Nessun keyframe al cursore: usa Prec. / Succ. per andarci.":
        "Asnjë kuadër kyç te kursori: përdorni Para. / Pas. për të shkuar te njëri.",
    "Il primo punto del percorso non si cancella: e' la partenza della figura.":
        "Pika e parë e shtegut nuk fshihet: është nisja e figurës.",
    "Seleziona prima dei punti sulla barra dell'effetto nella timeline (clic, Maiusc+clic per un intervallo, Ctrl+clic per aggiungerne).":
        "Zgjidhni fillimisht disa pika në shiritin e efektit në vijën kohore (klik, Shift+klik për një "
        "interval, Ctrl+klik për të shtuar).",
    "Nessun altro keyframe in quella direzione.": "Asnjë kuadër tjetër kyç në atë drejtim.",
    "Inseguimento": "Ndjekja",
    "L'inseguimento funziona solo su una clip video (non su un fermo immagine): la figura resta ferma.":
        "Ndjekja funksionon vetëm në një klip video (jo në një kuadër të ngrirë): figura mbetet e palëvizshme.",
    "Testo di prova": "Tekst prove",
    "La timeline e' vuota.": "Vija kohore është bosh.",
    "Esportazione completata": "Eksportimi përfundoi",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Scarica / Aggiorna prende il build ufficiale per Windows (release essentials) da gyan.dev e tiene solo ffmpeg.exe, LICENSE e README in tools/ffmpeg/. Nessuna installazione, nessuna modifica al PATH.":
        "ffmpeg nuk përfshihet në program: është një program i veçantë me licencën e vet. Shkarko / Përditëso "
        "merr versionin zyrtar për Windows (release essentials) nga gyan.dev dhe mban vetëm ffmpeg.exe, "
        "LICENSE dhe README në tools/ffmpeg/. Pa instalim, pa ndryshime në PATH.",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Su Linux e macOS si installa con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) oppure si mette un eseguibile ffmpeg in tools/ffmpeg/. Il download automatico vale solo per Windows.":
        "ffmpeg nuk përfshihet në program: është një program i veçantë me licencën e vet. Në Linux dhe macOS instalohet me menaxherin e paketave të sistemit (për shembull sudo apt install ffmpeg) ose vendoset një skedar ekzekutues ffmpeg në tools/ffmpeg/. Shkarkimi automatik vlen vetëm për Windows.",
    "Scarica / Aggiorna": "Shkarko / Përditëso",
    "Apri cartella tools": "Hap dosjen tools",
    "VitTrack e' un modello addestrato per seguire oggetti e persone: ritrova il soggetto dopo un palo o un passante e capisce quando e' perso. Viene dal repository ufficiale opencv_zoo (licenza Apache 2.0, compatibile con la GPL 3), circa 0,7 MB, in tools/vittrack/ con la sua licenza. Senza, l'inseguimento usa il confronto a modello.":
        "VitTrack është një model i trajnuar për të ndjekur objekte dhe persona: e rigjen subjektin pas një "
        "shtylle ose një kalimtari dhe e kupton kur është humbur. Vjen nga depoja zyrtare opencv_zoo (licenca "
        "Apache 2.0, e përputhshme me GPL 3), rreth 0,7 MB, në tools/vittrack/ me licencën e vet. Pa të, "
        "ndjekja përdor krahasimin me model.",
    "Scarica": "Shkarko",
    "Qualita' video (CRF, 15 = ottima, 28 = leggera)": "Cilësia e videos (CRF, 15 = shumë e mirë, 28 = e lehtë)",
    "Velocita' di codifica (preset x264)": "Shpejtësia e kodimit (preset x264)",
    "Audio (kbit/s)": "Audio (kbit/s)",
    "Durate proposte (secondi)": "Kohëzgjatjet e propozuara (sekonda)",
    "Pixelatura: grandezza dei pixel e soglia dell'inseguimento (0.2-0.9)":
        "Pikselimi: madhësia e pikselëve dhe pragu i ndjekjes (0.2-0.9)",
    "Salva impostazioni": "Ruaj cilësimet",
    "Carica immagine del logo...": "Ngarko imazhin e logos...",
    "Togli logo": "Hiq logon",
    "Testo dell'operatore (nome, qualifica, data...)": "Teksti i operatorit (emri, titulli, data...)",
    "Il pulsante Logo (tasto L) mette logo e testo nell'angolo scelto, fermi per tutto il video (o solo nella porzione IN-OUT, se e' segnata). Nel progetto si possono poi spostare, ridimensionare e cambiare dal pannello a destra.":
        "Butoni Logo (tasti L) vendos logon dhe tekstin në qoshen e zgjedhur, të palëvizshëm për gjithë "
        "videon (ose vetëm në pjesën IN-OUT, nëse është shënuar). Në projekt mund të lëvizen, t'u "
        "ndryshohen përmasat dhe të ndryshohen nga paneli djathtas.",
    "Proposti ai nuovi effetti, in % del lato corto (0 = angoli vivi, 50 = estremita' tonde); ogni effetto poi si regola nel suo pannello":
        "Propozohen për efektet e reja, në % të anës së shkurtër (0 = qoshe të mprehta, 50 = skaje të "
        "rrumbullakëta); çdo efekt pastaj rregullohet në panelin e vet",
    "nessun logo": "asnjë logo",
    "La lingua dell'interfaccia cambia subito, senza riavviare.":
        "Gjuha e ndërfaqes ndryshon menjëherë, pa rinisje.",
    "Valore non valido": "Vlerë e pavlefshme",
    "Controlla i numeri inseriti.": "Kontrolloni numrat e futur.",
    "ffmpeg scaricato in tools/ffmpeg.": "ffmpeg u shkarkua në tools/ffmpeg.",
    "VitTrack non scaricato: l'inseguimento usa il confronto a modello, che puo' perdere il soggetto dietro un ostacolo.":
        "VitTrack nuk është shkarkuar: ndjekja përdor krahasimin me model, i cili mund ta humbasë subjektin "
        "pas një pengese.",
    "Modello scaricato in tools/vittrack: l'inseguimento ora lo usa.":
        "Modeli u shkarkua në tools/vittrack: ndjekja tani e përdor.",
    "Cartella": "Dosja",
    "Progetto aperto: {file}": "Projekti u hap: {file}",
    "Salvataggio": "Ruajtja",
    "Progetto salvato: {path}": "Projekti u ruajt: {path}",
    "In coda": "Në fund",
    "Al cursore": "Te kursori",
    "Traccia audio aggiunta: {name} ({duration})": "Gjurma audio u shtua: {name} ({duration})",
    "Clip tagliata a {time}.": "Klipi u pre në {time}.",
    "Audio originale tolto fra {start} e {end} (il video resta).":
        "Audioja origjinale u hoq midis {start} dhe {end} (videoja mbetet).",
    "Slide di apertura aggiunta all'inizio: regolala nel pannello a destra.":
        "Slajdi i hapjes u shtua në fillim: rregullojeni në panelin djathtas.",
    "Fermo immagine di {seconds:g} s inserito.": "U fut një kuadër i ngrirë prej {seconds:g} s.",
    "Segna prima la porzione con IN e OUT (tasti I e O), oppure seleziona una clip.":
        "Shënoni fillimisht pjesën me IN dhe OUT (tastet I dhe O), ose zgjidhni një klip.",
    "Mostra l'icona dell'orologio con le lancette e la velocita' sotto":
        "Shfaq ikonën e orës me akrepa dhe shpejtësinë poshtë",
    "Velocita' {speed} applicata fra {start} e {end}.": "Shpejtësia {speed} u zbatua midis {start} dhe {end}.",
    "{effect} aggiunto: regola i valori nel pannello a destra o trascina sull'anteprima.":
        "{effect} u shtua: rregulloni vlerat në panelin djathtas ose zvarritni mbi parapamje.",
    "Fino all'istante (secondi della timeline)": "Deri në çastin (sekondat e vijës kohore)",
    "Grandezza dei pixel": "Madhësia e pikselëve",
    "Keyframe a {time}: trascina la figura per correggerla.":
        "Kuadër kyç në {time}: zvarritni figurën për ta korrigjuar.",
    "Inseguimento annullato.": "Ndjekja u anulua.",
    "Inseguimento completato: {frames} fotogrammi, {points} punti":
        "Ndjekja përfundoi: {frames} kuadro, {points} pika",
    "Esportazione annullata.": "Eksportimi u anulua.",
    "Esportazione fallita": "Eksportimi dështoi",
    "Esportazione fallita.": "Eksportimi dështoi.",
    "Apri cartella": "Hap dosjen",
    "Chiudi": "Mbyll",
    "PAGINE": "FAQET",
    "Inizio (Home)": "Fillimi (Home)",
    "Fotogramma precedente (Sinistra)": "Kuadri i mëparshëm (←)",
    "Fotogramma successivo (Destra)": "Kuadri tjetër (→)",
    "Fine (Fine)": "Fundi (End)",
    "Adatta la timeline": "Përshtat vijën kohore",
    "Ingrandisci la timeline (Ctrl+rotellina). Per spostarla: Alt+trascina, tasto centrale o rotellina":
        "Zmadho vijën kohore (Ctrl+rrotull). Për ta lëvizur: Alt+zvarritje, butoni i mesëm ose rrotulla",
    "Riduci la timeline": "Zvogëlo vijën kohore",
    "Configurazione": "Konfigurimi",
    "fermo immagine": "kuadër i ngrirë",
    "effetti": "efektet",
    "angolo": "qoshja",
    "disposizione": "vendosja",
    "colore testo": "ngjyra e tekstit",
    "sfondo sotto logo e scritta": "sfondi nën logon dhe shkrimin",
    "colore": "ngjyra",
    "Nessun logo: carica un'immagine (PNG con trasparenza, JPG...).":
        "Asnjë logo: ngarkoni një imazh (PNG me tejdukshmëri, JPG...).",
    "Immagini": "Imazhe",
    "ffmpeg NON trovato: scaricalo con il pulsante qui sotto.":
        "ffmpeg NUK u gjet: shkarkojeni me butonin më poshtë.",
    "{label}: {done:.1f} MB / {total:.1f} MB": "{label}: {done:.1f} MB / {total:.1f} MB",
    "{label}: {done:.1f} MB": "{label}: {done:.1f} MB",
    "Download fallito": "Shkarkimi dështoi",
    "{label}: {done:.2f} MB / {total:.2f} MB": "{label}: {done:.2f} MB / {total:.2f} MB",
    "{label}: {done:.2f} MB": "{label}: {done:.2f} MB",
    "Spazio riproduci  ·  ← → fotogramma  ·  I / O segna  ·  S taglia  ·  Canc elimina  ·  Ctrl+Z annulla  ·  Esc annulla disegno":
        "Hapësirë luaj  ·  ← → kuadër  ·  I / O shëno  ·  S prit  ·  Delete fshi  ·  Ctrl+Z zhbëj  ·  "
        "Esc anulo vizatimin",
    "Fotogramma non leggibile: {file}": "Kuadër i palexueshëm: {file}",
    "Questi file non si trovano piu':\n\n{files}": "Këta skedarë nuk gjenden më:\n\n{files}",
    "Video": "Video",
    "{file}\n\nAggiungerlo in coda alla timeline oppure inserirlo al cursore ({time})?":
        "{file}\n\nTa shtoj në fund të vijës kohore apo ta fut te kursori ({time})?",
    "Eliminata la porzione {start} - {end}.": "U fshi pjesa {start} - {end}.",
    "Audio originale spento (il video resta): riaccendilo dal pannello o con Ctrl+Z.":
        "Audioja origjinale u fik (videoja mbetet): rindizeni nga paneli ose me Ctrl+Z.",
    "Porzione {start} - {end}. Da 2x in su accelera, 0.5x e 0.25x rallentano (la porzione dura il doppio o il quadruplo); con 1x si torna alla velocita' normale.":
        "Pjesa {start} - {end}. Nga 2x e lart përshpejton, 0.5x dhe 0.25x ngadalësojnë (pjesa zgjat dyfish "
        "ose katërfish); me 1x kthehet në shpejtësinë normale.",
    "Disegna: {effect}  (Esc annulla)": "Vizato: {effect}  (Esc anulo)",
    "Logo e operatore aggiunti fra {start} e {end}: trascinali sull'anteprima o regolali nel pannello.":
        "Logoja dhe operatori u shtuan midis {start} dhe {end}: zvarritini mbi parapamje ose rregullojini "
        "në panel.",
    "Keyframe a {time}.": "Kuadër kyç në {time}.",
    "; soggetto uscito dall'inquadratura: l'effetto finisce a {time}":
        "; subjekti doli nga kuadri: efekti mbaron në {time}",
    "; soggetto perso: l'effetto finisce a {time}": "; subjekti u humb: efekti mbaron në {time}",
    "Video MP4": "Video MP4",
    "Esportato {path} ({size:.1f} MB in {seconds:.0f} s).":
        "U eksportua {path} ({size:.1f} MB në {seconds:.0f} s).",
    "{path}\n\n{size:.1f} MB in {seconds:.0f} secondi.\n\nAprire la cartella?":
        "{path}\n\n{size:.1f} MB në {seconds:.0f} sekonda.\n\nTë hapet dosja?",
    "{app} {version}. Montaggio video semplice per presentazioni: timeline, tagli, fermo immagine, avanzamento veloce, sovraimpressioni, zoom e pixelatura con inseguimento; esportazione mp4 con ffmpeg. Progetti in formato JSON.":
        "{app} {version}. Montazh i thjeshtë video për prezantime: vijë kohore, prerje, kuadër i ngrirë, "
        "përshpejtim, mbivendosje, zmadhim dhe pikselim me ndjekje; eksportim mp4 me ffmpeg. Projekte në "
        "formatin JSON.",
    "{copyright}. Software libero: GNU General Public License versione 3 con termini aggiuntivi (attribuzione dell'autore, nome e logo), vedi i file LICENSE e NOTICE. Nessuna garanzia. Usa librerie e programmi di terze parti con le loro licenze (elencati in NOTICE).":
        "{copyright}. Softuer i lirë: GNU General Public License versioni 3 me kushte shtesë (atribuimi i "
        "autorit, emri dhe logoja), shihni skedarët LICENSE dhe NOTICE. Pa asnjë garanci. Përdor biblioteka "
        "dhe programe të palëve të treta me licencat e tyre (të renditura në NOTICE).",
    "cartella tools/ffmpeg": "dosja tools/ffmpeg",
    "PATH di sistema": "PATH i sistemit",
    "VitTrack presente: l'inseguimento lo usa.\n{model}": "VitTrack është i pranishëm: ndjekja e përdor.\n{model}",
    "{width}x{height}  {fps:g} fps  {clips} clip  {duration}":
        "{width}x{height}  {fps:g} fps  {clips} klipe  {duration}",
    "Anteprima: {error}": "Parapamja: {error}",
    "Audio dell'anteprima non disponibile: {error}": "Audioja e parapamjes nuk është e disponueshme: {error}",
    "Impossibile aprire il progetto:\n{error}": "Projekti nuk mund të hapet:\n{error}",
    "Slide aggiunta a {time}: regolala nel pannello a destra.":
        "Slajdi u shtua në {time}: rregullojeni në panelin djathtas.",
    "Il fotogramma a {time} resta fermo per questo tempo; cio' che segue scorre in avanti.":
        "Kuadri në {time} mbetet i ngrirë për këtë kohë; ajo që vijon zhvendoset përpara.",
    "L'inseguimento parte dal cursore ({start}) e segue il soggetto fino a questo istante (al massimo la fine della clip: {clip_end}).":
        "Ndjekja nis nga kursori ({start}) dhe e ndjek subjektin deri në këtë çast (më së shumti deri në "
        "fund të klipit: {clip_end}).",
    "File non trovato: {path}": "Skedari nuk u gjet: {path}",
    "ffmpeg trovato ({where})\n{path}\nversione {version}": "ffmpeg u gjet ({where})\n{path}\nversioni {version}",
    "Segna IN e OUT (tasti I e O) oppure seleziona un elemento da eliminare.":
        "Shënoni IN dhe OUT (tastet I dhe O) ose zgjidhni një element për ta fshirë.",
    "Fotogramma {done} / {total}": "Kuadri {done} / {total}",
    "; soggetto non trovato da {time} al keyframe": "; subjekti nuk u gjet nga {time} deri te kuadri kyç",
    ", non trovato in {frames} fotogrammi": ", nuk u gjet në {frames} kuadro",
    "formato audio inatteso": "format audio i papritur",

    # ---------------------------------------------------------------- caratteri
    "Scegli il carattere": "Zgjidh shkronjat",
    "Cerca carattere...": "Kërko shkronja...",
    "{shown} / {total}  - caricamento...": "{shown} / {total}  - po ngarkohet...",
    "Caratteri della cartella font/ e di Windows, mostrati con il testo «{sample}». Clicca per scegliere.":
        "Shkronjat e dosjes font/ dhe të Windows, të shfaqura me tekstin «{sample}». Klikoni për të zgjedhur.",

    # ---------------------------------------------------------------- ffmpeg
    "ffmpeg non trovato: scaricalo dalla pagina Configurazione.":
        "ffmpeg nuk u gjet: shkarkojeni nga faqja Konfigurimi.",
    "Durata sconosciuta (file danneggiato o non riconosciuto).":
        "Kohëzgjatje e panjohur (skedar i dëmtuar ose i panjohur).",
    "Il file non contiene ne' video ne' audio riconoscibili.":
        "Skedari nuk përmban as video as audio të njohshme.",
    "ffmpeg non ha scritto il fotogramma.": "ffmpeg nuk e shkroi kuadrin.",
    "ffmpeg: codice di uscita {code}": "ffmpeg: kodi i daljes {code}",
    "Impossibile aprire il video: {path}": "Videoja nuk mund të hapet: {path}",

    # ---------------------------------------------------------------- opzioni
    "Testo a destra del logo": "Teksti djathtas logos",
    "Testo a sinistra del logo": "Teksti majtas logos",
    "Testo sotto il logo": "Teksti nën logon",
    "Riempi (taglia i bordi)": "Mbush (pret skajet)",
    "Intera (bande del colore)": "E plotë (shirita me ngjyrë)",
    "Stira": "Shtrij",
    "Al centro": "Në qendër",
    "Sinistra": "Majtas",
    "Centro": "Qendër",
    "Destra": "Djathtas",

    # ---------------------------------------------------------------- pannello proprieta'
    "Nessun elemento selezionato.\n\nClicca una clip, un effetto o una traccia audio nella timeline per vederne le proprieta'.\n\nFlusso di lavoro:\n1. Importa un video (Ctrl+I)\n2. Segna IN e OUT (tasti I e O) e taglia o elimina\n3. Aggiungi fermo immagine, velocita', testi, frecce, riquadri, zoom, pixelatura\n4. Esporta in mp4 (Ctrl+E)":
        "Asnjë element i zgjedhur.\n\nKlikoni një klip, një efekt ose një gjurmë audio në vijën kohore për "
        "të parë vetitë e tij.\n\nRrjedha e punës:\n1. Importoni një video (Ctrl+I)\n2. Shënoni IN dhe OUT "
        "(tastet I dhe O) dhe pritni ose fshini\n3. Shtoni kuadër të ngrirë, shpejtësi, tekste, shigjeta, "
        "korniza, zmadhim, pikselim\n4. Eksportoni në mp4 (Ctrl+E)",
    "Proprieta'": "Vetitë",
    "File": "Skedari",
    "Durata": "Kohëzgjatja",
    "Posizione": "Pozicioni",
    "Elimina clip": "Fshi klipin",
    "Transizioni": "Kalimet",
    "Dal nero (s)": "Nga e zeza (s)",
    "Al nero (s)": "Në të zezë (s)",
    "Durata (s)": "Kohëzgjatja (s)",
    "Colore sfondo": "Ngjyra e sfondit",
    "nessuna": "asnjë",
    "Elimina slide": "Fshi slajdin",
    "Tempo": "Koha",
    "Inizio (s)": "Fillimi (s)",
    "Fine (s)": "Fundi (s)",
    "Elimina effetto": "Fshi efektin",
    "Stato": "Gjendja",
    "Keyframe qui (fissa la posizione)": "Kuadër kyç këtu (fikson pozicionin)",
    "Audio originale attivo": "Audioja origjinale aktive",
    "Volume": "Volumi",
    "Dissolvenze": "Shuarjet",
    "All'inizio (s)": "Në fillim (s)",
    "Alla fine (s)": "Në fund (s)",
    "Elimina l'audio originale": "Fshi audion origjinale",
    "Pezzo": "Pjesa",
    "Audio di questo pezzo": "Audioja e kësaj pjese",
    "Volume di questo pezzo": "Volumi i kësaj pjese",
    "Entrata (s)": "Hyrja (s)",
    "Uscita (s)": "Dalja (s)",
    "Elimina audio di questo pezzo": "Fshi audion e kësaj pjese",
    "Nome": "Emri",
    "Porzione del file": "Pjesa e skedarit",
    "Dall'istante (s)": "Nga çasti (s)",
    "All'istante (s)": "Deri në çastin (s)",
    "Muta": "Pa zë",
    "Elimina traccia": "Fshi gjurmën",
    "video": "video",
    "Istante sorgente (s)": "Çasti në burim (s)",
    "Taglio nel video sorgente": "Prerja në videon burim",
    "Audio originale di questa clip": "Audioja origjinale e këtij klipi",
    "Volume audio originale (tutto il progetto)": "Volumi i audios origjinale (gjithë projekti)",
    "Velocita' (sotto 1x rallenta)": "Shpejtësia (nën 1x ngadalëson)",
    "Mostra orologio con la velocita'": "Shfaq orën me shpejtësinë",
    "Orologio (tutto il progetto)": "Ora (gjithë projekti)",
    "Dimensione (px)": "Madhësia (px)",
    "Colore": "Ngjyra",
    "Opacita' sfondo": "Opaciteti i sfondit",
    "Fusione con la succ. (s)": "Shkrirje me tjetrin (s)",
    "Slide di apertura": "Slajdi i hapjes",
    "Adattamento": "Përshtatja",
    "Allineamento": "Rreshtimi",
    "Ombra": "Hija",
    "Opacita' del testo": "Opaciteti i tekstit",
    "Sfondo dietro il testo": "Sfond pas tekstit",
    "Modifica testo...": "Ndrysho tekstin...",
    "fermo": "i palëvizshëm",
    "Ripeti inseguimento dal cursore": "Përsërit ndjekjen nga kursori",
    "Segui il soggetto": "Ndiq subjektin",
    "Non seguire piu'": "Mos ndiq më",
    "nessuno": "asnjë",
    "Togli keyframe al cursore": "Hiq kuadrin kyç te kursori",
    "Cancella i punti selezionati": "Fshi pikat e zgjedhura",
    "il file non ha audio": "skedari nuk ka audio",
    "= cursore": "= kursori",
    "Dal nero: la clip compare dal nero. Al nero: sparisce nel nero. Fusione: la clip sfuma nella successiva, a cavallo del taglio (la durata del video non cambia). Anche l'audio sale e scende. 0 = taglio netto.":
        "Nga e zeza: klipi shfaqet nga e zeza. Në të zezë: zhduket në të zezë. Shkrirje: klipi kalon "
        "butësisht te tjetri, rreth prerjes (kohëzgjatja e videos nuk ndryshon). Edhe audioja ngrihet dhe "
        "ulet. 0 = prerje e drejtpërdrejtë.",
    "La slide e' un fondo a tinta unita o un'immagine adattata alla misura del video. Testi e immagini si mettono sopra con gli strumenti Testo e Immagine: con il cursore sulla slide durano quanto lei.":
        "Slajdi është një sfond me ngjyrë të njëtrajtshme ose një imazh i përshtatur me përmasat e videos. "
        "Tekstet dhe imazhet vendosen sipër me mjetet Tekst dhe Imazh: me kursorin mbi slajd zgjasin sa ai.",
    "Larghezza (px)": "Gjerësia (px)",
    "Opacita'": "Opaciteti",
    "Dove l'inseguimento sbaglia: porta il cursore li' e trascina la figura sul soggetto (dagli angoli per la misura). Diventa un keyframe: il tratto prima viene corretto e l'inseguimento riparte da li' fino al keyframe successivo.\nNella timeline, sulla barra dell'effetto, i keyframe sono rombi e i punti dell'inseguimento pallini. Clic: seleziona e porta il cursore; Maiusc+clic: intervallo; Ctrl+clic: aggiunge o toglie. Canc o tasto destro: cancella i selezionati (li' la figura va dritta fra i punti rimasti).":
        "Aty ku ndjekja gabon: çojeni kursorin atje dhe zvarritni figurën mbi subjektin (nga qoshet për "
        "madhësinë). Bëhet kuadër kyç: pjesa para tij korrigjohet dhe ndjekja rinis që andej deri te kuadri "
        "kyç pasardhës.\nNë vijën kohore, në shiritin e efektit, kuadrot kyçe janë romba dhe pikat e ndjekjes "
        "rrathë të vegjël. Klik: zgjedh dhe çon kursorin; Shift+klik: interval; Ctrl+klik: shton ose heq. "
        "Delete ose butoni i djathtë: fshin të zgjedhurat (atje figura shkon drejt midis pikave të mbetura).",
    "< Prec.": "< Para.",
    "Succ. >": "Pas. >",
    "Centra orizz.": "Qendërzo horiz.",
    "Centra vert.": "Qendërzo vert.",
    "Valgono per l'audio originale di tutto il video: sale all'inizio e scende alla fine. Canc spegne tutto l'audio originale (il video resta). Per un solo pezzo clicca la sua barra nella riga dell'audio.":
        "Vlejnë për audion origjinale të gjithë videos: ngrihet në fillim dhe ulet në fund. Delete fik gjithë "
        "audion origjinale (videoja mbetet). Për një pjesë të vetme klikoni shiritin e saj në rreshtin e audios.",
    "Per togliere solo un tratto d'audio: segna IN e OUT (tasti I e O) e premi Canc con l'audio selezionato: il video resta. Oppure taglia con S e seleziona il pezzo d'audio: Canc lo elimina, qui ne regoli volume e dissolvenze.":
        "Për të hequr vetëm një pjesë audioje: shënoni IN dhe OUT (tastet I dhe O) dhe shtypni Delete me "
        "audion të zgjedhur: videoja mbetet. Ose pritni me S dhe zgjidhni pjesën e audios: Delete e fshin, "
        "këtu rregulloni volumin dhe shuarjet e saj.",
    "Il volume sale da zero all'inizio della traccia e scende a zero alla fine.":
        "Volumi ngrihet nga zero në fillim të gjurmës dhe ulet në zero në fund.",
    "slide": "slajd",
    "Clip: {kind}": "Klip: {kind}",
    "Traccia audio": "Gjurmë audio",
    "Slide di chiusura": "Slajdi i mbylljes",
    "Togli": "Hiq",
    "Sull'anteprima: trascina per spostare, dagli angoli per ingrandire, doppio clic per riscriverlo.":
        "Në parapamje: zvarritni për ta lëvizur, nga qoshet për ta zmadhuar, klik i dyfishtë për ta rishkruar.",
    "Largh.": "Gjer.",
    "  Alt.": "  Lart.",
    "Spessore bordo": "Trashësia e skajit",
    "Riempimento": "Mbushja",
    "Opacita' riempimento": "Opaciteti i mbushjes",
    "Il contenuto della figura fa da modello: la figura segue il soggetto nei fotogrammi successivi; quando esce dall'inquadratura l'effetto finisce.":
        "Përmbajtja e figurës shërben si model: figura ndjek subjektin në kuadrot pasardhëse; kur ai del nga "
        "kuadri, efekti mbaron.",
    "segue il soggetto ({points} punti)": "ndjek subjektin ({points} pika)",
    "Effetto: {name}": "Efekti: {name}",
    "Audio originale (un pezzo)": "Audioja origjinale (një pjesë)",
    "Carattere": "Shkronjat",
    "Sull'anteprima: trascina per spostarla, dagli angoli per ridimensionarla (le proporzioni restano quelle dell'immagine).":
        "Në parapamje: zvarritni për ta lëvizur, nga qoshet për t'i ndryshuar përmasat (proporcionet mbeten "
        "ato të imazhit).",
    "Coda X": "Bishti X",
    "Punta X": "Maja X",
    "Spessore": "Trashësia",
    "Audio originale (tutto)": "Audioja origjinale (e gjitha)",
    "Area da ingrandire": "Zona për t'u zmadhuar",
    "Forma": "Forma",
    "Angoli (rettangolare)": "Qoshet (drejtkëndor)",
    "Contorno colorato sull'area ingrandita": "Kontur me ngjyrë rreth zonës së zmadhuar",
    "Linea fra l'area e il riquadro": "Vijë midis zonës dhe kornizës",
    "Riquadro ingrandito": "Korniza e zmadhuar",
    "L'area fa da modello: lo zoom segue l'oggetto nei fotogrammi successivi, il riquadro ingrandito resta dove l'hai messo. Se l'oggetto esce dall'inquadratura lo zoom finisce.":
        "Zona shërben si model: zmadhimi ndjek objektin në kuadrot pasardhëse, korniza e zmadhuar mbetet aty "
        "ku e keni vendosur. Nëse objekti del nga kuadri, zmadhimi mbaron.",
    "Rettangolare": "Drejtkëndor",
    "Ingrandimento": "Zmadhimi",
    "Larghezza": "Gjerësia",
    "Per tutto il video": "Për gjithë videon",
    "Largh. logo (px)": "Gjer. logos (px)",
    "Dimensione testo": "Madhësia e tekstit",
    "Colore testo": "Ngjyra e tekstit",
    "Disposizione": "Vendosja",
    "Ombra sotto il testo": "Hije nën tekst",
    "Sfondo": "Sfondi",
    "Sfondo sotto logo e scritta": "Sfond nën logon dhe shkrimin",
    "Opacita' di tutto": "Opaciteti i së tërës",
    "Angolo": "Qoshja",
    "Il colore vale per il bordo del riquadro, il contorno dell'area e la linea. L'area scelta viene mostrata ingrandita nel riquadro, sopra il video, per la durata dell'effetto. Sull'anteprima: trascina l'area o il riquadro, ridimensiona l'area dagli angoli.":
        "Ngjyra vlen për skajin e kornizës, konturin e zonës dhe vijën. Zona e zgjedhur shfaqet e zmadhuar "
        "në kornizë, mbi videon, për kohëzgjatjen e efektit. Në parapamje: zvarritni zonën ose kornizën, "
        "ndryshoni përmasat e zonës nga qoshet.",
    "Pixelatura": "Pikselimi",
    "Grandezza pixel": "Madhësia e pikselëve",
    "Resta fermo nel punto scelto. Sull'anteprima trascinalo per spostarlo, tira un angolo per ingrandire o rimpicciolire logo e testo insieme. I valori proposti per i prossimi si cambiano in Configurazione.":
        "Mbetet i palëvizshëm në pikën e zgjedhur. Në parapamje zvarriteni për ta lëvizur, tërhiqni një qoshe "
        "për të zmadhuar ose zvogëluar logon dhe tekstin bashkë. Vlerat e propozuara për të ardhshmit "
        "ndryshohen te Konfigurimi.",
    "fisso": "i palëvizshëm",
    "Soggetto perso": "Subjekti u humb",
    "Ripeti l'inseguimento dopo aver cambiato inizio o fine.":
        "Përsëritni ndjekjen pasi të keni ndryshuar fillimin ose fundin.",
    "{points} punti": "{points} pika",
    "{frames} fotogrammi": "{frames} kuadro",

    # ---------------------------------------------------------------- anteprima
    "Trascina sull'anteprima per disegnare il riquadro": "Zvarritni mbi parapamje për të vizatuar kornizën",
    "Trascina sull'anteprima per disegnare l'ovale": "Zvarritni mbi parapamje për të vizatuar ovalin",
    "Trascina sull'anteprima un rettangolo sull'oggetto da ingrandire":
        "Zvarritni mbi parapamje një drejtkëndësh mbi objektin që do të zmadhohet",
    "Clicca dove far apparire il riquadro ingrandito  -  {factor}x  (rotellina o tasti 2, 3, 4, 6, 8)":
        "Klikoni ku të shfaqet korniza e zmadhuar  -  {factor}x  (rrotulla ose tastet 2, 3, 4, 6, 8)",
    "Clicca sull'anteprima dove mettere il tempo trascorso": "Klikoni mbi parapamje ku të vendoset koha e kaluar",
    "Trascina sull'anteprima l'area da pixelare: verra' inseguita nei fotogrammi successivi":
        "Zvarritni mbi parapamje zonën që do të pikselohet: do të ndiqet në kuadrot pasardhëse",
    "Trascina dalla coda alla punta della freccia": "Zvarritni nga bishti te maja e shigjetës",
    "Clicca sull'anteprima dove mettere il testo": "Klikoni mbi parapamje ku të vendoset teksti",
    "Importa un video per vedere l'anteprima": "Importoni një video për të parë parapamjen",

    # ---------------------------------------------------------------- timeline
    "segue il soggetto": "ndjek subjektin",
    "Logo e operatore": "Logoja dhe operatori",
    "Slide di apertura: {text}": "Slajdi i hapjes: {text}",
    "Slide di chiusura: {text}": "Slajdi i mbylljes: {text}",
    "Slide: {text}": "Slajd: {text}",
    "Fermo immagine ({name})": "Kuadër i ngrirë ({name})",

    # ---------------------------------------------------------------- esportazione
    "Percorso del progetto mancante": "Mungon shtegu i projektit",
    "La timeline e' vuota: importa almeno un video.": "Vija kohore është bosh: importoni të paktën një video.",
    "Preparazione dei segmenti": "Përgatitja e segmenteve",
    "Disegno delle sovraimpressioni": "Vizatimi i mbivendosjeve",
    "Preparazione": "Përgatitja",
    "Completato": "Përfundoi",
    "ffmpeg non ha scritto il file di uscita.": "ffmpeg nuk e shkroi skedarin e daljes.",
    "Disegno del contorno dello zoom": "Vizatimi i konturit të zmadhimit",
    "Disegno dell'orologio {speed}": "Vizatimi i orës {speed}",
    "Codifica: {done} / {total}": "Kodimi: {done} / {total}",
    "Audio originale": "Audioja origjinale",
    "muto": "pa zë",
    "immagine": "imazh",
    "orologio": "ora",
    "senza audio": "pa audio",
    "audio": "audio",
    "{name} ({points} punti)": "{name} ({points} pika)",
    "{name} (fisso)": "{name} (i palëvizshëm)",
    "{name} (segue)": "{name} (ndjek)",
    "audio {volume:.0f} %": "audio {volume:.0f} %",

    # ---------------------------------------------------------------- download
    "Risposta inattesa dal sito di download di ffmpeg.": "Përgjigje e papritur nga faqja e shkarkimit të ffmpeg.",
    "Il download automatico e' disponibile solo su Windows: installa ffmpeg con il gestore di pacchetti del sistema.":
        "Shkarkimi automatik është i disponueshëm vetëm në Windows: instalojeni ffmpeg me menaxherin e "
        "paketave të sistemit.",
    "licenza di VitTrack": "licenca e VitTrack",
    "Il file scaricato non e' un archivio zip valido.": "Skedari i shkarkuar nuk është një arkiv zip i vlefshëm.",
    "Estrazione di ffmpeg": "Po nxirret ffmpeg",
    "L'ffmpeg scaricato non si avvia su questo PC.": "Versioni i shkarkuar i ffmpeg nuk niset në këtë kompjuter.",
    "Il modello scaricato non corrisponde a quello atteso (impronta SHA-256 diversa).":
        "Modeli i shkarkuar nuk përputhet me atë të pritur (gjurmë SHA-256 e ndryshme).",
    "Il pacchetto scaricato non contiene {file}.": "Paketa e shkarkuar nuk përmban {file}.",
    "{file} manca dopo l'estrazione.": "{file} mungon pas nxjerrjes.",
    "Impossibile controllare l'ultima versione di ffmpeg: {error}":
        "Nuk mund të kontrollohet versioni më i fundit i ffmpeg: {error}",
    "Download di {name} fallito: {error}": "Shkarkimi i {name} dështoi: {error}",
    "Impossibile aggiornare '{folder}': file in uso. Aspetta la fine dell'esportazione e riprova.":
        "Nuk mund të përditësohet '{folder}': skedarët janë në përdorim. Prisni përfundimin e eksportimit "
        "dhe provoni përsëri.",
    "OpenCV non riesce a caricare il modello: {error}": "OpenCV nuk arrin ta ngarkojë modelin: {error}",
    "Archivio non valido: percorso sospetto '{path}'.": "Arkiv i pavlefshëm: shteg i dyshimtë '{path}'.",
    "Download di {name}": "Shkarkimi i {name}",
    "Nessun fotogramma all'istante di partenza.": "Asnjë kuadër në çastin e nisjes.",

    # ---------------------------------------------------------------- dialoghi
    "INFO": "INFO",
    "CONFERMA": "KONFIRMIM",
    "ATTENZIONE": "KUJDES",
    "ERRORE": "GABIM",
    "OK": "OK",
    "Annulla": "Anulo",
    "Si'": "Po",
    "No": "Jo",
    "Interruzione...": "Po ndërpritet...",
    "Invio va a capo, Ctrl+Invio conferma.": "Enter kalon në rresht të ri, Ctrl+Enter konfirmon.",
    "Allineamento delle righe": "Rreshtimi i rreshtave",
    "Scrivi il testo.": "Shkruani tekstin.",
    "Fondo scuro": "Sfond i errët",
    "Centra nel video": "Qendërzo në video",
    "Dimensione non valida.": "Madhësi e pavlefshme.",
    "{field}: valore fra {min:g} e {max:g}.": "{field}: vlerë midis {min:g} dhe {max:g}.",
    "{field}: inserisci un numero.": "{field}: futni një numër.",

    # ---------------------------------------------------------------- tempo trascorso
    "Tempo trascorso dall'inizio del video: clic dove metterlo, poi si sposta":
        "Koha e kaluar nga fillimi i videos: klik ku ta vendosni, pastaj mund të lëvizet",
    "Tempo trascorso aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.":
        "Koha e kaluar u shtua: zvarriteni ku të doni, rregullojeni në panelin djathtas.",
    "minuti:secondi (01:23)": "minuta:sekonda (01:23)",
    "ore:minuti:secondi (00:01:23)": "orë:minuta:sekonda (00:01:23)",
    "con i decimi (01:23.4)": "me të dhjetat (01:23.4)",
    "dall'inizio del video": "nga fillimi i videos",
    "dall'inizio dell'effetto": "nga fillimi i efektit",
    "Tempo trascorso": "Koha e kaluar",
    "Formato": "Formati",
    "Conta": "Numëro",
    "Testo davanti": "Tekst përpara",
    "Sfondo dietro il tempo": "Sfond pas kohës",
    "Sull'anteprima: trascinalo dove vuoi, dagli angoli per ingrandirlo.":
        "Në parapamje: zvarriteni ku të doni, nga qoshet për ta zmadhuar.",
    "Disegno del tempo trascorso": "Vizatimi i kohës së kaluar",

    # ------------------------------------------------------- riproduzione
    '10 fotogrammi indietro (Ctrl+Sinistra)': '10 kuadro prapa (Ctrl+←)',
    "Riproduci all'indietro / pausa (Maiusc+Spazio), senza audio": 'Luaj mbrapsht / pauzë (Shift+Hapësirë), pa zë',
    '10 fotogrammi avanti (Ctrl+Destra)': '10 kuadro përpara (Ctrl+→)',
    'Allunga fino al cursore': 'Zgjat deri te kursori',
    'Interrompi al cursore': 'Ndalo te kursori',
    '{effect} allungato fino a {t:.2f} s.': '{effect} u zgjat deri në {t:.2f} s.',
    '{effect} interrotto a {t:.2f} s.': '{effect} u ndal në {t:.2f} s.',
    "{effect} nascosto: non compare in anteprima ne' nel video esportato.": '{effect} u fsheh: nuk shfaqet as në parapamje, as në videon e eksportuar.',
    '{effect} di nuovo visibile.': '{effect} sërish i dukshëm.',
    '{zoom}% - trascina per spostarti, doppio clic centrale: adatta': "{zoom}% - tërhiqni për t'u zhvendosur, klikim i dyfishtë me butonin e mesit: përshtat",
    'Fotogrammi': 'Kuadrot',
    "Numero del fotogramma dall'inizio del video: clic dove metterlo, poi si sposta": 'Numri i kuadrit nga fillimi i videos: klikoni ku ta vendosni, pastaj zhvendoseni',
    'Numero del fotogramma aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.': 'Numri i kuadrit u shtua: tërhiqeni ku të doni, rregullojeni te paneli në të djathtë.',
    'Numero del fotogramma': 'Numri i kuadrit',
    'Primo fotogramma': 'Kuadri i parë',
    "Clicca sull'anteprima dove mettere il numero del fotogramma": 'Klikoni mbi parapamje ku të vendoset numri i kuadrit',
    'Anteprima': 'Parapamja',
    'Anteprima riattaccata.': 'Parapamja u ribashkua.',
    "Riattacca l'anteprima alla finestra principale": 'Ribashkoni parapamjen me dritaren kryesore',
    "Stacca l'anteprima in una finestra a parte (piu' spazio per la timeline)": 'Shkëputni parapamjen në një dritare më vete (më shumë hapësirë për vijën kohore)',
    'Anteprima in una finestra a parte: chiudila o usa il pulsante in alto a destra per riattaccarla.': 'Parapamja në një dritare më vete: mbylleni ose përdorni butonin lart djathtas për ta ribashkuar.',
    "Trascina un rettangolo attorno al soggetto: la freccia lo seguira' tenendo la punta dov'e'.": 'Tërhiqni një drejtkëndësh rreth subjektit: shigjeta do ta ndjekë duke e mbajtur majën aty ku është.',
    'soggetto della freccia': 'subjekti i shigjetës',
    "Si disegna un rettangolo attorno al soggetto: la freccia lo segue nei fotogrammi successivi tenendo la punta su di lui; quando esce dall'inquadratura l'effetto finisce.": 'Vizatohet një drejtkëndësh rreth subjektit: shigjeta e ndjek në kuadrot pasuese duke mbajtur majën mbi të; kur del nga kuadri, efekti mbaron.',
    'Scegli un altro soggetto': 'Zgjidhni një subjekt tjetër',
    'Trascina un rettangolo attorno al soggetto che la freccia deve seguire': 'Tërhiqni një drejtkëndësh rreth subjektit që duhet të ndjekë shigjeta',
}
