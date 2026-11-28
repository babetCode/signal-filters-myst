"""
Convert marimo notebooks (.py) to MyST (.md) files
for use with [jupyter-book-marimo](https://github.com/marimo-team/jupyter-book-marimo) plugin
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import yaml  # PyYAML, installed with marimo

PROJECT_ROOT = Path(__file__).parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
EXPORT_DIR = PROJECT_ROOT / ".marimo-export"  # raw `marimo export md` output; not committed
CONTENT_DIR = PROJECT_ROOT / "content"        # Jupyter Book project root
PAGES_DIR = CONTENT_DIR / "nb"                # postprocessed notebook pages
MYST_YML = CONTENT_DIR / "myst.yml"

# Directories under notebooks/ that should never be treated as notebook sources
# (e.g. marimo's own session/layout state).
IGNORED_DIRS = {"__marimo__", "__pycache__"}

# Set by --no-eval: skip cell evaluation for faster dev builds.
disable_eval = False

# Set by --force: re-run `marimo export` even when its cached output is newer
# than the notebook (e.g. after upgrading marimo).
force_export = False

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

# The first `<!-- jb-frontmatter ... -->` HTML comment in the file. Its
# contents are merged into the page's YAML frontmatter and then stripped
# from the rendered body. Only the first such comment is used.
JB_FRONTMATTER_PATTERN = re.compile(
    r"<!--\s*jb-frontmatter\s*\n(?P<content>.*?)\n\s*-->",
    re.DOTALL,
)
FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)", re.DOTALL)

# The keys a page's jb-frontmatter may set, in the order they are written
# (STYLEGUIDE.md, "Frontmatter"). `title` comes from `app_title`; everything else is set
# once for the whole book in content/myst.yml.
PAGE_FRONTMATTER_KEYS = ["subtitle", "short_title", "description", "label", "abbreviations"]
PROJECT_FRONTMATTER_KEYS = {"numbering", "math", "license"}
SHORT_TITLE_MAX = 40
DESCRIPTION_MAX = 160
# A description is plain text: markdown, math, and HTML do not render in it.
DESCRIPTION_MARKUP = re.compile(r"[$`*_\[\]{}<>\\]")

# Everything on an exported page that MyST's abbreviation transform does not
# touch: frontmatter, code (including `{marimo}` cells), math, inline code and
# role contents, links (text and target), citations, HTML, directive options,
# and `(label)=` targets. What is left is the prose that abbreviations apply to.
NON_PROSE_PATTERN = re.compile(
    r"""
      \A---\n.*?\n---\n
    | ^(`{3,}|~{3,}).*?^\1[ \t]*$
    | \$\$.*?\$\$
    | \$[^$\n]+\$
    | `[^`\n]*`
    | \[[^\]\n]*\]\([^)\n]*\)
    | \[@[^\]\n]*\]
    | @\w+
    | <!--.*?-->
    | <[^>\n]+>
    | ^:[\w-]+:[^\n]*$
    | ^\([^)\s]+\)=
    """,
    re.DOTALL | re.MULTILINE | re.VERBOSE,
)

# pymdownx-style `/// <kind> | Title` block, optionally followed by an
# `attrs: {class: ..., id: ...}` line, e.g.
#
#     /// admonition | 📐 **Theorem (Optimal Gain)**
#         attrs: {class: theorem dropdown, id: ch7-thm-optimal-gain}
#     Statement...
#     ///
#
# Blocks must not be nested: a block ends at the first `///` line.
ADMONITION_PATTERN = re.compile(
    r"^///[ \t]*(?P<kind>[\w-]+)[ \t]*(?:\|[ \t]*(?P<title>[^\n]*))?\n"
    r"(?:[ \t]*attrs:[ \t]*\{(?P<attrs>[^}\n]*)\}[ \t]*\n)?"
    r"(?P<body>.*?)"
    r"^///[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

# Admonition kinds MyST supports; `/// admonition` maps to MyST's generic one.
# Other pymdownx kinds (e.g. `info`, `success`) render in marimo but not MyST.
MYST_ADMONITION_KINDS = {
    "admonition", "note", "important", "hint", "seealso", "tip",
    "attention", "caution", "warning", "danger", "error",
}

# Classes that turn a block into a `prf:` directive instead of an admonition.
# Every other class is passed through to MyST's `:class:` (e.g. `dropdown`).
PRF_ROLE_CLASSES = {"theorem", "lemma", "corollary", "proof"}

# A glossary definition: a `/// note` block whose body starts with `<u>**Term**</u>`.
GLOSSARY_TERM_PATTERN = re.compile(r"<u>\*\*(?P<term>[^\n]+?)\*\*</u>[ \t]*$")

# A result's title, e.g. `📐 **Theorem (Optimal Gain)**`: the label word and
# the name in parentheses. The name may itself contain parentheses.
RESULT_TITLE_PATTERN = re.compile(r"\*\*(?P<word>[^\s(*]+)(?:[ \t]*\((?P<name>.*)\))?[ \t]*\*\*")

# `<!-- label: ch4-sec-kolmogorovs-axioms -->` on its own line, before the
# block it labels. Converted to MyST's `(ch4-sec-kolmogorovs-axioms)=`.
LABEL_COMMENT_PATTERN = re.compile(
    r"^[ \t]*<!--[ \t]*label:[ \t]*(?P<label>\S+?)[ \t]*-->[ \t]*$",
    re.MULTILINE,
)

# Label format from the style guide: lowercase ASCII words joined by hyphens.
LABEL_FORMAT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def spawn(cmd, **kwargs) -> subprocess.Popen:
    """Start a subprocess. On Mac/Linux, put it in its own process group so the
    whole tree (uv -> node -> server) can be killed together later."""
    if sys.platform != "win32":
        kwargs.setdefault("start_new_session", True)
    return subprocess.Popen(cmd, **kwargs)


def kill_tree(proc: subprocess.Popen) -> None:
    """Kill a process and everything it started."""
    if sys.platform == "win32":
        if proc.poll() is None:
            # /T = include child processes, /F = force
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                capture_output=True,
            )
        return

    # Mac/Linux: start_new_session=True made the process its own group leader,
    # so the group ID equals its PID.
    pgid = proc.pid
    try:
        os.killpg(pgid, signal.SIGTERM)  # polite request first
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(pgid, signal.SIGKILL)  # force anything still alive
    except ProcessLookupError:
        pass


def replace_with_retry(src: Path, dst: Path, attempts: int = 5) -> None:
    """os.replace, but retry briefly if Windows has the destination file locked."""
    for i in range(attempts):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if i == attempts - 1:
                raise
            time.sleep(0.05 * (i + 1))


def write_if_changed(path: Path, text: str) -> None:
    """Write text to path only if it differs from what's there, and do it
    atomically so the dev server never sees a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    replace_with_retry(tmp, path)


def iter_notebooks():
    """Yield all notebook .py files under NOTEBOOKS_DIR, skipping ignored dirs,
    paired with the path marimo should export raw markdown to."""
    for py_file in NOTEBOOKS_DIR.rglob("*.py"):
        rel_path = py_file.relative_to(NOTEBOOKS_DIR)
        parts = rel_path.parts[:-1]
        if IGNORED_DIRS.isdisjoint(parts):
            export_path = (EXPORT_DIR / rel_path).with_suffix(".md")
            yield py_file, export_path


def content_path_for(export_path: Path) -> Path:
    rel_path = export_path.relative_to(EXPORT_DIR)
    return PAGES_DIR / rel_path


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


def expected_page_label(stem: str) -> str:
    """The page label the style guide's "Labels" section prescribes for a notebook:
    `intro`, `ch7`, `appc`, or the stem itself (`index`)."""
    if stem == "introduction":
        return "intro"
    if match := re.match(r"(ch\d+)_", stem):
        return match.group(1)
    if match := re.match(r"appendix_([a-z])_", stem):
        return f"app{match.group(1)}"
    return stem


def project_abbreviations() -> dict:
    """`project.abbreviations` from content/myst.yml (read on every call, so
    the watcher picks up edits)."""
    try:
        config = yaml.safe_load(MYST_YML.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as error:
        warn(f"could not read abbreviations: {error}", str(MYST_YML))
        return {}
    return (config.get("project") or {}).get("abbreviations") or {}


def check_page_frontmatter(content: str, stem: str, source: str = "") -> dict:
    """Check a raw export's jb-frontmatter against STYLEGUIDE.md ("Frontmatter") and
    return its parsed contents."""
    match = JB_FRONTMATTER_PATTERN.search(content)
    if not match:
        warn("no `<!-- jb-frontmatter ... -->` comment", source)
        return {}
    try:
        page = yaml.safe_load(match.group("content")) or {}
    except yaml.YAMLError as error:
        warn(f"jb-frontmatter is not valid YAML: {error}", source)
        return {}
    if not isinstance(page, dict):
        warn("jb-frontmatter is not a mapping of keys to values", source)
        return {}

    for key in page:
        if key == "title":
            warn("`title` comes from `app_title`; remove it from jb-frontmatter", source)
        elif key in PROJECT_FRONTMATTER_KEYS:
            warn(f"`{key}` is set for the whole book in content/myst.yml; remove it from jb-frontmatter", source)
        elif key not in PAGE_FRONTMATTER_KEYS:
            warn(f"jb-frontmatter key `{key}` is not allowed", source)
    order = [key for key in page if key in PAGE_FRONTMATTER_KEYS]
    if order != sorted(order, key=PAGE_FRONTMATTER_KEYS.index):
        warn(f"jb-frontmatter keys should be in the order {', '.join(PAGE_FRONTMATTER_KEYS)}", source)

    required = ["description", "label"] + ([] if stem == "index" else ["subtitle"])
    for key in required:
        if not page.get(key):
            warn(f"jb-frontmatter has no `{key}`", source)

    label = page.get("label")
    if label and label != expected_page_label(stem):
        warn(f"page label `{label}` should be `{expected_page_label(stem)}`", source)

    title = ""
    if fm_match := FRONTMATTER_PATTERN.match(content):
        try:
            title = str((yaml.safe_load(fm_match.group(1)) or {}).get("title") or "")
        except yaml.YAMLError:
            pass
    short_title = page.get("short_title")
    if len(title) > SHORT_TITLE_MAX and not short_title:
        warn(f"title '{title}' is longer than {SHORT_TITLE_MAX} characters; add a `short_title`", source)
    if short_title and len(str(short_title)) > SHORT_TITLE_MAX:
        warn(f"`short_title` is longer than {SHORT_TITLE_MAX} characters", source)

    description = str(page.get("description") or "")
    if len(description) > DESCRIPTION_MAX:
        warn(f"`description` is {len(description)} characters; the limit is {DESCRIPTION_MAX}", source)
    if DESCRIPTION_MARKUP.search(description):
        warn("`description` is plain text: no markdown, math, or HTML", source)

    shared = project_abbreviations()
    for key in page.get("abbreviations") or {}:
        if key in shared:
            warn(f"abbreviation `{key}` is already in content/myst.yml; remove it from jb-frontmatter", source)
    return page


def check_abbreviation_matches(content: str, page_abbreviations: dict, source: str = "") -> None:
    """Warn about every abbreviation MyST would mark inside a longer word,
    such as `iff` in "Mifflin". This mirrors MyST's transform: each key is a
    case-sensitive substring, longer keys claim their text first, and a `null`
    key claims its text without adding a tooltip. A trailing plural `s`
    ("IMUs") is fine."""
    abbreviations = {**project_abbreviations(), **(page_abbreviations or {})}
    text = NON_PROSE_PATTERN.sub(lambda m: " " * len(m.group(0)), content)
    claimed = bytearray(len(text))
    found: dict[tuple[str, str], int] = {}
    for key in sorted((k for k in abbreviations if len(str(k)) > 1), key=lambda k: (-len(str(k)), str(k))):
        for match in re.finditer(re.escape(str(key)), text):
            start, end = match.span()
            if any(claimed[start:end]):
                continue
            claimed[start:end] = b"\x01" * (end - start)
            if abbreviations[key] is None:
                continue
            before = text[start - 1] if start else " "
            after = text[end:end + 1]
            plural = after == "s" and not text[end + 1:end + 2].isalpha()
            if before.isalpha() or (after.isalpha() and not plural):
                word_start, word_end = start, end
                while word_start and text[word_start - 1].isalpha():
                    word_start -= 1
                while word_end < len(text) and text[word_end].isalpha():
                    word_end += 1
                word = text[word_start:word_end]
                found[(str(key), word)] = found.get((str(key), word), 0) + 1
    for (key, word), count in found.items():
        warn(
            f"abbreviation `{key}` matches inside '{word}' ({count}x); "
            f"add `{word}: null` to the abbreviations in content/myst.yml",
            source,
        )


def comment_out_marimo_version(content: str) -> str:
    """Comment out the `marimo-version:` line marimo adds to frontmatter by
    default, so it's preserved for reference without being read as a page's
    actual YAML key."""
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return content

    yaml_text, rest = match.group(1), match.group(2)
    yaml_lines = [
        f"# {line}" if line.startswith(("marimo-version:", "css_file:")) else line
        for line in yaml_text.splitlines()
    ]
    return f"---\n{chr(10).join(yaml_lines)}\n---\n{rest}"


def warn(message: str, source: str = "") -> None:
    location = f" in {source}" if source else ""
    print(f"[marimo-sync] Warning{location}: {message}", file=sys.stderr)


def parse_attrs(text: str | None, source: str = "") -> tuple[list[str], str | None]:
    """Parse the inside of an `attrs: {class: a b, id: x}` line into its list
    of classes and its id. Both keys are optional."""
    classes: list[str] = []
    block_id = None
    if not text:
        return classes, block_id

    for item in text.split(","):
        if not item.strip():
            continue
        key, sep, value = item.partition(":")
        key, value = key.strip(), value.strip().strip("'\"")
        if not sep:
            warn(f"malformed attrs entry '{item.strip()}', skipping", source)
        elif key == "class":
            classes.extend(value.split())
        elif key == "id":
            block_id = value
        else:
            warn(f"unknown attrs key '{key}', skipping", source)

    if block_id is not None and not LABEL_FORMAT.match(block_id):
        warn(f"label '{block_id}' is not lowercase words joined by hyphens", source)
    return classes, block_id


def directive_options(block_id: str | None, classes: list[str]) -> list[str]:
    """MyST option lines for a block's label and its passed-through classes."""
    options = []
    if block_id:
        options.append(f":label: {block_id}")
    if classes:
        options.append(f":class: {' '.join(classes)}")
    return options


def convert_glossary(title: str, term: str, definition: str, options: list[str]) -> str:
    """A glossary definition: a MyST admonition wrapping a one-term glossary,
    with every definition line after the first indented by two spaces."""
    lines = definition.strip("\n").splitlines()
    definition_lines = [f": {lines[0]}"] + [
        f"  {line}" if line.strip() else "" for line in lines[1:]
    ]
    return "\n".join([
        f"::::{{admonition icon=false}} {title}",
        *options,
        ":::{glossary}",
        term,
        *definition_lines,
        ":::",
        "::::",
    ])


def convert_result(role: str, title: str, body: str, options: list[str], source: str) -> str:
    """A theorem, lemma, corollary, or proof: a MyST `prf:` directive, never
    numbered (results are referred to by name). MyST's book theme draws no
    end-of-proof mark, so a proof's own `$\\blacksquare$` is kept."""
    if role == "proof":
        return "\n".join([":::{prf:proof}", *options, ":enumerated: false", body, ":::"])

    name = ""
    title_match = RESULT_TITLE_PATTERN.search(title)
    if not title_match:
        warn(f"could not read the {role} title '{title}'", source)
    else:
        if title_match.group("word").lower() != role:
            warn(f"title '{title}' does not match its class '{role}'", source)
        name = (title_match.group("name") or "").strip()
        if not name:
            warn(f"{role} '{title}' has no name in parentheses", source)

    opening = f":::{{prf:{role}}}" + (f" {name}" if name else "")
    return "\n".join([opening, *options, ":enumerated: false", body, ":::"])


def apply_admonitions(content: str, source: str = "") -> str:
    """Convert every `/// <kind> | Title` block (with an optional `attrs` line)
    into MyST syntax:

    - a `/// note` block starting with `<u>**Term**</u>` becomes a glossary entry;
    - a block with a role class (`theorem`, `lemma`, `corollary`, `proof`)
      becomes the matching `prf:` directive;
    - any other block becomes a `:::{<kind> icon=false}` admonition.

    MyST icons are always off (`icon=false`). The `id` becomes `:label:`, and
    classes other than role classes are passed through as `:class:`."""

    def replace(match: re.Match) -> str:
        kind = match.group("kind")
        title = (match.group("title") or "").strip()
        body = match.group("body").strip("\n")
        classes, block_id = parse_attrs(match.group("attrs"), source)

        roles = [c for c in classes if c in PRF_ROLE_CLASSES]
        extra_classes = [c for c in classes if c not in PRF_ROLE_CLASSES]
        options = directive_options(block_id, extra_classes)

        if roles:
            if len(roles) > 1:
                warn(f"block '{title}' has several role classes {roles}; using '{roles[0]}'", source)
            if kind != "admonition":
                warn(f"{roles[0]} block '{title}' should be `/// admonition`, not `/// {kind}`", source)
            return convert_result(roles[0], title, body, options, source)

        if kind not in MYST_ADMONITION_KINDS:
            warn(f"`/// {kind}` has no MyST equivalent; left unconverted", source)
            return match.group(0)

        first_line, _, definition = body.partition("\n")
        term_match = GLOSSARY_TERM_PATTERN.match(first_line)
        if kind == "note" and term_match and definition.strip():
            return convert_glossary(title, term_match.group("term").strip(), definition, options)

        opening = f":::{{{kind} icon=false}}" + (f" {title}" if title else "")
        return "\n".join([opening, *options, body, ":::"])

    return ADMONITION_PATTERN.sub(replace, content)


def apply_label_comments(content: str, source: str = "") -> str:
    """Convert `<!-- label: x -->` lines into MyST `(x)=` targets."""

    def replace(match: re.Match) -> str:
        label = match.group("label")
        if not LABEL_FORMAT.match(label):
            warn(f"label '{label}' is not lowercase words joined by hyphens", source)
        return f"({label})="

    return LABEL_COMMENT_PATTERN.sub(replace, content)


def rewrite_public_paths(content: str) -> str:
    """Point `src="public/..."` asset references at the notebooks' public dir."""
    return content.replace('src="public/', 'src="../../notebooks/public/')


def remove_empty_comments(content: str) -> str:
    """Remove empty <!----> HTML comments."""
    return content.replace('<!---->', '  ')


def set_eval_false(content: str) -> str:
    return content.replace("```{marimo-config}\n", "```{marimo-config}\n:eval: false\n")


def postprocess_file(export_path: Path):
    """Read marimo's raw export from EXPORT_DIR, apply jb transforms, and
    write the result to the matching path in PAGES_DIR."""
    try:
        content = export_path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return

    page_frontmatter = check_page_frontmatter(content, export_path.stem, source=str(export_path))
    updated = apply_jb_options(content, source=str(export_path))
    updated = apply_jb_frontmatter(updated, source=str(export_path))
    updated = apply_label_comments(updated, source=str(export_path))
    updated = apply_admonitions(updated, source=str(export_path))
    updated = rewrite_public_paths(updated)
    updated = remove_empty_comments(updated)
    updated = comment_out_marimo_version(updated)
    if disable_eval:
        updated = set_eval_false(updated)
    check_abbreviation_matches(updated, page_frontmatter.get("abbreviations"), source=str(export_path))

    write_if_changed(content_path_for(export_path), updated)


def export_is_current(notebook_path: Path, export_path: Path) -> bool:
    """True if marimo's raw export is newer than the notebook, so `marimo
    export` (the slow step) can be skipped. `make clean` or --force resets this."""
    return (
        not force_export
        and export_path.exists()
        and export_path.stat().st_mtime >= notebook_path.stat().st_mtime
    )


def run_marimo_export(notebook_path: Path, export_path: Path) -> Path | None:
    if export_is_current(notebook_path, export_path):
        postprocess_file(export_path)
        return export_path

    export_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "marimo",
        "export",
        "md",
        str(notebook_path),
        "-o",
        str(export_path),
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
        postprocess_file(export_path)
        print(f"[marimo-sync] Successfully exported {notebook_path.name} -> {content_path_for(export_path).name}")
        return export_path

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


def export_all() -> bool:
    """Export every notebook. Each `marimo export` is a separate process, so
    they run in parallel."""
    notebooks = list(iter_notebooks())
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        results = list(pool.map(lambda args: run_marimo_export(*args), notebooks))
    return all(results)


def start_watcher(notebook_path: Path, export_path: Path) -> subprocess.Popen:
    export_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "marimo", "export", "md",
        str(notebook_path),
        "-o", str(export_path),
        "--flavor", "mystmd",
        "--watch",
    ]
    return spawn(cmd)


class JbOptionsHandler(PatternMatchingEventHandler):
    """Watches EXPORT_DIR for writes from marimo's own --watch processes and
    postprocesses each one into PAGES_DIR."""

    def __init__(self):
        super().__init__(patterns=["*.md"], ignore_directories=True)

    def on_created(self, event):
        postprocess_file(Path(event.src_path))

    def on_modified(self, event):
        postprocess_file(Path(event.src_path))


def serve(port: str, server_port: str):
    export_all()

    watchers: list[subprocess.Popen] = []
    jb_proc = None
    jb_observer = None
    try:
        for nb, export_path in iter_notebooks():
            watchers.append(start_watcher(nb, export_path))
        print(f"[marimo-sync] Watching {len(watchers)} notebook(s) with marimo --watch...")

        jb_observer = Observer()
        jb_observer.schedule(JbOptionsHandler(), str(EXPORT_DIR), recursive=True)
        jb_observer.start()

        jb_cmd = [
            "uv", "run", "jupyter-book", "start",
            "--port", port,
            "--server-port", server_port,
        ]
        print("[marimo-sync] Launching Jupyter Book dev server...")
        jb_proc = spawn(jb_cmd, cwd=CONTENT_DIR)
        jb_proc.wait()
    except KeyboardInterrupt:
        print("\n[marimo-sync] Shutting down...")
    finally:
        if jb_observer is not None:
            jb_observer.stop()
            jb_observer.join()
        for proc in [jb_proc, *watchers]:
            if proc is not None:
                kill_tree(proc)


def main():
    global disable_eval, force_export

    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Start watchers and dev server")
    parser.add_argument("--port", default="3102")
    parser.add_argument("--server-port", default="4102")
    parser.add_argument("--no-eval", action="store_true", help="Disable cell evaluation for faster builds")
    parser.add_argument("--force", action="store_true", help="Re-export every notebook, ignoring cached exports")
    args = parser.parse_args()
    disable_eval = args.no_eval
    force_export = args.force

    if args.serve:
        serve(args.port, args.server_port)
        
    elif not export_all():
        sys.exit(1)


if __name__=="__main__":
    main()