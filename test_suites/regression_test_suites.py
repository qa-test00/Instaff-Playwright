"""
Run ALL test suite modules in order, sequentially.
Captures failures, logs a summary, and references screenshots saved by conftest.

Usage (from project root):
  python test_suites/regression_test_suites.py
  python test_suites/regression_test_suites.py -- --headed -s
  python test_suites/regression_test_suites.py --continue-on-failure -- -s
"""

from __future__ import annotations

import argparse
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
)


def _safe_filename(path: str) -> str:
    """Convert a test file path to a safe filename stem."""
    return path.replace("/", "_").replace("\\", "_").replace(".py", "")


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

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("  REGRESSION TEST SUMMARY")
    lines.append(f"  Run ID  : {run_id}")
    lines.append(f"  Date    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append(f"  Test files  : {total_files}")
    lines.append(f"  Passed      : {passed_files}")
    lines.append(f"  Failed      : {failed_files}")
    lines.append(f"  Total fails : {len(all_failures)}")
    lines.append("=" * 70)

    if all_failures:
        lines.append("\nFAILED TESTS")
        lines.append("-" * 70)
        for idx, f in enumerate(all_failures, 1):
            lines.append(f"\n[{idx}] {f['test']}")
            lines.append(f"     Type       : {f['type'].upper()}")
            lines.append(f"     Reason     : {f['message']}")
            if f["detail"]:
                # Indent the traceback detail neatly.
                detail_lines = f["detail"].splitlines()
                for dl in detail_lines[-10:]:   # last 10 lines of traceback
                    lines.append(f"               {dl}")
            lines.append(f"     Screenshot : {f['screenshot']}")
    else:
        lines.append("\n  All tests PASSED.")

    lines.append("\n" + "=" * 70)
    lines.append("FILE-LEVEL RESULTS")
    lines.append("-" * 70)
    for r in results:
        status = "PASS" if r["rc"] == 0 else "FAIL"
        lines.append(f"  [{status}] {r['file']}")

    lines.append("=" * 70 + "\n")

    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run all test suite files in a fixed order.")
    parser.add_argument(
        "--continue-on-failure",
        action="store_true",
        help="Keep running remaining files even if one fails.",
    )
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
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    junit_dir = project_root / "reports" / "junit" / run_id
    junit_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Running ALL suites ({len(ORDERED_TEST_FILES)} test files)")
    print(f"  Run ID: {run_id}")
    print(f"{'='*60}")

    overall_rc = 0
    results: list[dict] = []
    stopped_early = False

    for test_file in ORDERED_TEST_FILES:
        xml_path = junit_dir / f"{_safe_filename(test_file)}.xml"
        rc = _run_pytest_for_file(project_root, test_file, extra_pytest_args, xml_path)
        failures = _parse_junit_xml(xml_path)
        results.append({"file": test_file, "rc": rc, "failures": failures})

        if rc != 0:
            overall_rc = rc
            if not args.continue_on_failure:
                print(f"\nStopping: {test_file} failed with exit code {rc}.")
                stopped_early = True
                break

    summary_path = _write_summary(project_root, run_id, results)

    # Print inline summary to console.
    passed = sum(1 for r in results if r["rc"] == 0)
    failed_list = [r["file"] for r in results if r["rc"] != 0]
    all_failures = [f for r in results for f in r["failures"]]

    print(f"\n{'='*60}")
    print(f"  SUMMARY  |  Passed: {passed}  |  Failed: {len(failed_list)}")
    if stopped_early:
        print("  (Run stopped on first failure — use --continue-on-failure to run all)")
    if failed_list:
        print("\n  Failed files:")
        for f in failed_list:
            print(f"    - {f}")
    if all_failures:
        print(f"\n  Failed tests ({len(all_failures)}):")
        for idx, f in enumerate(all_failures, 1):
            print(f"    [{idx}] {f['test']}")
            print(f"         Reason     : {f['message']}")
            print(f"         Screenshot : {f['screenshot']}")
    print(f"\n  Full report saved to:")
    print(f"    {summary_path}")
    print(f"{'='*60}\n")

    return overall_rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
