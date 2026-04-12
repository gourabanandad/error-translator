# Architecture: One Core Engine, Multiple Tools

Error Translator is built on a single translation engine that powers multiple delivery surfaces.

- One core engine: error parsing, regex matching, AST inspection, and JSON output.
- Multiple tools: CLI, Magic Import auto-hook, Python native API, FastAPI server, and VS Code extension.

This keeps behavior consistent across terminal workflows, editor UX, and backend integrations.

## The Core Engine

The core engine lives in error_translator/core.py and owns all translation logic.

It does four things fast:

1. Extracts the final error line from traceback input.
2. Matches against the local regex rule database.
3. Runs AST inspection only when an error type benefits from deeper context.
4. Returns structured JSON-style output for any renderer.

## Tool Surfaces

### 1. CLI

explain-error can run scripts, translate raw error strings, or process piped logs.

### 2. Magic Import Auto-Hook

import error_translator.auto overrides sys.excepthook and auto-translates unhandled crashes.

### 3. Python Native API

from error_translator.core import translate_error gives backend code direct access to JSON output.

### 4. FastAPI Server

error_translator.server exposes the same engine over HTTP for service environments.

### 5. VS Code Extension

The extension calls a PyInstaller-frozen executable of the same engine.

Why this matters:

- No Python environment setup required in the extension runtime path.
- Very low startup overhead for hover interactions.
- Consistent translation behavior with the CLI path.

## Data Flow

~~~mermaid
flowchart LR
    A[User Input: CLI / VS Code / Auto-Hook / API] --> B[Regex DB Matcher]
    B --> C{Needs deeper context?}
    C -- No --> D[JSON Output]
    C -- Yes --> E[AST Inspection]
    E --> D
    D --> F[Rendered UI: Terminal / Hover / API Response]
~~~

## Runtime Contract

Every entry point gets a predictable translation object with fields like:

- explanation
- fix
- matched_error
- file
- line
- code
- ast_insight

Stable output shape is intentional. It keeps integrations simple and lowers maintenance cost.

## Extension Strategy

When improving behavior, use this order:

1. Update rules first in error_translator/rules.json.
2. Add AST handlers only for cases where rules alone are insufficient.
3. Touch core pipeline last, and only for cross-cutting improvements.
4. Lock behavior with tests in tests/test_core.py.
