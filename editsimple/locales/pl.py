# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Polski: traduzione dei testi dell'interfaccia di EditSimple.

La chiave e' il testo italiano cosi' come compare nel codice (in tr() e N_()),
il valore la sua traduzione. I segnaposto tra graffe vanno lasciati identici.
Dopo ogni modifica:

    .venv\\Scripts\\python.exe scripts\\check_i18n.py pl
"""

from __future__ import annotations

NAME = "Polski"

CATALOG: dict[str, str] = {
    "Impossibile avviare l'interfaccia: {error}\n\nInstalla le dipendenze con:\n    {command}":
        "Nie można uruchomić interfejsu: {error}\n\nZainstaluj zależności poleceniem:\n    {command}",
    "In alto a sinistra": "U góry po lewej",
    "In alto a destra": "U góry po prawej",
    "In basso a sinistra": "Na dole po lewej",
    "In basso a destra": "Na dole po prawej",
    "Progetto EditSimple": "Projekt EditSimple",
    "Tutti i file": "Wszystkie pliki",
    "Apertura (all'inizio)": "Otwarcie (na początku)",
    "Chiusura (alla fine)": "Zamknięcie (na końcu)",
    "Apri progetto... (Ctrl+O)": "Otwórz projekt... (Ctrl+O)",
    "Progetto": "Projekt",
    "Nuovo": "Nowy",
    "Nuovo progetto (Ctrl+N)": "Nowy projekt (Ctrl+N)",
    "Apri": "Otwórz",
    "Apri progetto (Ctrl+O)": "Otwórz projekt (Ctrl+O)",
    "Salva": "Zapisz",
    "Salva progetto (Ctrl+S)": "Zapisz projekt (Ctrl+S)",
    "Annulla (Ctrl+Z)": "Cofnij (Ctrl+Z)",
    "Ripeti (Ctrl+Y)": "Ponów (Ctrl+Y)",
    "Clip": "Klip",
    "Importa video": "Importuj wideo",
    "Importa un video in coda o al cursore (Ctrl+I)": "Importuje wideo na końcu lub na kursorze (Ctrl+I)",
    "Audio": "Audio",
    "Aggiungi una traccia audio (commento, musica) al cursore":
        "Dodaje ścieżkę audio (komentarz, muzyka) na kursorze",
    "Taglia": "Tnij",
    "Taglia la clip al cursore (S)": "Tnie klip na kursorze (S)",
    "Elimina": "Usuń",
    "Elimina la porzione IN-OUT o l'elemento selezionato (Canc)":
        "Usuwa fragment IN-OUT lub zaznaczony element (Delete)",
    "Fermo": "Stop",
    "Fermo immagine del fotogramma al cursore (F)": "Stopklatka z klatki na kursorze (F)",
    "Slide": "Slajd",
    "Inserisci una slide": "Wstawia slajd",
    "Velocita'": "Prędkość",
    "Velocita' della porzione IN-OUT: piu' veloce o rallentata (V)":
        "Prędkość fragmentu IN-OUT: przyspieszony lub zwolniony (V)",
    "Sovraimpressioni": "Nakładki",
    "Testo": "Tekst",
    "Testo (T)": "Tekst (T)",
    "Immagine": "Obraz",
    "Immagine sopra il video, da spostare e ridimensionare":
        "Obraz nad wideo, do przesuwania i zmiany rozmiaru",
    "Logo": "Logo",
    "Logo e testo dell'operatore, fermi in un angolo (L)": "Logo i tekst operatora, nieruchome w rogu (L)",
    "Riquadro": "Ramka",
    "Riquadro (R): puo' seguire il soggetto": "Ramka (R): może śledzić obiekt",
    "Ovale": "Owal",
    "Ovale (E): puo' seguire il soggetto": "Owal (E): może śledzić obiekt",
    "Freccia": "Strzałka",
    "Freccia (A): puo' seguire il soggetto": "Strzałka (A): może śledzić obiekt",
    "Zoom": "Zoom",
    "Zoom rettangolare: l'area scelta in un riquadro ingrandito (Z)":
        "Zoom prostokątny: wybrany obszar w powiększonej ramce (Z)",
    "Zoom ovale: l'area scelta in un ovale ingrandito (Maiusc+Z)":
        "Zoom owalny: wybrany obszar w powiększonym owalu (Shift+Z)",
    "Pixel": "Piksele",
    "Pixelatura rettangolare che insegue il soggetto (P)": "Prostokątna pikselizacja śledząca obiekt (P)",
    "Pixelatura ovale che insegue il soggetto (K)": "Owalna pikselizacja śledząca obiekt (K)",
    "Uscita": "Wyjście",
    "Esporta MP4": "Eksportuj MP4",
    "Esporta il video finale (Ctrl+E)": "Eksportuje gotowe wideo (Ctrl+E)",
    "Inseguimento (VitTrack)": "Śledzenie (VitTrack)",
    "Esportazione": "Eksport",
    "Logo e testo dell'operatore": "Logo i tekst operatora",
    "Angoli arrotondati": "Zaokrąglone rogi",
    "Crediti": "Autorzy",
    "Lingua": "Język",
    "Impostazioni salvate.": "Ustawienia zapisane.",
    "Download di ffmpeg": "Pobieranie ffmpeg",
    "Download di VitTrack": "Pobieranie VitTrack",
    "Progetto non salvato": "Projekt niezapisany",
    "Salvare le modifiche al progetto?": "Zapisać zmiany w projekcie?",
    "Nuovo progetto.": "Nowy projekt.",
    "Lettura del video...": "Wczytywanie wideo...",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}":
        "Zaimportowano {file}: {width}x{height}, {fps:g} fps, {duration}",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}, senza audio":
        "Zaimportowano {file}: {width}x{height}, {fps:g} fps, {duration}, bez audio",
    "Audio di questo pezzo eliminato (il video resta). Ctrl+Z per riaverlo.":
        "Usunięto audio tego fragmentu (wideo zostaje). Ctrl+Z, aby je przywrócić.",
    "Clip eliminata.": "Klip usunięty.",
    "Fermo immagine": "Stopklatka",
    "Nuovo testo": "Nowy tekst",
    "Testo aggiunto: trascinalo, ingrandiscilo dagli angoli, doppio clic per riscriverlo.":
        "Dodano tekst: przeciągnij go, powiększ za rogi, dwuklik, aby go zmienić.",
    "Modifica testo": "Edytuj tekst",
    "Immagine aggiunta: trascinala per spostarla, dagli angoli per ridimensionarla.":
        "Dodano obraz: przeciągnij, aby go przesunąć, za rogi, aby zmienić rozmiar.",
    "Pixelatura con inseguimento": "Pikselizacja ze śledzeniem",
    "Cancellati {count} punti del percorso (il primo resta: e' la partenza della figura).":
        "Usunięto punkty ścieżki: {count} (pierwszy zostaje: to start figury).",
    "Cancellati {count} punti del percorso.": "Usunięto punkty ścieżki: {count}.",
    "Inseguimento del soggetto": "Śledzenie obiektu",
    "Esportazione in corso": "Trwa eksport",
    "montaggio video per presentazioni": "montaż wideo do prezentacji",
    "PROGETTO": "PROJEKT",
    "nuovo": "nowy",
    "Nessun video": "Brak wideo",
    "Montaggio": "Montaż",
    "Configura": "Konfiguruj",
    "Riproduci / pausa (Spazio)": "Odtwórz / pauza (Spacja)",
    "larghezza logo % del video": "szerokość logo % wideo",
    "altezza testo % del lato corto": "wysokość tekstu % krótszego boku",
    "distanza dai bordi % del lato corto": "odstęp od krawędzi % krótszego boku",
    "opacita' %": "krycie %",
    "angoli arrotondati %": "zaokrąglone rogi %",
    "sfondo del testo": "tło tekstu",
    "riquadro": "ramka",
    "zoom rettangolare": "zoom prostokątny",
    "pixel rettangolare": "piksele prostokątne",
    "Colore del testo": "Kolor tekstu",
    "Colore dello sfondo": "Kolor tła",
    "Immagine del logo": "Obraz logo",
    "Questa immagine non si apre.": "Nie można otworzyć tego obrazu.",
    "Controllo in corso...": "Sprawdzanie...",
    "Pronto.": "Gotowe.",
    "ffmpeg non e' stato trovato. Scaricalo dal riquadro FFmpeg della pagina Configurazione: senza, non si possono importare ne' esportare video.":
        "Nie znaleziono ffmpeg. Pobierz go z panelu FFmpeg na stronie Konfiguracja: bez niego nie można "
        "importować ani eksportować wideo.",
    "ffmpeg non e' stato trovato. Installalo con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) o copia un eseguibile ffmpeg in tools/ffmpeg/: senza, non si possono importare ne' esportare video.":
        "Nie znaleziono ffmpeg. Zainstaluj go menedżerem pakietów systemu (na przykład sudo apt install ffmpeg) albo skopiuj plik wykonywalny ffmpeg do tools/ffmpeg/: bez niego nie można importować ani eksportować wideo.",
    "Non salvare": "Nie zapisuj",
    "Niente da annullare.": "Nie ma czego cofnąć.",
    "inizio": "początek",
    "fine": "koniec",
    "Apri progetto": "Otwórz projekt",
    "File mancanti": "Brakujące pliki",
    "Salva progetto": "Zapisz projekt",
    "Dove inserire il video?": "Gdzie wstawić wideo?",
    "Importazione": "Import",
    "Il file non contiene video. Per l'audio usa il pulsante Audio.":
        "Plik nie zawiera wideo. Do audio użyj przycisku Audio.",
    "Importa prima un video.": "Najpierw zaimportuj wideo.",
    "Aggiungi traccia audio": "Dodaj ścieżkę audio",
    "Il file non contiene audio.": "Plik nie zawiera audio.",
    "Il cursore e' gia' su un confine fra clip.": "Kursor jest już na granicy między klipami.",
    "Importa prima un video: la slide prende la sua misura.":
        "Najpierw zaimportuj wideo: slajd przyjmie jego rozmiar.",
    "Al cursore ({time})": "Na kursorze ({time})",
    "Dove": "Gdzie",
    "Durata (secondi)": "Czas trwania (sekundy)",
    "Crea": "Utwórz",
    "La slide e' un fondo a tinta unita (il colore si sceglie nel pannello). Testi e immagini si aggiungono sopra con gli strumenti Testo e Immagine.":
        "Slajd to jednolite tło (kolor wybiera się w panelu). Teksty i obrazy dodaje się na nim narzędziami "
        "Tekst i Obraz.",
    "Slide di chiusura aggiunta alla fine: regolala nel pannello a destra.":
        "Dodano slajd zamykający na końcu: dostosuj go w panelu po prawej.",
    "Inserisci": "Wstaw",
    "Applica": "Zastosuj",
    "Effetti": "Efekty",
    "Pixel ovale": "Piksele owalne",
    "Pixel rettangolare": "Piksele prostokątne",
    "Zoom ovale (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Zoom owalny (prostokąt na obiekcie, potem kliknij, gdzie umieścić ramkę)",
    "Zoom (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Zoom (prostokąt na obiekcie, potem kliknij, gdzie umieścić ramkę)",
    "Carica l'immagine del logo e scrivi il testo dell'operatore nella pagina Configura, poi premi di nuovo Logo.":
        "Wczytaj obraz logo i wpisz tekst operatora na stronie Konfiguruj, potem ponownie naciśnij Logo.",
    "Logo e operatore aggiunti per tutto il video: trascinali sull'anteprima o regolali nel pannello.":
        "Dodano logo i operatora na całe wideo: przeciągnij je na podglądzie lub dostosuj w panelu.",
    "Zoom aggiunto (fermo: sul fermo immagine non c'e' nulla da inseguire).":
        "Dodano zoom (nieruchomy: na stopklatce nie ma czego śledzić).",
    "Insegui": "Śledź",
    "Keyframe": "Klatka kluczowa",
    "Porta il cursore dentro l'effetto.": "Przenieś kursor do wnętrza efektu.",
    "Nessun keyframe al cursore: usa Prec. / Succ. per andarci.":
        "Brak klatki kluczowej na kursorze: przejdź do niej przyciskami Poprz. / Nast.",
    "Il primo punto del percorso non si cancella: e' la partenza della figura.":
        "Pierwszego punktu ścieżki nie można usunąć: to start figury.",
    "Seleziona prima dei punti sulla barra dell'effetto nella timeline (clic, Maiusc+clic per un intervallo, Ctrl+clic per aggiungerne).":
        "Najpierw zaznacz punkty na pasku efektu na osi czasu (klik, Shift+klik dla zakresu, Ctrl+klik, "
        "aby dodać kolejne).",
    "Nessun altro keyframe in quella direzione.": "Brak kolejnych klatek kluczowych w tym kierunku.",
    "Inseguimento": "Śledzenie",
    "L'inseguimento funziona solo su una clip video (non su un fermo immagine): la figura resta ferma.":
        "Śledzenie działa tylko na klipie wideo (nie na stopklatce): figura pozostaje nieruchoma.",
    "Testo di prova": "Tekst próbny",
    "La timeline e' vuota.": "Oś czasu jest pusta.",
    "Esportazione completata": "Eksport zakończony",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Scarica / Aggiorna prende il build ufficiale per Windows (release essentials) da gyan.dev e tiene solo ffmpeg.exe, LICENSE e README in tools/ffmpeg/. Nessuna installazione, nessuna modifica al PATH.":
        "ffmpeg nie jest częścią programu: to osobny program na własnej licencji. Pobierz / Aktualizuj bierze "
        "oficjalną kompilację dla Windows (release essentials) z gyan.dev i zachowuje tylko ffmpeg.exe, "
        "LICENSE i README w tools/ffmpeg/. Bez instalacji, bez zmian w PATH.",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Su Linux e macOS si installa con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) oppure si mette un eseguibile ffmpeg in tools/ffmpeg/. Il download automatico vale solo per Windows.":
        "ffmpeg nie jest częścią programu: to osobny program na własnej licencji. W systemach Linux i macOS instaluje się go menedżerem pakietów systemu (na przykład sudo apt install ffmpeg) albo umieszcza plik wykonywalny ffmpeg w tools/ffmpeg/. Automatyczne pobieranie działa tylko w systemie Windows.",
    "Scarica / Aggiorna": "Pobierz / Aktualizuj",
    "Apri cartella tools": "Otwórz folder tools",
    "VitTrack e' un modello addestrato per seguire oggetti e persone: ritrova il soggetto dopo un palo o un passante e capisce quando e' perso. Viene dal repository ufficiale opencv_zoo (licenza Apache 2.0, compatibile con la GPL 3), circa 0,7 MB, in tools/vittrack/ con la sua licenza. Senza, l'inseguimento usa il confronto a modello.":
        "VitTrack to model wytrenowany do śledzenia przedmiotów i osób: odnajduje obiekt po słupie lub "
        "przechodniu i rozpoznaje, kiedy go zgubił. Pochodzi z oficjalnego repozytorium opencv_zoo (licencja "
        "Apache 2.0, zgodna z GPL 3), około 0,7 MB, w tools/vittrack/ wraz z licencją. Bez niego śledzenie "
        "używa dopasowania wzorca.",
    "Scarica": "Pobierz",
    "Qualita' video (CRF, 15 = ottima, 28 = leggera)": "Jakość wideo (CRF, 15 = bardzo dobra, 28 = lekka)",
    "Velocita' di codifica (preset x264)": "Szybkość kodowania (preset x264)",
    "Audio (kbit/s)": "Audio (kbit/s)",
    "Durate proposte (secondi)": "Proponowane czasy trwania (sekundy)",
    "Pixelatura: grandezza dei pixel e soglia dell'inseguimento (0.2-0.9)":
        "Pikselizacja: wielkość pikseli i próg śledzenia (0.2-0.9)",
    "Salva impostazioni": "Zapisz ustawienia",
    "Carica immagine del logo...": "Wczytaj obraz logo...",
    "Togli logo": "Usuń logo",
    "Testo dell'operatore (nome, qualifica, data...)": "Tekst operatora (imię, stanowisko, data...)",
    "Il pulsante Logo (tasto L) mette logo e testo nell'angolo scelto, fermi per tutto il video (o solo nella porzione IN-OUT, se e' segnata). Nel progetto si possono poi spostare, ridimensionare e cambiare dal pannello a destra.":
        "Przycisk Logo (klawisz L) umieszcza logo i tekst w wybranym rogu, nieruchomo na całe wideo (lub "
        "tylko we fragmencie IN-OUT, jeśli jest zaznaczony). W projekcie można je potem przesuwać, zmieniać "
        "ich rozmiar i ustawienia w panelu po prawej.",
    "Proposti ai nuovi effetti, in % del lato corto (0 = angoli vivi, 50 = estremita' tonde); ogni effetto poi si regola nel suo pannello":
        "Proponowane nowym efektom, w % krótszego boku (0 = ostre rogi, 50 = zaokrąglone końce); każdy efekt "
        "dostosowuje się potem w jego panelu",
    "nessun logo": "brak logo",
    "La lingua dell'interfaccia cambia subito, senza riavviare.":
        "Język interfejsu zmienia się od razu, bez ponownego uruchamiania.",
    "Valore non valido": "Nieprawidłowa wartość",
    "Controlla i numeri inseriti.": "Sprawdź wpisane liczby.",
    "ffmpeg scaricato in tools/ffmpeg.": "ffmpeg pobrano do tools/ffmpeg.",
    "VitTrack non scaricato: l'inseguimento usa il confronto a modello, che puo' perdere il soggetto dietro un ostacolo.":
        "VitTrack nie jest pobrany: śledzenie używa dopasowania wzorca, które może zgubić obiekt za przeszkodą.",
    "Modello scaricato in tools/vittrack: l'inseguimento ora lo usa.":
        "Model pobrano do tools/vittrack: śledzenie teraz go używa.",
    "Cartella": "Folder",
    "Progetto aperto: {file}": "Otwarto projekt: {file}",
    "Salvataggio": "Zapisywanie",
    "Progetto salvato: {path}": "Zapisano projekt: {path}",
    "In coda": "Na końcu",
    "Al cursore": "Na kursorze",
    "Traccia audio aggiunta: {name} ({duration})": "Dodano ścieżkę audio: {name} ({duration})",
    "Clip tagliata a {time}.": "Klip przecięty w {time}.",
    "Audio originale tolto fra {start} e {end} (il video resta).":
        "Usunięto oryginalne audio między {start} a {end} (wideo zostaje).",
    "Slide di apertura aggiunta all'inizio: regolala nel pannello a destra.":
        "Dodano slajd otwierający na początku: dostosuj go w panelu po prawej.",
    "Fermo immagine di {seconds:g} s inserito.": "Wstawiono stopklatkę {seconds:g} s.",
    "Segna prima la porzione con IN e OUT (tasti I e O), oppure seleziona una clip.":
        "Najpierw zaznacz fragment przez IN i OUT (klawisze I i O) albo zaznacz klip.",
    "Mostra l'icona dell'orologio con le lancette e la velocita' sotto":
        "Pokaż ikonę zegara ze wskazówkami i prędkością pod spodem",
    "Velocita' {speed} applicata fra {start} e {end}.": "Zastosowano prędkość {speed} między {start} a {end}.",
    "{effect} aggiunto: regola i valori nel pannello a destra o trascina sull'anteprima.":
        "Dodano {effect}: dostosuj wartości w panelu po prawej lub przeciągnij na podglądzie.",
    "Fino all'istante (secondi della timeline)": "Do chwili (sekundy osi czasu)",
    "Grandezza dei pixel": "Wielkość pikseli",
    "Keyframe a {time}: trascina la figura per correggerla.":
        "Klatka kluczowa w {time}: przeciągnij figurę, aby ją poprawić.",
    "Inseguimento annullato.": "Śledzenie anulowane.",
    "Inseguimento completato: {frames} fotogrammi, {points} punti":
        "Śledzenie zakończone: klatek {frames}, punktów {points}",
    "Esportazione annullata.": "Eksport anulowany.",
    "Esportazione fallita": "Eksport nie powiódł się",
    "Esportazione fallita.": "Eksport nie powiódł się.",
    "Apri cartella": "Otwórz folder",
    "Chiudi": "Zamknij",
    "PAGINE": "STRONY",
    "Inizio (Home)": "Początek (Home)",
    "Fotogramma precedente (Sinistra)": "Poprzednia klatka (←)",
    "Fotogramma successivo (Destra)": "Następna klatka (→)",
    "Fine (Fine)": "Koniec (End)",
    "Adatta la timeline": "Dopasuj oś czasu",
    "Ingrandisci la timeline (Ctrl+rotellina). Per spostarla: Alt+trascina, tasto centrale o rotellina":
        "Powiększ oś czasu (Ctrl+kółko). Aby ją przesunąć: Alt+przeciąganie, środkowy przycisk lub kółko",
    "Riduci la timeline": "Pomniejsz oś czasu",
    "Configurazione": "Konfiguracja",
    "fermo immagine": "stopklatka",
    "effetti": "efekty",
    "angolo": "róg",
    "disposizione": "układ",
    "colore testo": "kolor tekstu",
    "sfondo sotto logo e scritta": "tło pod logo i napisem",
    "colore": "kolor",
    "Nessun logo: carica un'immagine (PNG con trasparenza, JPG...).":
        "Brak logo: wczytaj obraz (PNG z przezroczystością, JPG...).",
    "Immagini": "Obrazy",
    "ffmpeg NON trovato: scaricalo con il pulsante qui sotto.":
        "NIE znaleziono ffmpeg: pobierz go przyciskiem poniżej.",
    "{label}: {done:.1f} MB / {total:.1f} MB": "{label}: {done:.1f} MB / {total:.1f} MB",
    "{label}: {done:.1f} MB": "{label}: {done:.1f} MB",
    "Download fallito": "Pobieranie nie powiodło się",
    "{label}: {done:.2f} MB / {total:.2f} MB": "{label}: {done:.2f} MB / {total:.2f} MB",
    "{label}: {done:.2f} MB": "{label}: {done:.2f} MB",
    "Spazio riproduci  ·  ← → fotogramma  ·  I / O segna  ·  S taglia  ·  Canc elimina  ·  Ctrl+Z annulla  ·  Esc annulla disegno":
        "Spacja odtwarzaj  ·  ← → klatka  ·  I / O zaznacz  ·  S tnij  ·  Delete usuń  ·  Ctrl+Z cofnij  ·  "
        "Esc przerwij rysowanie",
    "Fotogramma non leggibile: {file}": "Nie można odczytać klatki: {file}",
    "Questi file non si trovano piu':\n\n{files}": "Tych plików już nie ma:\n\n{files}",
    "Video": "Wideo",
    "{file}\n\nAggiungerlo in coda alla timeline oppure inserirlo al cursore ({time})?":
        "{file}\n\nDodać go na końcu osi czasu czy wstawić na kursorze ({time})?",
    "Eliminata la porzione {start} - {end}.": "Usunięto fragment {start} - {end}.",
    "Audio originale spento (il video resta): riaccendilo dal pannello o con Ctrl+Z.":
        "Oryginalne audio wyłączone (wideo zostaje): włącz je ponownie w panelu lub przez Ctrl+Z.",
    "Porzione {start} - {end}. Da 2x in su accelera, 0.5x e 0.25x rallentano (la porzione dura il doppio o il quadruplo); con 1x si torna alla velocita' normale.":
        "Fragment {start} - {end}. Od 2x w górę przyspiesza, 0.5x i 0.25x zwalniają (fragment trwa dwa lub "
        "cztery razy dłużej); 1x przywraca normalną prędkość.",
    "Disegna: {effect}  (Esc annulla)": "Rysuj: {effect}  (Esc przerywa)",
    "Logo e operatore aggiunti fra {start} e {end}: trascinali sull'anteprima o regolali nel pannello.":
        "Dodano logo i operatora między {start} a {end}: przeciągnij je na podglądzie lub dostosuj w panelu.",
    "Keyframe a {time}.": "Klatka kluczowa w {time}.",
    "; soggetto uscito dall'inquadratura: l'effetto finisce a {time}":
        "; obiekt wyszedł z kadru: efekt kończy się w {time}",
    "; soggetto perso: l'effetto finisce a {time}": "; obiekt zgubiony: efekt kończy się w {time}",
    "Video MP4": "Wideo MP4",
    "Esportato {path} ({size:.1f} MB in {seconds:.0f} s).":
        "Wyeksportowano {path} ({size:.1f} MB w {seconds:.0f} s).",
    "{path}\n\n{size:.1f} MB in {seconds:.0f} secondi.\n\nAprire la cartella?":
        "{path}\n\n{size:.1f} MB w {seconds:.0f} sekund.\n\nOtworzyć folder?",
    "{app} {version}. Montaggio video semplice per presentazioni: timeline, tagli, fermo immagine, avanzamento veloce, sovraimpressioni, zoom e pixelatura con inseguimento; esportazione mp4 con ffmpeg. Progetti in formato JSON.":
        "{app} {version}. Prosty montaż wideo do prezentacji: oś czasu, cięcia, stopklatka, przyspieszenie, "
        "nakładki, zoom i pikselizacja ze śledzeniem; eksport mp4 przez ffmpeg. Projekty w formacie JSON.",
    "{copyright}. Software libero: GNU General Public License versione 3 con termini aggiuntivi (attribuzione dell'autore, nome e logo), vedi i file LICENSE e NOTICE. Nessuna garanzia. Usa librerie e programmi di terze parti con le loro licenze (elencati in NOTICE).":
        "{copyright}. Wolne oprogramowanie: GNU General Public License wersja 3 z dodatkowymi warunkami "
        "(wskazanie autora, nazwa i logo), zobacz pliki LICENSE i NOTICE. Bez żadnej gwarancji. Używa "
        "bibliotek i programów innych firm na ich licencjach (wymienionych w NOTICE).",
    "cartella tools/ffmpeg": "folder tools/ffmpeg",
    "PATH di sistema": "systemowy PATH",
    "VitTrack presente: l'inseguimento lo usa.\n{model}": "VitTrack jest dostępny: śledzenie go używa.\n{model}",
    "{width}x{height}  {fps:g} fps  {clips} clip  {duration}":
        "{width}x{height}  {fps:g} fps  klipy: {clips}  {duration}",
    "Anteprima: {error}": "Podgląd: {error}",
    "Audio dell'anteprima non disponibile: {error}": "Audio podglądu niedostępne: {error}",
    "Impossibile aprire il progetto:\n{error}": "Nie można otworzyć projektu:\n{error}",
    "Slide aggiunta a {time}: regolala nel pannello a destra.":
        "Dodano slajd w {time}: dostosuj go w panelu po prawej.",
    "Il fotogramma a {time} resta fermo per questo tempo; cio' che segue scorre in avanti.":
        "Klatka w {time} pozostaje nieruchoma przez ten czas; to, co następuje, przesuwa się do przodu.",
    "L'inseguimento parte dal cursore ({start}) e segue il soggetto fino a questo istante (al massimo la fine della clip: {clip_end}).":
        "Śledzenie zaczyna się od kursora ({start}) i podąża za obiektem do tej chwili (najdalej do końca "
        "klipu: {clip_end}).",
    "File non trovato: {path}": "Nie znaleziono pliku: {path}",
    "ffmpeg trovato ({where})\n{path}\nversione {version}": "Znaleziono ffmpeg ({where})\n{path}\nwersja {version}",
    "Segna IN e OUT (tasti I e O) oppure seleziona un elemento da eliminare.":
        "Zaznacz IN i OUT (klawisze I i O) albo zaznacz element do usunięcia.",
    "Fotogramma {done} / {total}": "Klatka {done} / {total}",
    "; soggetto non trovato da {time} al keyframe": "; nie znaleziono obiektu od {time} do klatki kluczowej",
    ", non trovato in {frames} fotogrammi": ", nie znaleziono w klatkach: {frames}",
    "formato audio inatteso": "nieoczekiwany format audio",
    "Scegli il carattere": "Wybierz czcionkę",
    "Cerca carattere...": "Szukaj czcionki...",
    "{shown} / {total}  - caricamento...": "{shown} / {total}  - wczytywanie...",
    "Caratteri della cartella font/ e di Windows, mostrati con il testo «{sample}». Clicca per scegliere.":
        "Czcionki z folderu font/ i systemu Windows, pokazane z tekstem „{sample}”. Kliknij, aby wybrać.",
    "ffmpeg non trovato: scaricalo dalla pagina Configurazione.":
        "Nie znaleziono ffmpeg: pobierz go ze strony Konfiguracja.",
    "Durata sconosciuta (file danneggiato o non riconosciuto).":
        "Nieznany czas trwania (plik uszkodzony lub nierozpoznany).",
    "Il file non contiene ne' video ne' audio riconoscibili.":
        "Plik nie zawiera rozpoznawalnego wideo ani audio.",
    "ffmpeg non ha scritto il fotogramma.": "ffmpeg nie zapisał klatki.",
    "ffmpeg: codice di uscita {code}": "ffmpeg: kod wyjścia {code}",
    "Impossibile aprire il video: {path}": "Nie można otworzyć wideo: {path}",
    "Testo a destra del logo": "Tekst na prawo od logo",
    "Testo a sinistra del logo": "Tekst na lewo od logo",
    "Testo sotto il logo": "Tekst pod logo",
    "Riempi (taglia i bordi)": "Wypełnij (przytnij krawędzie)",
    "Intera (bande del colore)": "Całość (pasy w kolorze)",
    "Stira": "Rozciągnij",
    "Al centro": "Na środku",
    "Sinistra": "Do lewej",
    "Centro": "Do środka",
    "Destra": "Do prawej",
    "Nessun elemento selezionato.\n\nClicca una clip, un effetto o una traccia audio nella timeline per vederne le proprieta'.\n\nFlusso di lavoro:\n1. Importa un video (Ctrl+I)\n2. Segna IN e OUT (tasti I e O) e taglia o elimina\n3. Aggiungi fermo immagine, velocita', testi, frecce, riquadri, zoom, pixelatura\n4. Esporta in mp4 (Ctrl+E)":
        "Nie zaznaczono żadnego elementu.\n\nKliknij klip, efekt lub ścieżkę audio na osi czasu, aby zobaczyć "
        "jego właściwości.\n\nPrzebieg pracy:\n1. Zaimportuj wideo (Ctrl+I)\n2. Zaznacz IN i OUT (klawisze I "
        "i O) i tnij lub usuń\n3. Dodaj stopklatkę, prędkość, teksty, strzałki, ramki, zoom, pikselizację\n"
        "4. Eksportuj do mp4 (Ctrl+E)",
    "Proprieta'": "Właściwości",
    "File": "Plik",
    "Durata": "Czas trwania",
    "Posizione": "Pozycja",
    "Elimina clip": "Usuń klip",
    "Transizioni": "Przejścia",
    "Dal nero (s)": "Z czerni (s)",
    "Al nero (s)": "Do czerni (s)",
    "Durata (s)": "Czas trwania (s)",
    "Colore sfondo": "Kolor tła",
    "nessuna": "brak",
    "Elimina slide": "Usuń slajd",
    "Tempo": "Czas",
    "Inizio (s)": "Początek (s)",
    "Fine (s)": "Koniec (s)",
    "Elimina effetto": "Usuń efekt",
    "Stato": "Stan",
    "Keyframe qui (fissa la posizione)": "Klatka kluczowa tutaj (ustala pozycję)",
    "Audio originale attivo": "Oryginalne audio włączone",
    "Volume": "Głośność",
    "Dissolvenze": "Wyciszenia",
    "All'inizio (s)": "Na początku (s)",
    "Alla fine (s)": "Na końcu (s)",
    "Elimina l'audio originale": "Usuń oryginalne audio",
    "Pezzo": "Fragment",
    "Audio di questo pezzo": "Audio tego fragmentu",
    "Volume di questo pezzo": "Głośność tego fragmentu",
    "Entrata (s)": "Wejście (s)",
    "Uscita (s)": "Wyjście (s)",
    "Elimina audio di questo pezzo": "Usuń audio tego fragmentu",
    "Nome": "Nazwa",
    "Porzione del file": "Fragment pliku",
    "Dall'istante (s)": "Od chwili (s)",
    "All'istante (s)": "Do chwili (s)",
    "Muta": "Wycisz",
    "Elimina traccia": "Usuń ścieżkę",
    "video": "wideo",
    "Istante sorgente (s)": "Chwila w źródle (s)",
    "Taglio nel video sorgente": "Cięcie w wideo źródłowym",
    "Audio originale di questa clip": "Oryginalne audio tego klipu",
    "Volume audio originale (tutto il progetto)": "Głośność oryginalnego audio (cały projekt)",
    "Velocita' (sotto 1x rallenta)": "Prędkość (poniżej 1x zwalnia)",
    "Mostra orologio con la velocita'": "Pokaż zegar z prędkością",
    "Orologio (tutto il progetto)": "Zegar (cały projekt)",
    "Dimensione (px)": "Rozmiar (px)",
    "Colore": "Kolor",
    "Opacita' sfondo": "Krycie tła",
    "Fusione con la succ. (s)": "Przenikanie z nast. (s)",
    "Slide di apertura": "Slajd otwierający",
    "Adattamento": "Dopasowanie",
    "Allineamento": "Wyrównanie",
    "Ombra": "Cień",
    "Opacita' del testo": "Krycie tekstu",
    "Sfondo dietro il testo": "Tło za tekstem",
    "Modifica testo...": "Edytuj tekst...",
    "fermo": "nieruchomy",
    "Ripeti inseguimento dal cursore": "Powtórz śledzenie od kursora",
    "Segui il soggetto": "Śledź obiekt",
    "Non seguire piu'": "Przestań śledzić",
    "nessuno": "brak",
    "Togli keyframe al cursore": "Usuń klatkę kluczową na kursorze",
    "Cancella i punti selezionati": "Usuń zaznaczone punkty",
    "il file non ha audio": "plik nie ma audio",
    "= cursore": "= kursor",
    "Dal nero: la clip compare dal nero. Al nero: sparisce nel nero. Fusione: la clip sfuma nella successiva, a cavallo del taglio (la durata del video non cambia). Anche l'audio sale e scende. 0 = taglio netto.":
        "Z czerni: klip wyłania się z czerni. Do czerni: znika w czerni. Przenikanie: klip przechodzi płynnie "
        "w następny, na styku cięcia (czas trwania wideo się nie zmienia). Audio także narasta i opada. "
        "0 = ostre cięcie.",
    "La slide e' un fondo a tinta unita o un'immagine adattata alla misura del video. Testi e immagini si mettono sopra con gli strumenti Testo e Immagine: con il cursore sulla slide durano quanto lei.":
        "Slajd to jednolite tło lub obraz dopasowany do rozmiaru wideo. Teksty i obrazy umieszcza się na nim "
        "narzędziami Tekst i Obraz: z kursorem na slajdzie trwają tyle co on.",
    "Larghezza (px)": "Szerokość (px)",
    "Opacita'": "Krycie",
    "Dove l'inseguimento sbaglia: porta il cursore li' e trascina la figura sul soggetto (dagli angoli per la misura). Diventa un keyframe: il tratto prima viene corretto e l'inseguimento riparte da li' fino al keyframe successivo.\nNella timeline, sulla barra dell'effetto, i keyframe sono rombi e i punti dell'inseguimento pallini. Clic: seleziona e porta il cursore; Maiusc+clic: intervallo; Ctrl+clic: aggiunge o toglie. Canc o tasto destro: cancella i selezionati (li' la figura va dritta fra i punti rimasti).":
        "Tam, gdzie śledzenie się myli: przenieś tam kursor i przeciągnij figurę na obiekt (za rogi, aby "
        "zmienić rozmiar). Powstaje klatka kluczowa: odcinek przed nią zostaje poprawiony, a śledzenie rusza "
        "od niej aż do następnej klatki kluczowej.\nNa osi czasu, na pasku efektu, klatki kluczowe to romby, "
        "a punkty śledzenia to kropki. Klik: zaznacza i przenosi kursor; Shift+klik: zakres; Ctrl+klik: "
        "dodaje lub usuwa. Delete lub prawy przycisk: usuwa zaznaczone (tam figura biegnie prosto między "
        "pozostałymi punktami).",
    "< Prec.": "< Poprz.",
    "Succ. >": "Nast. >",
    "Centra orizz.": "Wyśrodkuj poz.",
    "Centra vert.": "Wyśrodkuj pion.",
    "Valgono per l'audio originale di tutto il video: sale all'inizio e scende alla fine. Canc spegne tutto l'audio originale (il video resta). Per un solo pezzo clicca la sua barra nella riga dell'audio.":
        "Dotyczą oryginalnego audio całego wideo: narasta na początku i opada na końcu. Delete wyłącza całe "
        "oryginalne audio (wideo zostaje). Dla jednego fragmentu kliknij jego pasek w wierszu audio.",
    "Per togliere solo un tratto d'audio: segna IN e OUT (tasti I e O) e premi Canc con l'audio selezionato: il video resta. Oppure taglia con S e seleziona il pezzo d'audio: Canc lo elimina, qui ne regoli volume e dissolvenze.":
        "Aby usunąć tylko odcinek audio: zaznacz IN i OUT (klawisze I i O) i naciśnij Delete przy zaznaczonym "
        "audio: wideo zostaje. Albo przetnij klawiszem S i zaznacz fragment audio: Delete go usuwa, a tutaj "
        "ustawiasz jego głośność i wyciszenia.",
    "Il volume sale da zero all'inizio della traccia e scende a zero alla fine.":
        "Głośność narasta od zera na początku ścieżki i opada do zera na końcu.",
    "slide": "slajd",
    "Clip: {kind}": "Klip: {kind}",
    "Traccia audio": "Ścieżka audio",
    "Slide di chiusura": "Slajd zamykający",
    "Togli": "Usuń",
    "Sull'anteprima: trascina per spostare, dagli angoli per ingrandire, doppio clic per riscriverlo.":
        "Na podglądzie: przeciągnij, aby przesunąć, za rogi, aby powiększyć, dwuklik, aby zmienić tekst.",
    "Largh.": "Szer.",
    "  Alt.": "  Wys.",
    "Spessore bordo": "Grubość obramowania",
    "Riempimento": "Wypełnienie",
    "Opacita' riempimento": "Krycie wypełnienia",
    "Il contenuto della figura fa da modello: la figura segue il soggetto nei fotogrammi successivi; quando esce dall'inquadratura l'effetto finisce.":
        "Zawartość figury służy jako wzorzec: figura śledzi obiekt w kolejnych klatkach; gdy obiekt wyjdzie "
        "z kadru, efekt się kończy.",
    "segue il soggetto ({points} punti)": "śledzi obiekt (punktów: {points})",
    "Effetto: {name}": "Efekt: {name}",
    "Audio originale (un pezzo)": "Oryginalne audio (jeden fragment)",
    "Carattere": "Czcionka",
    "Sull'anteprima: trascina per spostarla, dagli angoli per ridimensionarla (le proporzioni restano quelle dell'immagine).":
        "Na podglądzie: przeciągnij, aby przesunąć, za rogi, aby zmienić rozmiar (proporcje obrazu zostają "
        "zachowane).",
    "Coda X": "Ogon X",
    "Punta X": "Grot X",
    "Spessore": "Grubość",
    "Audio originale (tutto)": "Oryginalne audio (całe)",
    "Area da ingrandire": "Obszar do powiększenia",
    "Forma": "Kształt",
    "Angoli (rettangolare)": "Rogi (prostokątny)",
    "Contorno colorato sull'area ingrandita": "Kolorowy kontur na powiększanym obszarze",
    "Linea fra l'area e il riquadro": "Linia między obszarem a ramką",
    "Riquadro ingrandito": "Powiększona ramka",
    "L'area fa da modello: lo zoom segue l'oggetto nei fotogrammi successivi, il riquadro ingrandito resta dove l'hai messo. Se l'oggetto esce dall'inquadratura lo zoom finisce.":
        "Obszar służy jako wzorzec: zoom śledzi przedmiot w kolejnych klatkach, powiększona ramka zostaje "
        "tam, gdzie ją umieszczono. Jeśli przedmiot wyjdzie z kadru, zoom się kończy.",
    "Rettangolare": "Prostokątny",
    "Ingrandimento": "Powiększenie",
    "Larghezza": "Szerokość",
    "Per tutto il video": "Na całe wideo",
    "Largh. logo (px)": "Szer. logo (px)",
    "Dimensione testo": "Rozmiar tekstu",
    "Colore testo": "Kolor tekstu",
    "Disposizione": "Układ",
    "Ombra sotto il testo": "Cień pod tekstem",
    "Sfondo": "Tło",
    "Sfondo sotto logo e scritta": "Tło pod logo i napisem",
    "Opacita' di tutto": "Krycie całości",
    "Angolo": "Róg",
    "Il colore vale per il bordo del riquadro, il contorno dell'area e la linea. L'area scelta viene mostrata ingrandita nel riquadro, sopra il video, per la durata dell'effetto. Sull'anteprima: trascina l'area o il riquadro, ridimensiona l'area dagli angoli.":
        "Kolor dotyczy obramowania ramki, konturu obszaru i linii. Wybrany obszar jest pokazywany powiększony "
        "w ramce, nad wideo, przez czas trwania efektu. Na podglądzie: przeciągnij obszar lub ramkę, zmień "
        "rozmiar obszaru za rogi.",
    "Pixelatura": "Pikselizacja",
    "Grandezza pixel": "Wielkość pikseli",
    "Resta fermo nel punto scelto. Sull'anteprima trascinalo per spostarlo, tira un angolo per ingrandire o rimpicciolire logo e testo insieme. I valori proposti per i prossimi si cambiano in Configurazione.":
        "Pozostaje nieruchomo w wybranym miejscu. Na podglądzie przeciągnij, aby przesunąć, pociągnij róg, "
        "aby razem powiększyć lub pomniejszyć logo i tekst. Wartości proponowane dla kolejnych zmienia się "
        "w Konfiguracji.",
    "fisso": "stały",
    "Soggetto perso": "Obiekt zgubiony",
    "Ripeti l'inseguimento dopo aver cambiato inizio o fine.":
        "Powtórz śledzenie po zmianie początku lub końca.",
    "{points} punti": "punktów: {points}",
    "{frames} fotogrammi": "klatek: {frames}",
    "Trascina sull'anteprima per disegnare il riquadro": "Przeciągnij na podglądzie, aby narysować ramkę",
    "Trascina sull'anteprima per disegnare l'ovale": "Przeciągnij na podglądzie, aby narysować owal",
    "Trascina sull'anteprima un rettangolo sull'oggetto da ingrandire":
        "Przeciągnij na podglądzie prostokąt na przedmiocie do powiększenia",
    "Clicca dove far apparire il riquadro ingrandito  -  {factor}x  (rotellina o tasti 2, 3, 4, 6, 8)":
        "Kliknij, gdzie ma się pojawić powiększona ramka  -  {factor}x  (kółko lub klawisze 2, 3, 4, 6, 8)",
    "Clicca sull'anteprima dove mettere il tempo trascorso": "Kliknij na podglądzie, gdzie umieścić upływ czasu",
    "Trascina sull'anteprima l'area da pixelare: verra' inseguita nei fotogrammi successivi":
        "Przeciągnij na podglądzie obszar do pikselizacji: będzie śledzony w kolejnych klatkach",
    "Trascina dalla coda alla punta della freccia": "Przeciągnij od ogona do grotu strzałki",
    "Clicca sull'anteprima dove mettere il testo": "Kliknij na podglądzie, gdzie umieścić tekst",
    "Importa un video per vedere l'anteprima": "Zaimportuj wideo, aby zobaczyć podgląd",
    "segue il soggetto": "śledzi obiekt",
    "Logo e operatore": "Logo i operator",
    "Slide di apertura: {text}": "Slajd otwierający: {text}",
    "Slide di chiusura: {text}": "Slajd zamykający: {text}",
    "Slide: {text}": "Slajd: {text}",
    "Fermo immagine ({name})": "Stopklatka ({name})",
    "Percorso del progetto mancante": "Brak ścieżki projektu",
    "La timeline e' vuota: importa almeno un video.": "Oś czasu jest pusta: zaimportuj co najmniej jedno wideo.",
    "Preparazione dei segmenti": "Przygotowanie segmentów",
    "Disegno delle sovraimpressioni": "Rysowanie nakładek",
    "Preparazione": "Przygotowanie",
    "Completato": "Zakończono",
    "ffmpeg non ha scritto il file di uscita.": "ffmpeg nie zapisał pliku wyjściowego.",
    "Disegno del contorno dello zoom": "Rysowanie konturu zoomu",
    "Disegno dell'orologio {speed}": "Rysowanie zegara {speed}",
    "Codifica: {done} / {total}": "Kodowanie: {done} / {total}",
    "Audio originale": "Oryginalne audio",
    "muto": "wyciszone",
    "immagine": "obraz",
    "orologio": "zegar",
    "senza audio": "bez audio",
    "audio": "audio",
    "{name} ({points} punti)": "{name} (punktów: {points})",
    "{name} (fisso)": "{name} (stały)",
    "{name} (segue)": "{name} (śledzi)",
    "audio {volume:.0f} %": "audio {volume:.0f} %",
    "Risposta inattesa dal sito di download di ffmpeg.": "Nieoczekiwana odpowiedź ze strony pobierania ffmpeg.",
    "Il download automatico e' disponibile solo su Windows: installa ffmpeg con il gestore di pacchetti del sistema.":
        "Automatyczne pobieranie jest dostępne tylko w systemie Windows: zainstaluj ffmpeg menedżerem "
        "pakietów systemu.",
    "licenza di VitTrack": "licencja VitTrack",
    "Il file scaricato non e' un archivio zip valido.": "Pobrany plik nie jest prawidłowym archiwum zip.",
    "Estrazione di ffmpeg": "Rozpakowywanie ffmpeg",
    "L'ffmpeg scaricato non si avvia su questo PC.": "Pobrany ffmpeg nie uruchamia się na tym komputerze.",
    "Il modello scaricato non corrisponde a quello atteso (impronta SHA-256 diversa).":
        "Pobrany model nie jest oczekiwanym modelem (inny odcisk SHA-256).",
    "Il pacchetto scaricato non contiene {file}.": "Pobrany pakiet nie zawiera {file}.",
    "{file} manca dopo l'estrazione.": "Po rozpakowaniu brakuje {file}.",
    "Impossibile controllare l'ultima versione di ffmpeg: {error}":
        "Nie można sprawdzić najnowszej wersji ffmpeg: {error}",
    "Download di {name} fallito: {error}": "Pobieranie {name} nie powiodło się: {error}",
    "Impossibile aggiornare '{folder}': file in uso. Aspetta la fine dell'esportazione e riprova.":
        "Nie można zaktualizować '{folder}': pliki są w użyciu. Poczekaj na zakończenie eksportu i spróbuj "
        "ponownie.",
    "OpenCV non riesce a caricare il modello: {error}": "OpenCV nie może wczytać modelu: {error}",
    "Archivio non valido: percorso sospetto '{path}'.": "Nieprawidłowe archiwum: podejrzana ścieżka '{path}'.",
    "Download di {name}": "Pobieranie {name}",
    "Nessun fotogramma all'istante di partenza.": "Brak klatki w chwili początkowej.",
    "INFO": "INFO",
    "CONFERMA": "POTWIERDŹ",
    "ATTENZIONE": "OSTRZEŻENIE",
    "ERRORE": "BŁĄD",
    "OK": "OK",
    "Annulla": "Anuluj",
    "Si'": "Tak",
    "No": "Nie",
    "Interruzione...": "Przerywanie...",
    "Invio va a capo, Ctrl+Invio conferma.": "Enter: nowy wiersz, Ctrl+Enter: zatwierdź.",
    "Allineamento delle righe": "Wyrównanie wierszy",
    "Scrivi il testo.": "Wpisz tekst.",
    "Fondo scuro": "Ciemne tło",
    "Centra nel video": "Wyśrodkuj w wideo",
    "Dimensione non valida.": "Nieprawidłowy rozmiar.",
    "{field}: valore fra {min:g} e {max:g}.": "{field}: wartość od {min:g} do {max:g}.",
    "{field}: inserisci un numero.": "{field}: wpisz liczbę.",

    # ------------------------------------------------------- tempo trascorso
    "Tempo trascorso dall'inizio del video: clic dove metterlo, poi si sposta":
        "Czas od początku wideo: kliknij, gdzie go umieścić, potem można go przesunąć",
    "Tempo trascorso aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.":
        "Dodano upływ czasu: przeciągnij go, gdzie chcesz, dostosuj w panelu po prawej.",
    "minuti:secondi (01:23)": "minuty:sekundy (01:23)",
    "ore:minuti:secondi (00:01:23)": "godziny:minuty:sekundy (00:01:23)",
    "con i decimi (01:23.4)": "z dziesiątymi (01:23.4)",
    "dall'inizio del video": "od początku wideo",
    "dall'inizio dell'effetto": "od początku efektu",
    "Tempo trascorso": "Upływ czasu",
    "Formato": "Format",
    "Conta": "Licz",
    "Testo davanti": "Tekst przed",
    "Sfondo dietro il tempo": "Tło za czasem",
    "Sull'anteprima: trascinalo dove vuoi, dagli angoli per ingrandirlo.":
        "Na podglądzie: przeciągnij, gdzie chcesz, za rogi, aby powiększyć.",
    "Disegno del tempo trascorso": "Rysowanie upływu czasu",

    # ------------------------------------------------------- riproduzione
    '10 fotogrammi indietro (Ctrl+Sinistra)': '10 klatek wstecz (Ctrl+←)',
    "Riproduci all'indietro / pausa (Maiusc+Spazio), senza audio": 'Odtwarzaj wstecz / pauza (Shift+Spacja), bez dźwięku',
    '10 fotogrammi avanti (Ctrl+Destra)': '10 klatek do przodu (Ctrl+→)',
    'Allunga fino al cursore': 'Wydłuż do kursora',
    'Interrompi al cursore': 'Zakończ na kursorze',
    '{effect} allungato fino a {t:.2f} s.': '{effect}: wydłużono do {t:.2f} s.',
    '{effect} interrotto a {t:.2f} s.': '{effect}: zakończono na {t:.2f} s.',
    "{effect} nascosto: non compare in anteprima ne' nel video esportato.": '{effect}: ukryto, nie pojawia się w podglądzie ani w eksportowanym wideo.',
    '{effect} di nuovo visibile.': '{effect}: ponownie widoczne.',
    '{zoom}% - trascina per spostarti, doppio clic centrale: adatta': '{zoom}% - przeciągnij, aby przesunąć, podwójne kliknięcie środkowym: dopasuj',
    'Fotogrammi': 'Klatki',
    "Numero del fotogramma dall'inizio del video: clic dove metterlo, poi si sposta": 'Numer klatki od początku wideo: kliknij, gdzie go umieścić, potem przesuń',
    'Numero del fotogramma aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.': 'Dodano numer klatki: przeciągnij go, gdzie chcesz, i dostosuj w panelu po prawej.',
    'Numero del fotogramma': 'Numer klatki',
    'Primo fotogramma': 'Pierwsza klatka',
    "Clicca sull'anteprima dove mettere il numero del fotogramma": 'Kliknij w podglądzie, gdzie umieścić numer klatki',
    'Anteprima': 'Podgląd',
    'Anteprima riattaccata.': 'Podgląd ponownie przypięty.',
    "Riattacca l'anteprima alla finestra principale": 'Przypnij podgląd z powrotem do okna głównego',
    "Stacca l'anteprima in una finestra a parte (piu' spazio per la timeline)": 'Odłącz podgląd do osobnego okna (więcej miejsca na oś czasu)',
    'Anteprima in una finestra a parte: chiudila o usa il pulsante in alto a destra per riattaccarla.': 'Podgląd w osobnym oknie: zamknij je lub użyj przycisku w prawym górnym rogu, aby go przypiąć.',
    "Trascina un rettangolo attorno al soggetto: la freccia lo seguira' tenendo la punta dov'e'.": 'Przeciągnij prostokąt wokół obiektu: strzałka będzie za nim podążać, a grot zostanie na miejscu.',
    'soggetto della freccia': 'obiekt strzałki',
    "Si disegna un rettangolo attorno al soggetto: la freccia lo segue nei fotogrammi successivi tenendo la punta su di lui; quando esce dall'inquadratura l'effetto finisce.": 'Narysuj prostokąt wokół obiektu: strzałka podąża za nim w kolejnych klatkach, trzymając na nim grot; gdy wyjdzie z kadru, efekt się kończy.',
    'Scegli un altro soggetto': 'Wybierz inny obiekt',
    'Trascina un rettangolo attorno al soggetto che la freccia deve seguire': 'Przeciągnij prostokąt wokół obiektu, za którym ma podążać strzałka',
}
