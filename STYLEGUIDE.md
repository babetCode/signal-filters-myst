# Project Style Guide

This guide is the single reference for writing and revising the book's pages. It is written for the author and for any agent asked to improve a chapter. When this guide and an older document (such as `notebooks-old-drafts/v2_style_guide.md`) disagree, this guide wins.

Two markers flag conventions that are not fully in place yet:

- **(needs tooling):** the convention depends on a `scripts/sync_notebooks.py` change listed in [§12.1](#121-tooling-changes-this-guide-assumes). Until that change exists, do not convert existing notebooks to the new form.
- **(open):** the author has not decided yet. The options are listed in [§12.2](#122-open-decisions). Follow the interim rule given in the text.

## Contents

1. [How the Book Is Built](#1-how-the-book-is-built)
2. [Notebook Files](#2-notebook-files)
3. [Code the Reader Sees](#3-code-the-reader-sees)
4. [Figures and Interactive Elements](#4-figures-and-interactive-elements)
5. [Page Anatomy](#5-page-anatomy)
6. [Markdown Elements](#6-markdown-elements)
7. [Labels, Links, Terms, and Citations](#7-labels-links-terms-and-citations)
8. [Writing](#8-writing)
9. [Notation](#9-notation)
10. [Book Reference](#10-book-reference)
11. [Checking a Notebook](#11-checking-a-notebook)
12. [Pending Tooling and Open Decisions](#12-pending-tooling-and-open-decisions)

---

## 1. How the Book Is Built

- All pages are written as [marimo notebooks](https://docs.marimo.io) (`notebooks/*.py`).
- `scripts/sync_notebooks.py` exports each notebook to [MyST Markdown](https://mystmd.org/guide) in `content/nb/*.md`. Plain markdown cells become plain text, and code cells become `{marimo}` [directives](https://mystmd.org/guide/directives) that run as [islands](https://docs.marimo.io/guides/island_example/) in the reader's browser. The script also rewrites some marimo syntax into MyST syntax (admonitions, glossary entries, frontmatter, `# jb:` options).
- Jupyter Book 2, with the [jupyter-book-marimo](https://marimo-team.github.io/jupyter-book-marimo) plugin, builds `content/` into a static site.

```mermaid
flowchart LR
  mo("Marimo<br>Notebook<br>(.py)") -->|sync_notebooks.py| md("MyST<br>Markdown<br>(.md)")
  md -->|Jupyter Book Marimo| page("Webpage<br>(.html)")
```

```mermaid
graph LR
  jbm(Jupyter<br>Book<br>Marimo) -->|Plug-in for| jb(Jupyter<br>Book 2)
  jb -->|Wrapper around| myst(MyST<br>Document<br>Engine)
  myst -->|Creates| web(Final<br>Website)
```

**Source of truth.** Edit only `notebooks/*.py`. `content/nb/` is generated and git-ignored; never edit it by hand. The table of contents and part titles live in `content/myst.yml`.

**Make targets:**

| Target | What it does |
|:---|:---|
| `make sync-notebooks` | Export every notebook to `content/nb/` (add `NO_EVAL=1` to skip cell evaluation) |
| `make book-build` | Link the plugin, export, and run a strict HTML build into `content/_build/html/` |
| `make book-write` | Export, watch the notebooks, and serve with live reload |
| `make preview` | Serve the last static build at `http://localhost:8000` |
| `make clean` | Delete build output |

**Agent scope.** An agent assigned to a notebook may edit that `notebooks/*.py` file and its `notebooks/public/*.svg` outputs, and may add entries to `content/refs.bib`. Leave `content/myst.yml`, `scripts/`, other notebooks, and the rest of `content/` untouched unless asked.

---

## 2. Notebook Files

### 2.1 Skeleton

Copy this exactly, changing only the title, subtitle, abbreviations, and dependencies.

```python
# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="7. The Optimal α", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Combining Two Noisy Estimates"
    abbreviations:
      iff: if and only if
      diff: null
    numbering:
      equations: false
    -->
    """)
    return


@app.cell
def imports():
    # jb: include=false
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from textwrap import dedent
    from pathlib import Path

    return Path, dedent, mo, np, plt


@app.cell
def display_settings(dedent, mo, plt):
    # jb: include=false
    plt.style.use("default")

    def graphic(x):
        return mo.Html(dedent(f'''\
            <div class="graphic">
                {mo.as_html(x)}
            </div>
            '''))

    return (graphic,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Prose goes here. One `mo.md` cell per subsection.
    """)
    return


if __name__ == "__main__":
    app.run()
```

- **Title:** `app_title` is the page title shown on the site. Chapters use `"<n>. <Title>"`, appendices `"Appendix <L>: <Title>"` (see [§10.1](#101-book-structure)). Do not repeat the title as a `#` heading.
- **Frontmatter:** the first `<!-- jb-frontmatter ... -->` comment is merged into the page's YAML frontmatter by the sync script. Keep `numbering: equations: false`.
- **Dependencies:** list only what the notebook imports. Allowed: `marimo>=0.25.1`, `matplotlib==3.11.2`, `numpy==2.5.3`, `pandas==3.0.6`, `schemdraw==0.23`, `scipy==1.18.1`.
- **CSS:** keep `css_file="notebook-styles.css"`; the sync script comments it out of the exported frontmatter.

### 2.2 Named Cells

Every notebook has these named cells, in this order, at the top:

| Cell name | Contents | `# jb:` option |
|:---|:---|:---:|
| `frontmatter` | The `jb-frontmatter` comment | none |
| `imports` | Every import in the notebook, and nothing else | `include=false` |
| `display_settings` | `plt.style.use`, the `graphic` helper, and any other display-only setup (for example the LaTeX-macro cell in [§2.6](#26-latex-macros)) | `include=false` |

Hidden setup that later cells depend on (generated data, constants, helper functions the reader does not need to read) goes in `include=false` cells with descriptive names such as `data`, `simulator`, or `plot_helpers`. Prefer one `data` cell for a page's generated data. Some existing notebooks name their display cell `display_format`; rename it to `display_settings` when you next edit the notebook.

### 2.3 `# jb:` Options

The sync script turns cells into `{marimo}` directives. marimo-native settings (`hide_code`, cell name, `disabled`, column) are exported automatically. The others are set with a comment on the first line of the cell:

```python
# jb: option1=value1 option2=value2
```

| Option | Default | Effect | Use in this book |
|:---|:---:|:---|:---|
| `include` | `true` | Keep this cell's node in the page | `include=false` for imports, display settings, data, and figure-saving cells |
| `editor` | `false` | Show the source in an editable marimo editor | Reference implementations and editable examples ([§3](#3-code-the-reader-sees)) |
| `server-output` | `true` | Include build-time output in the island | `server-output=false` together with `editor=true` on cells that produce output, to avoid duplicated output when the reader re-runs the cell |
| `echo` | `false` | Show the source as static text | **Do not use** ([§3](#3-code-the-reader-sees)) |
| `eval` | `true` | Run the cell during the build | Leave at the default |
| `output` | `true` | Render the output island | Leave at the default |
| `error` | `true` | Render errors instead of failing | Leave at the default |
| `hide-output` | `false` | Hide the rendered output | Leave at the default |
| `unparsable` | `false` | Skip parsing invalid code | Leave at the default |

Apart from the uses above, avoid `# jb:` comments.

### 2.4 marimo Rules

- Every global name is defined in exactly one cell.
- Use `_`-prefixed names for cell-local variables (`_fig`, `_ax`).
- A cell's signature lists every global it reads, and its `return` tuple lists every global other cells use.
- Use raw strings (`r"""`) for anything with backslashes.
- In `rf"""` strings, double literal braces (`{{ }}`); LaTeX braces count.
- **Prose cells:** `@app.cell(hide_code=True)`, `def _(mo):`, `mo.md(r""" ... """)`, content indented 4 spaces. They are exported as plain MyST text. Use one cell per subsection.
- **Computed markdown:** an `mo.md` cell whose text depends on other variables (an `rf"""` string with live values) is exported as a marimo code cell and rendered by marimo, not MyST. In such cells, `{term}` references, `[@cite]` citations, footnotes, labels, and cross-reference links do not work on the site. Keep computed cells to plain text and math, keep them small, and put everything else in static cells whose only parameter is `mo`.
- **Interactive widgets:** create the `mo.ui` element in one cell and read `.value` in a different cell. Display the element with its output, e.g. `mo.vstack([slider, graphic(fig)])`.

### 2.5 Determinism, Speed, and Safety

- Seed every random generator: `rng = np.random.default_rng(<fixed seed>)`. Use the seeds in [§10.3](#103-running-examples) for the running examples.
- Keep each notebook's total run time under about 20 s: vectorize, and keep Monte Carlo sizes modest.
- Never call `eval` or `exec` on user input. Parse it with a small purpose-built parser.

### 2.6 LaTeX Macros

Only Chapters 1–3 and Appendices A–B use custom macros (`\existsin`, `\forallin`, `\existssubseteq`, `\forallsubseteq`). A page that uses them defines them in both places, copying the pattern in `notebooks/ch1_language_of_logic.py`:

- a `math:` block in the `jb-frontmatter` comment (for MyST), and
- an `include=false` cell in `display_settings` that calls `mo.latex(...)` with the `\newcommand` definitions, then `mo.output.clear()` (for the marimo editor).

Every other page writes `\operatorname{Var}`, `\mathbb E`, and so on explicitly. Do not add new macros.

---

## 3. Code the Reader Sees

Static `echo=true` source is not used: on the site it has no syntax highlighting and does not wrap lines. Show code in one of two ways.

- **Runnable code** (reference implementations such as `kalman_filter(...)`, and examples the reader is invited to change): a normal code cell with `# jb: editor=true`. The reader then sees the code that actually runs, with highlighting, and can edit it. Add `server-output=false` if the cell produces output.
- **Code that is not run** (a fragment, pseudo-code, a comparison with another library, a snippet in a language other than Python): a fenced block in a static prose cell, e.g. ```` ```python ````.

Never show the same code twice, and never show a fenced copy of code that a hidden cell runs: the two will drift apart.

Code the reader sees:

- uses ASCII only, in identifiers, comments, and docstrings, so it can be copied and typed: `x_hat`, `x_pred`, `delta_x_hat`, not `x̂` or `Δx̂`. In comments, write math the way code would, e.g. `x_hat[k]` or `P_pred`.
- uses names that match the text's symbols: `x_hat` for $\hat x_k$, `x_pred` for $\hat x_k^-$, `P_pred` for $P_k^-$, `K` for $K_k$, `y_tilde` for $\tilde y_k$.
- has a one-line docstring saying what the function returns, in terms of the text's quantities.
- is short. Each comment explains *why* a line exists or which equation it implements, not what Python does.

---

## 4. Figures and Interactive Elements

### 4.1 Figures

- **Interactive figures:** build the matplotlib figure in a cell that reads the widget values and output `graphic(fig)`.
- **Static figures and diagrams:**
  - An `include=false` cell saves an SVG to `Path(__file__).parent / "public" / "<page>_<name>.svg"`, e.g. `ch7_gain_curve.svg`. The page prefix keeps one notebook from overwriting another's figure.
  - A separate prose cell shows it with `<img src="public/ch7_gain_curve.svg" class="graphic" alt="..." />`. The `alt` text describes what the figure shows.
- **Plot style:** default matplotlib style; axis labels with units; `ax.grid(visible=True, alpha=0.9, linewidth=0.4)`; italic titles (`style='italic'`). Labels and legends use the same symbols as the text.
- **Color roles:**
  - measurements: hollow black circles, or C0 for dense streams
  - estimates: C1
  - truth: black solid line
  - predictions: red dotted line
  - ±2σ bands: C1 shading with `alpha=0.2`

### 4.2 Interactive Elements

Every page has at least one interactive element that teaches something the static text cannot. Each interactive element:

- is introduced by a paragraph immediately before it that states (1) what it shows, (2) what each control changes, and (3) what to look for when changing it.
- shows only quantities defined in the text, labeled with the text's symbols.
- discloses anything random or arbitrary in it (for example "the intervals are chosen at random" or "the first 20 rationals in the enumeration above"), and how each displayed object relates to the others.
- is followed, where it helps, by a sentence stating the conclusion the reader should have reached.

If a reader cannot say what an interactive demonstrates after reading its introduction, rewrite the introduction or replace the interactive.

---

## 5. Page Anatomy

Every page after the Introduction has, in order:

1. **Prerequisites box** ([§6.1](#61-admonitions)) listing exactly what the page uses, each item linked to the most specific target ([§7.2](#72-cross-references)).
2. **Opening paragraph:** the key concept and why it matters for filtering.
3. **Body:** `##` for sections, `###` for subsections. Never use `#` (the page title comes from `app_title`). Headings use title case.
4. **Summary** (`## Summary`): a short restatement of the key results.
5. **What's Next** (`## What's Next`): one paragraph linking to the next page and saying which question it answers.

---

## 6. Markdown Elements

### 6.1 Admonitions

Admonitions are written in marimo's `///` syntax so they render in the editor, and the sync script converts them to MyST. Each role below has exactly one form; do not use other admonition kinds without the author's approval.

| Role | marimo source | MyST output | Status |
|:---|:---|:---|:---:|
| Definition | `/// note \| 📖 **Definition**` | `admonition` + `glossary` ([§6.2](#62-definitions)) | in place |
| Key Idea | `/// attention \| 🗝️ **Key Idea**` | `attention` | in place |
| Assumptions and Failure Modes | `/// caution \| ⚠️ **Assumptions and Failure Modes**` | `caution` | in place |
| Tip (a skippable aside) | `/// tip \| **Title**` | `tip` | in place |
| Prerequisites | `/// info \| 🔗 **Prerequisites**` | `seealso` | **needs tooling** |
| Theorem, Lemma, Corollary | `/// important \| 📐 **Theorem (Name)**` | `prf:theorem`, `prf:lemma`, `prf:corollary` | **needs tooling** |
| Proof | `/// admonition \| ✍️ **Proof**` | `prf:proof` | **needs tooling** |

Interim rules until the tooling exists: Prerequisites boxes stay `/// seealso` (MyST renders it; marimo does not), and theorems and proofs stay as they are.

Every admonition's second line is exactly `    attrs: {class: no-icon}` (4 spaces), and the block ends with `///` alone on a line. The sync regexes depend on this. The kinds are reserved for these roles: for example, use `caution` only for Assumptions and Failure Modes.

- **Key Idea:** the one or two sentences a reader should remember from a section.
- **Assumptions and Failure Modes:** follows every major result (after its proof). It lists each assumption the result needs and what goes wrong when that assumption fails.
- **Tip:** material a reader can skip without losing the thread: notation in other texts, practical advice, a second route to a result.
- **Prerequisites:**

  ```
  /// seealso | 🔗 **Prerequisites**
      attrs: {class: no-icon}
  - [Chapter 6: Variance of a Linear Combination](#ch6-thm-variance-of-a-linear-combination): the variance of a weighted sum.
  - [Appendix C: Derivatives](#appc-sec-derivatives) (optional; only for the alternative derivation).
  ///
  ```

Never nest admonitions: the sync regexes end a block at the first `///` line. Do not use the hidden `:::{div}` heading trick.

### 6.2 Definitions

A definition is a glossary entry, so `{term}` references work across the book. The `<u>**Term**</u>` line comes immediately after the `attrs` line, followed by a blank line and the definition:

```
/// note | 📖 **Definition**
    attrs: {class: no-icon}
<u>**Covariance**</u>

The covariance of random variables $X$ and $Y$ with finite variances is
$$\operatorname{Cov}(X, Y) := \mathbb E\big[(X - \mathbb E X)(Y - \mathbb E Y)\big].$$
///
```

- The term is in sentence case (`Probability measure`), has no math, and is unique across the book ([§10.2](#102-glossary-terms)).
- The definition is a necessary-and-sufficient test ([§8.1](#81-guiding-principles)) and uses only words already defined.
- Related secondary terms defined in the same box (such as *pairwise disjoint* inside **Disjoint**) are italicized at their definition. They have no glossary entry of their own; link to them with the main term.

### 6.3 Theorems, Lemmas, Corollaries, and Proofs

Labels:

- **Theorem:** a main result.
- **Lemma:** a result used mainly to prove another.
- **Corollary:** a result that follows from a preceding result by a short additional argument.
- Never use "Proposition": the logic chapter's word is "statement", and "proposition" would be ambiguous.

Every result has a name, in title case and in parentheses, so that it can be referred to by name ([§8.2](#82-precise-language)). The proof follows its result immediately.

```
/// important | 📐 **Theorem (Optimal Gain)**
    attrs: {class: no-icon}
Statement...
///

/// admonition | ✍️ **Proof**
    attrs: {class: no-icon}
Proof text... $\blacksquare$
///
```

When a proof is not given, the proof box says so and cites or links to one: "Not proved here; see [@rudin1976, Thm. 7.16]."

**(needs tooling)** Once the sync script supports it, each result also gets a label in its `attrs` line, `attrs: {class: no-icon, id: ch7-thm-optimal-gain}`, and is exported as:

```
:::{prf:theorem} Optimal Gain
:label: ch7-thm-optimal-gain
Statement...
:::
```

### 6.4 Tables

- Every table's separator row has explicit alignment colons. Left-align columns of text (`:---`); center columns of short entries such as symbols, numbers, or yes/no (`:---:`).
- Keep cells short. A formula longer than a short expression does not belong in a cell after prose, where it would wrap mid-formula: give it its own column, or move it below the table.
- Every table is introduced by a sentence saying what it compares.

### 6.5 Math

- Inline math `$...$`; display math `$$...$$`. A display equation is part of the sentence around it and carries its punctuation.
- Use LaTeX for every mathematical symbol in prose, including Greek letters (`$\alpha$`, not α). Unicode math is allowed only where LaTeX cannot render: `app_title`, `content/myst.yml`, and code.
- Never put math inside `{term}` link text: MyST renders it as raw source. **(open)** Interim rule for terms whose name contains a symbol: put the symbol outside the link, `$\sigma$-{term}`algebra <sigma-algebra>``.
- Follow the notation in [§9](#9-notation). A page that needs a symbol not listed there defines it in the text before using it.

### 6.6 Footnotes

- A footnote (`[^name]`) is defined in the same `mo.md` cell that references it.
- Use footnotes for informal first uses of later terms ([§7.4](#74-words-used-before-their-definition)) and for side remarks that would interrupt the sentence. Anything the argument depends on belongs in the text.

---

## 7. Labels, Links, Terms, and Citations

### 7.1 Labels

A label is a name for a heading or a result that links can point to. Labels are unique across the book.

- **Format:** `<page>-<kind>-<slug>`, lowercase ASCII with hyphens.
  - `<page>`: `index`, `intro`, `ch1` … `ch21`, `appa` … `appd`.
  - `<kind>`: `sec` (heading), `thm`, `lem`, `cor` (results), `fig`, `tbl`, `eq`.
  - `<slug>`: the heading or result name, e.g. `ch4-sec-kolmogorovs-axioms`, `ch4-thm-discrete-probability-measures`, `appc-sec-series`.
- **Headings:** put `(label)=` on its own line immediately before the heading, in the same `mo.md` cell. **(open)** This line shows as plain text in the marimo editor; see [§12.2](#122-open-decisions).
- **Results:** see [§6.3](#63-theorems-lemmas-corollaries-and-proofs) **(needs tooling)**.
- Label every `##` and `###` heading and every named result that another page links to, or is likely to. Before renaming or removing a label, grep `notebooks/*.py` for links to it.

### 7.2 Cross-References

- **Link to the most specific target** that contains what is referenced: the theorem, definition, or section, not its page. Link to a whole page (`[Chapter 7](ch7_optimal_alpha.md)`) only when the whole page is meant.
- **Syntax:** `[link text](#label)`, which works across pages. Always give link text; never `[](#label)`, which renders a page-relative number such as "Theorem 3".
- **Link text** names the target. When the target is on another page, the link text or its sentence also names that page: "by the [Closure Properties lemma](#ch4-lem-closure-properties)" on the same page; "[Appendix C: Series](#appc-sec-series)" or "the [Recursion Theorem](#ch2-thm-recursion) of Chapter 2" from another page.
- **Definitions:** link to a defined term with `{term}`, not with a label.
- Until a target has a label, link to its page and name the section in the link text: `[Appendix C: Series](appendix_c_calculus.md)`.

### 7.3 Glossary Terms

- Reference a term with `` {term}`variance` `` or `` {term}`variances <variance>` ``. The part in angle brackets matches the glossary term's spelling; case does not matter.
- Link the first use of a term in each section. Do not link every use.
- Reference only terms that exist ([§10.2](#102-glossary-terms)) or that your page defines.
- No math inside the link text ([§6.5](#65-math)).

### 7.4 Words Used Before Their Definition

If a word must be used informally before its definition, mark the first informal use with a footnote that links to the definition:

```
[^informal-probability]: Used informally here; defined precisely in [Chapter 4: Probability Measures](#ch4-sec-kolmogorovs-axioms).
```

### 7.5 Citations

- Cite every published work (book, paper, preprint, datasheet) by its `content/refs.bib` key, not with an inline link. Use the form that reads best:
  - `[@kalman1960]` renders as (Kalman, 1960). This is the usual form.
  - `@kalman1960` renders as Kalman (1960). Use it when the authors are part of the sentence.
  - `[@barshalom2002, Ch. 5]` or `@barshalom2002 [Ch. 5]` points to a chapter or section; `[see @kalman1960]` adds a lead-in.
  - `[@godel1938; @cohen1963]` cites several works together.
- Add a missing work to `content/refs.bib` before citing it, without changing other entries. Key it by first author and year (`kalman1960`); datasheets and undated works get a descriptive key (`avia_hx711_datasheet`).
- Take an entry's details from its DOI record or publisher, never from memory. Give the `doi` if there is one, otherwise a `url`.

### 7.6 Web Links

Use an inline markdown link for web resources that are not published works (Wikipedia, software documentation, project websites). Link only URLs you have confirmed are correct.

---

## 8. Writing

### 8.1 Guiding Principles

These come from the Guiding Principles in `notebooks/index.py` and are not negotiable.

1. **Concision, as the author defines it:** first include everything in the dependency hierarchy that the key concept is built on, with complete understanding and precise definitions. Only then use as few words as possible. Achieve concision through choice of concepts, organization, and wording; never through imprecision, approximation, or assumed knowledge.
2. **Definitions:** define every word whose meaning here is different from, or more specific than, its everyday meaning. Define it before its first use, and afterwards use it only with that meaning. A definition is a set of requirements that are necessary and sufficient for belonging to the category the word names.
3. **Dependency order:** nothing is used before it is introduced.
4. **Example first:** start with a concrete example, then generalize.
5. **Justification:** justify every step. Prove when possible; otherwise state the result precisely and cite or link a proof.
6. **Interactivity:** every page has at least one meaningful interactive element ([§4.2](#42-interactive-elements)).
7. **Limits:** state assumptions, and what happens when they fail.
8. **Minimal prerequisites:** build concepts from the ground up. When a concept is not worth building in the book, link to a resource that does.

### 8.2 Precise Language

Each rule below came up in proofreading. The examples are from earlier drafts.

1. **Use quantifier words that cannot be misread.** Write "every" or "each" for "for all", and "some" or "at least one" for "there exists". Do not use "any", which can be read either way.
   - Unclear: "pairwise disjoint if any two distinct members of $\mathcal A$ are disjoint"
   - Clear: "pairwise disjoint if every two distinct members of $\mathcal A$ are disjoint"
2. **Name every result you refer to.** Do not write "the lemma", "the next theorem", "the result above", or "this". Write the result's name, and link it ([§7.2](#72-cross-references)).
   - Unclear: "the next theorem does this once for all models of this kind"
   - Clear: "the Discrete Probability Measures theorem below does this once for all models of this kind"
3. **Give every pronoun and abstract noun a clear antecedent.** "It", "this", "the connection", or "the result" must refer to something named in the same sentence or the one before. When a sentence asserts a relationship, it names both sides.
   - Unclear: "Chapter 6 proves the connection."
   - Clear: "Chapter 6 proves that the relative frequency of an event converges to its probability (the weak law of large numbers)."
4. **Keep types straight.** Do not say that an object *is* something of a different kind: a question is not a set, and a function is not a number. Say what corresponds to what.
   - Unclear: "A question about its value, 'is $X$ in $B$?', is the set of outcomes $X^{-1}[B]$."
   - Clear: "The question 'is $X$ in $B$?' has the answer *yes* exactly for the outcomes in $X^{-1}[B]$."
5. **Only a definition may look like a definition.** A sentence of the form "*X* is a *Y*: ..." or "a *Y* is ..." reads as a definition of *Y*. When the sentence only describes a property of *X*, rephrase it so it cannot be read as defining *Y*. Italics in running text mark a word being defined in that sentence.
   - Unclear: "Every filter in this book is a *recursion*: it computes the estimate $\hat x_k$ from the previous estimate $\hat x_{k-1}$ and the newest measurement $z_k$."
   - Clear: "Every filter in this book computes the estimate $\hat x_k$ from the previous estimate $\hat x_{k-1}$ and the newest measurement $z_k$. A rule of this kind, which defines each term of a sequence from the one before, is called a recursion (made precise by the Recursion Theorem below)."
6. **Never leave the reader in suspense.** Every forward reference says what is coming and where.
   - Unclear: "Not every subset of $\mathbb R$ is a Borel set; we meet one below."
   - Clear: "Not every subset of $\mathbb R$ is a Borel set (the [Vitali set](#ch4-sec-vitali) is an example)."
7. **Use the imperative only for mathematical steps and thought experiments.** "Choose $p \in [0, 1]$", "Let $A \subseteq \Omega$", and "Imagine that you step on the scale" are fine. A way of thinking about something is described, not commanded.
   - Unclear: "Think of $p_n$ as a mass placed at the outcome $\omega_n$."
   - Clear: "$p_n$ can be thought of as a mass placed at the outcome $\omega_n$."
8. **Use logical connectives only in their logical sense.** "Conversely" introduces the converse of the statement just made, and the sentence says which statement that is. "So", "hence", and "therefore" introduce a consequence of what precedes them. "Similarly" means the same argument works with named changes.
   - Unclear: "Conversely, every probability measure on $(\Omega, \mathcal P(\Omega))$ with $\Omega$ countable arises this way."
   - Clear: "The converse of the Discrete Probability Measures theorem also holds: every probability measure on $(\Omega, \mathcal P(\Omega))$ with $\Omega$ countable arises this way."
9. **Do not claim that something is obvious.** Do not write "clearly", "obviously", "trivially", or "it is easy to see". Give the one-line reason instead.
   - Unclear: "Axioms 1 and 2 clearly hold."
   - Clear: "Axiom 1 holds because $p$ and $1 - p$ are in $[0, 1]$, and axiom 2 because $\mathbb P(\Omega) = 1$ by definition."
10. **Explain unexpected generality on the spot.** When a statement is more general or weaker than the reader expects at that point, say why in the same place. For example, if a sum of probabilities is said to lie in $[0, \infty]$, say why the range is not yet known to be $[0, 1]$, and which fact narrows it.
11. **Answer the obvious question.** If a careful reader would stop and ask "why not just...?" or "is this the same as ...?", answer it where it arises, briefly, or link to where it is answered.

### 8.3 Spelling and Terminology

- American spelling. Spell-check every page.
- "Fraenkel", not "Frankel". AHRS stands for *attitude and heading reference system*.
- Call $\hat x_k^-$ the **prediction** until Chapter 8, where *prior* is defined.
- Use "statement", not "proposition" ([§6.3](#63-theorems-lemmas-corollaries-and-proofs)).

---

## 9. Notation

### 9.1 Global Notation

| Symbol | Meaning | Introduced |
|:---|:---|:---:|
| $k \in \mathbb N$ | time step; measurements start at $k = 1$; $k = 0$ is the initial condition | Intro |
| $x_k$ | true value (state) at step $k$ (scalar in Parts I–II) | Intro |
| $z_k$ | measurement at step $k$ | Intro |
| $\hat x_k$ | estimate after incorporating $z_k$ | Intro |
| $\hat x_k^-$ | prediction: estimate of $x_k$ before $z_k$ is incorporated (**not** called "prior" until Ch 8) | Intro |
| $\tilde y_k := z_k - \hat x_k^-$ (later $z_k - h\hat x_k^-$, $\mathbf z_k - \mathbf H\hat{\mathbf x}_k^-$) | innovation | Intro |
| $\alpha$, later $K_k$ | gain; Ch 7 derives the optimal $\alpha$ and renames it $K_k$ | Intro / Ch 7 |
| $\Delta x_k$ | predicted change from step $k-1$ to $k$ | Intro |
| $e_k := \hat x_k - x_k$, $e_k^- := \hat x_k^- - x_k$ | estimation and prediction errors | Ch 7 |
| $v_k := z_k - x_k$ (or $z_k - h x_k$), $R$ | measurement noise and its variance | Ch 5 / Ch 7 |
| $w_k$, $Q$ | process noise and its variance | Ch 9 |
| $P_k$, $P_k^-$ | error variances of $\hat x_k$ and $\hat x_k^-$ | Ch 7 |
| $S_k$ | innovation variance (covariance) | Ch 9 |
| $(\Omega, \mathcal F, \mathbb P)$ | probability space; $\mathbb P$ is blackboard bold to avoid clashing with $P_k$ | Ch 4 |
| $\mathbb E$, $\operatorname{Var}$, $\operatorname{Cov}$ | expectation, variance, covariance | Ch 6 |
| $X, Y, Z$ | random variables are uppercase in Ch 4–6; Ch 7 explicitly switches to the filtering convention of lowercase $x_k, z_k, v_k$ for random quantities | Ch 5 / Ch 7 |
| $F_X$, $f_X$, $p_X$ | CDF, PDF, PMF of $X$ | Ch 5 |
| $\mathcal N(\mu, \sigma^2)$, $\mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$ | normal distribution | Ch 5 / Ch 12 |
| $\mathbb N = \{0, 1, 2, \ldots\}$, $\mathbb N^+ := \mathbb N \setminus \{0\}$ | natural numbers | Ch 2 / Ch 3 |
| $A^c := \Omega \setminus A$ | complement relative to an ambient set | Ch 3 |
| $f[A]$, $f^{-1}[B]$ | image and preimage of sets; square brackets distinguish them from $f(a)$ and the inverse function | Ch 3 |
| bold lowercase / bold uppercase | vectors / matrices (Part III on); scalars stay plain | Ch 12 |
| $\mathbf x_k, \mathbf P_k, \mathbf F, \mathbf B, \mathbf u_k, \mathbf H, \mathbf Q, \mathbf R, \mathbf K_k, \mathbf S_k, \mathbf I$ | Kalman filter quantities (Part III) | Ch 13 |
| $f(\cdot)$, $h(\cdot)$, $\mathbf F_k = \partial f/\partial \mathbf x$, $\mathbf H_k = \partial h/\partial \mathbf x$ | nonlinear process and measurement functions and their Jacobians | Ch 15 |
| $\alpha_{\text{UT}}, \beta_{\text{UT}}, \kappa, \lambda$ | unscented-transform parameters (subscripted so they don't clash with the gains $\alpha$, $\beta$) | Ch 16 |
| $\Delta t$ | sample period | Ch 10 |
| $[\mathbf a]_\times$ | skew-symmetric (cross-product) matrix: $[\mathbf a]_\times \mathbf b = \mathbf a \times \mathbf b$ | App D / Ch 17 |

### 9.2 Orientation Conventions (Ch 17–21; identical in every chapter)

- **Navigation frame $n$:** local-level ENU: $x$ = East, $y$ = North, $z$ = Up. Gravity $\mathbf g^n = [0, 0, -g]^\top$ with $g = 9.81\ \text{m/s}^2$.
- **Body frame $b$:** FLU: $x$ = forward, $y$ = left, $z$ = up. At zero attitude the body frame coincides with ENU, facing East.
- $\mathbf R^n_b$ maps body coordinates to navigation coordinates: $\mathbf v^n = \mathbf R^n_b \mathbf v^b$.
- **Euler angles, ZYX (yaw–pitch–roll):** $\mathbf R^n_b = \mathbf R_z(\psi)\,\mathbf R_y(\theta)\,\mathbf R_x(\phi)$, with roll $\phi$, pitch $\theta$, yaw $\psi$. Elementary rotations are active and right-handed.
- **Quaternions:** Hamilton convention, scalar-first, $q = [q_w, q_x, q_y, q_z]$; product $\otimes$. $q^n_b$ rotates body to navigation: $[0, \mathbf v^n] = q^n_b \otimes [0, \mathbf v^b] \otimes (q^n_b)^*$. Mention that the JPL convention differs.
- **Kinematics:**
  - $\dot{\mathbf R}^n_b = \mathbf R^n_b [\boldsymbol\omega^b]_\times$
  - $\dot q = \tfrac12\, q \otimes [0, \boldsymbol\omega^b]$
  - $\boldsymbol\omega^b$ is the body angular rate relative to the navigation frame. Earth rotation is neglected; say so.
- **Specific force:** $\mathbf f^b = (\mathbf R^n_b)^\top(\mathbf a^n - \mathbf g^n)$. At rest and level it reads $[0, 0, +g]$.
- **IMU models:**
  - $\boldsymbol\omega_m = \boldsymbol\omega^b + \mathbf b_g + \mathbf n_g$
  - $\mathbf f_m = \mathbf f^b + \mathbf b_a + \mathbf n_a$
  - magnetometer: $\mathbf m_m = (\mathbf R^n_b)^\top \mathbf m^n + \mathbf n_m$, with $\mathbf m^n = [0, 22, -42]^\top\ \mu\text{T}$ (points North and down)
- **Error-state attitude convention** (Ch 19 and Ch 21): right (body-frame) perturbation, $q = \hat q \otimes \delta q(\delta\boldsymbol\theta)$, $\mathbf R = \hat{\mathbf R}\,\operatorname{Exp}(\delta\boldsymbol\theta) \approx \hat{\mathbf R}(\mathbf I + [\delta\boldsymbol\theta]_\times)$.
- **Default IMU parameters:**
  - 100 Hz
  - gyro white-noise $\sigma = 0.01$ rad/s; gyro bias 0.01 rad/s per axis (constant or a slow random walk)
  - accelerometer white-noise $\sigma = 0.05\ \text{m/s}^2$; accelerometer bias $0.05\ \text{m/s}^2$ per axis
  - magnetometer noise $\sigma = 0.5\ \mu\text{T}$

---

## 10. Book Reference

### 10.1 Book Structure

`content/myst.yml` is the source of truth for the order and the part titles. Titles and subtitles come from each notebook's `app_title` and `subtitle`.

| File | Title | Subtitle |
|:---|:---|:---|
| `index.py` | Home | |
| `introduction.py` | Introduction | Building Intuition |
| **Part I: Choosing α** | | |
| `ch1_language_of_logic.py` | 1. Language of Logic | From Statements to Proofs |
| `ch2_axioms_of_set_theory.py` | 2. Axioms of Set Theory | From Axioms to Natural Numbers |
| `ch3_sets_for_probability.py` | 3. Sets for Probability | Complements, Preimages, and Infinity |
| `ch4_probability_spaces.py` | 4. Probability Spaces | Measuring Uncertainty |
| `ch5_random_variables.py` | 5. Random Variables | From Outcomes to Numbers |
| `ch6_expectation_and_variance.py` | 6. Expectation and Variance | Why Averaging Works |
| `ch7_optimal_alpha.py` | 7. The Optimal α | Combining Two Noisy Estimates |
| `ch8_bayesian_view.py` | 8. The Bayesian View | Priors, Likelihoods, and Posteriors |
| **Part II: The Scalar Kalman Filter** | | |
| `ch9_noise_levels.py` | 9. Noise Levels | The Scalar Kalman Filter |
| `ch10_process_models.py` | 10. Process Models | Predicting the Next State |
| `ch11_measurement_functions.py` | 11. Measurement Functions | When Sensors Measure Something Else |
| **Part III: State Vectors** | | |
| `ch12_vectors_matrices_covariance.py` | 12. Vectors, Matrices, and Covariance | Uncertainty in Many Dimensions |
| `ch13_kalman_filter.py` | 13. The Kalman Filter | The Multivariate Filter |
| `ch14_kalman_filters_in_practice.py` | 14. Kalman Filters in Practice | Tuning, Fusion, and Consistency |
| **Part IV: Nonlinearity** | | |
| `ch15_extended_kalman_filter.py` | 15. The Extended Kalman Filter | Linearization |
| `ch16_unscented_kalman_filter.py` | 16. The Unscented Kalman Filter | Sigma Points |
| **Part V: Orientation** | | |
| `ch17_rotations.py` | 17. Rotations | Frames, Matrices, and Singularities |
| `ch18_quaternions.py` | 18. Quaternions | Singularity-Free Attitude |
| `ch19_ahrs.py` | 19. Attitude and Heading Reference Systems | Fusing Gyroscopes, Accelerometers, and Magnetometers |
| **Part VI: Inertial Navigation for Gait** | | |
| `ch20_strapdown_inertial_navigation.py` | 20. Strapdown Inertial Navigation | Dead Reckoning a Walking Foot |
| `ch21_zero_velocity_updates.py` | 21. Zero-Velocity Updates | Gait Analysis with a Foot-Mounted IMU |
| **Appendices** | | |
| `appendix_a_formal_logic.py` | Appendix A: Formal Logic | Syntax, Semantics, and Proof |
| `appendix_b_number_systems.py` | Appendix B: Constructing the Number Systems | From Natural Numbers to Real Numbers |
| `appendix_c_calculus.py` | Appendix C: Calculus | Limits, Derivatives, and Integrals |
| `appendix_d_linear_algebra.py` | Appendix D: Linear Algebra | From Vectors to Matrix Calculus |

**Main path and appendices.** The main path never sacrifices precision: every definition is precise and every result is proved or cited. The appendices hold foundational material that many readers already know. When a main-path page relies on an appendix result, its Prerequisites box says so and links to the specific section.

### 10.2 Glossary Terms

Each term is defined exactly once, on the page below; every other page references it with `{term}`. Before defining a new term, grep `notebooks/*.py` for `<u>**Term**</u>` (case-insensitive) to make sure it is not already defined, then add it to this table.

| Page | Terms defined |
|:---|:---|
| Index | Definition |
| Introduction | Signal, Noise, Estimate, Filter, Prediction, Innovation, Exponential moving average |
| Ch 1 | Statement, Truth table, Sufficient condition, Necessary condition, Tautology, Logically equivalent, Predicate, Quantifier, Axiom, Proof, Theorem, Lemma, Corollary, Counterexample |
| Ch 2 | Subset, Empty set, Union, Intersection, Set difference, Power set, Successor, Inductive set, Ordered pair, Cartesian product, Relation, Domain, Range, Function, Codomain, Natural numbers |
| Ch 3 | Complement, Indexed family, Sequence, Disjoint, Partition, Image, Preimage, Injective, Surjective, Bijective, Composition, Inverse function, Equinumerous, Finite, Countable, Uncountable, Field, Ordered field, Upper bound, Supremum, Infimum, Complete ordered field, Absolute value, Interval, Extended real numbers |
| Ch 4 | Sample space, Outcome, Sigma-algebra, Event, Generated sigma-algebra, Borel sigma-algebra, Probability measure, Probability space, Almost surely, Conditional probability, Independent events |
| Ch 5 | Random variable, Distribution, Cumulative distribution function, Discrete random variable, Probability mass function, Probability density function, Continuous random variable, Uniform distribution, Normal distribution, Joint distribution, Joint density, Marginal density, Independent random variables, Independent and identically distributed, Stochastic process, Measurement noise |
| Ch 6 | Expected value, Variance, Standard deviation, Covariance, Correlation coefficient, Uncorrelated, Estimator, Estimator bias, Unbiased, Mean squared error, Sample mean |
| Ch 7 | Estimation error, Error variance, Gain, Optimal gain |
| Ch 8 | Conditional density, Prior, Likelihood, Posterior, Evidence, Minimum mean squared error estimator, Maximum a posteriori estimate, Bayes filter |
| Ch 9 | Sample variance, Quantization, Process noise, White noise, Random walk, Kalman filter, Steady-state gain, Innovation variance, Normalized innovation squared, Chi-squared distribution, Filter consistency |
| Ch 10 | System, Control input, System state, Process model, Deterministic, Linear system, Discretization, Autocorrelation |
| Ch 11 | Measurement function, Measurement model, Calibration, Least squares, Sensor bias |
| Ch 12 | Random vector, Mean vector, Covariance matrix, Cross-covariance matrix, Multivariate normal distribution, Mahalanobis distance, Confidence ellipse |
| Ch 13 | State-space model, State transition matrix, Measurement matrix, Process noise covariance, Measurement noise covariance, Innovation covariance, Joseph form, Kalman gain, Observability, Alpha-beta filter |
| Ch 14 | Sequential update, Sensor fusion, Gating, Normalized estimation error squared, Filter divergence |
| Ch 15 | Nonlinear system, Linearization, Extended Kalman filter |
| Ch 16 | Sigma points, Unscented transform, Unscented Kalman filter, Particle filter |
| Ch 17 | Reference frame, Rotation matrix, Special orthogonal group, Euler angles, Angular velocity, Gimbal lock, Axis-angle representation, Rotation vector |
| Ch 18 | Quaternion, Hamilton product, Quaternion conjugate, Unit quaternion, Double cover |
| Ch 19 | Gyroscope, Specific force, Accelerometer, Inertial measurement unit, Magnetometer, Attitude, Heading, Complementary filter, Error-state Kalman filter |
| Ch 20 | Dead reckoning, Strapdown inertial navigation, Drift, Stride, Gait cycle, Stance phase, Swing phase, Zero-velocity detector |
| Ch 21 | Pseudo-measurement, Zero-velocity update, Zero angular rate update, Stride length, Cadence, Gait speed, Foot clearance |
| App A | Formula, Free variable, Bound variable, Sentence, Structure, Model, Theory, Logical consequence, Formal proof, Operation, Term, Conservative extension |
| App B | Equivalence relation, Equivalence class, Quotient set, Integers, Rational numbers, Dedekind cut |
| App C | Limit of a sequence, Convergent, Cauchy sequence, Series, Limit of a function, Continuous, Derivative, Differentiable, Taylor polynomial, Riemann sum, Riemann integral, Antiderivative, Exponential function, Natural logarithm, Improper integral, Partial derivative, Gradient, Jacobian, Differential equation |
| App D | Vector, Dot product, Norm, Matrix, Linear map, Matrix product, Transpose, Identity matrix, Invertible matrix, Linear independence, Basis, Rank, Determinant, Trace, Orthogonal matrix, Eigenvalue, Eigenvector, Symmetric matrix, Positive definite, Positive semidefinite, Cholesky decomposition, Schur complement, Cross product, Skew-symmetric matrix, Matrix exponential |

### 10.3 Running Examples

Reuse these exactly so that numbers agree from page to page.

- **Bathroom scale** (Intro, Ch 5–9):
  - true weight 155 lb, constant while standing
  - HX711 load-cell amplifier at 10 samples/s (it supports 10 or 80)
  - measurement noise $\sigma = 1$ lb ($R = 1\ \text{lb}^2$), Gaussian, seed 1
  - 3 s of data: 30 samples
- **Bulking** (Intro, Ch 9, 10, 13):
  - 28 daily weigh-ins starting at 155 lb; true gain 1.4 lb/week (0.2 lb/day)
  - daily reading noise $\sigma = 1$ lb (water and food fluctuations dominate)
  - person: age 23, height 175 cm, male, activity multiplier 1.5 (moderate)
  - Mifflin–St Jeor BMR; 3500 kcal per lb [@wishnofsky1958]
  - In Ch 10, TDEE is linear in weight, so the model is $x_k = a x_{k-1} + b u_k + c$ with $u_k$ the daily energy intake.
  - Canonical data: `k = np.arange(1, 29); x_true = 155 + 0.2*(k-1); z = np.round(x_true + np.random.default_rng(2).normal(0, 1, 28), 1)`. Pages that need a different truth (such as Ch 13's diet change) still use seed 2 for the measurement noise.
- **Load-cell counts** (Ch 11):
  - raw counts $z = h x + c + v$ with $h = 20{,}000$ counts/lb and offset $c = 85{,}000$ counts
  - noise $\sigma = 20{,}000$ counts (= 1 lb)
  - calibration plates: 0, 45, 90, 135 lb
- **1-D cart** (Ch 14): a position sensor at 10 Hz ($\sigma = 0.5$ m) plus an accelerometer at 100 Hz used as the control input; foreshadows Part VI.
- **Pendulum** (Ch 15–16):
  - $L = 1$ m, $g = 9.81\ \text{m/s}^2$, light damping $c = 0.1\ \text{s}^{-1}$
  - state $[\theta, \omega]$; $\Delta t = 0.01$ s; truth integrated with RK4
  - measurement: horizontal bob position $L\sin\theta$ at 20 Hz, $\sigma = 0.05$ m
- **IMU** (Ch 19–21): the default parameters in [§9.2](#92-orientation-conventions-ch-1721-identical-in-every-chapter). The gait simulator is written in Ch 20 and copied verbatim into Ch 21 (each notebook is self-contained).

---

## 11. Checking a Notebook

Run these from the project root after every change, and fix the notebook until all of them pass.

```sh
uv run marimo check --strict notebooks/<file>.py   # marimo's structural checks
uv run python notebooks/<file>.py                  # runs every cell; must finish without errors in about 20 s
make book-build                                    # exports all notebooks and runs a strict HTML build
```

The strict build fails on unresolved `{term}` references, cross-reference labels, and citations. Running a notebook rewrites its SVGs in `notebooks/public/`; that is expected.

Then read the rendered page (`make preview`) and check, by eye:

- every admonition rendered as a box, not as raw `///` text
- every link and `{term}` reference goes to the right place
- tables, math, and figures display without wrapping or overflow
- every interactive element works and matches its introduction

---

## 12. Pending Tooling and Open Decisions

### 12.1 Tooling Changes This Guide Assumes

These are changes to `scripts/sync_notebooks.py`. Until each is made, follow the interim rule in the section it belongs to.

1. **Prerequisites** ([§6.1](#61-admonitions)): convert `/// info` blocks to `:::{seealso icon=false}`, then change the existing `/// seealso` Prerequisites boxes to `/// info` so they render in the marimo editor.
2. **Labels in `attrs`** ([§6.3](#63-theorems-lemmas-corollaries-and-proofs)): accept `attrs: {class: no-icon, id: <label>}` in both admonition regexes. The current regexes match only `attrs: {class: no-icon}` exactly, so adding an `id` now silently breaks the conversion.
3. **Results** ([§6.3](#63-theorems-lemmas-corollaries-and-proofs)): convert `/// important | 📐 **Theorem (Name)**` to `:::{prf:theorem} Name` (and likewise `Lemma` to `prf:lemma`, `Corollary` to `prf:corollary`), with `:label:` taken from the `attrs` id.
4. **Proofs** ([§6.3](#63-theorems-lemmas-corollaries-and-proofs)): convert `/// admonition | ✍️ **Proof**` to `:::{prf:proof}`. Check whether MyST draws its own end-of-proof mark; if it does, strip the trailing `$\blacksquare$` during export.

### 12.2 Open Decisions

1. **Heading labels in the marimo editor** ([§7.1](#71-labels)): `(label)=` works in MyST today but shows as literal text in marimo. The alternative is an HTML comment, `<!-- label: ch4-sec-kolmogorovs-axioms -->`, which marimo hides and the sync script would convert to `(label)=`, in the same way it already handles `jb-frontmatter`.
2. **Math in glossary-term links** ([§6.5](#65-math)): for terms like σ-algebra, choose between
   - (a) the symbol outside the link, `$\sigma$-{term}`algebra <sigma-algebra>`` (the interim rule; only "algebra" is linked),
   - (b) the term spelled out in words, `{term}`sigma-algebra``, or
   - (c) a Unicode symbol in the link text, `{term}`σ-algebra <sigma-algebra>`` (has caused publishing problems before).
3. **Result numbering:** `prf:` directives are numbered per page by default ("Theorem 3"). Choose whether to keep the numbers (for example as `Theorem 4.3`, using a page enumerator) or turn them off, given that cross-references always use names ([§7.2](#72-cross-references)).
