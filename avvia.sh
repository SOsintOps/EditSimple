#!/bin/sh
# Avvio di EditSimple su Linux e macOS: usa il Python di .venv se c'e', altrimenti python3.
# Niente cd: i percorsi relativi passati come argomento restano validi.
dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ -x "$dir/.venv/bin/python" ]; then
    py="$dir/.venv/bin/python"
else
    py=python3
fi
exec "$py" "$dir/EditSimple.py" "$@"
