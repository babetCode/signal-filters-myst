.PHONY: book-build book-start clean

build:
	rm -f dist/jupyter_book_marimo-*.whl dist/jupyter_book_marimo-*.tar.gz
	uv build

book-build:
	cd book && uv run jupyter-book build --html --strict

book-start:
	cd book && uv run jupyter-book start --port 3102 --server-port 4102

clean:
	rm -rf dist _build _site .jupyter-book-marimo docs/_build docs/_site docs/.jupyter-book-marimo
	rm -f src/jupyter_book_marimo/assets/container-widget.mjs src/jupyter_book_marimo/assets/islands-bridge.css
	find $(PYTHON_PATHS) -type d -name __pycache__ -prune -exec rm -rf {} +