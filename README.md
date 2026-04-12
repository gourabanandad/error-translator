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

### Example C: Index out of range

Input traceback:

```text
Traceback (most recent call last):
  File "script.py", line 3, in <module>
    print(items[5])
IndexError: list index out of range
```

Translated output:

```text
Error Detected:
IndexError: list index out of range

Location: script.py (Line 3)

Explanation:
You tried to access an index (position 5) that doesn't exist in the list.

Suggested Fix:
Check the length of the list using len(items) - 1 to find the last valid index.
```

### Example D: Key not found in dictionary

Input error line:

```text
KeyError: 'age'
```

Translated output:

```text
Explanation:
You tried to access a dictionary key ('age') that doesn't exist.

Suggested Fix:
Use dict.get('age', default_value) to safely retrieve the key with a fallback,
or ensure the key is set before accessing it.
```

### Example E: Division by zero

Input error line:

```text
ZeroDivisionError: division by zero
```

Translated output:

```text
Explanation:
You attempted to divide a number by zero, which is mathematically undefined.

Suggested Fix:
Add a condition to check if the denominator is zero before performing division.
```

### Example F: File not found

Input traceback:

```text
Traceback (most recent call last):
  File "reader.py", line 2, in <module>
    with open('data.csv', 'r') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```

Translated output:

```text
Error Detected:
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'

Location: reader.py (Line 2)

Explanation:
Python cannot find the file 'data.csv' in the current working directory.

Suggested Fix:
Verify the file path and name. Use os.path.exists() to check before opening,
or provide an absolute path.
```

### Example G: Attribute error on wrong type

Input error line:

```text
AttributeError: 'int' object has no attribute 'append'
```

Translated output:

```text
Explanation:
You are trying to call .append() on an integer. .append() is a method for lists.

Suggested Fix:
If you meant to collect multiple values, initialize a list instead (my_list = []).
If you're working with a single integer, review what operation you intended.
```

### Example H: Import module not found

Input error line:

```text
ModuleNotFoundError: No module named 'requests'
```

Translated output:

```text
Explanation:
Python cannot find the 'requests' module. It is not part of the standard library
and needs to be installed separately or you have a typo in the module name.

Suggested Fix:
Install the missing package using pip: pip install requests.
If the module is your own file, check the import path and file location.
```

### Example I: Indentation mismatch

Input traceback:

```text
Traceback (most recent call last):
  File "script.py", line 5
    print("Hello")
        ^
IndentationError: expected an indented block
```

Translated output:

```text
Error Detected:
IndentationError: expected an indented block

Location: script.py (Line 5)

Explanation:
Python uses indentation to define blocks of code. You likely forgot to indent
after a statement that expects a nested block (e.g., after if, for, def).

Suggested Fix:
Add consistent spaces or tabs to the line after the colon. Use 4 spaces per level.
```

### Example J: Value conversion error

Input error line:

```text
ValueError: invalid literal for int() with base 10: '42.5'
```

Translated output:

```text
Explanation:
You are trying to convert the string '42.5' to an integer, but it contains a
decimal point, so it's not a valid whole number.

Suggested Fix:
If you need to keep the fractional part, use float() instead of int().
If you want to truncate, convert to float first then to int: int(float('42.5')).
```

### Example K: Recursion limit exceeded

Input traceback:

```text
Traceback (most recent call last):
  File "recursive.py", line 4, in <module>
    infinite()
  File "recursive.py", line 2, in infinite
    return infinite()
  File "recursive.py", line 2, in infinite
    return infinite()
  ...
RecursionError: maximum recursion depth exceeded
```

Translated output:

```text
Error Detected:
RecursionError: maximum recursion depth exceeded

Location: recursive.py (Line 2)

Explanation:
A function is calling itself so many times that Python's recursion limit has been reached. This usually happens when a recursive function lacks a proper base case or stop condition.

Suggested Fix:
Add a base case to stop the recursion. Check that the function arguments change in each call to eventually reach the base case. If deep recursion is intentional, you can increase the limit with sys.setrecursionlimit(), but restructuring the code to use iteration is often safer.
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
