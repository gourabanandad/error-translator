# Error Translator

<div align="left">
  <a href="https://pypi.org/project/error-translator-cli-v2/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/error-translator-cli-v2.svg"></a>
  <img alt="Python 3.9+" src="https://img.shields.io/badge/python-3.9%2B-blue.svg">
  <a href="https://github.com/gourabanandad/error-translator-cli-v2/stargazers"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/gourabanandad/error-translator-cli-v2?style=social"></a>
  <a href="https://pypi.org/project/error-translator-cli-v2/"><img alt="PyPI Downloads" src="https://img.shields.io/pypi/dm/error-translator-cli-v2"></a>
  <a href="https://github.com/gourabanandad/error-translator-cli-v2"><img alt="License" src="https://img.shields.io/github/license/gourabanandad/error-translator-cli-v2.svg"></a>
  <a href="https://github.com/gourabanandad/error-translator-cli-v2/actions/workflows/ci.yml"><img alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/gourabanandad/error-translator-cli-v2/ci.yml?branch=master&label=build"></a>
</div>

<br>

**Error Translator** is a powerful offline engine designed to parse raw Python tracebacks and translate them into crystal-clear explanations with immediately actionable fixes. Built with local-first development workflows in mind, it supports direct CLI usage, an automatic import hook, a programmatic Python API, and a FastAPI integration.

If this project saves you debugging time, please consider starring it on GitHub: https://github.com/gourabanandad/error-translator-cli-v2

## Why Developers Like It

* **Fast Feedback Loop**: Turn stack traces into direct next actions in seconds.
* **Works Offline**: No telemetry dependency for core translation behavior.
* **Beginner-Friendly Output**: Explanations are clear enough for learners, practical enough for teams.
* **Multiple Entry Points**: CLI, import hook, Python API, and FastAPI all share one deterministic engine.

## Key Features

* **CLI-First Architecture**: Seamlessly process scripts, direct error strings, or piped logs via the `explain-error` command.
* **Automatic Integration Mode**: Inject the module via `import error_translator.auto` to automatically override `sys.excepthook` for graceful, translated crash reporting.
* **Extensible API Surfaces**: Integrate natively within Python or expose the core engine over HTTP via the included FastAPI server.
* **Deterministic Rules Engine**: High-performance, regex-based matching powered by `rules.json` guarantees offline and privacy-first translations.
* **Optional AST Insight Hooks**: Registered handlers can append targeted hints (`ast_insight`) for selected error types.

## Installation

Python requirement: **3.9 or newer**.

Install the latest stable release directly from PyPI:

```bash
pip install error-translator-cli-v2
```

Verify the installation:

```bash
explain-error --version
```

## Usage Guide

### 1. Command-Line Interface (CLI)

Run a Python script and catch any unhandled exceptions:
```bash
explain-error run script.py
```

Provide an error string directly:
```bash
explain-error "NameError: name 'usr_count' is not defined"
```

Pipe system or Docker logs into the engine:
```bash
cat error.log | explain-error
```

### 2. Automatic Import Hook

Catch and translate unhandled exceptions globally by importing the module:

```python
import error_translator.auto

def main():
    # This TypeError will automatically trigger the error translator
    total = "Users: " + 42

if __name__ == "__main__":
    main()
```

### 3. FastAPI Service

Start the built-in HTTP server for remote translation services:

```bash
uvicorn error_translator.server:app --host 127.0.0.1 --port 8000 --reload
```

Submit a traceback payload via the exposed REST API:

```bash
curl -X POST http://127.0.0.1:8000/translate \
  -H "Content-Type: application/json" \
  -d "{\"traceback_setting\":\"Traceback (most recent call last):\\n  File 'app.py', line 14, in <module>\\n    total = 'Users: ' + 42\\nTypeError: can only concatenate str (not 'int') to str\"}"
```

Additional endpoints:

- `GET /health` returns service status.
- `GET /` serves the bundled web UI from `error_translator/static/index.html`.

## Documentation

Detailed documentation is located in the [`docs/`](docs/) directory:

- [**Real-World Examples**](docs/examples.md): Practical demonstrations comparing raw tracebacks with their translated counterparts.
- [**Architecture & Internals**](docs/ARCHITECTURE.md): Comprehensive teardown of the regex engine, AST integration, and internal design philosophy.
- [**Contributing Guidelines**](docs/CONTRIBUTING.md): Standards, PR checklists, and instructions for utilizing our AI-Powered Rule Builder.

## Maintainers

This project is actively developed and maintained by **Gourabananda Datta** alongside our open-source contributors.
