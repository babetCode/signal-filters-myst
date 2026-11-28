export PYTHONUTF8 = 1
export NODE_OPTIONS = --disable-warning=DEP0169

# Set NO_EVAL=1 to skip evaluating marimo cells (faster)
EVAL_FLAG = $(if $(NO_EVAL),--no-eval)

.PHONY: link-plugin sync-notebooks build-html start preview clean \
        book-build book-start book-dev check check-examples

# For jupyter-book-marimo plugin to work with Windows file paths
link-plugin:
	uv run python scripts/link_plugin.py

# Export marimo notebooks from notebooks/ to .md files in content/nb/
sync-notebooks:
	uv run python scripts/sync_notebooks.py $(EVAL_FLAG) && uv run python scripts/toc_generator.py

# Build static HTML in content/_build/html/
build-html:
	cd content && uv run jupyter-book build --html --strict

# Dev server for content/; does not watch notebooks
start:
	cd content && uv run myst start

# Serve the last static build at http://localhost:8000
preview:
	uv run python scripts/preview.py

# Full static build (used by CI)
book-build: link-plugin sync-notebooks build-html

# Export once, then start the dev server
book-start: link-plugin sync-notebooks start

# Export, watch notebooks, and start the dev server with live reload
book-write: link-plugin
	uv run python scripts/sync_notebooks.py --serve --port 3102 --server-port 4102 $(EVAL_FLAG)

# Check the notebooks against the style guide's mechanical rules (fast)
check:
	uv run python scripts/check_notebooks.py

# Also run every notebook and check the running examples (slow)
check-examples:
	uv run python scripts/check_notebooks.py --run

# Clean files
clean:
	uv run python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['content/_build', '_build', 'content/.jupyter-book-marimo', 'content/nb/.jupyter-book-marimo','.jupyter-book-marimo', 'content/.bin', '.bin', '.marimo-export']]"