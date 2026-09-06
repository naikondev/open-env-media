"""emdp command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from emdp import __version__, validate_package


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="emdp",
        description="Reference validator for Environmental Media Data Packages.",
    )
    parser.add_argument("--version", action="version", version=f"emdp {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    validate_cmd = sub.add_parser("validate", help="validate an EMDP package directory")
    validate_cmd.add_argument("path", help="package directory or datapackage.json")
    validate_cmd.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="print issues as JSON",
    )

    args = parser.parse_args(argv)
    if args.command == "validate":
        return _validate(Path(args.path), as_json=args.as_json)
    return 2


def _validate(path: Path, as_json: bool) -> int:
    report = validate_package(path)
    if as_json:
        print(
            json.dumps(
                {
                    "path": str(report.path),
                    "ok": report.ok,
                    "issues": [{"code": i.code, "message": i.message} for i in report.issues],
                },
                indent=2,
            )
        )
    elif report.ok:
        print(f"{report.path}: valid")
    else:
        print(f"{report.path}: invalid")
        for issue in report.issues:
            print(f"  {issue}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
