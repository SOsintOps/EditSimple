# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Deutsch: Übersetzung der Texte der Oberfläche von EditSimple.

Der Schlüssel ist der italienische Text, so wie er im Code steht (in tr() und N_()),
der Wert seine Übersetzung. Platzhalter in geschweiften Klammern bleiben unverändert.
Nach jeder Änderung:

    .venv\\Scripts\\python.exe scripts\\check_i18n.py de
"""

from __future__ import annotations

NAME = "Deutsch"

CATALOG: dict[str, str] = {
    "Impossibile avviare l'interfaccia: {error}\n\nInstalla le dipendenze con:\n    {command}":
        "Die Oberfläche kann nicht gestartet werden: {error}\n\nInstallieren Sie die Abhängigkeiten mit:\n    {command}",
    "In alto a sinistra":
        "Oben links",
    "In alto a destra":
        "Oben rechts",
    "In basso a sinistra":
        "Unten links",
    "In basso a destra":
        "Unten rechts",
    "Progetto EditSimple":
        "EditSimple-Projekt",
    "Tutti i file":
        "Alle Dateien",
    "Apertura (all'inizio)":
        "Vorspann (am Anfang)",
    "Chiusura (alla fine)":
        "Abspann (am Ende)",
    "Apri progetto... (Ctrl+O)":
        "Projekt öffnen... (Strg+O)",
    "Progetto":
        "Projekt",
    "Nuovo":
        "Neu",
    "Nuovo progetto (Ctrl+N)":
        "Neues Projekt (Strg+N)",
    "Apri":
        "Öffnen",
    "Apri progetto (Ctrl+O)":
        "Projekt öffnen (Strg+O)",
    "Salva":
        "Speichern",
    "Salva progetto (Ctrl+S)":
        "Projekt speichern (Strg+S)",
    "Annulla (Ctrl+Z)":
        "Rückgängig (Strg+Z)",
    "Ripeti (Ctrl+Y)":
        "Wiederholen (Strg+Y)",
    "Clip":
        "Clip",
    "Importa video":
        "Video importieren",
    "Importa un video in coda o al cursore (Ctrl+I)":
        "Ein Video am Ende oder am Cursor importieren (Strg+I)",
    "Audio":
        "Audio",
    "Aggiungi una traccia audio (commento, musica) al cursore":
        "Eine Audiospur (Kommentar, Musik) am Cursor hinzufügen",
    "Taglia":
        "Schneiden",
    "Taglia la clip al cursore (S)":
        "Den Clip am Cursor schneiden (S)",
    "Elimina":
        "Löschen",
    "Elimina la porzione IN-OUT o l'elemento selezionato (Canc)":
        "Den Bereich IN-OUT oder das gewählte Element löschen (Entf)",
    "Fermo":
        "Standbild",
    "Fermo immagine del fotogramma al cursore (F)":
        "Standbild des Frames am Cursor (F)",
    "Slide":
        "Folie",
    "Inserisci una slide":
        "Eine Folie einfügen",
    "Velocita'":
        "Tempo",
    "Velocita' della porzione IN-OUT: piu' veloce o rallentata (V)":
        "Tempo des Bereichs IN-OUT: schneller oder verlangsamt (V)",
    "Sovraimpressioni":
        "Einblendungen",
    "Testo":
        "Text",
    "Testo (T)":
        "Text (T)",
    "Immagine":
        "Bild",
    "Immagine sopra il video, da spostare e ridimensionare":
        "Bild über dem Video, verschieb- und skalierbar",
    "Logo":
        "Logo",
    "Logo e testo dell'operatore, fermi in un angolo (L)":
        "Logo und Text des Bedieners, fest in einer Ecke (L)",
    "Riquadro":
        "Rahmen",
    "Riquadro (R): puo' seguire il soggetto":
        "Rahmen (R): kann dem Motiv folgen",
    "Ovale":
        "Oval",
    "Ovale (E): puo' seguire il soggetto":
        "Oval (E): kann dem Motiv folgen",
    "Freccia":
        "Pfeil",
    "Freccia (A): puo' seguire il soggetto":
        "Pfeil (A): kann dem Motiv folgen",
    "Zoom":
        "Zoom",
    "Zoom rettangolare: l'area scelta in un riquadro ingrandito (Z)":
        "Rechteckiger Zoom: der gewählte Bereich vergrößert in einem Rahmen (Z)",
    "Zoom ovale: l'area scelta in un ovale ingrandito (Maiusc+Z)":
        "Ovaler Zoom: der gewählte Bereich vergrößert in einem Oval (Umschalt+Z)",
    "Pixel":
        "Pixel",
    "Pixelatura rettangolare che insegue il soggetto (P)":
        "Rechteckige Verpixelung, die dem Motiv folgt (P)",
    "Pixelatura ovale che insegue il soggetto (K)":
        "Ovale Verpixelung, die dem Motiv folgt (K)",
    "Uscita":
        "Ausgabe",
    "Esporta MP4":
        "MP4 exportieren",
    "Esporta il video finale (Ctrl+E)":
        "Das fertige Video exportieren (Strg+E)",
    "Inseguimento (VitTrack)":
        "Verfolgung (VitTrack)",
    "Esportazione":
        "Export",
    "Logo e testo dell'operatore":
        "Logo und Text des Bedieners",
    "Angoli arrotondati":
        "Abgerundete Ecken",
    "Crediti":
        "Credits",
    "Lingua":
        "Sprache",
    "Impostazioni salvate.":
        "Einstellungen gespeichert.",
    "Download di ffmpeg":
        "Download von ffmpeg",
    "Download di VitTrack":
        "Download von VitTrack",
    "Progetto non salvato":
        "Projekt nicht gespeichert",
    "Salvare le modifiche al progetto?":
        "Änderungen am Projekt speichern?",
    "Nuovo progetto.":
        "Neues Projekt.",
    "Lettura del video...":
        "Video wird gelesen...",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}":
        "{file} importiert: {width}x{height}, {fps:g} fps, {duration}",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}, senza audio":
        "{file} importiert: {width}x{height}, {fps:g} fps, {duration}, ohne Audio",
    "Audio di questo pezzo eliminato (il video resta). Ctrl+Z per riaverlo.":
        "Audio dieses Stücks gelöscht (das Video bleibt). Strg+Z stellt es wieder her.",
    "Clip eliminata.":
        "Clip gelöscht.",
    "Fermo immagine":
        "Standbild",
    "Nuovo testo":
        "Neuer Text",
    "Testo aggiunto: trascinalo, ingrandiscilo dagli angoli, doppio clic per riscriverlo.":
        "Text hinzugefügt: ziehen Sie ihn, vergrößern Sie ihn an den Ecken, Doppelklick zum Umschreiben.",
    "Modifica testo":
        "Text bearbeiten",
    "Immagine aggiunta: trascinala per spostarla, dagli angoli per ridimensionarla.":
        "Bild hinzugefügt: ziehen Sie es zum Verschieben, an den Ecken zum Skalieren.",
    "Pixelatura con inseguimento":
        "Verpixelung mit Verfolgung",
    "Cancellati {count} punti del percorso (il primo resta: e' la partenza della figura).":
        "{count} Punkte des Pfads gelöscht (der erste bleibt: er ist der Start der Figur).",
    "Cancellati {count} punti del percorso.":
        "{count} Punkte des Pfads gelöscht.",
    "Inseguimento del soggetto":
        "Verfolgung des Motivs",
    "Esportazione in corso":
        "Export läuft",
    "montaggio video per presentazioni":
        "Videoschnitt für Präsentationen",
    "PROGETTO":
        "PROJEKT",
    "nuovo":
        "neu",
    "Nessun video":
        "Kein Video",
    "Montaggio":
        "Schnitt",
    "Configura":
        "Konfiguration",
    "Riproduci / pausa (Spazio)":
        "Wiedergabe / Pause (Leertaste)",
    "larghezza logo % del video":
        "Logobreite in % des Videos",
    "altezza testo % del lato corto":
        "Texthöhe in % der kurzen Seite",
    "distanza dai bordi % del lato corto":
        "Randabstand in % der kurzen Seite",
    "opacita' %":
        "Deckkraft %",
    "angoli arrotondati %":
        "abgerundete Ecken %",
    "sfondo del testo":
        "Texthintergrund",
    "riquadro":
        "Rahmen",
    "zoom rettangolare":
        "rechteckiger Zoom",
    "pixel rettangolare":
        "rechteckige Pixel",
    "Colore del testo":
        "Textfarbe",
    "Colore dello sfondo":
        "Hintergrundfarbe",
    "Immagine del logo":
        "Logobild",
    "Questa immagine non si apre.":
        "Dieses Bild lässt sich nicht öffnen.",
    "Controllo in corso...":
        "Prüfung...",
    "Pronto.":
        "Bereit.",
    "ffmpeg non e' stato trovato. Scaricalo dal riquadro FFmpeg della pagina Configurazione: senza, non si possono importare ne' esportare video.":
        "ffmpeg wurde nicht gefunden. Laden Sie es im FFmpeg-Feld der Seite Konfiguration herunter: ohne ffmpeg lassen sich Videos weder importieren noch exportieren.",
    "ffmpeg non e' stato trovato. Installalo con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) o copia un eseguibile ffmpeg in tools/ffmpeg/: senza, non si possono importare ne' esportare video.":
        "ffmpeg wurde nicht gefunden. Installieren Sie es mit der Paketverwaltung des Systems (zum Beispiel sudo apt install ffmpeg) oder kopieren Sie eine ausführbare ffmpeg-Datei nach tools/ffmpeg/: ohne ffmpeg lassen sich Videos weder importieren noch exportieren.",
    "ffmpeg NON trovato: installalo con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) oppure metti un eseguibile ffmpeg in tools/ffmpeg/.":
        "ffmpeg wurde NICHT gefunden: Installieren Sie es mit der Paketverwaltung des Systems (zum Beispiel sudo apt install ffmpeg) oder legen Sie eine ausführbare ffmpeg-Datei in tools/ffmpeg/ ab.",
    "Non salvare":
        "Nicht speichern",
    "Niente da annullare.":
        "Nichts rückgängig zu machen.",
    "inizio":
        "Anfang",
    "fine":
        "Ende",
    "Apri progetto":
        "Projekt öffnen",
    "File mancanti":
        "Fehlende Dateien",
    "Salva progetto":
        "Projekt speichern",
    "Dove inserire il video?":
        "Wo soll das Video eingefügt werden?",
    "Importazione":
        "Import",
    "Il file non contiene video. Per l'audio usa il pulsante Audio.":
        "Die Datei enthält kein Video. Für Audio verwenden Sie die Schaltfläche Audio.",
    "Importa prima un video.":
        "Importieren Sie zuerst ein Video.",
    "Aggiungi traccia audio":
        "Audiospur hinzufügen",
    "Il file non contiene audio.":
        "Die Datei enthält kein Audio.",
    "Il cursore e' gia' su un confine fra clip.":
        "Der Cursor steht bereits auf einer Grenze zwischen Clips.",
    "Importa prima un video: la slide prende la sua misura.":
        "Importieren Sie zuerst ein Video: die Folie übernimmt seine Größe.",
    "Al cursore ({time})":
        "Am Cursor ({time})",
    "Dove":
        "Wo",
    "Durata (secondi)":
        "Dauer (Sekunden)",
    "Crea":
        "Erstellen",
    "La slide e' un fondo a tinta unita (il colore si sceglie nel pannello). Testi e immagini si aggiungono sopra con gli strumenti Testo e Immagine.":
        "Die Folie ist ein einfarbiger Hintergrund (die Farbe wählen Sie im Bereich rechts). Texte und Bilder fügen Sie mit den Werkzeugen Text und Bild darüber hinzu.",
    "Slide di chiusura aggiunta alla fine: regolala nel pannello a destra.":
        "Abspannfolie am Ende hinzugefügt: Passen Sie sie im Bereich rechts an.",
    "Inserisci":
        "Einfügen",
    "Applica":
        "Anwenden",
    "Effetti":
        "Effekte",
    "Pixel ovale":
        "Ovale Pixel",
    "Pixel rettangolare":
        "Rechteckige Pixel",
    "Zoom ovale (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Ovaler Zoom (Rechteck über dem Objekt, dann klicken, wo der Rahmen hin soll)",
    "Zoom (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Zoom (Rechteck über dem Objekt, dann klicken, wo der Rahmen hin soll)",
    "Carica l'immagine del logo e scrivi il testo dell'operatore nella pagina Configura, poi premi di nuovo Logo.":
        "Laden Sie das Logobild und schreiben Sie den Text des Bedieners auf der Seite Konfiguration, dann drücken Sie erneut Logo.",
    "Logo e operatore aggiunti per tutto il video: trascinali sull'anteprima o regolali nel pannello.":
        "Logo und Bediener für das ganze Video hinzugefügt: Ziehen Sie sie in der Vorschau oder passen Sie sie im Bereich an.",
    "Zoom aggiunto (fermo: sul fermo immagine non c'e' nulla da inseguire).":
        "Zoom hinzugefügt (fest: auf dem Standbild gibt es nichts zu verfolgen).",
    "Insegui":
        "Verfolgen",
    "Keyframe":
        "Keyframe",
    "Porta il cursore dentro l'effetto.":
        "Setzen Sie den Cursor in den Effekt.",
    "Nessun keyframe al cursore: usa Prec. / Succ. per andarci.":
        "Kein Keyframe am Cursor: Verwenden Sie Vorh. / Nächst., um dorthin zu gelangen.",
    "Il primo punto del percorso non si cancella: e' la partenza della figura.":
        "Der erste Punkt des Pfads lässt sich nicht löschen: er ist der Start der Figur.",
    "Seleziona prima dei punti sulla barra dell'effetto nella timeline (clic, Maiusc+clic per un intervallo, Ctrl+clic per aggiungerne).":
        "Wählen Sie zuerst Punkte auf dem Balken des Effekts in der Timeline (Klick, Umschalt+Klick für einen Bereich, Strg+Klick zum Hinzufügen).",
    "Nessun altro keyframe in quella direzione.":
        "Kein weiterer Keyframe in dieser Richtung.",
    "Inseguimento":
        "Verfolgung",
    "L'inseguimento funziona solo su una clip video (non su un fermo immagine): la figura resta ferma.":
        "Die Verfolgung funktioniert nur auf einem Videoclip (nicht auf einem Standbild): die Figur bleibt fest.",
    "Testo di prova":
        "Probetext",
    "La timeline e' vuota.":
        "Die Timeline ist leer.",
    "Esportazione completata":
        "Export abgeschlossen",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Scarica / Aggiorna prende il build ufficiale per Windows (release essentials) da gyan.dev e tiene solo ffmpeg.exe, LICENSE e README in tools/ffmpeg/. Nessuna installazione, nessuna modifica al PATH.":
        "ffmpeg ist nicht im Programm enthalten: es ist ein separates Programm mit eigener Lizenz. Herunterladen / Aktualisieren holt den offiziellen Windows-Build (release essentials) von gyan.dev und behält nur ffmpeg.exe, LICENSE und README in tools/ffmpeg/. Keine Installation, keine Änderung am PATH.",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Su Linux e macOS si installa con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) oppure si mette un eseguibile ffmpeg in tools/ffmpeg/. Il download automatico vale solo per Windows.":
        "ffmpeg ist nicht im Programm enthalten: es ist ein separates Programm mit eigener Lizenz. Unter Linux und macOS installieren Sie es mit der Paketverwaltung des Systems (zum Beispiel sudo apt install ffmpeg) oder legen eine ausführbare ffmpeg-Datei in tools/ffmpeg/ ab. Der automatische Download gilt nur für Windows.",
    "Scarica / Aggiorna":
        "Herunterladen / Aktualisieren",
    "Apri cartella tools":
        "Ordner tools öffnen",
    "VitTrack e' un modello addestrato per seguire oggetti e persone: ritrova il soggetto dopo un palo o un passante e capisce quando e' perso. Viene dal repository ufficiale opencv_zoo (licenza Apache 2.0, compatibile con la GPL 3), circa 0,7 MB, in tools/vittrack/ con la sua licenza. Senza, l'inseguimento usa il confronto a modello.":
        "VitTrack ist ein trainiertes Modell zum Verfolgen von Objekten und Personen: Es findet das Motiv nach einem Pfosten oder einem Passanten wieder und erkennt, wann es verloren ist. Es stammt aus dem offiziellen Repository opencv_zoo (Lizenz Apache 2.0, mit der GPL 3 vereinbar), etwa 0,7 MB, in tools/vittrack/ mit seiner Lizenz. Ohne VitTrack verwendet die Verfolgung den Vorlagenvergleich.",
    "Scarica":
        "Herunterladen",
    "Qualita' video (CRF, 15 = ottima, 28 = leggera)":
        "Videoqualität (CRF, 15 = sehr gut, 28 = leicht)",
    "Velocita' di codifica (preset x264)":
        "Kodiergeschwindigkeit (Preset x264)",
    "Audio (kbit/s)":
        "Audio (kbit/s)",
    "Durate proposte (secondi)":
        "Vorgeschlagene Dauern (Sekunden)",
    "Pixelatura: grandezza dei pixel e soglia dell'inseguimento (0.2-0.9)":
        "Verpixelung: Pixelgröße und Schwelle der Verfolgung (0.2-0.9)",
    "Salva impostazioni":
        "Einstellungen speichern",
    "Carica immagine del logo...":
        "Logobild laden...",
    "Togli logo":
        "Logo entfernen",
    "Testo dell'operatore (nome, qualifica, data...)":
        "Text des Bedieners (Name, Funktion, Datum...)",
    "Il pulsante Logo (tasto L) mette logo e testo nell'angolo scelto, fermi per tutto il video (o solo nella porzione IN-OUT, se e' segnata). Nel progetto si possono poi spostare, ridimensionare e cambiare dal pannello a destra.":
        "Die Schaltfläche Logo (Taste L) setzt Logo und Text in die gewählte Ecke, fest für das ganze Video (oder nur im Bereich IN-OUT, falls markiert). Im Projekt lassen sie sich dann im Bereich rechts verschieben, skalieren und ändern.",
    "Proposti ai nuovi effetti, in % del lato corto (0 = angoli vivi, 50 = estremita' tonde); ogni effetto poi si regola nel suo pannello":
        "Vorschlag für neue Effekte, in % der kurzen Seite (0 = spitze Ecken, 50 = runde Enden); jeder Effekt wird dann in seinem Bereich eingestellt",
    "nessun logo":
        "kein Logo",
    "La lingua dell'interfaccia cambia subito, senza riavviare.":
        "Die Sprache der Oberfläche wechselt sofort, ohne Neustart.",
    "Valore non valido":
        "Ungültiger Wert",
    "Controlla i numeri inseriti.":
        "Prüfen Sie die eingegebenen Zahlen.",
    "ffmpeg scaricato in tools/ffmpeg.":
        "ffmpeg nach tools/ffmpeg heruntergeladen.",
    "VitTrack non scaricato: l'inseguimento usa il confronto a modello, che puo' perdere il soggetto dietro un ostacolo.":
        "VitTrack nicht heruntergeladen: die Verfolgung verwendet den Vorlagenvergleich, der das Motiv hinter einem Hindernis verlieren kann.",
    "Modello scaricato in tools/vittrack: l'inseguimento ora lo usa.":
        "Modell nach tools/vittrack heruntergeladen: die Verfolgung verwendet es jetzt.",
    "Cartella":
        "Ordner",
    "Progetto aperto: {file}":
        "Projekt geöffnet: {file}",
    "Salvataggio":
        "Speichern",
    "Progetto salvato: {path}":
        "Projekt gespeichert: {path}",
    "In coda":
        "Am Ende",
    "Al cursore":
        "Am Cursor",
    "Traccia audio aggiunta: {name} ({duration})":
        "Audiospur hinzugefügt: {name} ({duration})",
    "Clip tagliata a {time}.":
        "Clip bei {time} geschnitten.",
    "Audio originale tolto fra {start} e {end} (il video resta).":
        "Originalton zwischen {start} und {end} entfernt (das Video bleibt).",
    "Slide di apertura aggiunta all'inizio: regolala nel pannello a destra.":
        "Vorspannfolie am Anfang hinzugefügt: Passen Sie sie im Bereich rechts an.",
    "Fermo immagine di {seconds:g} s inserito.":
        "Standbild von {seconds:g} s eingefügt.",
    "Segna prima la porzione con IN e OUT (tasti I e O), oppure seleziona una clip.":
        "Markieren Sie zuerst den Bereich mit IN und OUT (Tasten I und O) oder wählen Sie einen Clip.",
    "Mostra l'icona dell'orologio con le lancette e la velocita' sotto":
        "Uhrsymbol mit Zeigern und dem Tempo darunter anzeigen",
    "Velocita' {speed} applicata fra {start} e {end}.":
        "Tempo {speed} zwischen {start} und {end} angewendet.",
    "{effect} aggiunto: regola i valori nel pannello a destra o trascina sull'anteprima.":
        "{effect} hinzugefügt: Passen Sie die Werte im Bereich rechts an oder ziehen Sie in der Vorschau.",
    "Fino all'istante (secondi della timeline)":
        "Bis zum Zeitpunkt (Sekunden der Timeline)",
    "Grandezza dei pixel":
        "Pixelgröße",
    "Keyframe a {time}: trascina la figura per correggerla.":
        "Keyframe bei {time}: Ziehen Sie die Figur, um sie zu korrigieren.",
    "Inseguimento annullato.":
        "Verfolgung abgebrochen.",
    "Inseguimento completato: {frames} fotogrammi, {points} punti":
        "Verfolgung abgeschlossen: {frames} Frames, {points} Punkte",
    "Esportazione annullata.":
        "Export abgebrochen.",
    "Esportazione fallita":
        "Export fehlgeschlagen",
    "Esportazione fallita.":
        "Export fehlgeschlagen.",
    "Apri cartella":
        "Ordner öffnen",
    "Chiudi":
        "Schließen",
    "PAGINE":
        "SEITEN",
    "Inizio (Home)":
        "Anfang (Pos1)",
    "Fotogramma precedente (Sinistra)":
        "Vorheriger Frame (Links)",
    "Fotogramma successivo (Destra)":
        "Nächster Frame (Rechts)",
    "Fine (Fine)":
        "Ende (Ende)",
    "Adatta la timeline":
        "Timeline einpassen",
    "Ingrandisci la timeline (Ctrl+rotellina). Per spostarla: Alt+trascina, tasto centrale o rotellina":
        "Timeline vergrößern (Strg+Mausrad). Zum Verschieben: Alt+Ziehen, mittlere Taste oder Mausrad",
    "Riduci la timeline":
        "Timeline verkleinern",
    "Configurazione":
        "Konfiguration",
    "fermo immagine":
        "Standbild",
    "effetti":
        "Effekte",
    "angolo":
        "Ecke",
    "disposizione":
        "Anordnung",
    "colore testo":
        "Textfarbe",
    "sfondo sotto logo e scritta":
        "Hintergrund unter Logo und Schrift",
    "colore":
        "Farbe",
    "Nessun logo: carica un'immagine (PNG con trasparenza, JPG...).":
        "Kein Logo: Laden Sie ein Bild (PNG mit Transparenz, JPG...).",
    "Immagini":
        "Bilder",
    "ffmpeg NON trovato: scaricalo con il pulsante qui sotto.":
        "ffmpeg NICHT gefunden: Laden Sie es mit der Schaltfläche unten herunter.",
    "{label}: {done:.1f} MB / {total:.1f} MB":
        "{label}: {done:.1f} MB / {total:.1f} MB",
    "{label}: {done:.1f} MB":
        "{label}: {done:.1f} MB",
    "Download fallito":
        "Download fehlgeschlagen",
    "{label}: {done:.2f} MB / {total:.2f} MB":
        "{label}: {done:.2f} MB / {total:.2f} MB",
    "{label}: {done:.2f} MB":
        "{label}: {done:.2f} MB",
    "Spazio riproduci  ·  ← → fotogramma  ·  I / O segna  ·  S taglia  ·  Canc elimina  ·  Ctrl+Z annulla  ·  Esc annulla disegno":
        "Leertaste Wiedergabe  ·  ← → Frame  ·  I / O markieren  ·  S schneiden  ·  Entf löschen  ·  Strg+Z rückgängig  ·  Esc Zeichnen abbrechen",
    "Fotogramma non leggibile: {file}":
        "Frame nicht lesbar: {file}",
    "Questi file non si trovano piu':\n\n{files}":
        "Diese Dateien sind nicht mehr auffindbar:\n\n{files}",
    "Video":
        "Video",
    "{file}\n\nAggiungerlo in coda alla timeline oppure inserirlo al cursore ({time})?":
        "{file}\n\nAm Ende der Timeline anhängen oder am Cursor ({time}) einfügen?",
    "Eliminata la porzione {start} - {end}.":
        "Bereich {start} - {end} gelöscht.",
    "Audio originale spento (il video resta): riaccendilo dal pannello o con Ctrl+Z.":
        "Originalton stumm (das Video bleibt): Schalten Sie ihn im Bereich oder mit Strg+Z wieder ein.",
    "Porzione {start} - {end}. Da 2x in su accelera, 0.5x e 0.25x rallentano (la porzione dura il doppio o il quadruplo); con 1x si torna alla velocita' normale.":
        "Bereich {start} - {end}. Ab 2x wird beschleunigt, 0.5x und 0.25x verlangsamen (der Bereich dauert doppelt oder viermal so lang); mit 1x kehrt das normale Tempo zurück.",
    "Disegna: {effect}  (Esc annulla)":
        "Zeichnen: {effect}  (Esc bricht ab)",
    "Logo e operatore aggiunti fra {start} e {end}: trascinali sull'anteprima o regolali nel pannello.":
        "Logo und Bediener zwischen {start} und {end} hinzugefügt: Ziehen Sie sie in der Vorschau oder passen Sie sie im Bereich an.",
    "Keyframe a {time}.":
        "Keyframe bei {time}.",
    "; soggetto uscito dall'inquadratura: l'effetto finisce a {time}":
        "; Motiv hat das Bild verlassen: der Effekt endet bei {time}",
    "; soggetto perso: l'effetto finisce a {time}":
        "; Motiv verloren: der Effekt endet bei {time}",
    "Video MP4":
        "MP4-Video",
    "Esportato {path} ({size:.1f} MB in {seconds:.0f} s).":
        "{path} exportiert ({size:.1f} MB in {seconds:.0f} s).",
    "{path}\n\n{size:.1f} MB in {seconds:.0f} secondi.\n\nAprire la cartella?":
        "{path}\n\n{size:.1f} MB in {seconds:.0f} Sekunden.\n\nOrdner öffnen?",
    "{app} {version}. Montaggio video semplice per presentazioni: timeline, tagli, fermo immagine, avanzamento veloce, sovraimpressioni, zoom e pixelatura con inseguimento; esportazione mp4 con ffmpeg. Progetti in formato JSON.":
        "{app} {version}. Einfacher Videoschnitt für Präsentationen: Timeline, Schnitte, Standbild, Zeitraffer, Einblendungen, Zoom und Verpixelung mit Verfolgung; MP4-Export mit ffmpeg. Projekte im JSON-Format.",
    "{copyright}. Software libero: GNU General Public License versione 3 con termini aggiuntivi (attribuzione dell'autore, nome e logo), vedi i file LICENSE e NOTICE. Nessuna garanzia. Usa librerie e programmi di terze parti con le loro licenze (elencati in NOTICE).":
        "{copyright}. Freie Software: GNU General Public License Version 3 mit zusätzlichen Bedingungen (Nennung des Autors, Name und Logo), siehe die Dateien LICENSE und NOTICE. Keine Gewährleistung. Verwendet Bibliotheken und Programme Dritter mit ihren Lizenzen (in NOTICE aufgeführt).",
    "cartella tools/ffmpeg":
        "Ordner tools/ffmpeg",
    "PATH di sistema":
        "System-PATH",
    "VitTrack presente: l'inseguimento lo usa.\n{model}":
        "VitTrack vorhanden: die Verfolgung verwendet es.\n{model}",
    "{width}x{height}  {fps:g} fps  {clips} clip  {duration}":
        "{width}x{height}  {fps:g} fps  {clips} Clips  {duration}",
    "Anteprima: {error}":
        "Vorschau: {error}",
    "Audio dell'anteprima non disponibile: {error}":
        "Audio der Vorschau nicht verfügbar: {error}",
    "Impossibile aprire il progetto:\n{error}":
        "Das Projekt kann nicht geöffnet werden:\n{error}",
    "Slide aggiunta a {time}: regolala nel pannello a destra.":
        "Folie bei {time} hinzugefügt: Passen Sie sie im Bereich rechts an.",
    "Il fotogramma a {time} resta fermo per questo tempo; cio' che segue scorre in avanti.":
        "Der Frame bei {time} bleibt für diese Zeit stehen; das Folgende verschiebt sich nach hinten.",
    "L'inseguimento parte dal cursore ({start}) e segue il soggetto fino a questo istante (al massimo la fine della clip: {clip_end}).":
        "Die Verfolgung beginnt am Cursor ({start}) und folgt dem Motiv bis zu diesem Zeitpunkt (höchstens bis zum Ende des Clips: {clip_end}).",
    "File non trovato: {path}":
        "Datei nicht gefunden: {path}",
    "ffmpeg trovato ({where})\n{path}\nversione {version}":
        "ffmpeg gefunden ({where})\n{path}\nVersion {version}",
    "Segna IN e OUT (tasti I e O) oppure seleziona un elemento da eliminare.":
        "Markieren Sie IN und OUT (Tasten I und O) oder wählen Sie ein Element zum Löschen.",
    "Fotogramma {done} / {total}":
        "Frame {done} / {total}",
    "; soggetto non trovato da {time} al keyframe":
        "; Motiv nicht gefunden von {time} bis zum Keyframe",
    ", non trovato in {frames} fotogrammi":
        ", nicht gefunden in {frames} Frames",
    "formato audio inatteso":
        "unerwartetes Audioformat",
    "Scegli il carattere":
        "Schriftart wählen",
    "Cerca carattere...":
        "Schriftart suchen...",
    "{shown} / {total}  - caricamento...":
        "{shown} / {total}  - wird geladen...",
    "Caratteri della cartella font/ e di Windows, mostrati con il testo «{sample}». Clicca per scegliere.":
        "Schriftarten aus dem Ordner font/ und von Windows, gezeigt mit dem Text „{sample}“. Klicken Sie zum Auswählen.",
    "ffmpeg non trovato: scaricalo dalla pagina Configurazione.":
        "ffmpeg nicht gefunden: Laden Sie es auf der Seite Konfiguration herunter.",
    "Durata sconosciuta (file danneggiato o non riconosciuto).":
        "Unbekannte Dauer (Datei beschädigt oder nicht erkannt).",
    "Il file non contiene ne' video ne' audio riconoscibili.":
        "Die Datei enthält weder erkennbares Video noch Audio.",
    "ffmpeg non ha scritto il fotogramma.":
        "ffmpeg hat den Frame nicht geschrieben.",
    "ffmpeg: codice di uscita {code}":
        "ffmpeg: Exitcode {code}",
    "Impossibile aprire il video: {path}":
        "Das Video kann nicht geöffnet werden: {path}",
    "Testo a destra del logo":
        "Text rechts vom Logo",
    "Testo a sinistra del logo":
        "Text links vom Logo",
    "Testo sotto il logo":
        "Text unter dem Logo",
    "Riempi (taglia i bordi)":
        "Füllen (Ränder beschneiden)",
    "Intera (bande del colore)":
        "Ganz (Balken in der Farbe)",
    "Stira":
        "Strecken",
    "Al centro":
        "Mittig",
    "Sinistra":
        "Links",
    "Centro":
        "Mitte",
    "Destra":
        "Rechts",
    "Nessun elemento selezionato.\n\nClicca una clip, un effetto o una traccia audio nella timeline per vederne le proprieta'.\n\nFlusso di lavoro:\n1. Importa un video (Ctrl+I)\n2. Segna IN e OUT (tasti I e O) e taglia o elimina\n3. Aggiungi fermo immagine, velocita', testi, frecce, riquadri, zoom, pixelatura\n4. Esporta in mp4 (Ctrl+E)":
        "Kein Element ausgewählt.\n\nKlicken Sie in der Timeline auf einen Clip, einen Effekt oder eine Audiospur, um seine Eigenschaften zu sehen.\n\nArbeitsablauf:\n1. Ein Video importieren (Strg+I)\n2. IN und OUT markieren (Tasten I und O) und schneiden oder löschen\n3. Standbild, Tempo, Texte, Pfeile, Rahmen, Zoom, Verpixelung hinzufügen\n4. Als MP4 exportieren (Strg+E)",
    "Proprieta'":
        "Eigenschaften",
    "File":
        "Datei",
    "Durata":
        "Dauer",
    "Posizione":
        "Position",
    "Elimina clip":
        "Clip löschen",
    "Transizioni":
        "Übergänge",
    "Dal nero (s)":
        "Aus Schwarz (s)",
    "Al nero (s)":
        "Nach Schwarz (s)",
    "Durata (s)":
        "Dauer (s)",
    "Colore sfondo":
        "Hintergrundfarbe",
    "nessuna":
        "keine",
    "Elimina slide":
        "Folie löschen",
    "Tempo":
        "Zeit",
    "Inizio (s)":
        "Anfang (s)",
    "Fine (s)":
        "Ende (s)",
    "Elimina effetto":
        "Effekt löschen",
    "Stato":
        "Status",
    "Keyframe qui (fissa la posizione)":
        "Keyframe hier (Position fixieren)",
    "Audio originale attivo":
        "Originalton aktiv",
    "Volume":
        "Lautstärke",
    "Dissolvenze":
        "Blenden",
    "All'inizio (s)":
        "Am Anfang (s)",
    "Alla fine (s)":
        "Am Ende (s)",
    "Elimina l'audio originale":
        "Originalton löschen",
    "Pezzo":
        "Stück",
    "Audio di questo pezzo":
        "Audio dieses Stücks",
    "Volume di questo pezzo":
        "Lautstärke dieses Stücks",
    "Entrata (s)":
        "Einblenden (s)",
    "Uscita (s)":
        "Ausblenden (s)",
    "Elimina audio di questo pezzo":
        "Audio dieses Stücks löschen",
    "Nome":
        "Name",
    "Porzione del file":
        "Ausschnitt der Datei",
    "Dall'istante (s)":
        "Ab Zeitpunkt (s)",
    "All'istante (s)":
        "Bis Zeitpunkt (s)",
    "Muta":
        "Stumm",
    "Elimina traccia":
        "Spur löschen",
    "video":
        "Video",
    "Istante sorgente (s)":
        "Quellzeitpunkt (s)",
    "Taglio nel video sorgente":
        "Schnitt im Quellvideo",
    "Audio originale di questa clip":
        "Originalton dieses Clips",
    "Volume audio originale (tutto il progetto)":
        "Lautstärke Originalton (ganzes Projekt)",
    "Velocita' (sotto 1x rallenta)":
        "Tempo (unter 1x verlangsamt)",
    "Mostra orologio con la velocita'":
        "Uhr mit dem Tempo anzeigen",
    "Orologio (tutto il progetto)":
        "Uhr (ganzes Projekt)",
    "Dimensione (px)":
        "Größe (px)",
    "Colore":
        "Farbe",
    "Opacita' sfondo":
        "Deckkraft Hintergrund",
    "Fusione con la succ. (s)":
        "Überblendung mit dem nächsten (s)",
    "Slide di apertura":
        "Vorspannfolie",
    "Adattamento":
        "Anpassung",
    "Allineamento":
        "Ausrichtung",
    "Ombra":
        "Schatten",
    "Opacita' del testo":
        "Deckkraft des Textes",
    "Sfondo dietro il testo":
        "Hintergrund hinter dem Text",
    "Modifica testo...":
        "Text bearbeiten...",
    "fermo":
        "fest",
    "Ripeti inseguimento dal cursore":
        "Verfolgung ab Cursor wiederholen",
    "Segui il soggetto":
        "Dem Motiv folgen",
    "Non seguire piu'":
        "Nicht mehr folgen",
    "nessuno":
        "keiner",
    "Togli keyframe al cursore":
        "Keyframe am Cursor entfernen",
    "Cancella i punti selezionati":
        "Gewählte Punkte löschen",
    "il file non ha audio":
        "die Datei hat kein Audio",
    "= cursore":
        "= Cursor",
    "Dal nero: la clip compare dal nero. Al nero: sparisce nel nero. Fusione: la clip sfuma nella successiva, a cavallo del taglio (la durata del video non cambia). Anche l'audio sale e scende. 0 = taglio netto.":
        "Aus Schwarz: der Clip erscheint aus dem Schwarz. Nach Schwarz: er verschwindet ins Schwarz. Überblendung: der Clip geht in den nächsten über, über den Schnitt hinweg (die Videodauer ändert sich nicht). Auch der Ton wird ein- und ausgeblendet. 0 = harter Schnitt.",
    "La slide e' un fondo a tinta unita o un'immagine adattata alla misura del video. Testi e immagini si mettono sopra con gli strumenti Testo e Immagine: con il cursore sulla slide durano quanto lei.":
        "Die Folie ist ein einfarbiger Hintergrund oder ein Bild, an die Videogröße angepasst. Texte und Bilder setzen Sie mit den Werkzeugen Text und Bild darüber: steht der Cursor auf der Folie, dauern sie so lang wie sie.",
    "Larghezza (px)":
        "Breite (px)",
    "Opacita'":
        "Deckkraft",
    "Dove l'inseguimento sbaglia: porta il cursore li' e trascina la figura sul soggetto (dagli angoli per la misura). Diventa un keyframe: il tratto prima viene corretto e l'inseguimento riparte da li' fino al keyframe successivo.\nNella timeline, sulla barra dell'effetto, i keyframe sono rombi e i punti dell'inseguimento pallini. Clic: seleziona e porta il cursore; Maiusc+clic: intervallo; Ctrl+clic: aggiunge o toglie. Canc o tasto destro: cancella i selezionati (li' la figura va dritta fra i punti rimasti).":
        "Wo die Verfolgung danebenliegt: Setzen Sie den Cursor dorthin und ziehen Sie die Figur auf das Motiv (an den Ecken für die Größe). Daraus wird ein Keyframe: der Abschnitt davor wird korrigiert, und die Verfolgung startet von dort neu bis zum nächsten Keyframe.\nIn der Timeline, auf dem Balken des Effekts, sind Keyframes Rauten und Verfolgungspunkte Kreise. Klick: auswählen und Cursor setzen; Umschalt+Klick: Bereich; Strg+Klick: hinzufügen oder entfernen. Entf oder rechte Maustaste: Gewählte löschen (dort verläuft die Figur gerade zwischen den verbleibenden Punkten).",
    "< Prec.":
        "< Vorh.",
    "Succ. >":
        "Nächst. >",
    "Centra orizz.":
        "Horiz. zentrieren",
    "Centra vert.":
        "Vert. zentrieren",
    "Valgono per l'audio originale di tutto il video: sale all'inizio e scende alla fine. Canc spegne tutto l'audio originale (il video resta). Per un solo pezzo clicca la sua barra nella riga dell'audio.":
        "Gelten für den Originalton des ganzen Videos: er wird am Anfang ein- und am Ende ausgeblendet. Entf schaltet den gesamten Originalton stumm (das Video bleibt). Für ein einzelnes Stück klicken Sie seinen Balken in der Audiozeile.",
    "Per togliere solo un tratto d'audio: segna IN e OUT (tasti I e O) e premi Canc con l'audio selezionato: il video resta. Oppure taglia con S e seleziona il pezzo d'audio: Canc lo elimina, qui ne regoli volume e dissolvenze.":
        "Um nur einen Teil des Tons zu entfernen: Markieren Sie IN und OUT (Tasten I und O) und drücken Sie Entf bei gewähltem Audio: das Video bleibt. Oder schneiden Sie mit S und wählen Sie das Audiostück: Entf löscht es, hier regeln Sie Lautstärke und Blenden.",
    "Il volume sale da zero all'inizio della traccia e scende a zero alla fine.":
        "Die Lautstärke steigt am Anfang der Spur von null an und fällt am Ende auf null.",
    "slide":
        "Folie",
    "Clip: {kind}":
        "Clip: {kind}",
    "Traccia audio":
        "Audiospur",
    "Slide di chiusura":
        "Abspannfolie",
    "Togli":
        "Entfernen",
    "Sull'anteprima: trascina per spostare, dagli angoli per ingrandire, doppio clic per riscriverlo.":
        "In der Vorschau: ziehen zum Verschieben, an den Ecken zum Vergrößern, Doppelklick zum Umschreiben.",
    "Largh.":
        "Breite",
    "  Alt.":
        "  Höhe",
    "Spessore bordo":
        "Randstärke",
    "Riempimento":
        "Füllung",
    "Opacita' riempimento":
        "Deckkraft Füllung",
    "Il contenuto della figura fa da modello: la figura segue il soggetto nei fotogrammi successivi; quando esce dall'inquadratura l'effetto finisce.":
        "Der Inhalt der Figur dient als Vorlage: die Figur folgt dem Motiv in den nächsten Frames; verlässt es das Bild, endet der Effekt.",
    "segue il soggetto ({points} punti)":
        "folgt dem Motiv ({points} Punkte)",
    "Effetto: {name}":
        "Effekt: {name}",
    "Audio originale (un pezzo)":
        "Originalton (ein Stück)",
    "Carattere":
        "Schriftart",
    "Sull'anteprima: trascina per spostarla, dagli angoli per ridimensionarla (le proporzioni restano quelle dell'immagine).":
        "In der Vorschau: ziehen zum Verschieben, an den Ecken zum Skalieren (das Seitenverhältnis des Bildes bleibt erhalten).",
    "Coda X":
        "Ende X",
    "Punta X":
        "Spitze X",
    "Spessore":
        "Stärke",
    "Audio originale (tutto)":
        "Originalton (gesamt)",
    "Area da ingrandire":
        "Zu vergrößernder Bereich",
    "Forma":
        "Form",
    "Angoli (rettangolare)":
        "Ecken (rechteckig)",
    "Contorno colorato sull'area ingrandita":
        "Farbige Kontur um den vergrößerten Bereich",
    "Linea fra l'area e il riquadro":
        "Linie zwischen Bereich und Rahmen",
    "Riquadro ingrandito":
        "Vergrößerter Rahmen",
    "L'area fa da modello: lo zoom segue l'oggetto nei fotogrammi successivi, il riquadro ingrandito resta dove l'hai messo. Se l'oggetto esce dall'inquadratura lo zoom finisce.":
        "Der Bereich dient als Vorlage: der Zoom folgt dem Objekt in den nächsten Frames, der vergrößerte Rahmen bleibt, wo Sie ihn platziert haben. Verlässt das Objekt das Bild, endet der Zoom.",
    "Rettangolare":
        "Rechteckig",
    "Ingrandimento":
        "Vergrößerung",
    "Larghezza":
        "Breite",
    "Per tutto il video":
        "Für das ganze Video",
    "Largh. logo (px)":
        "Logobreite (px)",
    "Dimensione testo":
        "Textgröße",
    "Colore testo":
        "Textfarbe",
    "Disposizione":
        "Anordnung",
    "Ombra sotto il testo":
        "Schatten unter dem Text",
    "Sfondo":
        "Hintergrund",
    "Sfondo sotto logo e scritta":
        "Hintergrund unter Logo und Schrift",
    "Opacita' di tutto":
        "Deckkraft gesamt",
    "Angolo":
        "Ecke",
    "Il colore vale per il bordo del riquadro, il contorno dell'area e la linea. L'area scelta viene mostrata ingrandita nel riquadro, sopra il video, per la durata dell'effetto. Sull'anteprima: trascina l'area o il riquadro, ridimensiona l'area dagli angoli.":
        "Die Farbe gilt für den Rand des Rahmens, die Kontur des Bereichs und die Linie. Der gewählte Bereich wird vergrößert im Rahmen über dem Video gezeigt, für die Dauer des Effekts. In der Vorschau: Bereich oder Rahmen ziehen, Bereich an den Ecken skalieren.",
    "Pixelatura":
        "Verpixelung",
    "Grandezza pixel":
        "Pixelgröße",
    "Resta fermo nel punto scelto. Sull'anteprima trascinalo per spostarlo, tira un angolo per ingrandire o rimpicciolire logo e testo insieme. I valori proposti per i prossimi si cambiano in Configurazione.":
        "Bleibt an der gewählten Stelle fest. In der Vorschau ziehen Sie es zum Verschieben, an einer Ecke zum Vergrößern oder Verkleinern von Logo und Text zusammen. Die Vorschlagswerte für die nächsten ändern Sie in der Konfiguration.",
    "fisso":
        "fest",
    "Soggetto perso":
        "Motiv verloren",
    "Ripeti l'inseguimento dopo aver cambiato inizio o fine.":
        "Wiederholen Sie die Verfolgung nach Änderung von Anfang oder Ende.",
    "{points} punti":
        "{points} Punkte",
    "{frames} fotogrammi":
        "{frames} Frames",
    "Trascina sull'anteprima per disegnare il riquadro":
        "Ziehen Sie in der Vorschau, um den Rahmen zu zeichnen",
    "Trascina sull'anteprima per disegnare l'ovale":
        "Ziehen Sie in der Vorschau, um das Oval zu zeichnen",
    "Trascina sull'anteprima un rettangolo sull'oggetto da ingrandire":
        "Ziehen Sie in der Vorschau ein Rechteck über das zu vergrößernde Objekt",
    "Clicca dove far apparire il riquadro ingrandito  -  {factor}x  (rotellina o tasti 2, 3, 4, 6, 8)":
        "Klicken Sie, wo der vergrößerte Rahmen erscheinen soll  -  {factor}x  (Mausrad oder Tasten 2, 3, 4, 6, 8)",
    "Trascina sull'anteprima l'area da pixelare: verra' inseguita nei fotogrammi successivi":
        "Ziehen Sie in der Vorschau den zu verpixelnden Bereich: er wird in den nächsten Frames verfolgt",
    "Trascina dalla coda alla punta della freccia":
        "Ziehen Sie vom Ende zur Spitze des Pfeils",
    "Clicca sull'anteprima dove mettere il testo":
        "Klicken Sie in der Vorschau, wo der Text hin soll",
    "Importa un video per vedere l'anteprima":
        "Importieren Sie ein Video, um die Vorschau zu sehen",
    "segue il soggetto":
        "folgt dem Motiv",
    "Logo e operatore":
        "Logo und Bediener",
    "Slide di apertura: {text}":
        "Vorspannfolie: {text}",
    "Slide di chiusura: {text}":
        "Abspannfolie: {text}",
    "Slide: {text}":
        "Folie: {text}",
    "Fermo immagine ({name})":
        "Standbild ({name})",
    "Percorso del progetto mancante":
        "Projektpfad fehlt",
    "La timeline e' vuota: importa almeno un video.":
        "Die Timeline ist leer: Importieren Sie mindestens ein Video.",
    "Preparazione dei segmenti":
        "Vorbereitung der Segmente",
    "Disegno delle sovraimpressioni":
        "Zeichnen der Einblendungen",
    "Preparazione":
        "Vorbereitung",
    "Completato":
        "Abgeschlossen",
    "ffmpeg non ha scritto il file di uscita.":
        "ffmpeg hat die Ausgabedatei nicht geschrieben.",
    "Disegno del contorno dello zoom":
        "Zeichnen der Zoom-Kontur",
    "Disegno dell'orologio {speed}":
        "Zeichnen der Uhr {speed}",
    "Codifica: {done} / {total}":
        "Kodierung: {done} / {total}",
    "Audio originale":
        "Originalton",
    "muto":
        "stumm",
    "immagine":
        "Bild",
    "orologio":
        "Uhr",
    "senza audio":
        "ohne Audio",
    "audio":
        "Audio",
    "{name} ({points} punti)":
        "{name} ({points} Punkte)",
    "{name} (fisso)":
        "{name} (fest)",
    "{name} (segue)":
        "{name} (folgt)",
    "audio {volume:.0f} %":
        "Audio {volume:.0f} %",
    "Risposta inattesa dal sito di download di ffmpeg.":
        "Unerwartete Antwort der ffmpeg-Downloadseite.",
    "Il download automatico e' disponibile solo su Windows: installa ffmpeg con il gestore di pacchetti del sistema.":
        "Der automatische Download ist nur unter Windows verfügbar: Installieren Sie ffmpeg mit der Paketverwaltung des Systems.",
    "licenza di VitTrack":
        "Lizenz von VitTrack",
    "Il file scaricato non e' un archivio zip valido.":
        "Die heruntergeladene Datei ist kein gültiges Zip-Archiv.",
    "Estrazione di ffmpeg":
        "ffmpeg wird entpackt",
    "L'ffmpeg scaricato non si avvia su questo PC.":
        "Das heruntergeladene ffmpeg läuft auf diesem PC nicht.",
    "Il modello scaricato non corrisponde a quello atteso (impronta SHA-256 diversa).":
        "Das heruntergeladene Modell entspricht nicht dem erwarteten (abweichender SHA-256-Fingerabdruck).",
    "Il pacchetto scaricato non contiene {file}.":
        "Das heruntergeladene Paket enthält {file} nicht.",
    "{file} manca dopo l'estrazione.":
        "{file} fehlt nach dem Entpacken.",
    "Impossibile controllare l'ultima versione di ffmpeg: {error}":
        "Die neueste ffmpeg-Version kann nicht geprüft werden: {error}",
    "Download di {name} fallito: {error}":
        "Download von {name} fehlgeschlagen: {error}",
    "Impossibile aggiornare '{folder}': file in uso. Aspetta la fine dell'esportazione e riprova.":
        "'{folder}' kann nicht aktualisiert werden: Dateien in Benutzung. Warten Sie das Ende des Exports ab und versuchen Sie es erneut.",
    "OpenCV non riesce a caricare il modello: {error}":
        "OpenCV kann das Modell nicht laden: {error}",
    "Archivio non valido: percorso sospetto '{path}'.":
        "Ungültiges Archiv: verdächtiger Pfad '{path}'.",
    "Download di {name}":
        "Download von {name}",
    "Nessun fotogramma all'istante di partenza.":
        "Kein Frame zum Startzeitpunkt.",
    "INFO":
        "INFO",
    "CONFERMA":
        "BESTÄTIGEN",
    "ATTENZIONE":
        "WARNUNG",
    "ERRORE":
        "FEHLER",
    "OK":
        "OK",
    "Annulla":
        "Abbrechen",
    "Si'":
        "Ja",
    "No":
        "Nein",
    "Interruzione...":
        "Wird abgebrochen...",
    "Invio va a capo, Ctrl+Invio conferma.":
        "Eingabetaste für neue Zeile, Strg+Eingabetaste bestätigt.",
    "Allineamento delle righe":
        "Ausrichtung der Zeilen",
    "Scrivi il testo.":
        "Schreiben Sie den Text.",
    "Fondo scuro":
        "Dunkler Hintergrund",
    "Centra nel video":
        "Im Video zentrieren",
    "Dimensione non valida.":
        "Ungültige Größe.",
    "{field}: valore fra {min:g} e {max:g}.":
        "{field}: Wert zwischen {min:g} und {max:g}.",
    "{field}: inserisci un numero.":
        "{field}: Geben Sie eine Zahl ein.",
    "Tempo trascorso dall'inizio del video: clic dove metterlo, poi si sposta":
        "Verstrichene Zeit seit Videobeginn: klicken, wo sie hin soll, danach verschiebbar",
    "Tempo trascorso aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.":
        "Verstrichene Zeit hinzugefügt: Ziehen Sie sie, wohin Sie möchten, und passen Sie sie im Bereich rechts an.",
    "minuti:secondi (01:23)":
        "Minuten:Sekunden (01:23)",
    "ore:minuti:secondi (00:01:23)":
        "Stunden:Minuten:Sekunden (00:01:23)",
    "con i decimi (01:23.4)":
        "mit Zehnteln (01:23.4)",
    "dall'inizio del video":
        "ab Videobeginn",
    "dall'inizio dell'effetto":
        "ab Effektbeginn",
    "Tempo trascorso":
        "Verstrichene Zeit",
    "Formato":
        "Format",
    "Conta":
        "Zählt",
    "Testo davanti":
        "Text davor",
    "Sfondo dietro il tempo":
        "Hintergrund hinter der Zeit",
    "Sull'anteprima: trascinalo dove vuoi, dagli angoli per ingrandirlo.":
        "In der Vorschau: ziehen, wohin Sie möchten, an den Ecken zum Vergrößern.",
    "Clicca sull'anteprima dove mettere il tempo trascorso":
        "Klicken Sie in der Vorschau, wo die verstrichene Zeit hin soll",
    "Disegno del tempo trascorso":
        "Zeichnen der verstrichenen Zeit",

    # ------------------------------------------------------- riproduzione
    '10 fotogrammi indietro (Ctrl+Sinistra)': '10 Frames zurück (Strg+Links)',
    "Riproduci all'indietro / pausa (Maiusc+Spazio), senza audio": 'Rückwärts abspielen / Pause (Umschalt+Leertaste), ohne Ton',
    '10 fotogrammi avanti (Ctrl+Destra)': '10 Frames vor (Strg+Rechts)',
    'Allunga fino al cursore': 'Bis zum Cursor verlängern',
    'Interrompi al cursore': 'Am Cursor beenden',
    '{effect} allungato fino a {t:.2f} s.': '{effect} bis {t:.2f} s verlängert.',
    '{effect} interrotto a {t:.2f} s.': '{effect} bei {t:.2f} s beendet.',
    "{effect} nascosto: non compare in anteprima ne' nel video esportato.": '{effect} ausgeblendet: erscheint weder in der Vorschau noch im exportierten Video.',
    '{effect} di nuovo visibile.': '{effect} wieder sichtbar.',
    '{zoom}% - trascina per spostarti, doppio clic centrale: adatta': '{zoom}% - ziehen zum Verschieben, Doppelklick mittlere Taste: einpassen',
    'Fotogrammi': 'Frames',
    "Numero del fotogramma dall'inizio del video: clic dove metterlo, poi si sposta": 'Framenummer ab Videobeginn: dorthin klicken, wo sie stehen soll, dann verschieben',
    'Numero del fotogramma aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.': 'Framenummer hinzugefügt: an die gewünschte Stelle ziehen, im Bereich rechts anpassen.',
    'Numero del fotogramma': 'Framenummer',
    'Primo fotogramma': 'Erster Frame',
    "Clicca sull'anteprima dove mettere il numero del fotogramma": 'In der Vorschau dorthin klicken, wo die Framenummer stehen soll',
    'Anteprima': 'Vorschau',
    'Anteprima riattaccata.': 'Vorschau wieder angedockt.',
    "Riattacca l'anteprima alla finestra principale": 'Vorschau wieder im Hauptfenster andocken',
    "Stacca l'anteprima in una finestra a parte (piu' spazio per la timeline)": 'Vorschau in ein eigenes Fenster lösen (mehr Platz für die Timeline)',
    'Anteprima in una finestra a parte: chiudila o usa il pulsante in alto a destra per riattaccarla.': 'Vorschau in eigenem Fenster: schließen oder mit der Schaltfläche oben rechts wieder andocken.',
    "Trascina un rettangolo attorno al soggetto: la freccia lo seguira' tenendo la punta dov'e'.": 'Ziehe ein Rechteck um das Motiv: der Pfeil folgt ihm, die Spitze bleibt, wo sie ist.',
    'soggetto della freccia': 'Motiv des Pfeils',
    "Si disegna un rettangolo attorno al soggetto: la freccia lo segue nei fotogrammi successivi tenendo la punta su di lui; quando esce dall'inquadratura l'effetto finisce.": 'Ein Rechteck um das Motiv ziehen: der Pfeil folgt ihm in den nächsten Frames und hält die Spitze darauf; verlässt es das Bild, endet der Effekt.',
    'Scegli un altro soggetto': 'Anderes Motiv wählen',
    'Trascina un rettangolo attorno al soggetto che la freccia deve seguire': 'Ziehe ein Rechteck um das Motiv, dem der Pfeil folgen soll',
}
