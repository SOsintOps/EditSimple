# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Controlla che ogni testo dell'interfaccia abbia la traduzione in ogni lingua.

Legge i sorgenti senza eseguirli: raccoglie i testi passati a tr() e N_() e li
confronta con il catalogo di ogni lingua in editsimple/locales/. Segnala le
traduzioni mancanti, quelle che nessun testo usa piu', le chiavi ripetute e i
segnaposto {nome} che non coincidono tra inglese e traduzione. Da lanciare
dopo aver aggiunto o cambiato un testo o una traduzione:

    .venv\\Scripts\\python.exe scripts\\check_i18n.py          tutte le lingue
    .venv\\Scripts\\python.exe scripts\\check_i18n.py de fr    solo quelle indicate
"""

from __future__ import annotations

import ast
import string
import sys
from importlib import import_module
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from editsimple.locales import DEFAULT, LANGUAGES  # noqa: E402

MARKERS = {"tr", "N_"}
LOCALES = ROOT / "editsimple" / "locales"


def used_texts() -> dict[str, str]:
    """Testi marcati nei sorgenti, ognuno con il primo punto in cui compare."""
    found: dict[str, str] = {}
    sources = [ROOT / "EditSimple.py"] + sorted(
        p for p in (ROOT / "editsimple").rglob("*.py") if LOCALES not in p.parents)
    for path in sources:
        tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not node.args:
                continue
            name = getattr(node.func, "id", getattr(node.func, "attr", ""))
            first = node.args[0]
            if name not in MARKERS:
                continue
            where = f"{path.relative_to(ROOT)}:{node.lineno}"
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                found.setdefault(first.value, where)
            elif isinstance(first, ast.JoinedStr):
                # Una f-string cambia a ogni chiamata: non puo' fare da chiave.
                found.setdefault(f"<f-string in {where}>", where)
    return found


def repeated_keys(path: Path) -> list[str]:
    """Chiavi scritte due volte nel dizionario: la seconda cancellerebbe la prima."""
    tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
    seen: set[str] = set()
    repeated: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key in node.keys:
                if isinstance(key, ast.Constant):
                    if key.value in seen:
                        repeated.append(key.value)
                    seen.add(key.value)
    return repeated


def fields(text: str) -> set[str]:
    return {name for _literal, name, _spec, _conv in string.Formatter().parse(text) if name}


def check(code: str, used: dict[str, str]) -> list[str]:
    path = LOCALES / f"{code}.py"
    if not path.is_file():
        return [f"manca il modulo {path.relative_to(ROOT)}"]
    module = import_module(f"editsimple.locales.{code}")
    catalog = module.CATALOG
    problems: list[str] = []
    for text, where in used.items():
        if text not in catalog:
            problems.append(f"manca la traduzione ({where}): {text!r}")
    for text in catalog:
        if text not in used:
            problems.append(f"traduzione non piu' usata: {text!r}")
    for text in repeated_keys(path):
        problems.append(f"chiave ripetuta: {text!r}")
    for text, translated in catalog.items():
        if not isinstance(translated, str):
            problems.append(f"traduzione non testuale: {text!r}")
        elif fields(text) != fields(translated):
            problems.append(f"segnaposto diversi: {text!r} -> {translated!r}")
        elif not translated.strip() and text.strip():
            problems.append(f"traduzione vuota: {text!r}")
    return problems


def dump_keys(path: str) -> None:
    """Scrive in un file JSON i testi da tradurre, con il punto in cui compaiono (per chi traduce)."""
    import json
    Path(path).write_text(json.dumps(used_texts(), ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--dump":
        dump_keys(sys.argv[2])
        return 0
    used = used_texts()
    codes = sys.argv[1:] or [code for code in LANGUAGES if code != DEFAULT]
    total = 0
    for code in codes:
        if code not in LANGUAGES:
            print(f"{code}: lingua sconosciuta (vedi editsimple/locales/__init__.py)")
            total += 1
            continue
        problems = check(code, used)
        for line in problems:
            print(f"{code}: {line}")
        print(f"{code} ({LANGUAGES[code]}): {len(used)} testi, {len(problems)} problemi")
        total += len(problems)
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
