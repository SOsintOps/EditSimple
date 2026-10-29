# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Lingua dell'interfaccia: italiano (predefinita) o una delle lingue in locales/.

Nel codice i testi sono in italiano e fanno da chiave; le traduzioni stanno
nei moduli del pacchetto locales. tr() traduce nel momento in cui il testo serve: una
costante di modulo, valutata prima che la lingua sia nota, resta in italiano
(marcata con N_) e va passata a tr() quando si costruisce il widget.

La lingua si cambia a programma aperto. tr() restituisce una stringa che
ricorda la propria chiave (Text): again() la ritraduce, senza che chi l'ha
messa in un widget debba tenerne traccia.
"""

from __future__ import annotations

import unicodedata

from .locales import DEFAULT, LANGUAGES, catalog

_CATALOGS: dict[str, dict[str, str]] = {DEFAULT: {}}
_current = DEFAULT


class Text(str):
    """Testo tradotto: una normale stringa, che in piu' sa da quale chiave viene.

    format() conserva chiave e valori dei segnaposto, quindi si ritraduce anche
    un testo gia' composto. Maiuscole, concatenazioni e f-string danno invece
    una stringa semplice, che resta nella lingua in cui e' nata.
    """

    msgid: str
    args: tuple
    values: dict

    def __new__(cls, value: str, msgid: str, args: tuple = (), values: dict | None = None) -> Text:
        self = super().__new__(cls, value)
        self.msgid = msgid
        self.args = args
        self.values = values or {}
        return self

    def format(self, *args, **values) -> Text:
        return Text(super().format(*args, **values), self.msgid, args, values)


def set_language(code: object) -> str:
    """Sceglie la lingua; un codice sconosciuto riporta a quella predefinita."""
    global _current
    _current = code if code in LANGUAGES else DEFAULT
    if not _CATALOGS.get(_current) and _current != DEFAULT:
        _CATALOGS[_current] = catalog(_current)   # un catalogo vuoto (modulo assente) si riprova ogni volta
    return _current


def language() -> str:
    return _current


def tr(text: str) -> Text:
    """Testo nella lingua in uso; senza traduzione resta l'italiano."""
    key = text.msgid if isinstance(text, Text) else text
    return Text(_CATALOGS[_current].get(key, key), key)


def again(value):
    """Ritraduce nella lingua in uso un testo nato da tr(); ogni altro valore torna com'e'."""
    if not isinstance(value, Text):
        return value
    fresh = tr(value.msgid)
    if not value.args and not value.values:
        return fresh
    return fresh.format(
        *(again(item) for item in value.args),
        **{name: again(item) for name, item in value.values.items()},
    )


def upper(text: str) -> str:
    """Maiuscolo per titoli ed etichette: in greco le maiuscole perdono l'accento (tonos)."""
    text = str(text).upper()
    if any("Ͱ" <= char <= "Ͽ" for char in text):
        decomposed = unicodedata.normalize("NFD", text)
        text = unicodedata.normalize("NFC", "".join(c for c in decomposed if c not in "́͂"))
    return text


def N_(text: str) -> str:
    """Marca un testo che verra' tradotto piu' tardi con tr(): per le costanti di modulo."""
    return text
