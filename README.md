# Error Translator CLI

## Overview
A lightweight, rule-based command-line tool designed to translate confusing Python traceback errors into plain, human-readable English and suggest actionable fixes.

## Key Features
- **No AI or LLMs Required:** Runs entirely locally using fast, regex-based pattern matching.
- **Beginner Friendly:** Explains the root cause of errors in simple English terminology, making debugging more approachable.
- **Actionable Guidance:** Provides practical, suggested fixes tailored to your specific code context.
- **Pinpoint Accuracy:** Extracts and highlights the exact file name and line number where the code encountered an issue.
- **Improved Readability:** Utilizes well-formatted, color-coded terminal output to make reading errors easier.

## Installation
You can install this tool globally on your machine using pip:
```bash
pip install error-translator-cli-v2
```

## Quick Start Guide
You can use the Error Translator in three distinct ways, depending on your preferred workflow:

### 1. Magic Import (Recommended)
Simply add this single import statement at the top of your Python script. If your script crashes, the tool will automatically intercept and translate the error.

```python
import error_translator.auto

# Your normal code...
math_is_broken = 10 / 0  # This crash will be automatically intercepted and translated
```

### 2. Run Scripts via CLI
You can execute your Python files directly through the provided CLI tool. It will run your program normally and intercept any crashes if they occur.

```bash
explain-error run script.py
```

### 3. Translate Raw Error Strings
You can also pass raw error messages directly as a string or pipe them from another command.

**Pass directly:**
```bash
explain-error "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
```

**Pipe from a file:**
```bash
cat error.log | explain-error
```

## Supported Errors
Currently, the tool can accurately diagnose and explain the following Python errors:
- NameError
- TypeError
- IndexError
- KeyError
- ZeroDivisionError
- ModuleNotFoundError
- AttributeError

*Note: More error definitions are actively being added to the database.*

---
Built by Gourabananda Datta.