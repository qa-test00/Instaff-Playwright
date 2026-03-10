"""
Run ALL test suite modules in order, sequentially.
Always continues to the next module even if the current one fails.
Captures failures, logs a summary, and references screenshots saved by conftest.

Usage (from project root):
  python test_suites/regression_test_suites.py
  python test_suites/regression_test_suites.py -- --headed -s
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


# All test files across every module, in the intended execution order.
ORDERED_TEST_FILES: tuple[str, ...] = (
    # --- Time Tracking ---
    "tests/Timetracking/test_TT_Data_Entry.py",
    "tests/Timetracking/test_Approve_TT_Entry_Manager.py",
    "tests/Timetracking/test_Approve_TT_Entry_Admin.py",
    "tests/Timetracking/test_TT_TBT_Entry.py",
    "tests/Timetracking/test_Approve_TT_Entry_Manager.py",
    "tests/Timetracking/test_Approve_TT_Entry_Admin.py",
    "tests/Timetracking/test_TT_Reports.py",
    "tests/Timetracking/test_TT_Attendance_Report.py",
    # --- Time Off ---
    "tests/Timeoff/test_TO_Create_Req.py",
    "tests/Timeoff/test_Approve_TO_Req_Manager.py",
    "tests/Timeoff/test_Deny_TO_Req_Admin.py",
    "tests/Timeoff/test_TO_Add_Req_For_Employee.py",
    "tests/Timeoff/test_TO_Mgr_Add_Req_For_Employee.py",
    "tests/Timeoff/test_Generate_TO_Reports.py",
    "tests/Timeoff/test_TO_Time_Restriction.py",
    "tests/Timeoff/test_TO_Print_Download_Calendar.py",
    # --- Holiday ---
    "tests/Holiday/test_Create_Holiday.py",
    "tests/Holiday/test_Verify_Created_Holiday.py",
    "tests/Holiday/test_Delete_Holiday.py",
    # --- Announcement ---
    "tests/Announcement/test_Create_Announcement.py",
    "tests/Announcement/test_View_Announcement.py",
    "tests/Announcement/test_Delete_Announcement.py",
    # --- Survey ---
    "tests/Survey/test_Create_Survey.py",
    "tests/Survey/test_Respond_survey.py",
    "tests/Survey/test_View_Analytics_Responses.py",
    "tests/Survey/test_Close_Survey.py",
    # --- Certifications ---
    "tests/Certifications/test_Cert_Add_Custom_Fields.py",
    "tests/Certifications/test_Cert_Approve_Pending.py",
    "tests/Certifications/test_Cert_View.py",
    "tests/Certifications/test_Cert_Delete_Record.py",
    # --- Manager ---
    "tests/Manager/test_Manager_View_Files.py",
    # --- Paystubs ---
    "tests/Paystubs/test_View_Paystubs.py",
    # --- Employee Files ---
    "tests/Employee Filesv2/test_View_Files_Personal_Employee.py",
)


_MODULE_LABELS: dict[str, str] = {
    "Timetracking":     "Time Tracking",
    "Timeoff":          "Time Off",
    "Holiday":          "Holiday",
    "Announcement":     "Announcement",
    "Survey":           "Survey",
    "Certifications":   "Certifications",
    "Manager":          "Manager",
    "Paystubs":         "Paystubs",
    "Employee Filesv2": "Employee Files",
}


def _humanize_reason(message: str, detail: str) -> str:
    """Convert raw Playwright/pytest error text into a plain-English sentence."""
    msg = message.strip()
    det = detail.strip()

    timeout_match = re.search(r"Timeout (\d+)ms exceeded", msg)
    timeout_ms    = timeout_match.group(1) if timeout_match else None

    # ── Timeout errors ────────────────────────────────────────────────────
    if "TimeoutError" in msg or (timeout_ms and "exceeded" in msg):
        if "Page.goto" in msg or "navigation" in msg.lower():
            return f"Page navigation timed out after {timeout_ms}ms"

        # Look for the locator/selector being waited on inside the detail block
        locator_m = re.search(r'waiting for locator\("([^"]+)"\)', det)
        selector_m = re.search(r"waiting for selector ['\"]?([^'\"\\n]+)['\"]?", det)
        visible_m  = re.search(r"to be (visible|hidden|enabled|disabled|editable)", det)

        state = f" to be {visible_m.group(1)}" if visible_m else ""

        if locator_m:
            return f"Timed out after {timeout_ms}ms – element not found{state}: {locator_m.group(1)}"
        if selector_m:
            return f"Timed out after {timeout_ms}ms – element not found{state}: {selector_m.group(1).strip()}"
        return f"Operation timed out after {timeout_ms}ms"

    # ── Assertion errors ───────────────────────────────────────────────────
    if "AssertionError" in msg:
        # Prefer the assert detail line from the traceback
        for line in det.splitlines():
            stripped = line.strip()
            if stripped.startswith(("assert ", "AssertionError")):
                clean = re.sub(r"^AssertionError:\s*", "", stripped)
                return f"Assertion failed: {clean}"
        inline = re.sub(r"^.*AssertionError:\s*", "", msg)
        return f"Assertion failed: {inline}" if inline else "Assertion failed"

    # ── Generic Playwright element/action errors ───────────────────────────
    for pattern, label in [
        (r"element is not visible",           "Element is not visible"),
        (r"element is not enabled",           "Element is not enabled/clickable"),
        (r"element is outside of the viewport","Element is outside the viewport"),
        (r"Target page.*closed",              "Page or tab was closed unexpectedly"),
        (r"net::ERR_",                        "Network error – page failed to load"),
        (r"strict mode violation",            "Multiple elements matched the locator (strict mode)"),
    ]:
        if re.search(pattern, msg + det, re.IGNORECASE):
            return label

    # ── Strip Python module path prefix (e.g. playwright._impl._errors.Error:) ─
    clean = re.sub(r"^[\w.]+Error:\s*", "", msg)
    return clean if clean and clean != msg else msg


def _cleanup_old_results(project_root: Path) -> None:
    """Delete screenshots, junit XMLs, and summary reports from previous runs."""
    reports_dir = project_root / "reports"

    screenshots_dir = reports_dir / "screenshots"
    if screenshots_dir.exists():
        shutil.rmtree(screenshots_dir)

    junit_dir = reports_dir / "junit"
    if junit_dir.exists():
        shutil.rmtree(junit_dir)

    for summary in reports_dir.glob("regression_summary_*.txt"):
        summary.unlink()

    print("  Previous reports cleared.")


def _safe_filename(path: str) -> str:
    """Convert a test file path to a safe filename stem."""
    return path.replace("/", "_").replace("\\", "_").replace(".py", "")


def _friendly_test_name(test_file: str) -> str:
    """'tests/Timetracking/test_TT_Data_Entry.py' → 'TT Data Entry'"""
    stem = Path(test_file).stem  # e.g. test_TT_Data_Entry
    return stem.removeprefix("test_").replace("_", " ")


def _module_label(test_file: str) -> str:
    parts = Path(test_file).parts  # ('tests', 'Timetracking', 'test_....py')
    folder = parts[1] if len(parts) >= 3 else "Other"
    return _MODULE_LABELS.get(folder, folder)


def _run_pytest_for_file(
    project_root: Path,
    test_file: str,
    extra_pytest_args: list[str],
    junit_xml_path: Path,
) -> int:
    cmd = [
        sys.executable, "-m", "pytest",
        test_file,
        f"--junit-xml={junit_xml_path}",
        "--tb=short",
        *extra_pytest_args,
    ]
    print(f"\n=== Running: {test_file} ===")
    print(f"Command: {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=str(project_root))
    return int(completed.returncode)


def _parse_junit_xml(xml_path: Path) -> list[dict]:
    """Return a list of failure dicts from a JUnit XML file."""
    failures = []
    if not xml_path.exists():
        return failures

    tree = ET.parse(xml_path)
    root = tree.getroot()

    # JUnit XML may have <testsuite> as root or nested inside <testsuites>.
    suites = root.findall(".//testsuite") or [root]
    for suite in suites:
        for tc in suite.findall("testcase"):
            for child in tc:
                if child.tag in ("failure", "error"):
                    # Build a screenshot path using the same pattern as conftest.py
                    classname = tc.get("classname", "")
                    name = tc.get("name", "")
                    screenshot_candidates = list(
                        Path("reports/screenshots").glob(f"*{name}*.png")
                    ) if Path("reports/screenshots").exists() else []

                    failures.append({
                        "test": f"{classname}.{name}",
                        "type": child.tag,
                        "message": (child.get("message") or "").strip().splitlines()[0][:200],
                        "detail": (child.text or "").strip(),
                        "screenshot": str(screenshot_candidates[0]) if screenshot_candidates else "N/A",
                    })
    return failures


def _write_summary(
    project_root: Path,
    run_id: str,
    results: list[dict],  # [{"file": str, "rc": int, "failures": list[dict]}]
) -> Path:
    """Write a human-readable summary file and return its path."""
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    summary_path = reports_dir / f"regression_summary_{run_id}.txt"

    total_files = len(results)
    passed_files = sum(1 for r in results if r["rc"] == 0)
    failed_files = total_files - passed_files
    all_failures = [f for r in results for f in r["failures"]]
    overall_status = "PASSED" if failed_files == 0 else "FAILED"

    # Group results by module, preserving order of first appearance.
    module_order: list[str] = []
    module_results: dict[str, list[dict]] = {}
    for r in results:
        mod = _module_label(r["file"])
        if mod not in module_results:
            module_order.append(mod)
            module_results[mod] = []
        module_results[mod].append(r)

    W = 72  # report width
    SEP  = "=" * W
    SEP2 = "-" * W

    def section(title: str) -> str:
        return f"\n{SEP}\n  {title}\n{SEP2}"

    lines: list[str] = []

    # ── Header ──────────────────────────────────────────────────────────
    lines.append(SEP)
    lines.append("  REGRESSION TEST REPORT")
    lines.append(f"  Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  Run ID : {run_id}")
    lines.append(SEP)
    lines.append(f"  OVERALL : {overall_status}  |  {passed_files} / {total_files} test files passed  |  {len(all_failures)} failure(s)")
    lines.append(SEP)

    # ── Module summary table ────────────────────────────────────────────
    lines.append(section("MODULE SUMMARY"))
    lines.append(f"  {'Module':<26} {'Files':>5}   {'Passed':>6}   {'Failed':>6}   Status")
    lines.append(f"  {'-'*26} {'-----':>5}   {'------':>6}   {'------':>6}   ------")
    for mod in module_order:
        mod_results = module_results[mod]
        mod_passed = sum(1 for r in mod_results if r["rc"] == 0)
        mod_failed = len(mod_results) - mod_passed
        status = "PASSED" if mod_failed == 0 else "FAILED"
        lines.append(f"  {mod:<26} {len(mod_results):>5}   {mod_passed:>6}   {mod_failed:>6}   {status}")
    lines.append(SEP2)

    # ── Per-module test file results ────────────────────────────────────
    lines.append(section("TEST RESULTS"))
    # Track duplicates within each module for labelling
    for mod in module_order:
        lines.append(f"\n  [ {mod} ]")
        seen: dict[str, int] = {}
        for r in module_results[mod]:
            name = _friendly_test_name(r["file"])
            seen[name] = seen.get(name, 0) + 1
        run_count: dict[str, int] = {}
        for r in module_results[mod]:
            name = _friendly_test_name(r["file"])
            run_count[name] = run_count.get(name, 0) + 1
            label = f"{name} (run {run_count[name]})" if seen[name] > 1 else name
            status = "PASS" if r["rc"] == 0 else "FAIL"
            lines.append(f"    {status}  {label}")
    lines.append("\n" + SEP2)

    # ── Failures ────────────────────────────────────────────────────────
    lines.append(section(f"FAILURES  ({len(all_failures)})"))
    if not all_failures:
        lines.append("\n  None – all tests passed.")
    else:
        for idx, f in enumerate(all_failures, 1):
            # Derive a friendly name from the classname/test name in JUnit XML
            raw_name = f["test"].split(".")[-1]  # last segment is the function name
            friendly = raw_name.removeprefix("test_").replace("_", " ")
            lines.append(f"\n  [{idx}] {friendly}")
            lines.append(f"       Reason     : {_humanize_reason(f['message'], f['detail'])}")
            lines.append(f"       Screenshot : {f['screenshot']}")
    lines.append("\n" + SEP + "\n")

    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run all test suite files in a fixed order.")
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Extra args passed to pytest. Use after `--`, e.g. `-- -s --headed`.",
    )
    args = parser.parse_args(argv)

    extra_pytest_args = list(args.pytest_args)
    if extra_pytest_args[:1] == ["--"]:
        extra_pytest_args = extra_pytest_args[1:]

    project_root = Path(__file__).resolve().parent.parent
    _cleanup_old_results(project_root)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    junit_dir = project_root / "reports" / "junit" / run_id
    junit_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Running ALL suites ({len(ORDERED_TEST_FILES)} test files)")
    print(f"  Run ID: {run_id}")
    print(f"{'='*60}")

    overall_rc = 0
    results: list[dict] = []

    for test_file in ORDERED_TEST_FILES:
        xml_path = junit_dir / f"{_safe_filename(test_file)}.xml"
        rc = _run_pytest_for_file(project_root, test_file, extra_pytest_args, xml_path)
        failures = _parse_junit_xml(xml_path)
        results.append({"file": test_file, "rc": rc, "failures": failures})

        if rc != 0:
            overall_rc = rc
            print(f"\n  [!] {test_file} failed — continuing with next module.")

    summary_path = _write_summary(project_root, run_id, results)

    # Print inline summary to console.
    passed = sum(1 for r in results if r["rc"] == 0)
    failed_list = [r["file"] for r in results if r["rc"] != 0]
    all_failures = [f for r in results for f in r["failures"]]

    print(f"\n{'='*60}")
    print(f"  SUMMARY  |  Passed: {passed}  |  Failed: {len(failed_list)}")
    if failed_list:
        print("\n  Failed files:")
        for f in failed_list:
            print(f"    - {f}")
    if all_failures:
        print(f"\n  Failed tests ({len(all_failures)}):")
        for idx, f in enumerate(all_failures, 1):
            print(f"    [{idx}] {f['test']}")
            print(f"         Reason     : {_humanize_reason(f['message'], f['detail'])}")
            print(f"         Screenshot : {f['screenshot']}")
    print(f"\n  Full report saved to:")
    print(f"    {summary_path}")
    print(f"{'='*60}\n")

    return overall_rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
