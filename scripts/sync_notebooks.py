"""
Convert marimo notebooks (.py) to MyST (.md) files
for use with [jupyter-book-marimo](https://github.com/marimo-team/jupyter-book-marimo) plugin
"""

import argparse
import pathlib
import subprocess
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

def start_watcher(notebook_path: pathlib.Path, output_path: pathlib.Path) -> subprocess.Popen:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "marimo", "export", "md",
        str(notebook_path),
        "-o", str(output_path),
        "--flavor", "mystmd",
        "--watch",
    ]
    return subprocess.Popen(cmd)

def serve(port: str, server_port: str):
    watchers = [start_watcher(nb, out) for nb, out in iter_notebooks()]
    print(f"[marimo-sync] Watching {len(watchers)} notebook(s) with marimo --watch...")

    jb_cmd = [
        "uv", "run", "jupyter-book", "start",
        "--port", port,
        "--server-port", server_port,
    ]
    print("[marimo-sync] Launching Jupyter Book dev server...")
    jb_proc = subprocess.Popen(jb_cmd, cwd=CONTENT_DIR)

    try:
        jb_proc.wait()
    except KeyboardInterrupt:
        print("\n[marimo-sync] Shutting down...")
    finally:
        if jb_proc.poll() is None:
            jb_proc.terminate()
        for proc in watchers:
            if proc.poll() is None:
                proc.terminate()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Start watchers and dev server")
    parser.add_argument("--port", default="3102")
    parser.add_argument("--server-port", default="4102")
    args = parser.parse_args()

    if args.serve:
        serve(args.port, args.server_port)
    else:
        export_all()

if __name__=="__main__":
    main()