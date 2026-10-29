# EditSimple

Montaggio video semplice, pensato per costruire presentazioni a partire da
uno o più filmati: timeline a pellicola con traccia video e tracce audio,
tagli, fermo immagine, avanzamento veloce o rallentatore con orologio,
sovraimpressioni (testo, riquadri, ovali, frecce) che possono seguire un
soggetto, logo e testo dell'operatore fissi, zoom in un riquadro ingrandito e
pixelatura rettangolare o ovale che insegue un soggetto (volto, oggetto,
targa) e cresce quando si avvicina. Il risultato viene esportato in un mp4 con ffmpeg.
Un progetto è un file JSON.

Fa parte degli strumenti di [Seity](https://www.seity.com), il progetto principale
dell'autore: l'interfaccia è in CustomTkinter, con il tema scuro di Seity.

## Manuale

Il **manuale d'uso**, con gli screenshot di ogni funzione, è in
[docs/manual](docs/manual/README.md) in 9 lingue
([italiano](docs/manual/manual.it.md), [English](docs/manual/manual.en.md), ...).
Questo README riguarda installazione, struttura e funzionamento interno.

## Requisiti

- Windows 10/11 (64 bit). Il programma funziona anche su altri sistemi, ma la
  finestra senza barra del titolo e il download automatico di ffmpeg sono solo
  per Windows.
- Python 3.11 con `tkinter`.
- I pacchetti di `requirements.txt`: `customtkinter`, `pillow`, `numpy`,
  `opencv-python-headless`.
- **ffmpeg**, programma separato (vedi sotto): non è incluso.

## Installazione

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Il virtualenv va creato con il Python di questo PC: se `.venv\pyvenv.cfg`
punta a un interprete che non esiste, il programma non parte (`No Python at
...`). In quel caso correggi la riga `home` oppure ricrea il virtualenv.

## Avvio

```bash
.venv\Scripts\python.exe EditSimple.py [progetto.json | video.mp4]
```

oppure doppio clic su `Avvia.bat` (usa `pythonw.exe`, senza console). Come
argomento si può passare un progetto da aprire o un video da importare.

## FFmpeg

ffmpeg non è incluso: è un programma separato con la propria licenza e non
entra nel pacchetto né nell'eseguibile. Viene cercato in `tools\ffmpeg\ffmpeg.exe`
accanto al programma e poi nel PATH. Al primo avvio, se non lo trova, si apre
la pagina **Configurazione**: **Scarica / Aggiorna** prende il build ufficiale
per Windows ("release essentials") da <https://www.gyan.dev/ffmpeg/builds/>,
quello indicato dal sito di FFmpeg, e tiene solo `ffmpeg.exe`, `LICENSE` e
`README.txt` in `tools\ffmpeg\`. Nessuna installazione, nessuna modifica al
PATH. La cartella `tools\` è esclusa dal repository (`.gitignore`) e dal build.

Serve una **release** di ffmpeg (7.x o successiva: provata con la 9.0.2).
Evitare gli snapshot di sviluppo: quello del gennaio 2024 (`N-113347`) tronca
il video alla fine del primo segmento quando il filtro `concat` riceve più
ingressi, e l'esportazione esce incompleta.

## VitTrack (inseguimento)

L'inseguimento si fa con il confronto a modello e, se c'è, con l'aiuto di
**VitTrack**: un modello addestrato (vision transformer) del repository
ufficiale [opencv_zoo](https://github.com/opencv/opencv_zoo/tree/main/models/object_tracking_vittrack),
che OpenCV esegue da sé. I due lavorano insieme: quando il confronto è sicuro
ha ragione lui (e rimette VitTrack sul soggetto, se si è perso); quando non è
sicuro o non trova più il soggetto, per esempio dietro a un palo dove resta
agganciato allo sfondo, si segue VitTrack e il modello riparte da lì. Da solo
VitTrack non basta: su un volto o su un riquadro che contiene poco scivola via,
mentre il confronto a modello tiene. Come ffmpeg non è
incluso: nella pagina **Configurazione**, riquadro *Inseguimento (VitTrack)*,
**Scarica** prende il modello (circa 0,7 MB, controllato con l'impronta
SHA-256) e la sua licenza e li mette in `toolsittrack\`. La licenza del
modello è **Apache 2.0**, compatibile con la GPL 3 del programma (la FSF la
considera compatibile con la GPL 3, non con la GPL 2); in ogni caso il modello
non viene distribuito con il programma. Senza il modello resta il solo confronto a
modello (`cv2.matchTemplate`), che dietro a un ostacolo può restare
agganciato allo sfondo.

## Flusso di lavoro

1. **Importa video** (Ctrl+I). Il primo video fissa misura e frequenza del
   progetto (i successivi vengono adattati con bande nere se hanno proporzioni
   diverse). Il file importato viene diviso nei suoi canali: la clip va nella
   traccia **Video**, mostrata come pellicola di fotogrammi (ingrandendo la
   timeline con Ctrl+rotellina si arriva al singolo fotogramma), e il suo audio
   compare nella traccia **Audio originale**, che segue sempre gli stessi
   tagli. Gli altri video si aggiungono in coda o al cursore (il programma lo
   chiede).
2. **Sposta il cursore** con un clic sul righello, con ← → (un fotogramma),
   Maiusc+← → (un secondo), Home/Fine, oppure scrivendo il tempo nella casella.
   Spazio riproduce con l'audio, Maiusc+Spazio all'indietro (senza audio);
   Ctrl+← → salta di dieci fotogrammi.
3. **Segna IN e OUT** (tasti I e O, o i pulsanti) per selezionare una porzione.
   - **Elimina** (Canc) toglie la porzione IN–OUT: ciò che segue scorre indietro.
   - **Taglia** (S) spezza la clip al cursore; le clip si **riordinano
     trascinandole** nella timeline (gli effetti restano al loro tempo).
   - **Velocità** (V) applica alla porzione IN–OUT (o alla clip selezionata)
     un avanzamento veloce 2x, 4x, 8x, 16x o 32x oppure un **rallentatore**
     0.5x o 0.25x, con l'opzione di mostrare l'**icona di un orologio** con le
     lancette che girano e, sotto, la scritta della velocità. La timeline si
     accorcia o si allunga di conseguenza (anche l'audio rallenta); con 1x si
     torna alla velocità normale. Dimensione, posizione e colore dell'orologio si regolano nel
     pannello della clip.
4. **Fermo immagine** (F): il fotogramma al cursore resta fermo per N secondi;
   ciò che segue scorre avanti.
5. **Audio**: aggiunge una traccia (commento, musica) al cursore. Ogni traccia
   ha nome, posizione, porzione del file, **volume** e muto; si sposta
   trascinandola. Il volume dell'audio originale e l'esclusione per singola
   clip stanno nel pannello della clip.
6. **Sovraimpressioni**: premi **Testo** (T), **Riquadro** (R), **Ovale** (E)
   o **Freccia** (A) e disegna sull'anteprima (clic per il testo,
   trascinamento per le figure). L'effetto parte dal cursore e dura i secondi
   impostati in Configurazione; inizio e fine si cambiano nel pannello o
   trascinando la barra nella timeline (il bordo destro cambia la durata). Nel
   pannello: testo su più righe, **carattere** (finestra di scelta con
   l'anteprima di ogni carattere), dimensione, colore,
   allineamento, ombra, sfondo con opacità; colore, spessore e riempimento di
   riquadri, ovali e frecce. Sull'anteprima l'elemento selezionato si sposta
   trascinandolo e si ridimensiona dalle maniglie (le frecce dalle due punte).
   - **Segui il soggetto**: riquadri, ovali e frecce possono inseguire ciò che
     inquadrano (il contenuto della figura fa da modello; per la freccia si
     disegna un rettangolo attorno al soggetto e la punta resta agganciata a lui).
     Dove l'inseguimento sbaglia si trascina la figura sul soggetto: nasce un
     **keyframe**, il percorso viene corretto e l'inseguimento riparte da lì. Riquadri e ovali crescono e calano con il
     soggetto se si avvicina o si allontana. Se un soggetto in movimento sparisce
     dietro a qualcosa, la figura prosegue con la sua velocità fino a 1,5 s
     aspettando che ricompaia. Se il soggetto esce dall'inquadratura, la figura
     lo segue fuori con la sua velocità e poi l'effetto finisce; se il
     soggetto viene perso, l'effetto finisce lì. **Ripeti inseguimento dal
     cursore** riparte dalla posizione corrente; **Non seguire più** rende la
     figura ferma.
7. **Zoom** (Z): in due passi. Trascina un rettangolo sull'oggetto da
   ingrandire; poi sotto il mouse compare il **riquadro ingrandito** con il
   contenuto vero, e un clic lo mette in quel punto. L'ingrandimento va da **2x
   a 16x**: si sceglie durante il posizionamento con i tasti 2, 3, 4, 6, 8 o con
   la rotellina, e si cambia dopo nel pannello (il programma ricorda l'ultimo
   usato). Appena creato, lo zoom **segue l'oggetto** come riquadri e frecce:
   l'area ingrandita lo insegue e cresce o cala con lui (se si avvicina alla
   camera il riquadro continua a mostrarlo per intero), il riquadro resta
   dove l'hai messo e della sua misura; se l'oggetto esce dall'inquadratura
   lo zoom finisce. Un **contorno colorato** segna l'oggetto e una **linea**
   lo unisce al riquadro ingrandito (tutti e due si possono togliere nel
   pannello; il colore vale per bordo, contorno e linea). Area e riquadro si
   spostano sull'anteprima, l'area si ridimensiona dagli angoli; colore e
   spessore del bordo nel pannello.
8. **Pixel** (P rettangolare, K ovale): trascina il riquadro sul soggetto,
   indica fino a quando inseguirlo e la grandezza dei pixel. Il programma
   segue il soggetto nei fotogrammi successivi (correlazione a modello
   adattivo) e salva il percorso come punti.
   Il riquadro **segue anche la misura**: se il soggetto si avvicina alla
   camera (un veicolo fermo allo stop che riparte verso di te) la pixelatura
   cresce per coprirlo sempre, se si allontana cala.
   Quando il soggetto esce dall'inquadratura, la pixelatura lo segue fuori
   (il riquadro sporge dal bordo e sparisce con lui); se viene perso,
   finisce all'ultimo fotogramma in cui c'era. In nessun caso resta sul
   bordo a pixelare ciò che passa. La forma (rettangolare o ovale) si cambia
   anche nel pannello.
9. **Logo** (L): logo e testo dell'operatore, **fermi nell'angolo scelto**.
   Si preparano una volta nella pagina **Configura**: *Carica immagine del
   logo* (PNG con trasparenza, JPG...), il testo (nome, qualifica, data...),
   la larghezza del logo in % del video, l'altezza del testo e la distanza
   dai bordi in % del lato corto, l'angolo, la disposizione (testo a destra,
   a sinistra o sotto il logo) e il colore del testo. Il pulsante li mette per
   **tutto il video** (anche se poi si allunga o si accorcia) o solo nella
   porzione IN–OUT, se è segnata; un testo troppo lungo viene ridotto insieme
   al logo per stare nel fotogramma. Sull'anteprima si spostano trascinandoli
   e si **ridimensionano dagli angoli** (logo e testo insieme); nel pannello
   si cambiano immagine, larghezza del logo, testo, dimensione, colore,
   disposizione, angolo e posizione.
10. **Esporta MP4** (Ctrl+E): sceglie il file e rende tutto con ffmpeg (H.264 +
   AAC, qualità e velocità di codifica in Configurazione). La finestra di
   avanzamento si può annullare.

Annulla/Ripeti: Ctrl+Z / Ctrl+Y. Salva: Ctrl+S (Ctrl+Maiusc+S con nome).
Ctrl+rotellina sulla timeline la ingrandisce, la rotellina la scorre; la
rotellina sull'anteprima scorre di un fotogramma. Esc annulla un disegno.

## Il file di progetto

Un JSON con misura e frequenza del progetto, le clip in sequenza, le tracce
audio, gli effetti e le informazioni dei file sorgente (percorsi assoluti):

```json
{
  "width": 1920, "height": 1080, "fps": 25,
  "original_volume": 1.0,
  "clock": {"size": 160, "corner": "top-right", "margin": 24, "color": "#FFFFFF"},
  "clips": [
    {"id": "a1", "kind": "video", "source": "C:/video/a.mp4", "in": 0.0, "out": 12.5,
     "audio": true, "speed": 1, "clock": false},
    {"id": "a2", "kind": "freeze", "source": "C:/video/a.mp4", "at": 12.5, "duration": 3.0},
    {"id": "a3", "kind": "video", "source": "C:/video/a.mp4", "in": 12.5, "out": 40.0,
     "audio": true, "speed": 8, "clock": true}
  ],
  "audio_tracks": [
    {"id": "t1", "name": "commento", "source": "C:/audio/voce.mp3", "start": 2.0,
     "in": 0.0, "out": 30.0, "volume": 0.8, "muted": false}
  ],
  "effects": [
    {"id": "e1", "type": "text", "start": 1.0, "end": 5.0, "x": 80, "y": 60, "text": "Titolo",
     "font": "DejaVuSans-Bold.ttf", "size": 64, "color": "#FFFFFF", "bg": true,
     "bg_color": "#000000", "bg_alpha": 0.55, "shadow": true, "align": "left"},
    {"id": "e2", "type": "box", "start": 1.0, "end": 5.0, "x": 400, "y": 200, "w": 300, "h": 200,
     "color": "#FF3B30", "thickness": 5, "fill": false, "fill_alpha": 0.25, "radius": 0,
     "track": [[1.0, 400, 200], [2.4, 430, 190], [5.0, 520, 210]]},
    {"id": "e3", "type": "oval", "start": 1.0, "end": 5.0, "x": 900, "y": 300, "w": 200, "h": 260,
     "color": "#FFD700", "thickness": 5, "fill": false, "fill_alpha": 0.25},
    {"id": "e4", "type": "arrow", "start": 1.0, "end": 5.0, "x1": 100, "y1": 700, "x2": 400, "y2": 420,
     "color": "#FF3B30", "thickness": 8},
    {"id": "e5", "type": "zoom", "start": 6.0, "end": 9.0, "x": 300, "y": 150, "w": 200, "h": 150,
     "factor": 3, "bx": 1300, "by": 24, "color": "#FFFFFF", "thickness": 4, "outline": true,
     "track": [[6.0, 300, 150], [9.0, 420, 160]]},
    {"id": "e6", "type": "pixelate", "start": 3.0, "end": 8.0, "x": 500, "y": 120, "w": 160, "h": 160,
     "block": 16, "shape": "oval", "track": [[3.0, 500, 120, 1.0], [4.2, 540, 118, 1.2], [8.0, 700, 130, 2.1]]},
    {"id": "e7", "type": "logo", "start": 0.0, "end": 40.0, "full": true, "x": 1500, "y": 990,
     "logo": "C:/loghi/ente.png", "w": 230, "text": "Op. Mario Rossi", "size": 38, "color": "#FFFFFF",
     "layout": "right", "shadow": true, "corner": "bottom-right"}
  ],
  "sources": {"C:/video/a.mp4": {"duration": 40.0, "video_duration": 39.9, "fps": 25,
                                 "width": 1920, "height": 1080, "has_audio": true}}
}
```

Tempi in secondi del video finale (timeline), coordinate in pixel del
progetto. La durata di una clip è `(out - in) / speed` (`speed` da 0.25 a
32). `track` è il percorso dell'inseguimento: ogni punto è `[tempo, x, y,
scala]`, dove x, y è l'angolo del riquadro di partenza centrato sul soggetto
(per la freccia, la punta) e la scala la sua misura rispetto al primo punto
(manca nei progetti vecchi: vale 1). La pixelatura usa anche la scala, le
altre figure solo lo spostamento; fra un punto e l'altro si interpola. Un
logo con `full` copre sempre tutta la timeline. Quando si elimina una porzione o si inserisce qualcosa, gli effetti
e le tracce audio che seguono scorrono di conseguenza; i punti dentro una
porzione eliminata vengono tolti.

## Come avviene il rendering

`editsimple/render.py` costruisce un unico grafo di filtri ffmpeg (scritto in
un file e passato con `-/filter_complex`):

- ogni clip è un ingresso a sé (`-ss`/`-t` sul file sorgente) portato alla
  misura del progetto con `scale` + `pad`, `fps` e `format=yuv420p`; la
  velocità è `setpts=(PTS-STARTPTS)/N` sul video e una catena di `atempo`
  sull'audio;
- il fermo immagine è un PNG estratto da ffmpeg e ripetuto (`-loop 1 -t N`);
- la pixelatura è `split` → `crop` (con `x`/`y` espressi come funzione di `t`
  che interpola i punti dell'inseguimento) → `scale` giù e su con
  `flags=neighbor` (per l'ovale, `geq` dà alfa zero fuori dall'ellisse) →
  `overlay` nella stessa posizione, acceso solo nel suo intervallo (`enable`).
  `crop` e `scale` hanno misure fisse: se il soggetto cambia misura,
  l'intervallo si divide in tratti a misura costante (gradini del 6%, sempre
  appena più grandi del soggetto), ognuno ritagliato con `trim` sui propri
  fotogrammi e sovrapposto con `eof_action=pass`;
- i segmenti vengono uniti con `concat`; sopra passano lo zoom (`split` →
  `crop` → `scale` → `pad` per il bordo → `overlay`, più il contorno dell'area
  come PNG sovrapposto; se l'area segue un oggetto, `x` e `y` di `crop` e del
  contorno sono funzioni di `t`, mentre `drawbox` le calcolerebbe una volta sola;
  contorno e linea verso il riquadro sono una sequenza di PNG, uno per
  fotogramma, perché la linea cambia forma; se l'area cambia misura, `crop`
  lavora a tratti di misura costante come la pixelatura),
  le sovraimpressioni (PNG disegnati con Pillow da `overlays.py`, gli stessi
  dell'anteprima, con `overlay` ed `enable`; se seguono un soggetto, `x` e `y`
  sono funzioni di `t`) e l'orologio (sequenza di PNG in ciclo, una per
  velocità);
- le tracce audio aggiunte sono ritardate con `adelay` e mescolate con `amix`;
- uscita H.264 (`libx264`, CRF e preset configurabili) + AAC, `+faststart`.

L'anteprima compone lo stesso fotogramma con Pillow (`overlays.compose`), così
coincide con il risultato. I fotogrammi arrivano da OpenCV già ridotti alla
misura della vista (`media.Frames`); durante la riproduzione un thread tiene
il decoder una decina di fotogrammi avanti al cursore (senza mai tornare
indietro: un seek su un 4K costa centinaia di millisecondi) e prepara un
secondo decoder sul prossimo taglio, così il cambio di clip non ferma la
riproduzione; le miniature della pellicola si fermano finché si riproduce,
per non togliere CPU all'anteprima (provato: 4K a 30 fps e 1080p a 60 fps
senza perdere fotogrammi). L'inseguimento
(`tracking.py`) lavora su fotogrammi ridotti in scala di grigi con
`cv2.matchTemplate` e un modello che si aggiorna lentamente. A ogni
fotogramma prova cinque misure attorno a quella prevista (oggetto che si
avvicina o si allontana) e le confronta riportando la zona trovata alla misura
del modello, sia aggiornato sia originale: il modello che si aggiorna da solo
assorbirebbe l'errore di misura e resterebbe indietro. Quando il
soggetto arriva al bordo cerca solo la parte del modello ancora dentro al
fotogramma (il modello non impara mai il bordo, quindi non può restarci
incollato; le posizioni a cavallo del bordo si provano a gruppetti, e lì la
misura resta quella prevista), e si ferma quando il riquadro è per metà fuori, o per più di un
terzo e in allontanamento, oppure quando il soggetto non si ritrova per
0,4 s; da lì la figura prosegue con l'ultima velocità finché è tutta fuori. Il
percorso viene semplificato (Douglas–Peucker). Le miniature della pellicola le decodificano
due thread (`timeline_view.Thumbs`), prima quelle vicine al cursore.

## Limiti

- La riproduzione all'indietro è senza audio.
- Le frecce seguono gli spostamenti del soggetto ma restano della stessa
  misura. Le misure cambiano a gradini del 6%, sempre appena più grandi
  dell'oggetto.
- Senza VitTrack l'inseguimento confronta un modello d'immagine: una persona
  sottile davanti a uno sfondo ricco che passa dietro a un palo può far restare
  la figura sul palo. Anche con VitTrack due persone che si sovrappongono
  possono scambiarsi per qualche istante. Disegna il riquadro stretto sul
  soggetto; se la figura va sul soggetto sbagliato, porta il cursore dove il
  soggetto giusto ricompare e usa *Ripeti inseguimento dal cursore*. Se il soggetto viene perso prima del previsto, porta il cursore dove ricompare, sistema la figura e usa *Ripeti
  inseguimento dal cursore*.
- Gli effetti sono legati ai tempi della timeline: riordinando le clip
  restano dove sono.
- Zoom e velocità non sono animati (niente dissolvenze o zoom progressivo).

## Eseguibile unico

```bash
.venv\Scripts\python.exe scripts\build_exe.py
```

installa PyInstaller nel virtualenv se manca e compila `dist\EditSimple.exe`
(un solo file, senza console, icona "ES"). Dentro ci sono Python, le librerie,
logo, icona e i caratteri di `font\`. **I programmi di terze parti non entrano
nel bundle**: ffmpeg resta nella cartella `tools\` accanto all'eseguibile, da
scaricare con il programma stesso. `scripts\make_brand.py` rigenera logo e
icona (serve il carattere Panchang in `font\`).

## Struttura

| File | Contenuto |
| --- | --- |
| `EditSimple.py` | punto di ingresso |
| `editsimple/app.py` | finestra principale: intestazione, pagine Montaggio e Configurazione, azioni, inseguimento |
| `editsimple/project.py` | modello del progetto (clip, tracce audio, effetti) e file JSON |
| `editsimple/render.py` | esportazione: segmenti, grafo di filtri ffmpeg, avanzamento |
| `editsimple/overlays.py` | disegno di testo, riquadri, ovali, frecce, orologio; zoom e pixelatura; composizione del fotogramma |
| `editsimple/tracking.py` | inseguimento del soggetto (OpenCV) con rilevamento di uscita e perdita |
| `editsimple/media.py` | informazioni sui file (ffmpeg), fotogrammi per l'anteprima (OpenCV, lettura anticipata), tempi |
| `editsimple/timeline_view.py` | timeline: righello, pellicola di fotogrammi, audio, corsie degli effetti, trascinamenti |
| `editsimple/preview_view.py` | anteprima con disegno e modifica delle sovraimpressioni col mouse |
| `editsimple/panels.py` | pannello delle proprietà dell'elemento selezionato |
| `editsimple/fonts.py` | caratteri di `font/` e di Windows, finestra di scelta con anteprima |
| `editsimple/tools.py` | ricerca, download e aggiornamento di ffmpeg in `tools/` |
| `editsimple/theme.py`, `widgets.py`, `frameless.py` | tema scuro, componenti e dialoghi, finestra senza barra |
| `editsimple/procs.py`, `config.py` | processi figli legati all'app; impostazioni in `config.json` |
| `font/` | caratteri che viaggiano con il programma (DejaVu; Panchang per il logo) |
| `editsimple/i18n.py`, `editsimple/locales/` | lingue dell'interfaccia (italiano nel codice, cataloghi per le altre 8) |
| `editsimple/audio.py` | riproduzione dell'audio nell'anteprima (Windows) |
| `scripts/build_exe.py`, `scripts/make_brand.py` | eseguibile unico; logo e icona |
| `scripts/check_i18n.py` | controllo dei cataloghi delle lingue |
| `scripts/manual_screenshots.py` | rifà il progetto d'esempio passo per passo e prende gli screenshot del manuale |
| `docs/manual/` | manuale d'uso in 9 lingue con gli screenshot |
| `tools/` | programmi di terze parti scaricati (ffmpeg): fuori dal repository e dal bundle |

## Crediti

Andrea Cumini — andrea@osintinfo.net — www.osintinfo.net
