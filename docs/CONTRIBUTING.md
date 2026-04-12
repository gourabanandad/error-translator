# Contributing to Error Translator

First open-source contribution? You are absolutely welcome here.

This project is intentionally beginner-friendly. Most improvements happen in one JSON file, and many meaningful contributions require zero Python coding.

## New Contributor Path

1. Pick one real traceback that confused you.
2. Add or improve one rule in error_translator/rules.json.
3. Run tests.
4. Open a PR with your sample traceback and expected explanation.

That alone is a high-value contribution.

If you get stuck at any point, open a draft PR anyway and ask for help. Maintainers will guide you.

## Local Setup

~~~bash
pip install -r requirements.txt
pytest
~~~

If tests pass, you are ready.

## Easiest Way to Contribute: Add a Rule

You can extend coverage without writing any Python.

Open error_translator/rules.json and add a new object to the rules array.

Use this copy-paste template:

~~~json
{
  "pattern": "ValueError: invalid literal for int\\(\\) with base 10: '(.*)'",
  "explanation": "You tried to convert '{0}' into an integer, but it is not a valid whole number.",
  "fix": "Make sure '{0}' only contains digits, or parse it as float first if decimals are expected."
}
~~~

Example where this helps:

Input error line:

~~~text
ValueError: invalid literal for int() with base 10: '12.7'
~~~

Result after matching:

- {0} becomes 12.7
- Your explanation and fix are filled in automatically

How placeholders work:

- (.*) captures dynamic text from the error message.
- {0}, {1}, and so on insert those captured values into explanation and fix.

## Rule Writing Tips

- Keep patterns specific to avoid accidental matches.
- Keep explanations short and plain-language.
- Keep fixes actionable and immediate.
- Prefer one focused rule over one very broad rule.

## Where Changes Usually Go

- error_translator/rules.json for new or improved translations
- tests/test_core.py for behavior checks
- README.md and docs for user-facing updates

Only edit core engine files when rule-based changes are not enough.

## Pull Request Checklist

- [ ] I tested locally with pytest.
- [ ] I included a sample traceback in my PR description.
- [ ] My explanation is clear to a beginner.
- [ ] My fix is concrete and actionable.
- [ ] I updated docs if behavior changed.

## Suggested GIF for Your PR

Record a short terminal clip that shows:

1. Running explain-error on a failing traceback before your rule.
2. Adding your JSON rule in rules.json.
3. Running explain-error again to show the improved translation.

Record this as a short terminal GIF at normal speed with readable font size.

Ideal length: 15-30 seconds.

This makes review faster and helps maintainers merge with confidence.

Thanks for building this with us.
