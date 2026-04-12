# Error Translator Documentation

Welcome to the project documentation for **Error Translator**, a local Python toolkit that transforms traceback output into concise, actionable explanations.

This documentation is written for three audiences:

- **Users** who want fast error explanations from the CLI.
- **Integrators** who want to consume translation results from code or HTTP.
- **Contributors** who want to improve rules, architecture, and documentation over time.

## Project overview

Error Translator reads traceback text, extracts the final error line, and matches it against curated regex rules. It then enriches the response with available traceback metadata (file, line, code) and optional AST-based insights.

The result is a consistent structure that can be rendered in terminals, returned by API endpoints, or consumed by custom tooling.

!!! tip "Design principle"
    Keep the runtime simple and deterministic. Most enhancements should be expressed as rule and test changes rather than broad engine rewrites.

## Core outcomes

- Clear explanations designed for humans.
- Suggested fixes oriented toward immediate action.
- Stable output fields for downstream integration.
- Local-first behavior with no required external service.

## Installation

```bash
pip install error-translator-cli-v2
```

For local development:

```bash
pip install -r requirements.txt
```

## Quick start

### Automatic translation via import hook

```python title="script.py"
import error_translator.auto

maximum_user_connections = 100
print(maximum_user_connectons)
```

`error_translator.auto` replaces `sys.excepthook` for that process, translating unhandled exceptions automatically.

### CLI translation

```bash
explain-error run script.py
```

```bash
explain-error "NameError: name 'x' is not defined"
```

```bash
cat error.log | explain-error
```

### API translation

```bash
uvicorn error_translator.server:app --reload
```

`POST /translate` request body:

```json
{
  "traceback_setting": "Traceback (most recent call last): ..."
}
```

## Documentation map

- **Architecture**: `ARCHITECTURE.md`
- **Contributor workflow**: `CONTRIBUTING.md`

## Contributor first steps

If you are new to the repository, start with a small, reviewable improvement:

1. Fix one doc gap, one rule, or one missing test.
2. Validate with `pytest`.
3. Keep language user-centric and technically precise.

Professional documentation is a shared responsibility; every merged change should make the next contributor faster.
