# Error Translator

[![PyPI Version](https://img.shields.io/pypi/v/error-translator-cli-v2.svg)](https://pypi.org/project/error-translator-cli-v2/)
[![Python Version](https://img.shields.io/pypi/pyversions/error-translator-cli-v2.svg)](https://pypi.org/project/error-translator-cli-v2/)
[![License](https://img.shields.io/github/license/gourabanandad/error-translator)](https://github.com/gourabanandad/error-translator)
[![Build Status](https://img.shields.io/github/actions/workflow/status/gourabanandad/error-translator/ci.yml?branch=master&label=build)](https://github.com/gourabanandad/error-translator/actions/workflows/ci.yml)

Translate raw Python tracebacks into clear explanations and actionable fixes.
Built for local-first developer workflows: CLI, import-hook auto mode, Python API, and FastAPI.

## ✨ Key Features

-  **CLI-first workflow**: run a script, paste an error, or pipe logs directly into `explain-error`.
-  **Auto mode**: `import error_translator.auto` installs a custom `sys.excepthook` for unhandled crashes.
-  **HTTP API**: expose the same engine through FastAPI for service integrations.
-  **Rules engine**: regex-based matching from `rules.json` for deterministic, offline translations.
-  **AST analysis hooks**: error-type-specific handlers (via registry) can add deeper typo/context insight.

##  Installation

### Install from PyPI

```bash
pip install error-translator-cli-v2
```
### Check if the CLI is working:

```bash
explain-error --version
```


### Local development setup

```bash
git clone https://github.com/gourabanandad/error-translator.git
cd error-translator
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
pytest
```

##  Usage

### 1) CLI usage

Run a Python script and translate unhandled errors:

```bash
explain-error run script.py
```

Translate a raw error string directly:

```bash
explain-error "NameError: name 'usr_count' is not defined"
```

Translate piped traceback logs:

```bash
cat error.log | explain-error
```

### 2) Python auto-import mode

```python
import error_translator.auto

# Any unhandled exception in this process is intercepted
# and rendered as a translated, colorized explanation.

def main():
    total = "Users: " + 42

main()
```

### 3) FastAPI server usage

Start server:

```bash
uvicorn error_translator.server:app --host 127.0.0.1 --port 8000 --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/
```

Translate via API:

```bash
curl -X POST http://127.0.0.1:8000/translate \
  -H "Content-Type: application/json" \
  -d "{\"traceback_setting\":\"Traceback (most recent call last):\\n  File 'app.py', line 14, in <module>\\n    total = 'Users: ' + 42\\nTypeError: can only concatenate str (not 'int') to str\"}"
```

##  Real-World Input → Output Examples

### Example A: Type mismatch

Input traceback:

```text
Traceback (most recent call last):
  File "app.py", line 14, in <module>
    total = "Users: " + 42
TypeError: can only concatenate str (not "int") to str
```

Translated output (CLI render):

```text
Error Detected:
TypeError: can only concatenate str (not "int") to str

Location: app.py (Line 14)

Explanation:
You are trying to add a string to an int, which Python cannot do.

Suggested Fix:
Convert the int to a string first using str() before concatenating.
```

### Example B: Missing variable typo

Input error line:

```text
NameError: name 'usr_count' is not defined
```

Translated output:

```text
Explanation:
You tried to use a variable or function named 'usr_count', but Python doesn't recognize it.

Suggested Fix:
Check if 'usr_count' is spelled correctly, or ensure you defined/imported it before using it.
```

##  Architecture

Error Translator uses one core engine with multiple entry points.

1. **Input ingestion**: traceback text from CLI, API, or auto-hook.
2. **Rule matching**: `core.py` checks the last error line against compiled regex rules from `rules.json`.
3. **Context extraction**: file path, line number, and source line are extracted when available.
4. **Optional AST insight**: for selected error types, handlers from `ast_handlers.py` can add extra hints.
5. **Structured output**: returns a stable dictionary (`explanation`, `fix`, `file`, `line`, `code`, `matched_error`, optional `ast_insight`).

##  How It Works Internally

- `load_rules()` reads `rules.json` once and caches it.
- `compiled_rules()` compiles regex patterns once for fast repeated matching.
- `translate_error()`:
  - normalizes traceback input,
  - finds the terminal error line,
  - applies first matching rule,
  - formats placeholders (`{0}`, `{1}`, ...),
  - enriches with file/line/code context,
  - dispatches to `AST_REGISTRY` by error type when applicable.
- If no rule matches, a safe fallback explanation/fix from `default` is returned.

##  Project Structure

```text
error-translator/
├─ error_translator/
│  ├─ core.py           # Translation pipeline, rule loading, context extraction
│  ├─ rules.json        # Regex patterns + explanations + fixes
│  ├─ ast_handlers.py   # AST handler registry and insight plugins
│  ├─ cli.py            # `explain-error` command and colorized terminal renderer
│  ├─ auto.py           # Auto mode via sys.excepthook override
│  └─ server.py         # FastAPI app and /translate endpoint
├─ tests/
│  └─ test_core.py      # Core translation and regex extraction tests
└─ docs/
   ├─ ARCHITECTURE.md
   └─ CONTRIBUTING.md
```

##  How To Add New Rules

Add a new object to `error_translator/rules.json` under `rules`:

```json
{
  "pattern": "ValueError: invalid literal for int\\(\\) with base 10: '(.*)'",
  "explanation": "You tried to convert '{0}' to an integer, but it is not a valid whole number.",
  "fix": "Ensure '{0}' contains only digits, or parse it as float if decimals are expected."
}
```

Guidelines:

- Keep regex patterns specific to avoid false positives.
- Use capture groups for dynamic values and reference them with `{0}`, `{1}`, etc.
- Keep explanations beginner-friendly and fixes immediately actionable.
- Add/extend tests in `tests/test_core.py` for each new rule.

##  Contributing

Contributions are welcome, from first-time contributors to maintainers.

Typical workflow:

1. Fork and clone the repository.
2. Create a feature branch.
3. Add or improve rules/tests/docs.
4. Run `pytest`.
5. Open a PR with a sample traceback and expected translation.

Please see:

- `docs/CONTRIBUTING.md`
- `docs/ARCHITECTURE.md`

##  Maintainer

Built and maintained by Gourabananda Datta and contributors.
