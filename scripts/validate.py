#!/usr/bin/env python3
"""Repo checks: JSON syntax, valid examples, and negative fixtures.

For a single package use the reference CLI: `emdp validate PATH`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from emdp.validate import load_json, profile_schema, schema_dir, validate_package

ROOT = Path(__file__).resolve().parents[1]
VALID_PACKAGES = [
    ROOT / "examples/sample-package",
    ROOT / "examples/repeat-photo-package",
]
INVALID_ROOT = ROOT / "examples/invalid"


def validate_repo_json() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts or "invalid" in path.parts or ".venv" in path.parts:
            continue
        try:
            load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"json: {path}: {exc}")
    Draft202012Validator.check_schema(profile_schema())
    if not (schema_dir() / "emdp-profile.json").exists():
        errors.append("json: bundled profile schema missing")
    return errors


def main() -> int:
    failed = False
    schema_errors = validate_repo_json()
    if schema_errors:
        failed = True
        print("Schema/JSON errors")
        for item in schema_errors:
            print(f"  {item}")

    print("Valid packages")
    for package_dir in VALID_PACKAGES:
        report = validate_package(package_dir)
        if report.ok:
            print(f"  ok   {package_dir.relative_to(ROOT)}")
        else:
            failed = True
            print(f"  FAIL {package_dir.relative_to(ROOT)}")
            for item in report:
                print(f"    {item}")

    print("Invalid fixtures (must fail)")
    for fixture in sorted(
        p for p in INVALID_ROOT.iterdir() if p.is_dir() and (p / "expected.json").exists()
    ):
        token = load_json(fixture / "expected.json")["code"]
        report = validate_package(fixture)
        codes = " ".join(str(item) for item in report)
        if report.ok:
            failed = True
            print(f"  FAIL {fixture.name}: package validated but should not")
        elif token not in codes:
            failed = True
            print(f"  FAIL {fixture.name}: expected {token!r} in errors, got:")
            for item in report:
                print(f"    {item}")
        else:
            print(f"  ok   {fixture.name} ({token})")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
