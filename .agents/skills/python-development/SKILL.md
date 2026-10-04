---
name: python-development
description: >-
  Use this skill for standard Python development tasks including writing code, enforcing best practices, linting, formatting, and running tests.
---

# Python Development Skill

This skill provides guidelines and common procedures for Python development in this workspace.

## Best Practices

- **Formatting & Linting:** Use tools like `black`, `ruff`, or `flake8` to maintain code quality and follow PEP-8 conventions.
- **Type Hinting:** Use standard Python type hinting to make code more readable and catch errors early.
- **Virtual Environments:** Always run commands within the context of a virtual environment if one is present.
- **Documentation:** Use docstrings for all modules, classes, and functions.

## Common Runbooks

### 1. Running Scripts
Execute Python files using the standard interpreter:
`python <filename>.py`

### 2. Testing
If tests are written, they should typically be run with `pytest` or `unittest`.
Example:
`python -m pytest`

### 3. Managing Dependencies
Keep track of dependencies in `requirements.txt` or `pyproject.toml`.
To install dependencies:
`pip install -r requirements.txt`

## Verification
Whenever editing code, ensure you check for syntax errors or execute the code to verify it works as intended.
