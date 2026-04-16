# Contributing to Error Translator

Thank you for your interest in contributing to Error Translator! This project was built to be highly accessible and welcoming to new developers. Most improvements to the engine's translation mapping occur within a single JSON configuration file, meaning impactful contributions are possible even without extensive Python experience.

## Developer Setup

Clone the repository and set up your virtual environment for local development:

```bash
git clone https://github.com/gourabanandad/error-translator.git
cd error-translator
python -m venv .venv

# Activate environment (Windows)
.\.venv\Scripts\activate
# Activate environment (macOS/Linux)
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
pytest
```

If the test suite passes successfully, your local environment is correctly configured.

## Writing Meaningful Rules

The core of Error Translator is driven by `rules.json`. Adding a rule significantly enhances the translation engine's coverage.

Navigate to `error_translator/rules.json` and append your pattern to the `rules` array.

### Schema Template

```json
{
  "pattern": "ValueError: invalid literal for int\\(\\) with base 10: '(.*)'",
  "explanation": "You tried to convert '{0}' into an integer, but it is not a valid whole number.",
  "fix": "Make sure '{0}' only contains digits, or parse it as float first if decimals are expected."
}
```

### Capturing Mechanism

- The engine evaluates Python `re` syntax against the target exception.
- `(.*)` evaluates and captures dynamic runtime variables from the raw traceback.
- `{0}`, `{1}`, etc., inject those extracted sub-patterns into your defined `explanation` and `fix` strings for rich user context.

## The Fastest Workflow: AI-Powered Rule Builder

If you have a Google Gemini API key, you can utilize our integrated tooling to automate the rule creation lifecycle entirely:

1. **Scrape Reference Errors**: Download the standard library error map natively.
   ```bash
   python scraper.py
   ```
   *(This hydrates `scraped_errors_database.json`)*

2. **Run the Interactive Builder**: Export your authentication credentials and invoke the rule generator.
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="your_api_key_here"
   python builder.py
   
   # macOS/Linux
   export GEMINI_API_KEY="your_api_key_here"
   python builder.py
   ```

The script autonomously identifies gaps between `rules.json` and official Python specs, queries the Gemini model to synthesize high-quality regex `pattern` matching, and generates accessible `explanation`s and `fix`es. You can then interactively Accept, Edit, or Skip the proposal.

## Pull Request Standards

Before submitting a Pull Request, please ensure the following:

- [ ] **Test Coverage**: You have verified new rules locally via `pytest` and updated `tests/test_core.py` when applicable.
- [ ] **Accessibility**: Explanations are drafted in plain, supportive terminology without unnecessary technical jargon.
- [ ] **Actionability**: Suggested fixes are concrete, deterministic, and immediately applicable by a developer.
- [ ] **Demonstration**: Include the raw traceback and the output translation directly in your Pull Request description.

We appreciate your commitment to building a better developer experience with us!
