"""Windows dev shim for jupyter-book-marimo.

1. Make the Unix plugin path in content/myst.yml work locally.
2. Copy the plugin's assets into content/nb/. The plugin links to them as
   "/.jupyter-book-marimo/..." (relative to content/), but MyST on Windows
   looks for that path in the page's own folder.
"""

import os
import shutil
import sys
import sysconfig
from pathlib import Path

from jupyter_book_marimo.projection import stage_assets

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Must match the plugin path in content/myst.yml
PLUGIN = PROJECT_ROOT / ".venv" / "bin" / "jupyter-book-marimo"
# Must match PAGES_DIR in sync_notebooks.py
PAGES_DIR = PROJECT_ROOT / "content" / "nb"


def main() -> None:
    if os.name != "nt":
        return  # neither workaround is needed on Linux and macOS

    source = Path(sysconfig.get_path("scripts")) / "jupyter-book-marimo.exe"
    if not source.is_file():
        sys.exit(f"{source} not found. Run `uv sync`.")

    PLUGIN.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, PLUGIN.with_suffix(".exe"))
    PLUGIN.write_text("Placeholder: Windows runs the .exe beside this file.\n")

    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    stage_assets(root=PAGES_DIR)  # writes PAGES_DIR/.jupyter-book-marimo/


if __name__ == "__main__":
    main()