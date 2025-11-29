# Test Report

- **Date**: 2025-11-29
- **Command**: `/Users/halayaghi/Documents/yr3sem1/devops/recipe_manager2/.venv/bin/python -m pytest --cov=. --cov-report=term-missing`
- **Result**: 20 tests passed
- **Coverage**: 97% (per `coverage report --fail-under=70`)
- **Notable gaps**: `config.py` lines 10, 35, 37 and `main.py` lines 35-39, 82-83 remain uncovered (startup/exception paths)
- **Artifacts**: `coverage.xml`, `htmlcov/`, `reports/tests.xml`
