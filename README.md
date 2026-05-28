# Pyomo Learning - Modular Architecture

This project is a highly modularized Pyomo optimization project. It dynamically discovers and constructs variables, objectives, and constraints using Python's reflection and package utilities.

## Architecture

- `src/datastore/`: Contains coefficients and variable bounds.
- `src/variables/`: Contains deeply nested scripts that define model variables.
- `src/objectives/`: Contains scripts that store Objective expressions.
- `src/constraints/`: Contains pure Python constraint rules, discovered dynamically.
- `src/builder/`: Orchestrates the assembly of the Pyomo model by dynamically traversing the stores.
- `src/utils/`: Utilities for solving and solution extraction.
- `tests/`: Import tests verifying the structure.

## Running the Model

From the root directory, run the solution script:

```bash
python src/utils/runner/main.py
```

## Running Tests

```bash
python -m unittest discover -s tests
```

## Variable Documentation

Rule Definitions:
- **PEP 8 Conventions:** Variables must use `snake_case` (`lowercase_with_underscores`). 
- **Naming:**Constants should use `UPPER_CASE_WITH_UNDERSCORES`. 
- **Naming:**Avoid using ambiguous characters like `l` (lowercase L), `O` (uppercase O), or `I` (uppercase i) as single-character names.
- **Constants:** Defined at the module level. Must be immutable and represent fixed physical parameters or hyper-parameters.
- **Scope:** Private variables (module/class-level) must be prefixed with a single underscore.
- **Clarity:** Variable names must be descriptive, including units where applicable (e.g., _mw, _mwh, _eur).
- **Consistency:** Avoid single-letter variables unless used as indices in mathematical summations (e.g., $i, j, k$).

*Note: Do not refactor mathematical indices or summands (e.g., $i, j, k, t$) within optimization expressions or loops. Maintain their brevity to ensure alignment with standard mathematical notation used in OR literature.*

## Package Management
uv is used for package manegement

### How to Maintain Dependencies
- **Add a dependency**: uv add <package>
- **Add a dev dependency**: uv add --dev <package>
- **Remove a dependency**: uv remove <package>
- **Sync environment**: uv sync (creates/updates uv.lock and syncs .venv)
- **Run scripts safely**: uv run python src/utils/runner/main.py

### How to Maintain Dependencies
- **Add a dependency**: uv add <package>
- **Add a dev dependency**: uv add --dev <package>
- **Remove a dependency**: uv remove <package>
- **Sync environment**: uv sync (creates/updates uv.lock and syncs .venv)
- **Run scripts safely**: uv run python src/utils/runner/main.py
