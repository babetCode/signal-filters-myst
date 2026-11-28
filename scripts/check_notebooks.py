"""
Check the notebooks against the mechanical rules of STYLEGUIDE.md.

    uv run python scripts/check_notebooks.py            # static checks (a second or two)
    uv run python scripts/check_notebooks.py --run      # also run every notebook and check
                                                         # the running examples
    uv run python scripts/check_notebooks.py notebooks/ch7_optimal_alpha.py   # report on one page

Every finding is printed as `path:line: error|note: message`. Errors break a rule and
make the script exit with status 1; notes point at something to review by eye and never
fail. Cross-page rules (unique glossary terms, which pages need a What's Next section)
always read every notebook, even when only some are reported on.

The rules, and where the style guide states them:

- fenced copies match their running cell                     (Code the Reader Sees)
- every editable cell is introduced by the editable-code note (Code the Reader Sees)
- page anatomy: Prerequisites, Summary, What's Next           (Page Anatomy)
- every `##`/`###` heading has a label                        (Labels)
- glossary terms are unique across the book                   (Glossary Terms)
- no Unicode math characters                                  (Math)
- no "proposition", no `echo=true`                            (Theorems; `# jb:` Options)
- SI units only (no pounds, feet, ...)                        (Units and Numbers)
- dependencies come from ALLOWED_DEPENDENCIES and match the imports   (Skeleton)
- with --run: running-example globals match scripts/running_examples.toml (Running Examples)
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import sys
import textwrap
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
EXAMPLES_TOML = PROJECT_ROOT / "scripts" / "running_examples.toml"

# The only dependencies a notebook may declare, with their exact specifiers.
ALLOWED_DEPENDENCIES = {
    "marimo>=0.25.1",
    "matplotlib==3.11.2",
    "numpy==2.5.3",
    "pandas==3.0.6",
    "schemdraw==0.23",
    "scipy==1.18.1",
}

# Pages exempt from parts of the page anatomy.
NO_PREREQUISITES = {"index", "introduction"}
NO_SUMMARY = {"index"}

EDITABLE_NOTE = (
    "**Editable code:** the output below is produced by the code in the editor that follows it. "
    "Edit the code and re-run the cell to see how the output changes."
)
PREREQUISITES_OPENING = "/// important | 🔗 **Prerequisites**"

JB_LINE = re.compile(r"^[ \t]*#\s*jb:\s*(?P<options>.+?)\s*$", re.M)
FENCED_COPY = re.compile(r"\A```python\n(?P<code>.*?)\n```\Z", re.S)
HEADING = re.compile(r"^(?P<hashes>#{2,3})[ \t]+(?P<text>.+?)[ \t]*$", re.M)
LABEL_COMMENT = re.compile(r"^[ \t]*<!--[ \t]*label:[ \t]*(?P<label>\S+?)[ \t]*-->[ \t]*$")
GLOSSARY_TERM = re.compile(r"^<u>\*\*(?P<term>[^\n]+?)\*\*</u>[ \t]*$", re.M)
TERM_ROLE = re.compile(r"\{term\}`(?:[^`<]*<(?P<target>[^>`]+)>|(?P<plain>[^`]+))`")
LINK_TARGET = re.compile(r"\]\(#(?P<label>[a-z0-9-]+)\)")
PAGE_OF_LABEL = re.compile(r"^(?P<page>index|intro|ch\d+|app[a-z])(?:-|$)")
BANNED_WORDS = re.compile(r"\bpropositions?\b", re.I)
REVIEW_WORDS = re.compile(r"\b(clearly|obviously|trivially|it is easy to see)\b", re.I)
IMPERIAL_UNITS = re.compile(
    r"\b(lbs?|pounds?|inch(?:es)?|ft|yards?|miles?|mph|ounces?|oz|fahrenheit)\b|°F", re.I
)
# Unicode math: Greek letters, combining accents (x̂), sub/superscripts, arrows,
# mathematical operators and symbols, and the Latin-1 signs ± × ÷ ² ³ ¹ ½ µ.
UNICODE_MATH = re.compile(
    "[̀-ͯͰ-Ͽ⁰-₟←-⇿∀-⋿⟀-⟯"
    "⦀-⧿⨀-⫿±×÷²³¹½µ]"
)
# Text the unit and math checks skip: label comments, `attrs` ids, and link targets
# (labels never change, so an old label may still name a unit).
SKIP_FOR_UNITS = re.compile(r"<!--\s*label:[^>]*-->|\bid:\s*[a-z0-9-]+|\]\(#[a-z0-9-]+\)")

# Notebook globals checked by --run: (global name, key in running_examples.toml,
# notebooks the name means this in, or None for every notebook that defines it).
EXAMPLE_GLOBALS = [
    ("true_weight", "scale.true_weight", None),
    ("scale_x", "scale.true_weight", None),
    ("scale_R", "scale.sigma**2", None),
    ("shift_R", "scale.sigma**2", None),
    ("bulk_rate", "bulking.rate", None),
    ("RW_RATE", "bulking.rate", None),
    ("R_BULK", "bulking.sigma**2", None),
    ("H_TRUE", "load_cell.h", None),
    ("tare_h", "load_cell.h", None),
    ("C_TRUE", "load_cell.c", None),
    ("tare_c", "load_cell.c", None),
    ("tare_sigma", "load_cell.sigma", None),
    ("PLATES", "load_cell.plates", None),
    ("PEND_L", "pendulum.length", None),
    ("GRAV", "pendulum.gravity", None),
    ("DAMP_C", "pendulum.damping", None),
    ("SIGMA_Z", "pendulum.sigma", {"ch15_extended_kalman_filter", "ch16_unscented_kalman_filter"}),
    ("FS", "imu.rate", {"ch19_ahrs"}),
    ("SIGMA_G", "imu.gyro_sigma", {"ch19_ahrs"}),
    ("GYRO_BIAS", "imu.gyro_bias", {"ch19_ahrs"}),
    ("SIGMA_A", "imu.accel_sigma", {"ch19_ahrs"}),
    ("ACCEL_BIAS", "imu.accel_bias", {"ch19_ahrs"}),
    ("SIGMA_M", "imu.mag_sigma", {"ch19_ahrs"}),
    ("M_N", "imu.mag_field", {"ch19_ahrs"}),
    ("GRAVITY", "imu.gravity", {"ch19_ahrs"}),
    ("G", "imu.gravity", {"ch20_strapdown_inertial_navigation", "ch21_zero_velocity_updates"}),
]
# Pages whose data reproduce only the first days of the canonical bulking data
# (a different truth afterwards, the same seed for the noise).
BULK_PREFIX = {"ch13_kalman_filter": 15}


# --- parsing -----------------------------------------------------------------


@dataclass
class Cell:
    name: str
    line: int                 # line of the `def`
    body: str                 # dedented source of the body, comments included
    params: list[str]
    markdown: str | None      # text of a static prose cell, dedented
    markdown_line: int = 0    # line where the markdown string starts
    jb: dict[str, str] = field(default_factory=dict)
    code_without_return: str = ""  # body without `# jb:` lines and the final return


@dataclass
class Notebook:
    path: Path
    text: str
    lines: list[str]
    cells: list[Cell]

    @property
    def stem(self) -> str:
        return self.path.stem


def is_app_cell(node: ast.AST) -> bool:
    if not isinstance(node, ast.FunctionDef):
        return False
    for deco in node.decorator_list:
        target = deco.func if isinstance(deco, ast.Call) else deco
        if isinstance(target, ast.Attribute) and target.attr == "cell":
            return True
    return False


def static_markdown(node: ast.FunctionDef) -> tuple[str | None, int]:
    """The text of a static prose cell (`def _(mo): mo.md("..."); return`)."""
    params = [a.arg for a in node.args.args]
    if params != ["mo"]:
        return None, 0
    stmts = [s for s in node.body if not isinstance(s, ast.Return)]
    if len(stmts) != 1 or not isinstance(stmts[0], ast.Expr):
        return None, 0
    call = stmts[0].value
    if not (
        isinstance(call, ast.Call)
        and isinstance(call.func, ast.Attribute)
        and call.func.attr == "md"
        and len(call.args) == 1
        and isinstance(call.args[0], ast.Constant)
        and isinstance(call.args[0].value, str)
    ):
        return None, 0
    return textwrap.dedent(call.args[0].value).strip("\n"), call.args[0].lineno


def parse_notebook(path: Path) -> Notebook:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    cells = []
    for node in ast.parse(text).body:
        if not is_app_cell(node):
            continue
        # The body starts after the signature, which ends at the first line ending in ":".
        start = node.lineno - 1
        while not lines[start].rstrip().endswith(":"):
            start += 1
        body_lines = lines[start + 1:node.end_lineno]
        body = textwrap.dedent("\n".join(body_lines))
        jb = {}
        if match := JB_LINE.search(body):
            for pair in match.group("options").split():
                key, _, value = pair.partition("=")
                jb[key] = value
        # The running code: without `# jb:` lines and without the final `return`.
        last = node.body[-1]
        keep_until = (last.lineno - 1) if isinstance(last, ast.Return) else node.end_lineno
        code = textwrap.dedent("\n".join(lines[start + 1:keep_until]))
        code = "\n".join(l for l in code.splitlines() if not JB_LINE.match(l)).strip("\n")
        markdown, md_line = static_markdown(node)
        cells.append(Cell(
            name=node.name, line=node.lineno, body=body, params=[a.arg for a in node.args.args],
            markdown=markdown, markdown_line=md_line, jb=jb, code_without_return=code,
        ))
    return Notebook(path=path, text=text, lines=lines, cells=cells)


# --- reporting -----------------------------------------------------------------


class Report:
    def __init__(self, only: set[Path] | None):
        self.only = only
        self.errors = 0
        self.notes = 0

    def add(self, nb: Notebook, line: int, kind: str, message: str) -> None:
        if self.only is not None and nb.path.resolve() not in self.only:
            return
        rel = nb.path.resolve().relative_to(PROJECT_ROOT)
        print(f"{rel}:{line}: {kind}: {message}")
        if kind == "error":
            self.errors += 1
        else:
            self.notes += 1

    def error(self, nb: Notebook, line: int, message: str) -> None:
        self.add(nb, line, "error", message)

    def note(self, nb: Notebook, line: int, message: str) -> None:
        self.add(nb, line, "note", message)


# --- checks ----------------------------------------------------------------------


def check_fenced_copies(nb: Notebook, report: Report) -> None:
    for prose, code in zip(nb.cells, nb.cells[1:]):
        if prose.markdown is None or not (match := FENCED_COPY.match(prose.markdown)):
            continue
        if code.jb.get("include") != "false":
            continue  # a fence of code that is not run, not a copy
        copy = textwrap.dedent(match.group("code")).strip("\n")
        if copy.rstrip() != code.code_without_return.rstrip():
            copy_lines, run_lines = copy.splitlines(), code.code_without_return.splitlines()
            first = next(
                (i for i, (a, b) in enumerate(zip(copy_lines, run_lines)) if a.rstrip() != b.rstrip()),
                min(len(copy_lines), len(run_lines)),
            )
            report.error(nb, code.line, f"running cell differs from the fenced copy above it "
                                        f"(first difference at line {first + 1} of the code)")


def check_editable_cells(nb: Notebook, report: Report) -> None:
    for before, cell in zip([None, *nb.cells], nb.cells):
        if cell.jb.get("editor") != "true":
            continue
        if cell.jb.get("server-output") != "false":
            report.error(nb, cell.line, "an `editor=true` cell needs `server-output=false`")
        if before is None or before.markdown is None or before.markdown.strip() != EDITABLE_NOTE:
            report.error(nb, cell.line, "an `editor=true` cell must follow a prose cell with exactly the editable-code note")


def check_echo(nb: Notebook, report: Report) -> None:
    for cell in nb.cells:
        if cell.jb.get("echo") == "true":
            report.error(nb, cell.line, "`echo=true` is not used; show code as a fenced copy instead")


def prose_cells(nb: Notebook) -> list[Cell]:
    return [c for c in nb.cells if c.markdown is not None and c.name != "frontmatter"]


def check_anatomy(nb: Notebook, needs_whats_next: bool, report: Report) -> None:
    prose = prose_cells(nb)
    if not prose:
        report.error(nb, 1, "no prose cells")
        return
    if nb.stem not in NO_PREREQUISITES and not prose[0].markdown.startswith(PREREQUISITES_OPENING):
        report.error(nb, prose[0].markdown_line, "the first prose cell must be the Prerequisites box")

    headings = [(c, m.group("text")) for c in prose for m in HEADING.finditer(c.markdown) if m.group("hashes") == "##"]
    titles = [t for _, t in headings]
    if nb.stem not in NO_SUMMARY:
        if "Summary" not in titles:
            report.error(nb, 1, "no `## Summary` section")
        elif needs_whats_next:
            if "What's Next" not in titles:
                report.error(nb, 1, "no `## What's Next` section, but another page's Prerequisites box needs this page")
            elif titles[-2:] != ["Summary", "What's Next"]:
                report.error(nb, 1, "the last two `##` sections must be Summary, then What's Next")
        elif titles[-1] not in ("Summary", "What's Next") or ("What's Next" in titles and titles[-2:] != ["Summary", "What's Next"]):
            report.error(nb, 1, "the page must end with `## Summary` (and then `## What's Next`, if it has one)")


def check_heading_labels(nb: Notebook, report: Report) -> None:
    for cell in prose_cells(nb):
        lines = cell.markdown.splitlines()
        for i, line in enumerate(lines):
            if HEADING.match(line) and not (i > 0 and LABEL_COMMENT.match(lines[i - 1])):
                report.error(nb, cell.markdown_line + i, f"heading '{line.strip()}' has no `<!-- label: ... -->` line before it")


def check_text_rules(nb: Notebook, report: Report) -> None:
    in_header = True
    for number, line in enumerate(nb.lines, start=1):
        if in_header and not line.startswith("#"):
            in_header = False
        scrubbed = SKIP_FOR_UNITS.sub(" ", line)
        for match in UNICODE_MATH.finditer(scrubbed):
            report.error(nb, number, f"Unicode math character '{match.group(0)}' (U+{ord(match.group(0)):04X}); write it in LaTeX or in words")
        for match in IMPERIAL_UNITS.finditer(scrubbed):
            report.error(nb, number, f"non-SI unit '{match.group(0)}'")
    for cell in prose_cells(nb):
        for i, line in enumerate(cell.markdown.splitlines()):
            if match := BANNED_WORDS.search(line):
                report.error(nb, cell.markdown_line + i, f"'{match.group(0)}': results are theorems, lemmas, or corollaries, and the logic chapter's word is 'statement'")
            if match := REVIEW_WORDS.search(line):
                report.note(nb, cell.markdown_line + i, f"'{match.group(0)}': fine for the size of an effect, not in place of a justification")


def check_dependencies(nb: Notebook, report: Report) -> None:
    header = re.search(r"^# /// script\n(?P<body>(?:#.*\n)*?)# ///$", nb.text, re.M)
    if not header:
        report.error(nb, 1, "no `# /// script` dependency header")
        return
    declared = re.findall(r'"([^"]+)"', header.group("body"))
    for dep in declared:
        if dep not in ALLOWED_DEPENDENCIES:
            report.error(nb, 1, f"dependency '{dep}' is not in ALLOWED_DEPENDENCIES ({', '.join(sorted(ALLOWED_DEPENDENCIES))})")
    declared_names = {re.split(r"[<>=!~\[]", d, maxsplit=1)[0] for d in declared}
    imported = set()
    for node in ast.walk(ast.parse(nb.text)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported.add(node.module.split(".")[0])
    third_party = {re.split(r"[<>=]", d, maxsplit=1)[0] for d in ALLOWED_DEPENDENCIES}
    for name in sorted((imported & third_party) - declared_names):
        report.error(nb, 1, f"'{name}' is imported but not listed in the dependency header")
    for name in sorted(declared_names - imported - {"marimo"}):
        report.error(nb, 1, f"'{name}' is listed in the dependency header but never imported")


def glossary_terms(nb: Notebook) -> list[tuple[str, int]]:
    terms = []
    for cell in prose_cells(nb):
        for i, line in enumerate(cell.markdown.splitlines()):
            if match := GLOSSARY_TERM.match(line):
                terms.append((match.group("term").strip(), cell.markdown_line + i))
    return terms


def page_label(stem: str) -> str:
    if stem == "introduction":
        return "intro"
    if match := re.match(r"(ch\d+)_", stem):
        return match.group(1)
    if match := re.match(r"appendix_([a-z])_", stem):
        return f"app{match.group(1)}"
    return stem


def prerequisite_pages(nb: Notebook, term_pages: dict[str, str]) -> set[str]:
    """Labels of the pages this page's Prerequisites box needs. Items marked
    "(optional" are not needs, nor are "**Before ...**" pointers for a later page."""
    prose = prose_cells(nb)
    if not prose or not prose[0].markdown.startswith(PREREQUISITES_OPENING):
        return set()
    needed = set()
    for item in prose[0].markdown.splitlines()[1:]:
        if "(optional" in item or item.lstrip("- ").startswith("**Before"):
            continue
        for match in LINK_TARGET.finditer(item):
            if page := PAGE_OF_LABEL.match(match.group("label")):
                needed.add(page.group("page"))
        for match in TERM_ROLE.finditer(item):
            term = (match.group("target") or match.group("plain")).strip().lower()
            if term in term_pages:
                needed.add(term_pages[term])
    needed.discard(page_label(nb.stem))
    return needed


# --- running examples ----------------------------------------------------------


def lookup(examples: dict, key: str):
    path, _, power = key.partition("**")
    section, name = path.split(".")
    value = examples[section][name]
    return value ** int(power) if power else value


def canonical_arrays(examples: dict):
    import numpy as np

    s = examples["scale"]
    scale_z = np.round(s["true_weight"] + np.random.default_rng(s["seed"]).normal(0.0, s["sigma"], s["n_samples"]), s["decimals"])
    b = examples["bulking"]
    days = np.arange(1, b["days"] + 1)
    bulk_x = b["start_weight"] + b["rate"] * (days - 1)
    bulk_z = np.round(bulk_x + np.random.default_rng(b["seed"]).normal(0.0, b["sigma"], b["days"]), b["decimals"])
    return {"scale_z": scale_z, "bulk_z": bulk_z}


def run_notebook(path: Path) -> dict:
    import matplotlib

    matplotlib.use("Agg")
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location(f"_check_{path.stem}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _, defs = module.app.run()
        return dict(defs)
    finally:
        sys.path.remove(str(path.parent))


def check_running_examples(nb: Notebook, examples: dict, canonical: dict, report: Report) -> None:
    import numpy as np

    try:
        defs = run_notebook(nb.path)
    except Exception as error:  # noqa: BLE001 - report any failure to run
        report.error(nb, 1, f"could not run the notebook: {error!r}")
        return
    for name, key, notebooks in EXAMPLE_GLOBALS:
        if name not in defs or (notebooks is not None and nb.stem not in notebooks):
            continue
        expected = lookup(examples, key)
        if not np.allclose(np.asarray(defs[name], dtype=float), np.asarray(expected, dtype=float)):
            report.error(nb, 1, f"`{name}` is {defs[name]!r}; running_examples.toml says {key} = {expected!r}")
    for name, expected in canonical.items():
        if name not in defs:
            continue
        actual = np.asarray(defs[name], dtype=float)
        n = BULK_PREFIX.get(nb.stem, len(expected)) if name == "bulk_z" else len(expected)
        if actual.shape != expected.shape or not np.allclose(actual[:n], expected[:n]):
            report.error(nb, 1, f"`{name}` differs from the canonical data built from running_examples.toml")


# --- main ------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("notebooks", nargs="*", type=Path, help="report only on these notebooks")
    parser.add_argument("--run", action="store_true", help="also run every notebook and check the running examples")
    args = parser.parse_args()

    paths = sorted(NOTEBOOKS_DIR.glob("*.py"))
    only = {p.resolve() for p in args.notebooks} if args.notebooks else None
    notebooks = [parse_notebook(p) for p in paths]
    report = Report(only)

    # Cross-page facts: where each term is defined, and which pages are needed.
    term_pages: dict[str, str] = {}
    first_definition: dict[str, tuple[Notebook, int, str]] = {}
    for nb in notebooks:
        for term, line in glossary_terms(nb):
            key = term.lower()
            if key in first_definition:
                other, other_line, _ = first_definition[key]
                report.error(nb, line, f"glossary term '{term}' is already defined in {other.path.name}:{other_line}")
            else:
                first_definition[key] = (nb, line, term)
                term_pages[key] = page_label(nb.stem)
    needed_by: dict[str, set[str]] = {}
    for nb in notebooks:
        for page in prerequisite_pages(nb, term_pages):
            needed_by.setdefault(page, set()).add(page_label(nb.stem))

    examples = canonical = None
    if args.run:
        examples = tomllib.loads(EXAMPLES_TOML.read_text(encoding="utf-8"))
        canonical = canonical_arrays(examples)

    for nb in notebooks:
        if only is not None and nb.path.resolve() not in only:
            continue
        check_fenced_copies(nb, report)
        check_editable_cells(nb, report)
        check_echo(nb, report)
        check_anatomy(nb, bool(needed_by.get(page_label(nb.stem))), report)
        check_heading_labels(nb, report)
        check_text_rules(nb, report)
        check_dependencies(nb, report)
        if args.run:
            check_running_examples(nb, examples, canonical, report)

    checked = len(only) if only is not None else len(notebooks)
    print(f"[check-notebooks] {checked} notebook(s): {report.errors} error(s), {report.notes} note(s)")
    sys.exit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
