"""
Convert marimo notebooks (.py) to MyST (.md) files
for use with [jupyter-book-marimo](https://github.com/marimo-team/jupyter-book-marimo) plugin
"""

import subprocess
import pathlib
import sys

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
CONTENT_DIR = PROJECT_ROOT / "content"

# Directories under notebooks/ that should never be treated as notebook sources
# (e.g. marimo's own session/layout state).
IGNORED_DIRS = {"__marimo__", "__pycache__"}

def iter_notebooks():
    """Yield all notebook .py files under NOTEBOOKS_DIR, skipping ignored dirs."""
    for py_file in NOTEBOOKS_DIR.rglob("*.py"):
        rel_path = py_file.relative_to(NOTEBOOKS_DIR)
        parts = rel_path.parts[:-1]
        if IGNORED_DIRS.isdisjoint(parts):
            output_path = (CONTENT_DIR / rel_path).with_suffix(".md")
            yield py_file, output_path

def run_marimo_export(notebook_path: pathlib.Path, output_path: pathlib.Path) -> pathlib.Path | None:
    cmd = [
        "marimo",
        "export",
        "md",
        str(notebook_path),
        "-o",
        str(output_path),
        "--flavor",
        "mystmd",
    ]

    try:
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        print(f"[marimo-sync] Successfully exported {notebook_path.name} -> {output_path.name}")
        return output_path

    except subprocess.CalledProcessError as e:
        print(f"[marimo-sync] Error exporting {notebook_path.name}:", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        return None

    except FileNotFoundError:
        print(
            f"[marimo-sync] 'marimo' command not found while trying to export {notebook_path.name}. "
            "Is marimo installed and on your PATH?",
            file=sys.stderr,
        )
        return None

def export_all():
    for file, output_path in iter_notebooks():
        run_marimo_export(file, output_path)

def main():
    export_all()

if __name__=="__main__":
    main()