"""
Generate the book's table of contents at content/nb/toc.md.

The generated file looks like:

    ---
    title: Table of Contents
    ---

    ## [Home](#index)

    ## Part I: Choosing Alpha

    ### [4. Probability Spaces](#ch4)

    - [Sigma-Algebras](#ch4-sec-sigma-algebras)
      - 📖 {term}`Sigma-algebra`
      - 📐 [Lemma (Closure Properties)](#ch4-lem-closure-properties)
      - [Generated Sigma-Algebras](#ch4-sec-generated-sigma-algebras)
        - ...

Every page in `content/myst.yml`'s toc is listed in order. Parts are `##`
headings and the pages inside them `###` headings (a page outside any part,
such as Home, is a `##` heading beside the parts). Under each page heading is
a nested list of its headings (nested by level), and under each heading the
glossary terms, results (theorems, lemmas, corollaries), and other labeled
blocks it contains, in the order the page presents them. Every entry is a
cross-reference: pages link to their frontmatter `label` (or, without one,
to their file), headings and results to their
label, and glossary terms use `{term}`.

Pages are read from the postprocessed MyST in content/nb/, so run
scripts/sync_notebooks.py first. Only the standard library is used (no YAML
import) and each page is scanned by one compiled regex, so a run takes a few
tens of milliseconds.
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
MYST_YML = CONTENT_DIR / "myst.yml"
TOC_PATH = CONTENT_DIR / "nb" / "toc.md"

TOC_HEADER = "---\ntitle: Table of Contents\n---\n\n"
INDENT = "  "

# The page's leading YAML frontmatter, and its `title:` key.
FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(?P<yaml>[\s\S]*?)\r?\n---[ \t]*(?:\r?\n|\Z)")
FRONTMATTER_TITLE = re.compile(r"^title:[ \t]*(?P<value>.+?)[ \t]*$", re.M)
FRONTMATTER_LABEL = re.compile(r"^label:[ \t]*(?P<value>.+?)[ \t]*$", re.M)

# Everything on a page the TOC cares about, plus the blocks it must step over
# (code fences, HTML comments) so `#` lines inside them aren't read as headings.
# All alternatives start at a line start, so the scan is a single C-level pass.
TOKEN = re.compile(
    r"""^(?:
        [ \t]*(?P<fence>`{3,}|~{3,})(?P<info>[^\n]*)\n                   # code fence ...
            (?P<fence_body>[\s\S]*?)^[ \t]*(?P=fence)[ \t]*$               # ... to its close
      | <!--[\s\S]*?-->                                                    # HTML comment
      | \((?P<label>[^\s()]+)\)=[ \t]*$                                    # (label)=
      | (?P<hashes>\#{1,6})[ \t]+(?P<heading>[^\n]+?)(?:[ \t]+\#+)?[ \t]*$  # ## Heading
      | (?P<colons>:{3,})\{(?P<name>[^\s}]+)[^}\n]*\}[ \t]*(?P<arg>[^\n]*?)[ \t]*$  # :::{name} arg
    )""",
    re.M | re.X,
)

# The `:key: value` option lines directly after a directive's opening line.
OPTION_BLOCK = re.compile(r"(?:^:[\w-]+:[^\n]*(?:\n|\Z))*", re.M)
OPTION_LABEL = re.compile(r"^:label:[ \t]*(?P<label>\S+)", re.M)

# A glossary term: a non-blank line inside a glossary that is neither indented
# (definition continuation) nor starts with `:` (definition or option).
GLOSSARY_TERM = re.compile(r"^(?![ \t:])(?P<term>[^\n]*\S)[ \t]*$", re.M)

IMG_ALT = re.compile(r"""<img\b[^>]*\balt=(["'])(?P<alt>.*?)\1""")

# Closing-fence patterns for colon directives, keyed by colon count.
_closers: dict[int, re.Pattern] = {}

warnings: list[str] = []


def warn(message: str) -> None:
    warnings.append(message)


def closer(n: int) -> re.Pattern:
    pattern = _closers.get(n)
    if pattern is None:
        pattern = _closers[n] = re.compile(rf"^:{{{n}}}[ \t]*$", re.M)
    return pattern


def unquote(value: str) -> str:
    """Strip YAML scalar quotes (and a trailing comment from a plain scalar)."""
    value = value.strip()
    if value[:1] == "'":
        end = value.find("'", 1)
        while end != -1 and value[end + 1:end + 2] == "'":  # '' escapes '
            end = value.find("'", end + 2)
        return value[1:end if end != -1 else None].replace("''", "'")
    if value[:1] == '"':
        end = value.find('"', 1)
        while end != -1 and value[end - 1] == "\\":
            end = value.find('"', end + 1)
        return value[1:end if end != -1 else None].replace('\\"', '"').replace("\\\\", "\\")
    return value.split(" #", 1)[0].rstrip()


# --- myst.yml ----------------------------------------------------------------

TOC_KEY = re.compile(r"^(?P<indent>[ \t]*)toc:[ \t]*(?:#.*)?$")
TOC_LINE = re.compile(r"^(?P<indent>[ \t]*)(?P<dash>-[ \t]+)?(?P<key>[\w-]+):[ \t]*(?P<value>.*)$")


def read_toc(path: Path) -> list[dict]:
    """Parse `project.toc` from myst.yml into nested dicts with the keys
    `file`, `title`, `url` and `children`. Handles the block-style list of
    mappings MyST documents, which is what myst.yml uses."""
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next((i for i, line in enumerate(lines) if TOC_KEY.match(line)), None)
    if start is None:
        sys.exit(f"[toc] No `toc:` key found in {path}")
    toc_indent = len(TOC_KEY.match(lines[start]).group("indent"))

    root: list[dict] = []
    stack: list[tuple[int, dict]] = []  # (dash column, entry)
    for line in lines[start + 1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = TOC_LINE.match(line)
        indent = len(line) - len(line.lstrip())
        if indent <= toc_indent and not (match and match.group("dash") and indent == toc_indent):
            break  # left the toc block
        if not match:
            continue

        key, value = match.group("key"), unquote(match.group("value"))
        if match.group("dash"):
            column = len(match.group("indent"))
            while stack and stack[-1][0] >= column:
                stack.pop()
            entry: dict = {}
            (stack[-1][1].setdefault("children", []) if stack else root).append(entry)
            stack.append((column, entry))
        else:
            # A key belongs to the innermost entry whose dash is left of it.
            while stack and stack[-1][0] >= indent:
                stack.pop()
            if not stack:
                continue
            entry = stack[-1][1]
        if key == "children":
            entry.setdefault("children", [])
        elif value:
            entry[key] = value
    return root


# --- pages -------------------------------------------------------------------

def scan_page(text: str, page_link: str, source: str) -> tuple[str | None, list[tuple[int, str]]]:
    """Return a page's frontmatter title and its TOC entries as
    (depth below the page, markdown) pairs, in page order."""
    title = None
    pos = 0
    frontmatter = FRONTMATTER.match(text)
    if frontmatter:
        pos = frontmatter.end()
        title_match = FRONTMATTER_TITLE.search(frontmatter.group("yaml"))
        if title_match:
            title = unquote(title_match.group("value"))

    entries: list[tuple[int, str]] = []
    levels: list[int] = []  # heading levels enclosing the current position
    pending_label: str | None = None
    pending_end = 0

    def add(text: str) -> None:
        entries.append((len(levels) + 1, text))

    def add_terms(body: str) -> None:
        for term in GLOSSARY_TERM.finditer(body):
            add(f"📖 {{term}}`{term.group('term')}`")

    def flush_label(next_start: int) -> None:
        """Emit a `(label)=` that no heading or directive directly claimed."""
        nonlocal pending_label
        if pending_label is None:
            return
        following = text[pending_end:next_start if next_start > pending_end else len(text)].lstrip()
        first_line = following.split("\n", 1)[0]
        alt = IMG_ALT.search(first_line)
        name = f"Figure: {alt.group('alt')}" if alt else (
            "Table" if first_line.startswith("|") else pending_label)
        add(f"🏷️ [{name}](#{pending_label})")
        pending_label = None

    while (match := TOKEN.search(text, pos)) is not None:
        pos = match.end()
        # A pending label belongs to this token only if nothing sits in between.
        claimable = pending_label is not None and not text[pending_end:match.start()].strip()
        if pending_label is not None and not claimable:
            flush_label(match.start())

        if match.group("fence"):
            if match.group("info").strip().startswith("{glossary}"):
                add_terms(OPTION_BLOCK.sub("", match.group("fence_body"), count=1))
            continue

        if (label := match.group("label")) is not None:
            flush_label(match.start())
            pending_label, pending_end = label, match.end()
            continue

        if (hashes := match.group("hashes")) is not None:
            level = len(hashes)
            heading = match.group("heading")
            while levels and levels[-1] >= level:
                levels.pop()
            if claimable:
                add(f"[{heading}](#{pending_label})")
                pending_label = None
            else:
                add(f"[{heading}]({page_link})")
                if level >= 2:
                    warn(f"{source}: heading '{heading}' has no label; linked to its page")
            levels.append(level)
            continue

        if match.group("colons") is None:
            continue  # HTML comment

        # A colon-fence directive: read its options for a `:label:`.
        name, arg = match.group("name"), match.group("arg")
        options = OPTION_BLOCK.match(text, pos + 1)
        options_text = options.group(0)
        label_match = OPTION_LABEL.search(options_text)
        label = label_match.group("label") if label_match else None
        if claimable:
            label = label or pending_label
            pending_label = None
        if options_text:
            pos = options.end()

        if name == "glossary":
            close = closer(len(match.group("colons"))).search(text, pos)
            end = close.start() if close else len(text)
            add_terms(text[pos:end])
            pos = close.end() if close else len(text)
        elif name.startswith("prf:"):
            kind = name[4:]
            if kind == "proof" and label is None:
                continue
            display = f"{kind.title()} ({arg})" if arg else kind.title()
            if label:
                add(f"📐 [{display}](#{label})")
            else:
                add(f"📐 [{display}]({page_link})")
                warn(f"{source}: {kind} '{arg}' has no label; linked to its page")
        elif label:
            add(f"🏷️ [{arg or label}](#{label})")

    flush_label(len(text))
    return title, entries


def render(toc: list[dict], out: list[str], depth: int = 0) -> int:
    """Append the markdown lines for `toc` to `out`; return the page count.

    Each toc entry becomes a heading one level below its parent's: top-level
    parts and pages are `##`, the pages inside a part `###`. A page's own
    contents follow its heading as a nested list."""
    pages = 0
    hashes = "#" * min(2 + depth, 6)
    for entry in toc:
        file, title, url = entry.get("file"), entry.get("title"), entry.get("url")
        if file:
            path = (CONTENT_DIR / file).resolve()
            if path == TOC_PATH.resolve():
                continue
            link = Path(os.path.relpath(path, TOC_PATH.parent)).as_posix()
            try:
                text = path.read_text(encoding="utf-8")
            except FileNotFoundError:
                warn(f"{file} not found (run scripts/sync_notebooks.py first)")
                out.append(f"{hashes} [{title or path.stem}]({link})\n")
                continue
            frontmatter = FRONTMATTER.match(text)
            label = frontmatter and FRONTMATTER_LABEL.search(frontmatter.group("yaml"))
            if label:
                link = f"#{unquote(label.group('value'))}"
            page_title, entries = scan_page(text, link, file)
            out.append(f"{hashes} [{title or page_title or path.stem}]({link})\n")
            if entries:
                out.extend(f"{INDENT * (d - 1)}- {item}" for d, item in entries)
                out.append("")
            pages += 1
        elif url:
            out.append(f"{hashes} [{title or url}]({url})\n")
        elif title:
            out.append(f"{hashes} {title}\n")
        else:
            warn(f"skipped toc entry with no file, url, or title: {entry}")
            continue
        pages += render(entry.get("children", []), out, depth + 1)
    return pages


def write_if_changed(path: Path, text: str) -> bool:
    """Atomically write `text` to `path` unless it is already there, so the
    dev server doesn't rebuild for nothing."""
    try:
        if path.read_text(encoding="utf-8") == text:
            return False
    except FileNotFoundError:
        pass
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)
    return True


def main() -> None:
    start = time.perf_counter()
    lines: list[str] = []
    pages = render(read_toc(MYST_YML), lines)
    changed = write_if_changed(TOC_PATH, TOC_HEADER + "\n".join(lines) + "\n")

    sys.stderr.reconfigure(errors="backslashreplace")
    for message in warnings:
        print(f"[toc] Warning: {message}", file=sys.stderr)
    elapsed = (time.perf_counter() - start) * 1000
    status = "Wrote" if changed else "Unchanged:"
    print(f"[toc] {status} {TOC_PATH.relative_to(PROJECT_ROOT).as_posix()} "
          f"({pages} pages, {len(lines)} entries) in {elapsed:.0f} ms")


if __name__ == "__main__":
    main()
