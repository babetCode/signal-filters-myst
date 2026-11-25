export PYTHONUTF8 = 1

.PHONY: sync-notebooks link-plugin book-build book-start clean

link-plugin: # For jupyter-book-marimo on Windows
	uv run python scripts/link_plugin.py

sync-notebooks:
	uv run python scripts/sync_notebooks.py

book-build: sync-notebooks
	cd content && uv run jupyter-book build --html --strict

book-start: link-plugin # use `make book-start NO_EVAL=1` to avoid building marimo cells (faster)
	uv run python scripts/sync_notebooks.py --serve --port 3102 --server-port 4102

clean:
	uv run python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['content/_build', '_build', 'content/.jupyter-book-marimo', 'content/nb/.jupyter-book-marimo','.jupyter-book-marimo', 'content/.bin', '.bin', '.marimo-export']]"