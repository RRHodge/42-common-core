PYTHON  := python3
MAP     ?= maps/test.txt
SRC     := $(wildcard *.py)
MYPY_FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

.PHONY: install run gui debug lint lint-strict clean fclean help

help:
	@echo "make install       - installe pydantic, pygame, flake8, mypy"
	@echo "make run MAP=file  - simulation en terminal (defaut: $(MAP))"
	@echo "make gui MAP=file  - interface graphique 3D"
	@echo "make debug MAP=file- simulation sous pdb"
	@echo "make lint          - flake8 + mypy"
	@echo "make lint-strict   - flake8 + mypy --strict"
	@echo "make clean         - supprime les caches"

install:
	$(PYTHON) -m pip install pydantic pygame flake8 mypy

run:
	$(PYTHON) main.py $(MAP)

gui:
	$(PYTHON) gui.py $(MAP)

debug:
	$(PYTHON) -m pdb main.py $(MAP)

lint:
	$(PYTHON) -m flake8 $(SRC)
	$(PYTHON) -m mypy $(MYPY_FLAGS) $(SRC)

lint-strict:
	$(PYTHON) -m flake8 $(SRC)
	$(PYTHON) -m mypy --strict --ignore-missing-imports $(SRC)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache

fclean: clean
