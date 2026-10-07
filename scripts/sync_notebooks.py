"""
Convert marimo notebooks (.py) to MyST (.md) files
for use with [jupyter-book-marimo](https://github.com/marimo-team/jupyter-book-marimo) plugin
"""

import argparse
import pathlib
import re
import subprocess
import sys

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
CONTENT_DIR = PROJECT_ROOT / "content"

# Directories under notebooks/ that should never be treated as notebook sources
# (e.g. marimo's own session/layout state).
IGNORED_DIRS = {"__marimo__", "__pycache__"}

# jupyter-book-marimo directive options with no marimo-native equivalent.
# --flavor mystmd already handles everything else (name, column, hide-code,
# disabled) directly from marimo cell kwargs. Set these per-cell via a
# `# jb: key=value ...` comment anywhere in the cell.
JB_ONLY_OPTIONS = {
    "eval", "echo", "editor", "output",
    "server-output", "error", "include",
    "hide-output", "unparsable",
}

JB_COMMENT_PATTERN = re.compile(r"^[ \t]*#\s*jb:\s*(.+?)\s*$\n?", re.MULTILINE)
MARIMO_FENCE_PATTERN = re.compile(
    r"```\{marimo\}\s*python\n(?P<options>(?::[^\n]*\n)*)(?P<body>.*?\n)```",
    re.DOTALL,
)

# The first `<!-- jb-frontmatter ... -->` HTML comment in the file, typically
# written inside a `mo.md(r"""...""")` markdown cell. Its contents are merged
# into the page's YAML frontmatter and then stripped from the rendered body.
# Only the first such comment is used; later ones are left untouched.
JB_FRONTMATTER_PATTERN = re.compile(
    r"<!--\s*jb-frontmatter\s*\n(?P<content>.*?)\n\s*-->",
    re.DOTALL,
)
FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)", re.DOTALL)

def iter_notebooks():
    """Yield all notebook .py files under NOTEBOOKS_DIR, skipping ignored dirs."""
    for py_file in NOTEBOOKS_DIR.rglob("*.py"):
        rel_path = py_file.relative_to(NOTEBOOKS_DIR)
        parts = rel_path.parts[:-1]
        if IGNORED_DIRS.isdisjoint(parts):
            output_path = (CONTENT_DIR / rel_path).with_suffix(".md")
            yield py_file, output_path

def apply_jb_options(content: str, source: str = "") -> str:
    """Find `{marimo}` cells with a `# jb: key=value ...` comment, turn that
    comment into MyST directive options, and strip it from the visible code."""

    def replace(match: re.Match) -> str:
        body = match.group("body")
        jb_match = JB_COMMENT_PATTERN.search(body)
        if not jb_match:
            return match.group(0)

        new_options = []
        for pair in jb_match.group(1).split():
            if "=" not in pair:
                print(f"[marimo-sync] Warning: malformed jb option '{pair}' in {source}, skipping", file=sys.stderr)
                continue
            key, value = pair.split("=", 1)
            if key not in JB_ONLY_OPTIONS:
                print(f"[marimo-sync] Warning: unknown jb option '{key}' in {source}", file=sys.stderr)
                continue
            new_options.append(f":{key}: {value}\n")

        cleaned_body = JB_COMMENT_PATTERN.sub("", body, count=1)
        return f"```{{marimo}} python\n{match.group('options')}{''.join(new_options)}{cleaned_body}```"

    return MARIMO_FENCE_PATTERN.sub(replace, content)

def apply_jb_frontmatter(content: str, source: str = "") -> str:
    """Merge the first `<!-- jb-frontmatter ... -->` comment's contents into
    the file's YAML frontmatter, and strip the comment from the body."""
    match = JB_FRONTMATTER_PATTERN.search(content)
    if not match:
        return content

    extra_yaml = match.group("content").strip("\n")
    stripped = content[:match.start()] + content[match.end():]
    stripped = re.sub(r"\n{3,}", "\n\n", stripped)

    if not extra_yaml:
        return stripped

    fm_match = FRONTMATTER_PATTERN.match(stripped)
    if fm_match:
        yaml_text, rest = fm_match.group(1), fm_match.group(2)
        merged_yaml = yaml_text.rstrip("\n") + "\n" + extra_yaml
        return f"---\n{merged_yaml}\n---\n{rest}"

    return f"---\n{extra_yaml}\n---\n\n{stripped.lstrip()}"

def postprocess_file(output_path: pathlib.Path):
    try:
        content = output_path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return
    updated = apply_jb_options(content, source=str(output_path))
    updated = apply_jb_frontmatter(updated, source=str(output_path))
    if updated != content:
        output_path.write_text(updated, encoding="utf-8")

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
        postprocess_file(output_path)
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

class JbOptionsHandler(PatternMatchingEventHandler):
    """Watches content/*.md for writes from marimo's own --watch processes
    and re-applies `# jb:` and `jb-frontmatter` processing after each one."""

    def __init__(self):
        super().__init__(patterns=["*.md"], ignore_directories=True)

    def on_created(self, event):
        postprocess_file(pathlib.Path(event.src_path))

    def on_modified(self, event):
        postprocess_file(pathlib.Path(event.src_path))

def serve(port: str, server_port: str):
    watchers = [start_watcher(nb, out) for nb, out in iter_notebooks()]
    print(f"[marimo-sync] Watching {len(watchers)} notebook(s) with marimo --watch...")

    jb_observer = Observer()
    jb_observer.schedule(JbOptionsHandler(), str(CONTENT_DIR), recursive=True)
    jb_observer.start()

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
        jb_observer.stop()
        jb_observer.join()
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