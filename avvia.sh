#!/bin/sh
# Avvio di EditSimple su Linux e macOS: usa il Python di .venv se c'e', altrimenti python3.
# Niente cd: i percorsi relativi passati come argomento restano validi.
# Se lo script e' raggiunto da un link simbolico (per esempio ~/bin/editsimple -> .../avvia.sh)
# si risale prima al file vero, cosi' dir e' la cartella del programma; solo readlink semplice, l'opzione -f di readlink manca su macOS.
f=$0
hops=0
while [ -h "$f" ]; do
    # senza readlink (o se fallisce) il link non si risolve e si parte dalla sua cartella, senza messaggi
    link=$(readlink -- "$f" 2>/dev/null) || break
    case $link in
        /*) f=$link ;;
        *) f=$(dirname -- "$f")/$link ;;
    esac
    hops=$((hops + 1))
    [ "$hops" -lt 40 ] || break   # un giro di link non deve bloccare l'avvio
done
dir=$(CDPATH= cd -- "$(dirname -- "$f")" && pwd)
if [ -x "$dir/.venv/bin/python" ]; then
    py="$dir/.venv/bin/python"
else
    py=python3
fi
exec "$py" "$dir/EditSimple.py" "$@"
