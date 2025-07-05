---
applyTo: '**/*.py'
---

# Python rules

- Use type hints for all function parameters and return values
- Avoid using Async code because streamlit doesn't support it
- Use `async def` for asynchronous functions
- Use `await` for asynchronous calls
- Use Pydantic models for dataclasses
- All python functions should have a docstring

## Testing

- Use `pytest` for testing
- Tests should be organized in folders: `tests/unit` for unit tests and `tests/integration` for integration tests
- Prefer flat test functions instead of using test classes
- Place test fixtures in `conftest.py` files, which can be at different levels in the test hierarchy

## Formatting and Linting

The project is using Use `ruff` and `mypy` for type checking and validations.

Always format all python files by running `uv run invoke format`
You can validate that all files are formatted correctly by running `uv run invoke lint`
If needed, you can ignore some rules for ruff or mypy in the `pyproject.toml` file. 
The recommentation is to disable rules per file, not globally.
If you need to disable a rule for a specific file, you can use the `# noqa: <rule>` comment at the end of the line for `ruff` or `# type: ignore[<rule>]` for `mypy`.