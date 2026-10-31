*This project has been created as part of the 42 curriculum by rarabeto.*

# Call Me Maybe

Function calling with a small language model (Qwen3-0.6B), made reliable by
**constrained decoding**: a finite state machine (FSM) forbids, at every step,
any token that would break the expected JSON structure.

## Description

Given a natural-language request such as *"What is the sum of 2 and 3?"* and a
list of available functions, the program outputs the call to make:

```json
{
  "prompt": "What is the sum of 2 and 3?",
  "name": "fn_add_numbers",
  "parameters": { "a": 2.0, "b": 3.0 }
}
```

A small model asked to "answer in JSON" regularly produces invalid or
off-schema output. Instead of hoping for the best (or retrying), this project
intervenes **during generation**: the model still chooses *what* to say (which
function, which values), but the FSM decides *what it is allowed to write*.
The result is a valid JSON object that matches the function schemas, by
construction.

## Instructions

### Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (dependency management)
- the provided `llm_sdk/` directory at the project root

`pyproject.toml` declares `numpy`, `pydantic`, `torch`, `transformers` and the
local `llm-sdk` project. `uv sync` builds and installs `llm_sdk/` in editable
mode, which is what makes `from llm_sdk import Small_LLM_Model` work inside
`uv run`. The SDK is shipped with its own `pyproject.toml`/`uv.lock`; it is not
published on PyPI.

### Installation

```bash
make install        # uv sync: installs dependencies and the local llm-sdk
make compile        # byte-compile src/ to catch syntax errors
```

The Makefile keeps the uv cache inside the project (`.cache/uv`), because some
environments export a read-only `UV_CACHE_DIR`. Override it when needed:

```bash
make UV_CACHE_DIR=/tmp/uv-cache install
```

### Run

```bash
make run            # same as: uv run python -m src
make debug          # same, with --debug

# explicit paths:
make run FUNCTIONS=data/input/functions_definition.json \
         INPUT=data/input/function_calling_tests.json \
         OUTPUT=data/output/function_calling_results.json

# or invoke the module directly:
uv run python -m src
```

`make run` checks that `llm_sdk/` exists and prints a clear error otherwise.
The first run downloads `Qwen/Qwen3-0.6B` (about 1.2 GB) into
`.cache/huggingface` (the program sets `HF_HOME`); later runs reuse the cache.
On CPU, expect the first call to be noticeably slower than the following ones.

### Troubleshooting

- `ImportError: cannot import name 'Small_LLM_Model' from 'llm_sdk'`:
  `llm_sdk/` is not a package at the project root, it is a separate uv project.
  Run `uv sync` (or `make install`) so that the editable local dependency is
  installed; a plain `python -m src` outside `uv` cannot see it.
- `Could not acquire lock ... Read-only file system ... UV_CACHE_DIR`: use
  `make run` (the Makefile points the uv cache to `./.cache/uv`) or export a
  writable `UV_CACHE_DIR`.

### Make targets

| Target | Action |
|---|---|
| `make install` | Install dependencies and the local `llm-sdk` with `uv sync` |
| `make compile` | Byte-compile `src/` (syntax check) |
| `make run` | Run the pipeline on the default data files |
| `make debug` | Run the pipeline with `--debug` |
| `make test` | Run the pytest suite (no `llm_sdk` needed) |
| `make lint` | Run `flake8` on `src/` and `tests/` |
| `make typecheck` | Run `mypy --strict` on `src/` |
| `make check` | `compile` + `lint` + `typecheck` + `test` |
| `make clean` | Remove caches and build artifacts |
| `make fclean` | `clean` + remove `.venv` and the uv cache |
| `make re` | `fclean` then `install` |
| `make help` | List the targets |

If the default files are not found, the program also looks for
`data/functions_definition.json` / `data/function_calling_tests.json` and for
the same names in the current directory.

### Project layout

```
call_me_maybe/
├── data/
│   ├── input/                       # functions_definition.json, function_calling_tests.json
│   ├── output/                      # function_calling_results.json (generated)
│   └── tests/
├── llm_sdk/                         # provided SDK (own uv project, Small_LLM_Model)
├── src/
│   ├── __main__.py                  # CLI entry point and generation loop
│   ├── fsm.py                       # JSON state machine (constrained decoding)
│   ├── incremental.py               # optional KV-cache incremental decoding
│   ├── logit_masker.py              # cached logit masks, argmax selection
│   ├── vocabulary.py                # vocab.json loading and byte-level decoding
│   ├── prompts.py                   # ChatML prompt (Qwen3) with the tool list
│   ├── models.py                    # Pydantic models
│   └── loaders.py                   # JSON reading / writing + validation
├── tests/                           # pytest suite (synthetic vocab, no SDK)
├── .flake8
├── .gitignore
├── Makefile
├── pyproject.toml
├── uv.lock                          # generated/updated by uv sync
└── README.md
```

### Input / output format

`functions_definition.json` is a list of functions. Both parameter notations
are accepted:

```json
{ "name": "fn_add_numbers", "description": "...",
  "parameters": { "a": {"type": "number"}, "b": {"type": "number"} },
  "returns": {"type": "number"} }
```

```json
{ "name": "fn_add_numbers", "description": "...",
  "parameters": { "type": "object",
                  "properties": { "a": {"type": "number"}, "b": {"type": "number"} },
                  "required": ["a", "b"] },
  "returns": {"type": "number"} }
```

Supported value types: `number`, `integer`, `string`, `boolean`. When no
`required` list is given, every declared parameter is required. An explicit
`"required": []` means that every parameter is optional, so the function may be
called with `{}`. `returns` is optional.
`function_calling_tests.json` is a list of `{"prompt": "..."}` objects.
The output is a list of `{"prompt", "name", "parameters"}` objects.

## Algorithm: constrained decoding

At each step the model produces one logit per vocabulary token. The program:

1. asks the FSM which tokens are **allowed** in the current state;
2. adds a mask (`0` for allowed tokens, `-inf` for the others) to the logits;
3. picks the best remaining token with `argmax`;
4. feeds it back to the model and to the FSM (`advance`).

The generated text always has the shape
`{"name": "<function>", "parameters": {"<param>": <value>, ...}}`.

| State | What is written | Constraint |
|---|---|---|
| `START` | `{"name": "` | fixed text |
| `FUNCTION_NAME` | function name + `"` | only the names of the known functions |
| `PARAMS_KEY` / `PARAMS_OPEN` | `, "parameters": {` | fixed text |
| `PARAM_NAME` | `"<param>": ` (+ the opening quote for strings) | the next required parameter, in schema order, written without a model call; optional parameters are chosen by the model; `}}` is allowed when no parameter is required |
| `PARAM_VALUE` | the value | number/integer: valid JSON number; boolean: `true`/`false`; string: no raw `"`, `\`, control character |
| `PARAM_COMMA` | `,` or `}}` | `}}` only once all required parameters are present; `,` only if parameters remain |
| `END` | — | generation stops |

The prompt itself is not generated by the model: it is copied into the result
by the program, which avoids any mismatch with the input.

## Design decisions

- **Multi-token literals.** A BPE token can span several characters (`":`,
  ` "`, `}}`...). A token is allowed if its text is a *prefix of what is still
  expected* in the current state, so every valid tokenisation is accepted.
- **Combined closing tokens.** Qwen has tokens such as `",`, `"}` and `"}}` that
  close a string *and* start the following JSON syntax. The FSM allows them and
  consumes the remainder after the quote; without this, the model kept writing
  text inside the value until the 100-token cap.
- **Cached masks.** Each distinct situation (state + remaining text) gets one
  NumPy mask, built once and reused (`LogitMasker`). Tokens are indexed by their
  first character at start-up, so building a literal mask never scans the whole
  vocabulary; string masks scan it once and are cached too.
- **Forced tokens.** When only one text is possible (fixed JSON syntax, a single
  function, the rest of a chosen name), the FSM returns the token directly
  (`forced_token`) and the model is **not called**. The skipped tokens are
  accumulated and injected into the KV cache as one batch, so they cost no
  separate forward pass.
- **Incremental KV cache.** The public SDK method recomputes logits for the whole
  sequence on every call. When the SDK object exposes its underlying model
  (`_model`/`_device`), `IncrementalLogits` keeps the KV cache and forwards only
  the new tokens; on any incompatibility it falls back to
  `get_logits_from_input_ids`. This is transparent for the FSM.
- **Forced required parameters.** Required parameter names are written by the FSM
  in schema order: their order has no meaning in JSON and only their values are a
  real model decision. This removes one forward pass per required parameter and
  prevents the model from picking a different (but equivalent) argument order.
  When every parameter is optional, `}}` is offered at the first parameter so a
  no-argument call is possible.
- **Escaped names.** Function and parameter names are inserted into the generated
  JSON with `json.dumps` (`ensure_ascii=True`), so a schema name containing a
  quote, a backslash or a non-ASCII character still produces valid JSON.
- **One FSM for all prompts.** The tables are built once; `reset()` is called
  between prompts. The tool list of the system prompt is serialized once per run.
- **Byte-level vocabulary.** `vocab.json` stores bytes as unicode characters
  (`Ġ` = space, `Ã©` = `é`). `Vocabulary` decodes them properly so accented
  characters in string values are written correctly.
- **Logits longer than the vocabulary.** The model outputs a few more logits than
  `vocab.json` has entries (padding); the extra ones are ignored.
- **Length caps.** A string value is forced to close after 100 tokens and a number
  after 20 characters. The per-prompt token budget is derived from the schema
  (`max_generation_steps`), so a function with several long strings can still
  finish instead of hitting a fixed 200-token ceiling.
- **Debug mode.** `uv run python -m src --debug` prints timings, every generated
  token (forced or chosen by the model) and the FSM transitions on stderr.
- **Types.** Numbers are cast to the declared type after parsing
  (`2` → `2.0` for a `number`).
- **Value normalization.** After parsing, `regex`/`replacement` values are
  lightly normalized: a redundant outer capturing group around a simple
  class/escape atom, a trailing `\s`, and surrounding whitespace are removed
  (`([0-9]+)\s` → `[0-9]+`, ` *` → `*`). This repairs common small-model
  artifacts and leaves structured regexes/source strings untouched.

## Performance

- The FSM is built once (about a quarter of a second for a 151k-token
  vocabulary in my tests).
- Mask selection costs well under a millisecond per step in practice; the model
  forward pass dominates.
- Fixed JSON syntax and required parameter names cost zero model calls: only the
  function choice, each value and the decision to add optional parameters reach
  the model. This removes one avoidable forward pass per required parameter (the
  last one was already forced).
- Forced tokens are accumulated and injected into the KV cache in one batch.
- On CPU, a full forward pass costs 3.9–9.2 s, while a cached incremental step
  costs 0.3–1.4 s. With the combined closing tokens, the 11-prompt set now runs
  in about 33 s: the first eight prompts take 2.0–3.0 s each, and the three
  substitution prompts take 4.2–6.2 s (16–27 model calls). The same run took
  more than 15 minutes with full forwards.
- Prompt 9 (three string parameters) now takes 6.2 s and 27 model calls; before
  the closing-token fix it spent minutes repeating a regex until the cap.
- The tool list is serialized once per run instead of once per prompt.
- Forced tokens are resolved from the literal prefix cache before any token set
  is built, so the fixed JSON syntax does no vocabulary work at all.
- The 100-token string cap remains as a safety net; with the combined closing
  tokens the provided prompts close naturally well before it.

## Challenges

- The first approach allowed one token per JSON state, which cannot work with a
  BPE vocabulary where function names and values span several tokens. Switching
  to "text still expected" fixed this.
- Escaped characters (`\\d+` in a regex) were impossible to write until JSON escapes
  were allowed in strings.
- Generation was slow because the FSM tables were rebuilt for every prompt and
  the model was called even for fixed syntax. Both are now avoided.
- Required parameter names were chosen by the model even though their order is
  irrelevant, which cost a forward pass per parameter; the FSM now writes them.
- A fixed 200-token ceiling was smaller than `100 × number of string parameters`,
  so calls with several long strings aborted; the budget is now derived from the
  schema.
- An explicit `"required": []` was treated like an omitted list, so an
  all-optional function always received an argument. The two cases are now
  distinguished, and the empty object is reachable.
- The model tried to close strings with natural Qwen tokens like `",` and `"}`
  while the FSM only allowed the lone quote; it therefore wrote text inside the
  value until the 100-token cap. The FSM now consumes the remainder after the
  closing quote.
- Normalizing the regex/replacement artifacts (`([0-9]+)\s` → `[0-9]+`,
  ` *` → `*`) turns the model's still-imperfect values into usable calls.
- Schema names were interpolated into JSON without escaping, which could produce
  invalid JSON for a name containing a quote or a backslash; names are escaped now.
- Accented characters were corrupted until the byte-level decoding was added.

## Testing strategy

- `make test` runs the pytest suite (28 tests) with a synthetic byte-level
  vocabulary (no SDK needed): numbers, integers, strings with accents and JSON
  escapes, booleans, a function without parameters, an all-optional function
  (including the zero-argument call), required parameters that cannot be
  skipped, escaped function/parameter names, combined closing tokens (`",`,
  `"}}`), regex/replacement normalization, length caps, loader validation,
  logit masks and the incremental-provider fallback.
- During development the FSM was also fuzzed with hundreds of random-logit
  generations: every generation that finished was valid JSON, used a known
  function, contained all required parameters and respected each declared type.
- The real SDK was exercised on the 11 provided prompts; the KV-cache path was
  checked against the public full-forward logits (maximum difference ~3e-5).
  The final run produces `[0-9]+`/`NUMBERS`, `[aeiouAEIOU]`/`*` and
  `cat`/`dog` for the three substitution prompts.
- `make lint` runs `flake8` on `src/` and `tests/`; `make typecheck` runs
  `mypy --strict` on `src/`. `make check` runs all four checks.

Limitations: array and object parameters are not supported (treated as
strings). A string value can only use characters that exist in the vocabulary as
whole tokens, and `\uXXXX` escapes are not accepted inside values (function and
parameter names are escaped automatically). The KV-cache path relies on the
private `_model`/`_device` attributes of the provided SDK and falls back to the
public API if they are unavailable. Regex/replacement normalization is a
deliberate, documented heuristic for small-model artifacts; it does not try to
repair arbitrary regexes.

## Resources

- [Qwen3 model card](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Pydantic documentation](https://docs.pydantic.dev/)
- Willard & Louf, *Efficient Guided Generation for LLMs* (2023)

AI was used to review the code, fix inconsistencies and write this README.
All code was read and tested before being kept.
