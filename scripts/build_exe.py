# EditSimple — montaggio video per presentazioni.  Copyright (C) 2026 Andrea Cumini <andrea@osintinfo.net>
# SPDX-License-Identifier: GPL-3.0-only
# GNU GPL v3 con termini aggiuntivi (attribuzione dell'autore): vedi LICENSE e NOTICE.
"""Compila EditSimple in un unico eseguibile Windows con PyInstaller.

    .venv\\Scripts\\python.exe scripts\\build_exe.py                        solo dist/EditSimple.exe
    .venv\\Scripts\\python.exe scripts\\build_exe.py --release              + zip e note di rilascio in dist/
    .venv\\Scripts\\python.exe scripts\\build_exe.py --release --no-build   rifa' solo zip e note

--release produce dist/EditSimple-<versione>-windows-x64.zip (exe, LICENSE,
NOTICE, README.md e licenses/) e dist/release-notes-<versione>.md con le
novita' della sezione piu' recente di CHANGELOG.md e l'impronta SHA-256 dello
zip. La pubblicazione su GitHub si fa a mano (git push, poi gh release create).

Installa PyInstaller nel virtualenv se manca, scrive un file spec in build/ e
compila dist/EditSimple.exe: un solo file, senza finestra console, con l'icona
"ES" e le proprieta' del file. Dentro ci sono Python, le librerie (customtkinter,
Pillow, NumPy, OpenCV), il logo, l'icona e i caratteri DejaVu della cartella font/
con la loro licenza (Panchang, il carattere del logo, non si ridistribuisce).
Accanto all'exe, in dist/, vengono copiati LICENSE, NOTICE, README.md e la
cartella licenses/ con i file di licenza di Python e delle librerie contenute.

I programmi di terze parti NON entrano nel bundle: ffmpeg.exe resta fuori in
ogni forma (la cartella tools/ non viene copiata e il pacchetto imageio-ffmpeg,
se presente, e' escluso). L'eseguibile cerca ffmpeg in tools/ffmpeg/ accanto a
se' e, se manca, propone di scaricarlo dalla pagina Configurazione. La libreria
FFmpeg del wheel di OpenCV (opencv_videoio_ffmpeg*.dll, LGPL) invece resta:
serve alla lettura dei fotogrammi per l'anteprima e all'inseguimento.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import platform
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from editsimple import APP_NAME, AUTHOR, AUTHOR_EMAIL, AUTHOR_URL, COPYRIGHT, __version__  # noqa: E402

PACKAGE = "editsimple"
ASSETS = ROOT / PACKAGE / "assets"
FONT = ROOT / "font"
ICON = ASSETS / "editsimple.ico"
BUILD = ROOT / "build"
DIST = ROOT / "dist"
EXE = DIST / f"{APP_NAME}.exe"
CHANGELOG = ROOT / "CHANGELOG.md"
ZIP = DIST / f"{APP_NAME}-{__version__}-windows-x64.zip"
NOTES = DIST / f"release-notes-{__version__}.md"
REPO_URL = "https://github.com/tingon11/EditSimple"

RELEASE_NOTES = """\
{intro}

## What's new in {version}

{changes}

## Download

**{zip}** is the standalone program for Windows 10/11 (64-bit). Python is
not needed: unzip it anywhere and run `{exe}`.

## First start

- The interface is available in English, Italian, German, French, Spanish,
  Dutch, Polish, Greek and Albanian (*Language* box of the Configure page; the
  change is immediate).
- User manual with screenshots, in every language:
  [docs/manual]({repo}/tree/main/docs/manual).
- ffmpeg is not included: at first start the program offers to download the
  official Windows build into a `tools` folder next to the executable.
- The VitTrack tracking model is optional and not included: download it from
  the *Tracking (VitTrack)* box of the Configure page. Without it, tracking
  works with template matching only.
- The executable is not signed, so Windows SmartScreen may show a warning the
  first time it runs.

## Verify the download

SHA-256 of `{zip}`:

```
{sha256}
```

## Bundled software

`{exe}` contains the Python interpreter, the DejaVu fonts and these libraries,
each under its own license; their license files are in the `licenses` folder of
the zip:

{bundled}

## Downloaded on request (not included)

- **ffmpeg**, the official Windows build from <https://www.gyan.dev/ffmpeg/builds/>
  (GNU LGPL / GPL), into `tools/ffmpeg`: reads and writes the video.
- **VitTrack** (`object_tracking_vittrack_2023sep.onnx`, Apache 2.0, from the
  OpenCV model zoo), into `tools/vittrack`: helps the subject tracking.

## License

{name} is free software under the GNU GPL version 3 with additional attribution
terms (see `LICENSE` and `NOTICE`). {author} - {email} - {url}
"""

VERSION_INFO = """\
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={numbers}, prodvers={numbers},
    mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0),
  ),
  kids=[
    StringFileInfo([StringTable('040904B0', [
      StringStruct('CompanyName', {author!r}),
      StringStruct('FileDescription', {description!r}),
      StringStruct('FileVersion', {version!r}),
      StringStruct('InternalName', {name!r}),
      StringStruct('LegalCopyright', {copyright!r}),
      StringStruct('OriginalFilename', {exe!r}),
      StringStruct('ProductName', {name!r}),
      StringStruct('ProductVersion', {version!r}),
    ])]),
    VarFileInfo([VarStruct('Translation', [0x0409, 1200])]),
  ],
)
"""

SPEC = """\
# -*- mode: python ; coding: utf-8 -*-
# Generato da scripts/build_exe.py a ogni build: non modificare a mano.
from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    [{entry!r}],
    pathex=[{root!r}],
    binaries=[],
    # logo e icona accanto a theme.py; caratteri in font/; temi e caratteri di customtkinter
    datas=[({assets!r}, {assets_dest!r})] + {fonts!r} + collect_data_files("customtkinter"),
    hiddenimports=["PIL._tkinter_finder"],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    # ffmpeg resta fuori: sta in tools/ accanto all'exe, non nel bundle
    excludes=["imageio_ffmpeg", "imageio"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name={name!r},
    debug=False, bootloader_ignore_signals=False, strip=False, upx=True, upx_exclude=[],
    runtime_tmpdir=None, console=False, disable_windowed_traceback=False,
    argv_emulation=False, target_arch=None, codesign_identity=None, entitlements_file=None,
    version={version_file!r},
    icon=[{icon!r}],
)
"""


# librerie messe nell'eseguibile e la loro licenza (quella dichiarata dal pacchetto)
BUNDLED = (
    ("customtkinter", "CC0-1.0"),
    ("darkdetect", "BSD-3-Clause"),
    ("packaging", "Apache-2.0 OR BSD-2-Clause"),
    ("pillow", "MIT-CMU"),
    ("numpy", "BSD-3-Clause (bundled components under 0BSD, MIT, Zlib and CC0-1.0)"),
    ("opencv-python-headless", "Apache-2.0; the codecs and libraries built into it, among them the FFmpeg "
                               "library opencv_videoio_ffmpeg*.dll (LGPL-2.1-or-later), are listed in "
                               "LICENSE-3RD-PARTY.txt"),
)


def bundled_fonts() -> list[tuple[str, str]]:
    """I caratteri DejaVu con la loro licenza: Panchang (logo) resta fuori, non si ridistribuisce."""
    files = sorted(FONT.glob("DejaVu*.ttf"))
    licence = FONT / "LICENSE-DejaVu.txt"
    if not files or not licence.is_file():
        sys.exit(f"Mancano i caratteri DejaVu o {licence} in {FONT}.")
    return [(str(f), "font") for f in files] + [(str(licence), "font")]


def license_files(dist: importlib.metadata.Distribution) -> list[tuple[Path, str]]:
    """File di licenza dichiarati da un pacchetto installato (campo License-File)."""
    folder = next((Path(dist.locate_file(f.parent)) for f in dist.files or ()
                   if f.name == "METADATA" and f.parent.name.endswith(".dist-info")), None)
    label = f"{dist.metadata['Name']} {dist.version}"
    if folder is None:
        sys.exit(f"Non trovo la cartella dist-info di {label}.")
    names = dist.metadata.get_all("License-File") or sorted(
        p.name for p in folder.iterdir() if p.is_file() and p.name.upper().startswith(("LICENSE", "LICENCE", "COPYING")))
    found = []
    for name in names:
        for candidate in (folder / "licenses" / name, folder / name):
            if candidate.is_file():
                found.append((candidate, name.replace("\\", "/")))
                break
        else:
            sys.exit(f"Manca il file di licenza {name} di {label} in {folder}.")
    return found


def copy_licenses() -> None:
    """LICENSE, NOTICE, README e licenses/ (Python e librerie dell'eseguibile) accanto all'exe."""
    for name in ("LICENSE", "NOTICE", "README.md"):
        shutil.copyfile(ROOT / name, DIST / name)
    target = DIST / "licenses"
    shutil.rmtree(target, ignore_errors=True)
    lines = [f"THIRD-PARTY SOFTWARE IN {APP_NAME}.exe", "",
             "Each library keeps its own license; its files are in the folder named after it.", ""]
    for name, licence in BUNDLED:
        dist = importlib.metadata.distribution(name)
        folder = target / f"{dist.metadata['Name']}-{dist.version}"
        for path, relative in license_files(dist):
            (folder / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, folder / relative)
        lines += [f"{dist.metadata['Name']} {dist.version}", f"  License: {licence}", f"  Files:   {folder.name}/", ""]
    python_licence = Path(sys.base_prefix) / "LICENSE.txt"
    if not python_licence.is_file():
        sys.exit(f"Manca la licenza di Python: {python_licence}")
    folder = target / f"Python-{platform.python_version()}"
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(python_licence, folder / "LICENSE.txt")
    lines += [f"Python {platform.python_version()}", "  License: PSF-2.0", f"  Files:   {folder.name}/", "",
              "The DejaVu fonts inside the executable come with font/LICENSE-DejaVu.txt (also inside it).",
              "FFmpeg (tools/ffmpeg) and the VitTrack model (tools/vittrack) are not in the executable:",
              "they are downloaded on request together with their own license files. See NOTICE."]
    (target / "README.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Licenze copiate in {target}")


def ensure_pyinstaller() -> None:
    if importlib.util.find_spec("PyInstaller") is None:
        print("Installo PyInstaller nel virtualenv...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)


def version_numbers() -> tuple[int, int, int, int]:
    parts = [int(p) for p in __version__.split(".") if p.isdigit()][:4]
    while len(parts) < 4:
        parts.append(0)
    return tuple(parts)  # type: ignore[return-value]


def changelog_section() -> tuple[str, str]:
    """Introduzione e novita' della versione corrente da CHANGELOG.md (sezione «## <versione>»)."""
    if not CHANGELOG.is_file():
        sys.exit(f"Manca {CHANGELOG.name}: scrivi la sezione «## {__version__}» con le novita'.")
    text = CHANGELOG.read_text(encoding="utf-8")
    match = re.search(rf"^## {re.escape(__version__)}\b[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if match is None:
        sys.exit(f"{CHANGELOG.name} non ha la sezione «## {__version__}».")
    lines = [line.rstrip() for line in match.group(1).strip().splitlines()]
    first = next((n for n, line in enumerate(lines) if line.startswith(("- ", "* ", "### "))), len(lines))
    intro = "\n".join(lines[:first]).strip() or f"{APP_NAME} {__version__}."
    changes = "\n".join(lines[first:]).strip() or "- Maintenance release."
    return intro, changes


def package() -> None:
    """Zip di rilascio (exe, LICENSE, NOTICE, README, licenses/) e note con l'impronta SHA-256."""
    if not EXE.is_file() or not (DIST / "licenses").is_dir():
        sys.exit(f"Manca {EXE} o la cartella licenses: esegui prima il build.")
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(EXE, EXE.name)
        for name in ("LICENSE", "NOTICE", "README.md"):
            zf.write(ROOT / name, name)
        for path in sorted((DIST / "licenses").rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(DIST).as_posix())
    sha256 = hashlib.sha256(ZIP.read_bytes()).hexdigest()
    intro, changes = changelog_section()
    bundled = []
    for name, licence in BUNDLED:
        dist = importlib.metadata.distribution(name)
        # nelle note (Markdown) l'asterisco di opencv_videoio_ffmpeg*.dll va protetto
        bundled.append(f"- {dist.metadata['Name']} {dist.version}: {licence}".replace("*", "\\*"))
    bundled.append(f"- Python {platform.python_version()}: PSF-2.0")
    NOTES.write_text(RELEASE_NOTES.format(
        intro=intro, version=__version__, changes=changes, zip=ZIP.name, exe=EXE.name, sha256=sha256,
        bundled="\n".join(bundled), repo=REPO_URL, name=APP_NAME, author=AUTHOR, email=AUTHOR_EMAIL,
        url=AUTHOR_URL), encoding="utf-8")
    print(f"{ZIP}  ({ZIP.stat().st_size / 1e6:.1f} MB)\n{NOTES}\nSHA-256 {sha256}")


def main() -> None:
    args = set(sys.argv[1:])
    unknown = args - {"--release", "--no-build"}
    if unknown:
        sys.exit(f"Opzioni sconosciute: {' '.join(sorted(unknown))}")
    if "--no-build" in args:
        if "--release" in args:
            package()
        return
    if not ICON.is_file():
        sys.exit(f"Icona mancante: {ICON}. Esegui prima scripts/make_brand.py.")
    ensure_pyinstaller()
    BUILD.mkdir(exist_ok=True)
    version_file = BUILD / "version_info.txt"
    version_file.write_text(VERSION_INFO.format(
        numbers=version_numbers(), author=AUTHOR, description=f"{APP_NAME} - montaggio video per presentazioni",
        version=__version__, name=APP_NAME, copyright=COPYRIGHT, exe=f"{APP_NAME}.exe"), encoding="utf-8")
    spec = BUILD / f"{APP_NAME}.spec"
    spec.write_text(SPEC.format(
        entry=str(ROOT / "EditSimple.py"), root=str(ROOT), assets=str(ASSETS), assets_dest=f"{PACKAGE}/assets",
        fonts=bundled_fonts(), name=APP_NAME, version_file=str(version_file), icon=str(ICON)), encoding="utf-8")
    print(f"Compilo {EXE} ...")
    subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--distpath", str(DIST),
                    "--workpath", str(BUILD / "work"), str(spec)], check=True, cwd=str(ROOT))
    if not EXE.is_file():
        sys.exit("PyInstaller non ha prodotto l'eseguibile.")
    copy_licenses()
    print(f"\nFatto: {EXE} ({EXE.stat().st_size / 1e6:.1f} MB)")
    print("ffmpeg non e' nel bundle: al primo avvio l'exe propone di scaricarlo in tools/ffmpeg accanto a se'.")
    if "--release" in args:
        package()


if __name__ == "__main__":
    main()
