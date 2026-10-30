# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Español: traduzione dei testi dell'interfaccia di EditSimple.

La chiave e' il testo italiano cosi' come compare nel codice (in tr() e N_()),
il valore la sua traduzione. I segnaposto tra graffe vanno lasciati identici.
Dopo ogni modifica:

    .venv\\Scripts\\python.exe scripts\\check_i18n.py es
"""

from __future__ import annotations

NAME = "Español"

CATALOG: dict[str, str] = {
    # ---------------------------------------------------------------- avvio
    "Impossibile avviare l'interfaccia: {error}\n\nInstalla le dipendenze con:\n    {command}":
        "No se puede iniciar la interfaz: {error}\n\nInstale las dependencias con:\n    {command}",

    # ------------------------------------------------------------------ app
    "In alto a sinistra": "Arriba a la izquierda",
    "In alto a destra": "Arriba a la derecha",
    "In basso a sinistra": "Abajo a la izquierda",
    "In basso a destra": "Abajo a la derecha",
    "Progetto EditSimple": "Proyecto EditSimple",
    "Tutti i file": "Todos los archivos",
    "Apertura (all'inizio)": "Apertura (al principio)",
    "Chiusura (alla fine)": "Cierre (al final)",
    "Apri progetto... (Ctrl+O)": "Abrir proyecto... (Ctrl+O)",
    "Progetto": "Proyecto",
    "Nuovo": "Nuevo",
    "Nuovo progetto (Ctrl+N)": "Nuevo proyecto (Ctrl+N)",
    "Apri": "Abrir",
    "Apri progetto (Ctrl+O)": "Abrir proyecto (Ctrl+O)",
    "Salva": "Guardar",
    "Salva progetto (Ctrl+S)": "Guardar proyecto (Ctrl+S)",
    "Annulla (Ctrl+Z)": "Deshacer (Ctrl+Z)",
    "Ripeti (Ctrl+Y)": "Rehacer (Ctrl+Y)",
    "Clip": "Clip",
    "Importa video": "Importar vídeo",
    "Importa un video in coda o al cursore (Ctrl+I)": "Importa un vídeo al final o en el cursor (Ctrl+I)",
    "Audio": "Audio",
    "Aggiungi una traccia audio (commento, musica) al cursore":
        "Añade una pista de audio (comentario, música) en el cursor",
    "Taglia": "Cortar",
    "Taglia la clip al cursore (S)": "Corta el clip en el cursor (S)",
    "Elimina": "Eliminar",
    "Elimina la porzione IN-OUT o l'elemento selezionato (Canc)":
        "Elimina la porción IN-OUT o el elemento seleccionado (Supr)",
    "Fermo": "Congelar",
    "Fermo immagine del fotogramma al cursore (F)": "Congela el fotograma del cursor (F)",
    "Slide": "Diapositiva",
    "Inserisci una slide": "Inserta una diapositiva",
    "Velocita'": "Velocidad",
    "Velocita' della porzione IN-OUT: piu' veloce o rallentata (V)":
        "Velocidad de la porción IN-OUT: más rápida o ralentizada (V)",
    "Sovraimpressioni": "Superposiciones",
    "Testo": "Texto",
    "Testo (T)": "Texto (T)",
    "Immagine": "Imagen",
    "Immagine sopra il video, da spostare e ridimensionare":
        "Imagen sobre el vídeo, para mover y redimensionar",
    "Logo": "Logo",
    "Logo e testo dell'operatore, fermi in un angolo (L)":
        "Logo y texto del operador, fijos en una esquina (L)",
    "Riquadro": "Recuadro",
    "Riquadro (R): puo' seguire il soggetto": "Recuadro (R): puede seguir al sujeto",
    "Ovale": "Óvalo",
    "Ovale (E): puo' seguire il soggetto": "Óvalo (E): puede seguir al sujeto",
    "Freccia": "Flecha",
    "Freccia (A): puo' seguire il soggetto": "Flecha (A): puede seguir al sujeto",
    "Zoom": "Zoom",
    "Zoom rettangolare: l'area scelta in un riquadro ingrandito (Z)":
        "Zoom rectangular: el área elegida en un recuadro ampliado (Z)",
    "Zoom ovale: l'area scelta in un ovale ingrandito (Maiusc+Z)":
        "Zoom ovalado: el área elegida en un óvalo ampliado (Mayús+Z)",
    "Pixel": "Píxel",
    "Pixelatura rettangolare che insegue il soggetto (P)":
        "Pixelado rectangular que sigue al sujeto (P)",
    "Pixelatura ovale che insegue il soggetto (K)": "Pixelado ovalado que sigue al sujeto (K)",
    "Uscita": "Salida",
    "Esporta MP4": "Exportar MP4",
    "Esporta il video finale (Ctrl+E)": "Exporta el vídeo final (Ctrl+E)",
    "Inseguimento (VitTrack)": "Seguimiento (VitTrack)",
    "Esportazione": "Exportación",
    "Logo e testo dell'operatore": "Logo y texto del operador",
    "Angoli arrotondati": "Esquinas redondeadas",
    "Crediti": "Créditos",
    "Lingua": "Idioma",
    "Impostazioni salvate.": "Ajustes guardados.",
    "Download di ffmpeg": "Descarga de ffmpeg",
    "Download di VitTrack": "Descarga de VitTrack",
    "Progetto non salvato": "Proyecto no guardado",
    "Salvare le modifiche al progetto?": "¿Guardar los cambios del proyecto?",
    "Nuovo progetto.": "Nuevo proyecto.",
    "Lettura del video...": "Leyendo el vídeo...",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}":
        "Importado {file}: {width}x{height}, {fps:g} fps, {duration}",
    "Importato {file}: {width}x{height}, {fps:g} fps, {duration}, senza audio":
        "Importado {file}: {width}x{height}, {fps:g} fps, {duration}, sin audio",
    "Audio di questo pezzo eliminato (il video resta). Ctrl+Z per riaverlo.":
        "Audio de este fragmento eliminado (el vídeo se queda). Ctrl+Z para recuperarlo.",
    "Clip eliminata.": "Clip eliminado.",
    "Fermo immagine": "Imagen congelada",
    "Nuovo testo": "Nuevo texto",
    "Testo aggiunto: trascinalo, ingrandiscilo dagli angoli, doppio clic per riscriverlo.":
        "Texto añadido: arrástrelo, amplíelo desde las esquinas, doble clic para reescribirlo.",
    "Modifica testo": "Editar texto",
    "Immagine aggiunta: trascinala per spostarla, dagli angoli per ridimensionarla.":
        "Imagen añadida: arrástrela para moverla, desde las esquinas para redimensionarla.",
    "Pixelatura con inseguimento": "Pixelado con seguimiento",
    "Cancellati {count} punti del percorso (il primo resta: e' la partenza della figura).":
        "Borrados {count} puntos del recorrido (el primero se queda: es el inicio de la figura).",
    "Cancellati {count} punti del percorso.": "Borrados {count} puntos del recorrido.",
    "Inseguimento del soggetto": "Seguimiento del sujeto",
    "Esportazione in corso": "Exportación en curso",
    "montaggio video per presentazioni": "edición de vídeo para presentaciones",
    "PROGETTO": "PROYECTO",
    "nuovo": "nuevo",
    "Nessun video": "Ningún vídeo",
    "Montaggio": "Edición",
    "Configura": "Configurar",
    "Riproduci / pausa (Spazio)": "Reproducir / pausa (Espacio)",
    "larghezza logo % del video": "ancho del logo % del vídeo",
    "altezza testo % del lato corto": "altura del texto % del lado corto",
    "distanza dai bordi % del lato corto": "distancia a los bordes % del lado corto",
    "opacita' %": "opacidad %",
    "angoli arrotondati %": "esquinas redondeadas %",
    "sfondo del testo": "fondo del texto",
    "riquadro": "recuadro",
    "zoom rettangolare": "zoom rectangular",
    "pixel rettangolare": "píxel rectangular",
    "Colore del testo": "Color del texto",
    "Colore dello sfondo": "Color del fondo",
    "Immagine del logo": "Imagen del logo",
    "Questa immagine non si apre.": "Esta imagen no se puede abrir.",
    "Controllo in corso...": "Comprobando...",
    "Pronto.": "Listo.",
    "ffmpeg non e' stato trovato. Scaricalo dal riquadro FFmpeg della pagina Configurazione: senza, non si possono importare ne' esportare video.":
        "ffmpeg no encontrado. Descárguelo desde el recuadro FFmpeg de la página Configuración: "
        "sin él no se pueden importar ni exportar vídeos.",
    "ffmpeg non e' stato trovato. Installalo con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) o copia un eseguibile ffmpeg in tools/ffmpeg/: senza, non si possono importare ne' esportare video.":
        "ffmpeg no encontrado. Instálelo con el gestor de paquetes del sistema (por ejemplo sudo apt install ffmpeg) o copie un ejecutable de ffmpeg en tools/ffmpeg/: sin él no se pueden importar ni exportar vídeos.",
    "Non salvare": "No guardar",
    "Niente da annullare.": "Nada que deshacer.",
    "inizio": "inicio",
    "fine": "fin",
    "Apri progetto": "Abrir proyecto",
    "File mancanti": "Archivos que faltan",
    "Salva progetto": "Guardar proyecto",
    "Dove inserire il video?": "¿Dónde insertar el vídeo?",
    "Importazione": "Importación",
    "Il file non contiene video. Per l'audio usa il pulsante Audio.":
        "El archivo no contiene vídeo. Para el audio use el botón Audio.",
    "Importa prima un video.": "Importe primero un vídeo.",
    "Aggiungi traccia audio": "Añadir pista de audio",
    "Il file non contiene audio.": "El archivo no contiene audio.",
    "Il cursore e' gia' su un confine fra clip.": "El cursor ya está en un límite entre clips.",
    "Importa prima un video: la slide prende la sua misura.":
        "Importe primero un vídeo: la diapositiva toma su tamaño.",
    "Al cursore ({time})": "En el cursor ({time})",
    "Dove": "Dónde",
    "Durata (secondi)": "Duración (segundos)",
    "Crea": "Crear",
    "La slide e' un fondo a tinta unita (il colore si sceglie nel pannello). Testi e immagini si aggiungono sopra con gli strumenti Testo e Immagine.":
        "La diapositiva es un fondo de color liso (el color se elige en el panel). "
        "Textos e imágenes se añaden encima con las herramientas Texto e Imagen.",
    "Slide di chiusura aggiunta alla fine: regolala nel pannello a destra.":
        "Diapositiva de cierre añadida al final: ajústela en el panel de la derecha.",
    "Inserisci": "Insertar",
    "Applica": "Aplicar",
    "Effetti": "Efectos",
    "Pixel ovale": "Píxel ovalado",
    "Pixel rettangolare": "Píxel rectangular",
    "Zoom ovale (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Zoom ovalado (rectángulo sobre el objeto, luego clic donde poner el recuadro)",
    "Zoom (rettangolo sull'oggetto, poi clic dove mettere il riquadro)":
        "Zoom (rectángulo sobre el objeto, luego clic donde poner el recuadro)",
    "Carica l'immagine del logo e scrivi il testo dell'operatore nella pagina Configura, poi premi di nuovo Logo.":
        "Cargue la imagen del logo y escriba el texto del operador en la página Configurar, "
        "luego pulse de nuevo Logo.",
    "Logo e operatore aggiunti per tutto il video: trascinali sull'anteprima o regolali nel pannello.":
        "Logo y operador añadidos a todo el vídeo: arrástrelos en la vista previa o ajústelos en el panel.",
    "Zoom aggiunto (fermo: sul fermo immagine non c'e' nulla da inseguire).":
        "Zoom añadido (fijo: en la imagen congelada no hay nada que seguir).",
    "Insegui": "Seguir",
    "Keyframe": "Keyframe",
    "Porta il cursore dentro l'effetto.": "Lleve el cursor dentro del efecto.",
    "Nessun keyframe al cursore: usa Prec. / Succ. per andarci.":
        "Ningún keyframe en el cursor: use Ant. / Sig. para ir a uno.",
    "Il primo punto del percorso non si cancella: e' la partenza della figura.":
        "El primer punto del recorrido no se borra: es el inicio de la figura.",
    "Seleziona prima dei punti sulla barra dell'effetto nella timeline (clic, Maiusc+clic per un intervallo, Ctrl+clic per aggiungerne).":
        "Seleccione primero puntos en la barra del efecto en la línea de tiempo "
        "(clic, Mayús+clic para un intervalo, Ctrl+clic para añadir).",
    "Nessun altro keyframe in quella direzione.": "No hay más keyframes en esa dirección.",
    "Inseguimento": "Seguimiento",
    "L'inseguimento funziona solo su una clip video (non su un fermo immagine): la figura resta ferma.":
        "El seguimiento solo funciona en un clip de vídeo (no en una imagen congelada): la figura queda fija.",
    "Testo di prova": "Texto de prueba",
    "La timeline e' vuota.": "La línea de tiempo está vacía.",
    "Esportazione completata": "Exportación completada",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Scarica / Aggiorna prende il build ufficiale per Windows (release essentials) da gyan.dev e tiene solo ffmpeg.exe, LICENSE e README in tools/ffmpeg/. Nessuna installazione, nessuna modifica al PATH.":
        "ffmpeg no está incluido en el programa: es un programa aparte con su propia licencia. "
        "Descargar / Actualizar toma la compilación oficial para Windows (release essentials) de gyan.dev "
        "y conserva solo ffmpeg.exe, LICENSE y README en tools/ffmpeg/. "
        "Sin instalación, sin cambios en el PATH.",
    "ffmpeg non e' incluso nel programma: e' un programma separato con la propria licenza. Su Linux e macOS si installa con il gestore di pacchetti del sistema (per esempio sudo apt install ffmpeg) oppure si mette un eseguibile ffmpeg in tools/ffmpeg/. Il download automatico vale solo per Windows.":
        "ffmpeg no está incluido en el programa: es un programa aparte con su propia licencia. En Linux y macOS se instala con el gestor de paquetes del sistema (por ejemplo sudo apt install ffmpeg) o se coloca un ejecutable de ffmpeg en tools/ffmpeg/. La descarga automática solo está disponible en Windows.",
    "Scarica / Aggiorna": "Descargar / Actualizar",
    "Apri cartella tools": "Abrir carpeta tools",
    "VitTrack e' un modello addestrato per seguire oggetti e persone: ritrova il soggetto dopo un palo o un passante e capisce quando e' perso. Viene dal repository ufficiale opencv_zoo (licenza Apache 2.0, compatibile con la GPL 3), circa 0,7 MB, in tools/vittrack/ con la sua licenza. Senza, l'inseguimento usa il confronto a modello.":
        "VitTrack es un modelo entrenado para seguir objetos y personas: recupera al sujeto tras un poste "
        "o un transeúnte y sabe cuándo lo ha perdido. Procede del repositorio oficial opencv_zoo "
        "(licencia Apache 2.0, compatible con la GPL 3), unos 0,7 MB, en tools/vittrack/ con su licencia. "
        "Sin él, el seguimiento usa la comparación con plantilla.",
    "Scarica": "Descargar",
    "Qualita' video (CRF, 15 = ottima, 28 = leggera)": "Calidad de vídeo (CRF, 15 = óptima, 28 = ligera)",
    "Velocita' di codifica (preset x264)": "Velocidad de codificación (preset x264)",
    "Audio (kbit/s)": "Audio (kbit/s)",
    "Durate proposte (secondi)": "Duraciones propuestas (segundos)",
    "Pixelatura: grandezza dei pixel e soglia dell'inseguimento (0.2-0.9)":
        "Pixelado: tamaño de los píxeles y umbral del seguimiento (0.2-0.9)",
    "Salva impostazioni": "Guardar ajustes",
    "Carica immagine del logo...": "Cargar imagen del logo...",
    "Togli logo": "Quitar logo",
    "Testo dell'operatore (nome, qualifica, data...)": "Texto del operador (nombre, cargo, fecha...)",
    "Il pulsante Logo (tasto L) mette logo e testo nell'angolo scelto, fermi per tutto il video (o solo nella porzione IN-OUT, se e' segnata). Nel progetto si possono poi spostare, ridimensionare e cambiare dal pannello a destra.":
        "El botón Logo (tecla L) pone logo y texto en la esquina elegida, fijos durante todo el vídeo "
        "(o solo en la porción IN-OUT, si está marcada). En el proyecto se pueden luego mover, "
        "redimensionar y cambiar desde el panel de la derecha.",
    "Proposti ai nuovi effetti, in % del lato corto (0 = angoli vivi, 50 = estremita' tonde); ogni effetto poi si regola nel suo pannello":
        "Propuestos para los efectos nuevos, en % del lado corto (0 = esquinas vivas, 50 = extremos redondos); "
        "luego cada efecto se ajusta en su panel",
    "nessun logo": "ningún logo",
    "La lingua dell'interfaccia cambia subito, senza riavviare.":
        "El idioma de la interfaz cambia al instante, sin reiniciar.",
    "Valore non valido": "Valor no válido",
    "Controlla i numeri inseriti.": "Compruebe los números introducidos.",
    "ffmpeg scaricato in tools/ffmpeg.": "ffmpeg descargado en tools/ffmpeg.",
    "VitTrack non scaricato: l'inseguimento usa il confronto a modello, che puo' perdere il soggetto dietro un ostacolo.":
        "VitTrack no descargado: el seguimiento usa la comparación con plantilla, "
        "que puede perder al sujeto tras un obstáculo.",
    "Modello scaricato in tools/vittrack: l'inseguimento ora lo usa.":
        "Modelo descargado en tools/vittrack: el seguimiento ya lo usa.",
    "Cartella": "Carpeta",
    "Progetto aperto: {file}": "Proyecto abierto: {file}",
    "Salvataggio": "Guardado",
    "Progetto salvato: {path}": "Proyecto guardado: {path}",
    "In coda": "Al final",
    "Al cursore": "En el cursor",
    "Traccia audio aggiunta: {name} ({duration})": "Pista de audio añadida: {name} ({duration})",
    "Clip tagliata a {time}.": "Clip cortado en {time}.",
    "Audio originale tolto fra {start} e {end} (il video resta).":
        "Audio original quitado entre {start} y {end} (el vídeo se queda).",
    "Slide di apertura aggiunta all'inizio: regolala nel pannello a destra.":
        "Diapositiva de apertura añadida al principio: ajústela en el panel de la derecha.",
    "Fermo immagine di {seconds:g} s inserito.": "Imagen congelada de {seconds:g} s insertada.",
    "Segna prima la porzione con IN e OUT (tasti I e O), oppure seleziona una clip.":
        "Marque primero la porción con IN y OUT (teclas I y O), o seleccione un clip.",
    "Mostra l'icona dell'orologio con le lancette e la velocita' sotto":
        "Muestra el icono del reloj con las agujas y la velocidad debajo",
    "Velocita' {speed} applicata fra {start} e {end}.": "Velocidad {speed} aplicada entre {start} y {end}.",
    "{effect} aggiunto: regola i valori nel pannello a destra o trascina sull'anteprima.":
        "{effect} añadido: ajuste los valores en el panel de la derecha o arrastre en la vista previa.",
    "Fino all'istante (secondi della timeline)": "Hasta el instante (segundos de la línea de tiempo)",
    "Grandezza dei pixel": "Tamaño de los píxeles",
    "Keyframe a {time}: trascina la figura per correggerla.":
        "Keyframe en {time}: arrastre la figura para corregirla.",
    "Inseguimento annullato.": "Seguimiento cancelado.",
    "Inseguimento completato: {frames} fotogrammi, {points} punti":
        "Seguimiento completado: {frames} fotogramas, {points} puntos",
    "Esportazione annullata.": "Exportación cancelada.",
    "Esportazione fallita": "Exportación fallida",
    "Esportazione fallita.": "Exportación fallida.",
    "Apri cartella": "Abrir carpeta",
    "Chiudi": "Cerrar",
    "PAGINE": "PÁGINAS",
    "Inizio (Home)": "Inicio (Inicio)",
    "Fotogramma precedente (Sinistra)": "Fotograma anterior (Izquierda)",
    "Fotogramma successivo (Destra)": "Fotograma siguiente (Derecha)",
    "Fine (Fine)": "Fin (Fin)",
    "Adatta la timeline": "Ajustar la línea de tiempo",
    "Ingrandisci la timeline (Ctrl+rotellina). Per spostarla: Alt+trascina, tasto centrale o rotellina":
        "Ampliar la línea de tiempo (Ctrl+rueda). Para desplazarla: Alt+arrastrar, botón central o rueda",
    "Riduci la timeline": "Reducir la línea de tiempo",
    "Configurazione": "Configuración",
    "fermo immagine": "imagen congelada",
    "effetti": "efectos",
    "angolo": "esquina",
    "disposizione": "disposición",
    "colore testo": "color del texto",
    "sfondo sotto logo e scritta": "fondo bajo logo y texto",
    "colore": "color",
    "Nessun logo: carica un'immagine (PNG con trasparenza, JPG...).":
        "Ningún logo: cargue una imagen (PNG con transparencia, JPG...).",
    "Immagini": "Imágenes",
    "ffmpeg NON trovato: scaricalo con il pulsante qui sotto.":
        "ffmpeg NO encontrado: descárguelo con el botón de abajo.",
    "{label}: {done:.1f} MB / {total:.1f} MB": "{label}: {done:.1f} MB / {total:.1f} MB",
    "{label}: {done:.1f} MB": "{label}: {done:.1f} MB",
    "Download fallito": "Descarga fallida",
    "{label}: {done:.2f} MB / {total:.2f} MB": "{label}: {done:.2f} MB / {total:.2f} MB",
    "{label}: {done:.2f} MB": "{label}: {done:.2f} MB",
    "Spazio riproduci  ·  ← → fotogramma  ·  I / O segna  ·  S taglia  ·  Canc elimina  ·  Ctrl+Z annulla  ·  Esc annulla disegno":
        "Espacio reproduce  ·  ← → fotograma  ·  I / O marca  ·  S corta  ·  Supr elimina  ·  "
        "Ctrl+Z deshace  ·  Esc cancela dibujo",
    "Fotogramma non leggibile: {file}": "Fotograma no legible: {file}",
    "Questi file non si trovano piu':\n\n{files}": "Estos archivos ya no se encuentran:\n\n{files}",
    "Video": "Vídeo",
    "{file}\n\nAggiungerlo in coda alla timeline oppure inserirlo al cursore ({time})?":
        "{file}\n\n¿Añadirlo al final de la línea de tiempo o insertarlo en el cursor ({time})?",
    "Eliminata la porzione {start} - {end}.": "Eliminada la porción {start} - {end}.",
    "Audio originale spento (il video resta): riaccendilo dal pannello o con Ctrl+Z.":
        "Audio original apagado (el vídeo se queda): reactívelo desde el panel o con Ctrl+Z.",
    "Porzione {start} - {end}. Da 2x in su accelera, 0.5x e 0.25x rallentano (la porzione dura il doppio o il quadruplo); con 1x si torna alla velocita' normale.":
        "Porción {start} - {end}. De 2x hacia arriba acelera, 0.5x y 0.25x ralentizan "
        "(la porción dura el doble o el cuádruple); con 1x se vuelve a la velocidad normal.",
    "Disegna: {effect}  (Esc annulla)": "Dibuje: {effect}  (Esc cancela)",
    "Logo e operatore aggiunti fra {start} e {end}: trascinali sull'anteprima o regolali nel pannello.":
        "Logo y operador añadidos entre {start} y {end}: arrástrelos en la vista previa o ajústelos en el panel.",
    "Keyframe a {time}.": "Keyframe en {time}.",
    "; soggetto uscito dall'inquadratura: l'effetto finisce a {time}":
        "; sujeto fuera del encuadre: el efecto termina en {time}",
    "; soggetto perso: l'effetto finisce a {time}": "; sujeto perdido: el efecto termina en {time}",
    "Video MP4": "Vídeo MP4",
    "Esportato {path} ({size:.1f} MB in {seconds:.0f} s).":
        "Exportado {path} ({size:.1f} MB en {seconds:.0f} s).",
    "{path}\n\n{size:.1f} MB in {seconds:.0f} secondi.\n\nAprire la cartella?":
        "{path}\n\n{size:.1f} MB en {seconds:.0f} segundos.\n\n¿Abrir la carpeta?",
    "{app} {version}. Montaggio video semplice per presentazioni: timeline, tagli, fermo immagine, avanzamento veloce, sovraimpressioni, zoom e pixelatura con inseguimento; esportazione mp4 con ffmpeg. Progetti in formato JSON.":
        "{app} {version}. Edición de vídeo sencilla para presentaciones: línea de tiempo, cortes, "
        "imagen congelada, avance rápido, superposiciones, zoom y pixelado con seguimiento; "
        "exportación mp4 con ffmpeg. Proyectos en formato JSON.",
    "{copyright}. Software libero: GNU General Public License versione 3 con termini aggiuntivi (attribuzione dell'autore, nome e logo), vedi i file LICENSE e NOTICE. Nessuna garanzia. Usa librerie e programmi di terze parti con le loro licenze (elencati in NOTICE).":
        "{copyright}. Software libre: GNU General Public License versión 3 con términos adicionales "
        "(atribución del autor, nombre y logo), véanse los archivos LICENSE y NOTICE. Sin garantía. "
        "Usa bibliotecas y programas de terceros con sus licencias (enumerados en NOTICE).",
    "cartella tools/ffmpeg": "carpeta tools/ffmpeg",
    "PATH di sistema": "PATH del sistema",
    "VitTrack presente: l'inseguimento lo usa.\n{model}": "VitTrack presente: el seguimiento lo usa.\n{model}",
    "{width}x{height}  {fps:g} fps  {clips} clip  {duration}":
        "{width}x{height}  {fps:g} fps  {clips} clips  {duration}",
    "Anteprima: {error}": "Vista previa: {error}",
    "Audio dell'anteprima non disponibile: {error}": "Audio de la vista previa no disponible: {error}",
    "Impossibile aprire il progetto:\n{error}": "No se puede abrir el proyecto:\n{error}",
    "Slide aggiunta a {time}: regolala nel pannello a destra.":
        "Diapositiva añadida en {time}: ajústela en el panel de la derecha.",
    "Il fotogramma a {time} resta fermo per questo tempo; cio' che segue scorre in avanti.":
        "El fotograma en {time} queda congelado durante este tiempo; lo que sigue se desplaza hacia delante.",
    "L'inseguimento parte dal cursore ({start}) e segue il soggetto fino a questo istante (al massimo la fine della clip: {clip_end}).":
        "El seguimiento parte del cursor ({start}) y sigue al sujeto hasta este instante "
        "(como máximo el final del clip: {clip_end}).",
    "File non trovato: {path}": "Archivo no encontrado: {path}",
    "ffmpeg trovato ({where})\n{path}\nversione {version}": "ffmpeg encontrado ({where})\n{path}\nversión {version}",
    "Segna IN e OUT (tasti I e O) oppure seleziona un elemento da eliminare.":
        "Marque IN y OUT (teclas I y O) o seleccione un elemento para eliminar.",
    "Fotogramma {done} / {total}": "Fotograma {done} / {total}",
    "; soggetto non trovato da {time} al keyframe": "; sujeto no encontrado desde {time} hasta el keyframe",
    ", non trovato in {frames} fotogrammi": ", no encontrado en {frames} fotogramas",

    # ---------------------------------------------------------- audio, fonts
    "formato audio inatteso": "formato de audio inesperado",
    "Scegli il carattere": "Elegir la fuente",
    "Cerca carattere...": "Buscar fuente...",
    "{shown} / {total}  - caricamento...": "{shown} / {total}  - cargando...",
    "Caratteri della cartella font/ e di Windows, mostrati con il testo «{sample}». Clicca per scegliere.":
        "Fuentes de la carpeta font/ y de Windows, mostradas con el texto «{sample}». Haga clic para elegir.",

    # ----------------------------------------------------------------- media
    "ffmpeg non trovato: scaricalo dalla pagina Configurazione.":
        "ffmpeg no encontrado: descárguelo desde la página Configuración.",
    "Durata sconosciuta (file danneggiato o non riconosciuto).":
        "Duración desconocida (archivo dañado o no reconocido).",
    "Il file non contiene ne' video ne' audio riconoscibili.":
        "El archivo no contiene ni vídeo ni audio reconocibles.",
    "ffmpeg non ha scritto il fotogramma.": "ffmpeg no ha escrito el fotograma.",
    "ffmpeg: codice di uscita {code}": "ffmpeg: código de salida {code}",
    "Impossibile aprire il video: {path}": "No se puede abrir el vídeo: {path}",

    # -------------------------------------------------------------- overlays
    "Testo a destra del logo": "Texto a la derecha del logo",
    "Testo a sinistra del logo": "Texto a la izquierda del logo",
    "Testo sotto il logo": "Texto debajo del logo",
    "Riempi (taglia i bordi)": "Rellenar (recorta los bordes)",
    "Intera (bande del colore)": "Entera (bandas del color)",
    "Stira": "Estirar",

    # ---------------------------------------------------------------- panels
    "Al centro": "En el centro",
    "Sinistra": "Izquierda",
    "Centro": "Centro",
    "Destra": "Derecha",
    "Nessun elemento selezionato.\n\nClicca una clip, un effetto o una traccia audio nella timeline per vederne le proprieta'.\n\nFlusso di lavoro:\n1. Importa un video (Ctrl+I)\n2. Segna IN e OUT (tasti I e O) e taglia o elimina\n3. Aggiungi fermo immagine, velocita', testi, frecce, riquadri, zoom, pixelatura\n4. Esporta in mp4 (Ctrl+E)":
        "Ningún elemento seleccionado.\n\nHaga clic en un clip, un efecto o una pista de audio en la línea "
        "de tiempo para ver sus propiedades.\n\nFlujo de trabajo:\n1. Importe un vídeo (Ctrl+I)\n"
        "2. Marque IN y OUT (teclas I y O) y corte o elimine\n"
        "3. Añada imagen congelada, velocidad, textos, flechas, recuadros, zoom, pixelado\n"
        "4. Exporte en mp4 (Ctrl+E)",
    "Proprieta'": "Propiedades",
    "File": "Archivo",
    "Durata": "Duración",
    "Posizione": "Posición",
    "Elimina clip": "Eliminar clip",
    "Transizioni": "Transiciones",
    "Dal nero (s)": "Desde negro (s)",
    "Al nero (s)": "A negro (s)",
    "Durata (s)": "Duración (s)",
    "Colore sfondo": "Color de fondo",
    "nessuna": "ninguna",
    "Elimina slide": "Eliminar diapositiva",
    "Tempo": "Tiempo",
    "Inizio (s)": "Inicio (s)",
    "Fine (s)": "Fin (s)",
    "Elimina effetto": "Eliminar efecto",
    "Stato": "Estado",
    "Keyframe qui (fissa la posizione)": "Keyframe aquí (fija la posición)",
    "Audio originale attivo": "Audio original activo",
    "Volume": "Volumen",
    "Dissolvenze": "Fundidos",
    "All'inizio (s)": "Al principio (s)",
    "Alla fine (s)": "Al final (s)",
    "Elimina l'audio originale": "Eliminar el audio original",
    "Pezzo": "Fragmento",
    "Audio di questo pezzo": "Audio de este fragmento",
    "Volume di questo pezzo": "Volumen de este fragmento",
    "Entrata (s)": "Entrada (s)",
    "Uscita (s)": "Salida (s)",
    "Elimina audio di questo pezzo": "Eliminar audio de este fragmento",
    "Nome": "Nombre",
    "Porzione del file": "Porción del archivo",
    "Dall'istante (s)": "Desde el instante (s)",
    "All'istante (s)": "Hasta el instante (s)",
    "Muta": "Silenciar",
    "Elimina traccia": "Eliminar pista",
    "video": "vídeo",
    "Istante sorgente (s)": "Instante de origen (s)",
    "Taglio nel video sorgente": "Corte en el vídeo de origen",
    "Audio originale di questa clip": "Audio original de este clip",
    "Volume audio originale (tutto il progetto)": "Volumen del audio original (todo el proyecto)",
    "Velocita' (sotto 1x rallenta)": "Velocidad (por debajo de 1x ralentiza)",
    "Mostra orologio con la velocita'": "Mostrar reloj con la velocidad",
    "Orologio (tutto il progetto)": "Reloj (todo el proyecto)",
    "Dimensione (px)": "Tamaño (px)",
    "Colore": "Color",
    "Opacita' sfondo": "Opacidad del fondo",
    "Fusione con la succ. (s)": "Fundido con el sig. (s)",
    "Slide di apertura": "Diapositiva de apertura",
    "Adattamento": "Ajuste",
    "Allineamento": "Alineación",
    "Ombra": "Sombra",
    "Opacita' del testo": "Opacidad del texto",
    "Sfondo dietro il testo": "Fondo detrás del texto",
    "Modifica testo...": "Editar texto...",
    "fermo": "fijo",
    "Ripeti inseguimento dal cursore": "Repetir seguimiento desde el cursor",
    "Segui il soggetto": "Seguir al sujeto",
    "Non seguire piu'": "Dejar de seguir",
    "nessuno": "ninguno",
    "Togli keyframe al cursore": "Quitar keyframe del cursor",
    "Cancella i punti selezionati": "Borrar los puntos seleccionados",
    "il file non ha audio": "el archivo no tiene audio",
    "= cursore": "= cursor",
    "Dal nero: la clip compare dal nero. Al nero: sparisce nel nero. Fusione: la clip sfuma nella successiva, a cavallo del taglio (la durata del video non cambia). Anche l'audio sale e scende. 0 = taglio netto.":
        "Desde negro: el clip aparece desde negro. A negro: desaparece en negro. Fundido: el clip se funde "
        "con el siguiente, a caballo del corte (la duración del vídeo no cambia). También el audio sube y baja. "
        "0 = corte seco.",
    "La slide e' un fondo a tinta unita o un'immagine adattata alla misura del video. Testi e immagini si mettono sopra con gli strumenti Testo e Immagine: con il cursore sulla slide durano quanto lei.":
        "La diapositiva es un fondo de color liso o una imagen ajustada al tamaño del vídeo. Textos e imágenes "
        "se ponen encima con las herramientas Texto e Imagen: con el cursor en la diapositiva duran lo mismo que ella.",
    "Larghezza (px)": "Ancho (px)",
    "Opacita'": "Opacidad",
    "Dove l'inseguimento sbaglia: porta il cursore li' e trascina la figura sul soggetto (dagli angoli per la misura). Diventa un keyframe: il tratto prima viene corretto e l'inseguimento riparte da li' fino al keyframe successivo.\nNella timeline, sulla barra dell'effetto, i keyframe sono rombi e i punti dell'inseguimento pallini. Clic: seleziona e porta il cursore; Maiusc+clic: intervallo; Ctrl+clic: aggiunge o toglie. Canc o tasto destro: cancella i selezionati (li' la figura va dritta fra i punti rimasti).":
        "Donde el seguimiento falla: lleve el cursor allí y arrastre la figura sobre el sujeto (desde las esquinas "
        "para el tamaño). Se convierte en un keyframe: el tramo anterior se corrige y el seguimiento vuelve a "
        "empezar desde allí hasta el keyframe siguiente.\nEn la línea de tiempo, en la barra del efecto, los "
        "keyframes son rombos y los puntos del seguimiento, círculos. Clic: selecciona y lleva el cursor; "
        "Mayús+clic: intervalo; Ctrl+clic: añade o quita. Supr o botón derecho: borra los seleccionados "
        "(allí la figura va en línea recta entre los puntos restantes).",
    "< Prec.": "< Ant.",
    "Succ. >": "Sig. >",
    "Centra orizz.": "Centrar horiz.",
    "Centra vert.": "Centrar vert.",
    "Valgono per l'audio originale di tutto il video: sale all'inizio e scende alla fine. Canc spegne tutto l'audio originale (il video resta). Per un solo pezzo clicca la sua barra nella riga dell'audio.":
        "Valen para el audio original de todo el vídeo: sube al principio y baja al final. Supr apaga todo "
        "el audio original (el vídeo se queda). Para un solo fragmento haga clic en su barra en la fila del audio.",
    "Per togliere solo un tratto d'audio: segna IN e OUT (tasti I e O) e premi Canc con l'audio selezionato: il video resta. Oppure taglia con S e seleziona il pezzo d'audio: Canc lo elimina, qui ne regoli volume e dissolvenze.":
        "Para quitar solo un tramo de audio: marque IN y OUT (teclas I y O) y pulse Supr con el audio "
        "seleccionado: el vídeo se queda. O corte con S y seleccione el fragmento de audio: Supr lo elimina, "
        "aquí se ajustan su volumen y fundidos.",
    "Il volume sale da zero all'inizio della traccia e scende a zero alla fine.":
        "El volumen sube desde cero al principio de la pista y baja a cero al final.",
    "slide": "diapositiva",
    "Clip: {kind}": "Clip: {kind}",
    "Traccia audio": "Pista de audio",
    "Slide di chiusura": "Diapositiva de cierre",
    "Togli": "Quitar",
    "Sull'anteprima: trascina per spostare, dagli angoli per ingrandire, doppio clic per riscriverlo.":
        "En la vista previa: arrastre para mover, desde las esquinas para ampliar, doble clic para reescribirlo.",
    "Largh.": "Ancho",
    "  Alt.": "  Alto",
    "Spessore bordo": "Grosor del borde",
    "Riempimento": "Relleno",
    "Opacita' riempimento": "Opacidad del relleno",
    "Il contenuto della figura fa da modello: la figura segue il soggetto nei fotogrammi successivi; quando esce dall'inquadratura l'effetto finisce.":
        "El contenido de la figura sirve de plantilla: la figura sigue al sujeto en los fotogramas siguientes; "
        "cuando sale del encuadre el efecto termina.",
    "segue il soggetto ({points} punti)": "sigue al sujeto ({points} puntos)",
    "Effetto: {name}": "Efecto: {name}",
    "Audio originale (un pezzo)": "Audio original (un fragmento)",
    "Carattere": "Fuente",
    "Sull'anteprima: trascina per spostarla, dagli angoli per ridimensionarla (le proporzioni restano quelle dell'immagine).":
        "En la vista previa: arrástrela para moverla, desde las esquinas para redimensionarla "
        "(se mantienen las proporciones de la imagen).",
    "Coda X": "Cola X",
    "Punta X": "Punta X",
    "Spessore": "Grosor",
    "Audio originale (tutto)": "Audio original (todo)",
    "Area da ingrandire": "Área que ampliar",
    "Forma": "Forma",
    "Angoli (rettangolare)": "Esquinas (rectangular)",
    "Contorno colorato sull'area ingrandita": "Contorno de color en el área ampliada",
    "Linea fra l'area e il riquadro": "Línea entre el área y el recuadro",
    "Riquadro ingrandito": "Recuadro ampliado",
    "L'area fa da modello: lo zoom segue l'oggetto nei fotogrammi successivi, il riquadro ingrandito resta dove l'hai messo. Se l'oggetto esce dall'inquadratura lo zoom finisce.":
        "El área sirve de plantilla: el zoom sigue al objeto en los fotogramas siguientes, el recuadro ampliado "
        "se queda donde lo puso. Si el objeto sale del encuadre el zoom termina.",
    "Rettangolare": "Rectangular",
    "Ingrandimento": "Ampliación",
    "Larghezza": "Ancho",
    "Per tutto il video": "Todo el vídeo",
    "Largh. logo (px)": "Ancho logo (px)",
    "Dimensione testo": "Tamaño del texto",
    "Colore testo": "Color del texto",
    "Disposizione": "Disposición",
    "Ombra sotto il testo": "Sombra bajo el texto",
    "Sfondo": "Fondo",
    "Sfondo sotto logo e scritta": "Fondo bajo logo y texto",
    "Opacita' di tutto": "Opacidad del conjunto",
    "Angolo": "Esquina",
    "Il colore vale per il bordo del riquadro, il contorno dell'area e la linea. L'area scelta viene mostrata ingrandita nel riquadro, sopra il video, per la durata dell'effetto. Sull'anteprima: trascina l'area o il riquadro, ridimensiona l'area dagli angoli.":
        "El color vale para el borde del recuadro, el contorno del área y la línea. El área elegida se muestra "
        "ampliada en el recuadro, sobre el vídeo, durante el efecto. En la vista previa: arrastre el área o el "
        "recuadro, redimensione el área desde las esquinas.",
    "Pixelatura": "Pixelado",
    "Grandezza pixel": "Tamaño de píxel",
    "Resta fermo nel punto scelto. Sull'anteprima trascinalo per spostarlo, tira un angolo per ingrandire o rimpicciolire logo e testo insieme. I valori proposti per i prossimi si cambiano in Configurazione.":
        "Se queda fijo en el punto elegido. En la vista previa arrástrelo para moverlo, tire de una esquina para "
        "ampliar o reducir logo y texto a la vez. Los valores propuestos para los siguientes se cambian en "
        "Configuración.",
    "fisso": "fijo",
    "Soggetto perso": "Sujeto perdido",
    "Ripeti l'inseguimento dopo aver cambiato inizio o fine.":
        "Repita el seguimiento después de cambiar el inicio o el fin.",
    "{points} punti": "{points} puntos",
    "{frames} fotogrammi": "{frames} fotogramas",

    # ---------------------------------------------------------- preview_view
    "Trascina sull'anteprima per disegnare il riquadro": "Arrastre en la vista previa para dibujar el recuadro",
    "Trascina sull'anteprima per disegnare l'ovale": "Arrastre en la vista previa para dibujar el óvalo",
    "Trascina sull'anteprima un rettangolo sull'oggetto da ingrandire":
        "Arrastre en la vista previa un rectángulo sobre el objeto que ampliar",
    "Clicca dove far apparire il riquadro ingrandito  -  {factor}x  (rotellina o tasti 2, 3, 4, 6, 8)":
        "Haga clic donde mostrar el recuadro ampliado  -  {factor}x  (rueda o teclas 2, 3, 4, 6, 8)",
    "Clicca sull'anteprima dove mettere il tempo trascorso":
        "Haga clic en la vista previa donde poner el tiempo transcurrido",
    "Trascina sull'anteprima l'area da pixelare: verra' inseguita nei fotogrammi successivi":
        "Arrastre en la vista previa el área que pixelar: se seguirá en los fotogramas siguientes",
    "Trascina dalla coda alla punta della freccia": "Arrastre desde la cola hasta la punta de la flecha",
    "Clicca sull'anteprima dove mettere il testo": "Haga clic en la vista previa donde poner el texto",
    "Importa un video per vedere l'anteprima": "Importe un vídeo para ver la vista previa",
    "segue il soggetto": "sigue al sujeto",

    # --------------------------------------------------------------- project
    "Logo e operatore": "Logo y operador",
    "Slide di apertura: {text}": "Diapositiva de apertura: {text}",
    "Slide di chiusura: {text}": "Diapositiva de cierre: {text}",
    "Slide: {text}": "Diapositiva: {text}",
    "Fermo immagine ({name})": "Imagen congelada ({name})",
    "Percorso del progetto mancante": "Falta la ruta del proyecto",

    # ---------------------------------------------------------------- render
    "La timeline e' vuota: importa almeno un video.": "La línea de tiempo está vacía: importe al menos un vídeo.",
    "Preparazione dei segmenti": "Preparación de los segmentos",
    "Disegno delle sovraimpressioni": "Dibujo de las superposiciones",
    "Preparazione": "Preparación",
    "Completato": "Completado",
    "ffmpeg non ha scritto il file di uscita.": "ffmpeg no ha escrito el archivo de salida.",
    "Disegno del contorno dello zoom": "Dibujo del contorno del zoom",
    "Disegno dell'orologio {speed}": "Dibujo del reloj {speed}",
    "Codifica: {done} / {total}": "Codificación: {done} / {total}",

    # --------------------------------------------------------- timeline_view
    "Audio originale": "Audio original",
    "muto": "silenciado",
    "immagine": "imagen",
    "orologio": "reloj",
    "senza audio": "sin audio",
    "audio": "audio",
    "{name} ({points} punti)": "{name} ({points} puntos)",
    "{name} (fisso)": "{name} (fijo)",
    "{name} (segue)": "{name} (sigue)",
    "audio {volume:.0f} %": "audio {volume:.0f} %",

    # ----------------------------------------------------------------- tools
    "Risposta inattesa dal sito di download di ffmpeg.": "Respuesta inesperada del sitio de descarga de ffmpeg.",
    "Il download automatico e' disponibile solo su Windows: installa ffmpeg con il gestore di pacchetti del sistema.":
        "La descarga automática solo está disponible en Windows: instale ffmpeg con el gestor de paquetes del sistema.",
    "licenza di VitTrack": "licencia de VitTrack",
    "Il file scaricato non e' un archivio zip valido.": "El archivo descargado no es un archivo zip válido.",
    "Estrazione di ffmpeg": "Extracción de ffmpeg",
    "L'ffmpeg scaricato non si avvia su questo PC.": "El ffmpeg descargado no se ejecuta en este PC.",
    "Il modello scaricato non corrisponde a quello atteso (impronta SHA-256 diversa).":
        "El modelo descargado no corresponde al esperado (huella SHA-256 distinta).",
    "Il pacchetto scaricato non contiene {file}.": "El paquete descargado no contiene {file}.",
    "{file} manca dopo l'estrazione.": "Falta {file} después de la extracción.",
    "Impossibile controllare l'ultima versione di ffmpeg: {error}":
        "No se puede comprobar la última versión de ffmpeg: {error}",
    "Download di {name} fallito: {error}": "La descarga de {name} ha fallado: {error}",
    "Impossibile aggiornare '{folder}': file in uso. Aspetta la fine dell'esportazione e riprova.":
        "No se puede actualizar '{folder}': archivos en uso. Espere al final de la exportación e inténtelo de nuevo.",
    "OpenCV non riesce a caricare il modello: {error}": "OpenCV no consigue cargar el modelo: {error}",
    "Archivio non valido: percorso sospetto '{path}'.": "Archivo no válido: ruta sospechosa '{path}'.",
    "Download di {name}": "Descarga de {name}",

    # -------------------------------------------------------------- tracking
    "Nessun fotogramma all'istante di partenza.": "Ningún fotograma en el instante de partida.",

    # --------------------------------------------------------------- widgets
    "INFO": "INFO",
    "CONFERMA": "CONFIRMAR",
    "ATTENZIONE": "AVISO",
    "ERRORE": "ERROR",
    "OK": "OK",
    "Annulla": "Cancelar",
    "Si'": "Sí",
    "No": "No",
    "Interruzione...": "Interrumpiendo...",
    "Invio va a capo, Ctrl+Invio conferma.": "Intro inserta un salto de línea, Ctrl+Intro confirma.",
    "Allineamento delle righe": "Alineación de las líneas",
    "Scrivi il testo.": "Escriba el texto.",
    "Fondo scuro": "Fondo oscuro",
    "Centra nel video": "Centrar en el vídeo",
    "Dimensione non valida.": "Tamaño no válido.",
    "{field}: valore fra {min:g} e {max:g}.": "{field}: valor entre {min:g} y {max:g}.",
    "{field}: inserisci un numero.": "{field}: introduzca un número.",

    # ------------------------------------------------------- tempo trascorso
    "Tempo trascorso dall'inizio del video: clic dove metterlo, poi si sposta":
        "Tiempo transcurrido desde el inicio del vídeo: clic donde ponerlo, luego se mueve",
    "Tempo trascorso aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.":
        "Tiempo transcurrido añadido: arrástrelo donde quiera, ajústelo en el panel de la derecha.",
    "minuti:secondi (01:23)": "minutos:segundos (01:23)",
    "ore:minuti:secondi (00:01:23)": "horas:minutos:segundos (00:01:23)",
    "con i decimi (01:23.4)": "con décimas (01:23.4)",
    "dall'inizio del video": "desde el inicio del vídeo",
    "dall'inizio dell'effetto": "desde el inicio del efecto",
    "Tempo trascorso": "Tiempo transcurrido",
    "Formato": "Formato",
    "Conta": "Cuenta",
    "Testo davanti": "Texto delante",
    "Sfondo dietro il tempo": "Fondo detrás del tiempo",
    "Sull'anteprima: trascinalo dove vuoi, dagli angoli per ingrandirlo.":
        "En la vista previa: arrástrelo donde quiera, desde las esquinas para ampliarlo.",
    "Disegno del tempo trascorso": "Dibujo del tiempo transcurrido",

    # ------------------------------------------------------- riproduzione
    '10 fotogrammi indietro (Ctrl+Sinistra)': '10 fotogramas atrás (Ctrl+Izquierda)',
    "Riproduci all'indietro / pausa (Maiusc+Spazio), senza audio": 'Reproducir hacia atrás / pausa (Mayús+Espacio), sin audio',
    '10 fotogrammi avanti (Ctrl+Destra)': '10 fotogramas adelante (Ctrl+Derecha)',
    'Allunga fino al cursore': 'Alargar hasta el cursor',
    'Interrompi al cursore': 'Cortar en el cursor',
    '{effect} allungato fino a {t:.2f} s.': '{effect} alargado hasta {t:.2f} s.',
    '{effect} interrotto a {t:.2f} s.': '{effect} cortado en {t:.2f} s.',
    "{effect} nascosto: non compare in anteprima ne' nel video esportato.": '{effect} oculto: no aparece en la vista previa ni en el vídeo exportado.',
    '{effect} di nuovo visibile.': '{effect} visible de nuevo.',
    '{zoom}% - trascina per spostarti, doppio clic centrale: adatta': '{zoom}% - arrastre para moverse, doble clic central: ajustar',
    'Fotogrammi': 'Fotogramas',
    "Numero del fotogramma dall'inizio del video: clic dove metterlo, poi si sposta": 'Número de fotograma desde el inicio del vídeo: clic donde ponerlo, luego se mueve',
    'Numero del fotogramma aggiunto: trascinalo dove vuoi, regolalo nel pannello a destra.': 'Número de fotograma añadido: arrástrelo donde quiera y ajústelo en el panel de la derecha.',
    'Numero del fotogramma': 'Número de fotograma',
    'Primo fotogramma': 'Primer fotograma',
    "Clicca sull'anteprima dove mettere il numero del fotogramma": 'Haga clic en la vista previa donde poner el número de fotograma',
    'Anteprima': 'Vista previa',
    'Anteprima riattaccata.': 'Vista previa acoplada de nuevo.',
    "Riattacca l'anteprima alla finestra principale": 'Volver a acoplar la vista previa a la ventana principal',
    "Stacca l'anteprima in una finestra a parte (piu' spazio per la timeline)": 'Separar la vista previa en otra ventana (más espacio para la línea de tiempo)',
    'Anteprima in una finestra a parte: chiudila o usa il pulsante in alto a destra per riattaccarla.': 'Vista previa en otra ventana: ciérrela o use el botón de arriba a la derecha para volver a acoplarla.',
    "Trascina un rettangolo attorno al soggetto: la freccia lo seguira' tenendo la punta dov'e'.": 'Arrastre un rectángulo alrededor del sujeto: la flecha lo seguirá manteniendo la punta donde está.',
    'soggetto della freccia': 'sujeto de la flecha',
    "Si disegna un rettangolo attorno al soggetto: la freccia lo segue nei fotogrammi successivi tenendo la punta su di lui; quando esce dall'inquadratura l'effetto finisce.": 'Se dibuja un rectángulo alrededor del sujeto: la flecha lo sigue en los fotogramas siguientes manteniendo la punta sobre él; cuando sale del encuadre el efecto termina.',
    'Scegli un altro soggetto': 'Elegir otro sujeto',
    'Trascina un rettangolo attorno al soggetto che la freccia deve seguire': 'Arrastre un rectángulo alrededor del sujeto que debe seguir la flecha',
}
