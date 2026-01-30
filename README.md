# Playwright Python Project

A Python-only Playwright testing project using pytest.

## Setup

1. **Create and activate a virtual environment** (if not already done):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**:
   ```powershell
   python -m playwright install
   ```

## Running Tests

Run all tests:
```powershell
pytest
```

Run a specific test file:
```powershell
pytest tests/test_TT_TBT_Entry.py
```

Run with verbose output:
```powershell
pytest -v
```

Run with browser visible (default):
```powershell
pytest --headed
```

Run headless:
```powershell
pytest --headless
```

## Using Playwright CLI (Python)

Since this is a Python-only project, use Python's module system to run Playwright CLI commands:

**Code generation** (interactive recorder):
```powershell
python -m playwright codegen https://marben.staging.instaff.org
```

**Install browsers**:
```powershell
python -m playwright install
```

**Show help**:
```powershell
python -m playwright --help
```

**Note**: Do NOT use `playwright` directly - use `python -m playwright` instead.

## Project Structure

```
.
├── tests/
│   ├── conftest.py          # Shared pytest fixtures
│   ├── test_TT_TBT_Entry.py # Track By Timer test
│   ├── test_TT_Data_Entry.py # Data Entry test
│   └── test_example.py      # Example test
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## Using Fixtures

The `conftest.py` file provides reusable fixtures:
- `playwright`: Session-scoped Playwright instance
- `browser`: Function-scoped browser instance
- `context`: Function-scoped browser context with geolocation
- `page`: Function-scoped page instance

Example usage:
```python
def test_my_feature(page):
    page.goto("https://example.com")
    # Your test code here
```
