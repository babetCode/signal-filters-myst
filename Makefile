export PYTHONUTF8 = 1

.PHONY: sync-notebooks book-build book-start clean

sync-notebooks:
	uv run python scripts/sync_notebooks.py

book-build: sync-notebooks
	cd content && uv run jupyter-book build --html --strict

book-start:
	uv run python scripts/sync_notebooks.py --serve --port 3102 --server-port 4102

clean:
	uv run python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['content/_build', '_build', 'content/.jupyter-book-marimo', '.jupyter-book-marimo', 'content/.bin', '.bin', '.marimo-export']]"