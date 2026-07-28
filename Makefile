PYTHON = python3
MAIN_SCRIPT = a_maze_ing.py
CONFIG = config.txt

install:
	$(PYTHON) -m pip install --user --upgrade pip build flake8 mypy wheel || true

run:
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG)

lint:
	flake8 .
	$(PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	$(PYTHON) -m mypy --strict .

clean:
	rm -rf __pycache__ .mypy_cache build dist *.egg-info

fclean: clean
	rm -f mazegen-*.whl mazegen-*.tar.gz

package: fclean
	$(PYTHON) -m build
	mv dist/mazegen-*.whl .
	mv dist/mazegen-*.tar.gz .
	rm -rf dist *.egg-info


.PHONY: install run debug clean fclean lint lint-strict package
