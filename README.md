# Error Translator

Error Translator is a Python toolkit that converts raw tracebacks into clear, actionable guidance. The project is designed for local use, deterministic output, and easy extension by contributors.

It can be used as:

- A CLI (`explain-error`) for direct translation and script execution.
- An import hook (`error_translator.auto`) for automatic translation of unhandled exceptions.
- A small FastAPI service (`error_translator.server`) for integrations.

## Why this project exists

Python's default tracebacks are precise but can be difficult for beginners and occasional Python users to act on quickly. Error Translator narrows that gap by matching final traceback lines against a curated set of regex rules and returning:

- A plain-language explanation.
- A concrete suggested fix.
- Location/context metadata when available (`file`, `line`, `code`).
- Optional AST-based hints for selected error families.

## Key capabilities

- **Local and deterministic**: no external API is required for normal translation.
- **Structured output**: returns a predictable dictionary for CLI, library, and API consumers.
- **Multiple entry points**: CLI, import hook, and HTTP API share the same core engine.
- **Contributor-friendly rule model**: behavior is primarily driven by `error_translator/rules.json`.

## Installation

### Install from package

```bash
pip install error-translator-cli-v2
```

### Install for local development

```bash
pip install -r requirements.txt
```

## Usage

### 1) Automatic crash interception

```python
import error_translator.auto

maximum_user_connections = 100
print(maximum_user_connectons)
```

Importing `error_translator.auto` installs a custom `sys.excepthook`, so unhandled exceptions are translated automatically in that process.

### 2) CLI mode

Run a script and translate any failure from `stderr`:

```bash
explain-error run script.py
```

Translate a single raw error string:

```bash
explain-error "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
```

Pipe traceback text from a file:

```bash
cat error.log | explain-error
```

PowerShell:

```bash
Get-Content error.log | explain-error
```

### 3) Programmatic usage

```python
from error_translator.core import translate_error

result = translate_error(traceback_text)
print(result["explanation"])
```

### 4) HTTP API

Start the API:

```bash
uvicorn error_translator.server:app --reload
```

`POST /translate` expects:

```json
{
  "traceback_setting": "Traceback (most recent call last): ..."
}
```

## Response contract

`translate_error()` returns a dictionary with these fields when available:

- `explanation`
- `fix`
- `matched_error`
- `file`
- `line`
- `code`
- `ast_insight`

## Repository structure

- `error_translator/core.py`: translation pipeline and rule matching.
- `error_translator/cli.py`: terminal interface (`explain-error`).
- `error_translator/auto.py`: automatic exception-hook integration.
- `error_translator/server.py`: FastAPI surface.
- `error_translator/ast_handlers.py`: optional contextual heuristics.
- `error_translator/rules.json`: primary rule database.
- `tests/test_core.py`: regression tests for translation behavior.

## Contributing

We welcome contributions of all sizes. If you are new to the project:

1. Start with one narrowly scoped improvement.
2. Add or update tests for behavior changes.
3. Run `pytest` before submitting.
4. Keep user-facing docs aligned with implementation.

See `docs/CONTRIBUTING.md` for full contributor workflow and review standards.

---

Maintained by Gourabananda Datta and contributors.
