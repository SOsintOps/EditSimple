# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Cataloghi delle traduzioni, un modulo per lingua (codice ISO 639-1).

Ogni modulo espone NAME (il nome della lingua, scritto in quella lingua) e
CATALOG, il dizionario testo italiano -> traduzione. L'italiano e' la lingua
dei testi nel codice e non ha catalogo. Per aggiungere una lingua: un nuovo modulo qui, il suo codice in
LANGUAGES, e `scripts/check_i18n.py` per verificare che non manchi nulla.
"""

from __future__ import annotations

import importlib
from importlib import import_module

# codice -> nome della lingua, nell'ordine in cui compaiono nell'interfaccia
LANGUAGES: dict[str, str] = {
    "en": "English",
    "it": "Italiano",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "nl": "Nederlands",
    "pl": "Polski",
    "el": "Ελληνικά",
    "sq": "Shqip",
}
DEFAULT = "it"


def catalog(code: str) -> dict[str, str]:
    """Il dizionario della lingua `code`; vuoto per l'italiano o per una lingua senza modulo."""
    if code == DEFAULT or code not in LANGUAGES:
        return {}
    try:
        return import_module(f"{__name__}.{code}").CATALOG
    except ImportError:
        # il modulo puo' essere comparso dopo l'avvio: l'elenco dei file del pacchetto va riletto
        importlib.invalidate_caches()
        try:
            return import_module(f"{__name__}.{code}").CATALOG
        except ImportError:
            return {}
