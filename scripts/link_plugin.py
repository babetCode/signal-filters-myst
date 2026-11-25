"""Windows dev shim: make the Unix plugin path in content/myst.yml work locally."""

import os
import shutil
import sys
import sysconfig
from pathlib import Path

# Must match the plugin path in content/myst.yml
PLUGIN = Path(__file__).resolve().parent.parent / ".venv" / "bin" / "jupyter-book-marimo"


def main() -> None:
    if os.name != "nt":
        return  # the path already exists on Linux and macOS

    source = Path(sysconfig.get_path("scripts")) / "jupyter-book-marimo.exe"
    if not source.is_file():
        sys.exit(f"{source} not found. Run `uv sync`.")

    PLUGIN.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, PLUGIN.with_suffix(".exe"))
    PLUGIN.write_text("Placeholder: Windows runs the .exe beside this file.\n")


if __name__ == "__main__":
    main()