# Error Translator

[![PyPI Version](https://img.shields.io/pypi/v/error-translator-cli-v2.svg)](https://pypi.org/project/error-translator-cli-v2/)
[![Python Version](https://img.shields.io/pypi/pyversions/error-translator-cli-v2.svg)](https://pypi.org/project/error-translator-cli-v2/)
[![License](https://img.shields.io/github/license/gourabanandad/error-translator)](https://github.com/gourabanandad/error-translator)
[![Build Status](https://img.shields.io/github/actions/workflow/status/gourabanandad/error-translator/ci.yml?branch=master&label=build)](https://github.com/gourabanandad/error-translator/actions/workflows/ci.yml)

Translate raw Python tracebacks into developer-ready fixes in milliseconds with one offline engine powering CLI, APIs, and editor hovers.

## Show, Don’t Tell

### Raw traceback

~~~text
Traceback (most recent call last):
  File "app.py", line 14, in <module>
    total = "Users: " + 42
TypeError: can only concatenate str (not "int") to str
~~~

### Translated output

~~~markdown
### Error Detected
TypeError: can only concatenate str (not "int") to str

### Location
app.py (line 14)

### Explanation
You are trying to add a string to an int, which Python cannot do.

### Suggested Fix
Convert the int to a string first using str() before concatenating.
~~~

### Colorized terminal view

*When run in a terminal, the output appears as:*

~~~
🔴 Error Detected:
TypeError: can only concatenate str (not "int") to str

🟡 Location: app.py (Line 14)

🔵 Explanation:
You are trying to add a string to an int, which Python cannot do.

🟢 Suggested Fix:
Convert the int to a string first using str() before concatenating.
~~~

(Red, yellow, blue, and green text for visual hierarchy in terminal)

##  Quickstart

Install first:

~~~bash
pip install error-translator-cli-v2
~~~

### 1. CLI mode (run scripts, strings, or pipes)

~~~bash
explain-error run script.py
explain-error "NameError: name 'usr_count' is not defined"
cat error.log | explain-error
~~~

### 2. Magic Import (auto-hook)

~~~python
import error_translator.auto

# Unhandled exceptions are auto-translated through sys.excepthook.
~~~

### 3. VS Code Extension

Install the Error Translator extension and hover on traceback output.

The extension invokes a PyInstaller-frozen executable of the same core engine for offline, near-zero-latency UI help.

## Why Error Translator?

- Offline and private: your stack traces never leave your machine.
- Blazing fast: regex-first matching with targeted AST inspection for typo hints.
- Editor native: VS Code extension uses a PyInstaller-frozen executable for near-instant hover help.

## Five Core Features

1. Magic Import (Auto-Hook)
2. CLI execution, raw-string translation, and log piping
3. VS Code extension with frozen offline engine
4. Python native API via error_translator.core.translate_error
5. FastAPI server via error_translator.server

## Documentation Map

- Architecture: ARCHITECTURE.md
- Contributing: CONTRIBUTING.md

## Recommended Demo Recording

Record a 20-30 second GIF that shows this exact flow:

1. Run a script that throws a NameError caused by a typo.
2. Show the raw traceback in terminal for one second.
3. Immediately run explain-error on the same error and show the translated explanation and fix.
4. Fix the typo and rerun to show success.

This gives new users proof of speed, clarity, and practical value in one clip.
