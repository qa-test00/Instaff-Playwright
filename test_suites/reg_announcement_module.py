"""
Run an ordered suite of pytest files (sequentially).

Usage (from project root):
  python test_suites/reg_announcement_module.py
  python test_suites/reg_announcement_module.py -- --headed -s
  python test_suites/reg_announcement_module.py --continue-on-failure -- -s
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ORDERED_TEST_FILES: tuple[str, ...] = (
    "tests/Announcement/test_Create_Announcement.py",
    "tests/Announcement/test_View_Announcement.py",
    "tests/Announcement/test_Delete_Announcement.py",
)


def _run_pytest_for_file(project_root: Path, test_file: str, extra_pytest_args: list[str]) -> int:
    cmd = [sys.executable, "-m", "pytest", test_file, *extra_pytest_args]
    print(f"\n=== Running: {test_file} ===")
    print(f"Command: {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=str(project_root))
    return int(completed.returncode)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run pytest files in a fixed order.")
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

    # Strip the `--` separator if present in REMAINDER.
    extra_pytest_args = list(args.pytest_args)
    if extra_pytest_args[:1] == ["--"]:
        extra_pytest_args = extra_pytest_args[1:]

    # This file lives in `test_suites/`, so project root is one level up.
    project_root = Path(__file__).resolve().parent.parent

    overall_rc = 0
    for test_file in ORDERED_TEST_FILES:
        rc = _run_pytest_for_file(project_root, test_file, extra_pytest_args)
        if rc != 0:
            overall_rc = rc
            if not args.continue_on_failure:
                print(f"\nStopping: {test_file} failed with exit code {rc}.")
                return overall_rc

    return overall_rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

