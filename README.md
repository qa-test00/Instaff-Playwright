<<<<<<< HEAD
# Playwright Python Project

A Playwright + pytest automation suite for the Instaff staging HR web application.

## Setup

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**:
   ```bash
   python -m playwright install
   ```

## Configuration

All settings are centralised in `config.py` and can be overridden via environment variables:

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://marben.staging.instaff.org` | Target application URL |
| `HEADLESS` | `false` | Run browser headlessly |
| `SLOW_MO` | `0` | Milliseconds between actions (debug aid) |
| `DEFAULT_TIMEOUT` | `30000` | Default element timeout (ms) |
| `NAVIGATION_TIMEOUT` | `30000` | Navigation timeout (ms) |
| `ADMIN_EMAIL` | *(see config.py)* | Admin user credentials |
| `EMPLOYEE_EMAIL` | *(see config.py)* | Employee user credentials |

## Running Tests

Run all tests:
```bash
pytest
```

Run a specific module folder:
```bash
pytest tests/Timetracking/
```

Run a specific test file:
```bash
pytest tests/Timetracking/test_TT_TBT_Entry.py
```

Run with verbose output:
```bash
pytest -v
```

Run headless:
```bash
HEADLESS=true pytest
```

## Project Structure

```
.
├── config.py                        # Centralised config & credentials
├── pytest.ini                       # Pytest configuration
├── shared_data.json                 # Shared state between tests (e.g. holiday name/date)
├── requirements.txt
└── tests/
    ├── conftest.py                  # Shared fixtures: page, admin_page, employee_page
    ├── pages/                       # Page Object Model
    │   ├── base_page.py
    │   ├── login_page.py
    │   ├── time_tracking_page.py
    │   ├── time_off_page.py
    │   ├── holiday_page.py
    │   ├── announcement_page.py
    │   ├── survey_page.py
    │   ├── certifications_page.py
    │   ├── paystubs_page.py
    │   ├── manager_page.py
    │   ├── company_directory_page.py
    │   ├── employee_files_page.py
    │   └── upload_docs_page.py
    ├── Timetracking/
    │   ├── test_TT_TBT_Entry.py
    │   ├── test_TT_Data_Entry.py
    │   ├── test_TT_Bulk_Add_Entries.py
    │   ├── test_TT_Reports.py
    │   ├── test_TT_Attendance_Report.py
    │   ├── test_Approve_TT_Entry_Admin.py
    │   └── test_Approve_TT_Entry_Manager.py
    ├── Timeoff/
    │   ├── test_TO_Create_Req.py
    │   ├── test_TO_Add_Req_For_Employee.py
    │   ├── test_TO_Mgr_Add_Req_For_Employee.py
    │   ├── test_Approve_TO_Req_Manager.py
    │   ├── test_Deny_TO_Req_Admin.py
    │   ├── test_TO_Time_Restriction.py
    │   ├── test_TO_Print_Download_Calendar.py
    │   └── test_Generate_TO_Reports.py
    ├── Holiday/
    │   ├── test_Create_Holiday.py
    │   ├── test_Verify_Created_Holiday.py
    │   └── test_Delete_Holiday.py
    ├── Announcement/
    │   ├── test_Create_Announcement.py
    │   ├── test_View_Announcement.py
    │   └── test_Delete_Announcement.py
    ├── Survey/
    │   ├── test_Create_Survey.py
    │   ├── test_Respond_survey.py
    │   ├── test_View_Analytics_Responses.py
    │   └── test_Close_Survey.py
    ├── Certifications/
    │   ├── test_Cert_View.py
    │   ├── test_Cert_Add_Custom_Fields.py
    │   ├── test_Cert_Approve_Pending.py
    │   └── test_Cert_Delete_Record.py
    ├── Paystubs/
    │   └── test_View_Paystubs.py
    ├── Manager/
    │   └── test_Manager_View_Files.py
    ├── CompanyDirectory/
    │   ├── test_Verify_List.py
    │   └── test_Organization_Chart.py
    ├── UploadDocs/
    │   ├── test_Upload_Normal_PS.py
    │   └── test_UploadScheduled_PS.py
    └── Employee Filesv2/
        └── test_View_Files_Personal_Employee.py
```

## Architecture

- **Page Object Model** — each feature module has a corresponding page class in `tests/pages/`
- **Fixtures** — `conftest.py` provides `page` (admin), `admin_page`, and `employee_page`; browser is session-scoped, context and page are function-scoped (isolated per test)
- **Shared state** — `shared_data.json` passes data between dependent tests (e.g. Holiday create → verify → delete)

## Playwright CLI

Use Python's module system for Playwright CLI commands:

```bash
# Interactive code recorder
python -m playwright codegen https://marben.staging.instaff.org

# Install browsers
python -m playwright install

# Help
python -m playwright --help
```

> Note: Use `python -m playwright` — do NOT call `playwright` directly.
=======
# Repo Number: Project Name

### Description

Short description of this project, what it's functions are, and it's overall goal from a business perspective.

-----

### Environment Requirements

**1. Sage Version**
- [Version]

**2. Run Modes**
- Automated (if so, what is the argument to pass?)
- Manual

**3. Environment Setup**

Anything you needed to turn on/enable, or set up to make the program work.

If applicable, list them here, for example:

- Orchid EFT must be installed in Sage
- Sage Multiple Contacts must be installed
- AutoSimply Production Planning must be installed in Sage
- GL Account structures must be a certain way in Sage
- Multicurrency must be enabled in Sage
- An sFTP server must be set up for testing
- API connections, credentials and where to get them (Dev sandbox, client account?)


**4. Sage Optional Fields Setup**

| Optional Field Name | Module/Location | Purpose |
| --- | --- | --- |
| | | |
| | | |
| | | |

Note: If applicable, add a screenshot of the common services optional field screen to illustrate the mapping.


**5. Program Configuration**

List out the configuration settings (and possibly a screenshot if it helps illustrate) in the program, and what each setting is for.

| Configuration | Value | Purpose |
| --- | --- | --- |
| | | |
| | | |
| | | |

-----

### Functionality

**1. Function 1 (e.g. Importing into AR Invoices from Excel File)**

Describe the functionality of this process, and possibly screenshots to illustrate the source and destination. List out any relevant mappings if it makes sense. Describe any notable logic.

**2. Function 2 (e.g. Updating web API with receipts into)**

Describe the functionality of this process, and possibly screenshots to illustrate the source and destination. List out any relevant mappings if it makes sense. Describe any notable logic.

-----

### Logging

What should it be logging? Each transaction? Details? IDs?

-----

### UI

If notable, include a screenshot of the UI while highlighting important parts.

-----

### Testing data

**1. Testing Database**

Put the location of the testing database file if there is any. eg. \\fs1\database archive\...

**2. Testing Account/Credentials**

If necessary, put Notedock links here.

For example, credentials of Shopify, Docuware.

-----

### Developer Notes

**1. SQL Query**

If necessary, paste SQL queries used in the program for quick reference.

**2. Special UI/Functions/Extensions**

Any code related things that the future developers need to know. Can be a special function, method, UI, extensions, ...
>>>>>>> ea664c8a1defaf0dacc2965dd8f8a9bd8aaa9e8e
