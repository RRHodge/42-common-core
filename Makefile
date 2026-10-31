# Call Me Maybe - constrained decoding
#
# The environment may define UV_CACHE_DIR on a read-only filesystem; keep the
# uv cache inside the project. Override it on the command line if needed:
#   make UV_CACHE_DIR=/path/to/cache install
UV ?= uv
PYTHON ?= python3
UV_CACHE_DIR := $(CURDIR)/.cache/uv
export UV_CACHE_DIR

SRC := src
TESTS := tests
FUNCTIONS ?= data/input/functions_definition.json
INPUT ?= data/input/function_calling_tests.json
OUTPUT ?= data/output/function_calling_results.json
ARGS ?=

RUN = $(UV) run python -m src \
	--functions_definition "$(FUNCTIONS)" \
	--input "$(INPUT)" \
	--output "$(OUTPUT)"

.DEFAULT_GOAL := all
.PHONY: all install compile run debug test lint typecheck check \
	clean fclean re help check-uv check-sdk

all: install

check-uv:
	@command -v $(UV) >/dev/null 2>&1 || { \
		echo "error: uv is required (https://docs.astral.sh/uv/)." >&2; \
		exit 1; \
	}

install: check-uv check-sdk
	@mkdir -p "$(UV_CACHE_DIR)"
	$(UV) sync

# Byte-compile the sources: this is the fastest way to catch syntax errors
# without importing the model SDK.
compile:
	$(PYTHON) -m compileall -q $(SRC)

check-sdk:
	@if [ ! -d llm_sdk ] && [ ! -f llm_sdk.py ]; then \
		echo "error: llm_sdk/ is missing." >&2; \
		echo "Copy the llm_sdk package provided with the subject to $(CURDIR)/llm_sdk." >&2; \
		exit 1; \
	fi

run: check-uv check-sdk
	$(RUN) $(ARGS)

debug: check-uv check-sdk
	$(RUN) --debug $(ARGS)

test: check-uv
	$(UV) run pytest

lint: check-uv
	$(UV) run flake8 $(SRC) $(TESTS)

typecheck: check-uv
	$(UV) run mypy $(SRC)

check: compile lint typecheck test

clean:
	find . \( -path ./.venv -o -path ./.cache -o -path ./llm_sdk \) -prune \
		-o -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info

fclean: clean
	rm -rf .venv .cache/uv

re: fclean all

help:
	@printf '%s\n' \
		'make install     Install dependencies with uv (creates .venv)' \
		'make compile     Byte-compile src/ to check syntax' \
		'make run         Run the pipeline' \
		'make debug       Run the pipeline with --debug' \
		'make test        Run the pytest suite' \
		'make lint        Run flake8' \
		'make typecheck   Run mypy --strict on src/' \
		'make check       compile + lint + typecheck + test' \
		'make clean       Remove caches and build artifacts' \
		'make fclean      clean + remove .venv and the uv cache' \
		'make re          fclean then install' \
		'' \
		'Overridable variables:' \
		'  FUNCTIONS, INPUT, OUTPUT, ARGS, UV, PYTHON, UV_CACHE_DIR'
