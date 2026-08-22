.PHONY: book-build book-start clean

setup-plugin:
	@uv run python -c "import shutil, sys, os, pathlib; \
	src = pathlib.Path('.venv/Scripts/jupyter-book-marimo.exe') if sys.platform == 'win32' else pathlib.Path('.venv/bin/jupyter-book-marimo'); \
	dst = pathlib.Path('.venv/jupyter-book-marimo.exe'); \
	shutil.copy(src, dst); \
	os.chmod(dst, 0o755) if sys.platform != 'win32' else None"

build:
	rm -f dist/jupyter_book_marimo-*.whl dist/jupyter_book_marimo-*.tar.gz
	uv build

book-build: setup-plugin
	cd book && uv run jupyter-book build --html --strict

book-start: setup-plugin
	cd book && uv run jupyter-book start --port 3102 --server-port 4102

clean:
	rm -rf dist _build _site .jupyter-book-marimo docs/_build docs/_site docs/.jupyter-book-marimo
	rm -f src/jupyter_book_marimo/assets/container-widget.mjs src/jupyter_book_marimo/assets/islands-bridge.css
	find $(PYTHON_PATHS) -type d -name __pycache__ -prune -exec rm -rf {} +