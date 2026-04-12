# Contributing to Error Translator

Thank you for contributing to Error Translator. This guide defines the working standards for code, rules, tests, and documentation so the project remains reliable and easy to maintain.

## Contribution principles

- **Clarity over cleverness**: prefer straightforward logic and plain language.
- **Small, reviewable changes**: scoped PRs are easier to test and maintain.
- **Tests with behavior changes**: new behavior should be covered by regression tests.
- **Docs as part of the feature**: user-facing behavior changes require documentation updates.

## Local setup

```bash
pip install -r requirements.txt
pytest
```

If tests pass, the environment is ready for contribution work.

## Where to make changes

- `error_translator/rules.json`:
  - Add or improve regex patterns, explanations, and fixes.
  - Preferred location for most translation improvements.
- `error_translator/core.py`:
  - Update matching/parsing flow only when rule changes are insufficient.
- `error_translator/ast_handlers.py`:
  - Add contextual source-aware insights for specific error families.
- `tests/test_core.py`:
  - Add coverage for any changed behavior.
- `README.md` and `docs/`:
  - Keep onboarding and operational guidance accurate.

## Recommended workflow

1. Identify one concrete issue (incorrect match, unclear fix, missing docs, etc.).
2. Reproduce it with a traceback sample.
3. Implement the minimal fix in rule, code, or docs.
4. Add/adjust tests.
5. Run `pytest`.
6. Re-read modified docs for correctness and tone.

## Rule authoring standards

When adding or refining a rule:

- Match as specifically as practical to avoid false positives.
- Keep explanations concise, neutral, and actionable.
- Keep fixes concrete (what to change and where to look).
- Avoid broad language that could describe many unrelated failures.
- Validate with at least one representative test case.

## Documentation standards

To keep docs professional and useful for future contributors:

- Use clear headings and short paragraphs.
- Define terms before using project-specific shorthand.
- Prefer imperative guidance for contributor steps.
- Avoid promises not backed by current implementation.
- Update docs in the same PR as behavior changes.

## Optional maintenance tools

- `python builder.py`:
  - Generates draft rules from the scraped dataset.
  - Requires `GEMINI_API_KEY`.
- `python scraper.py`:
  - Refreshes `scraped_errors_database.json` from Python documentation.

## Pull request readiness checklist

Before opening a PR, verify:

- [ ] Scope is focused and reviewable.
- [ ] Tests pass locally (`pytest`).
- [ ] Changed behavior has test coverage.
- [ ] Docs were updated where needed.
- [ ] Wording is clear for future contributors.

Thanks again for helping improve the project for the next contributor.
