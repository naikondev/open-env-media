"""Validate an EMDP package directory."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from jsonschema import Draft202012Validator

MISSING = {"", "NA", "NaN", "nan"}
ISO_DT = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$"
)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BUNDLED_BY_RESOURCE = {
    "deployments": "deployments-table-schema.json",
    "media": "media-table-schema.json",
    "observations": "observations-table-schema.json",
    "measurements": "measurements-table-schema.json",
    "alignments": "alignments-table-schema.json",
    "contextJoins": "context-joins-table-schema.json",
    "attributionRecords": "attribution-records-table-schema.json",
}


@dataclass
class Issue:
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


@dataclass
class Report:
    path: Path
    issues: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def add(self, code: str, message: str) -> None:
        self.issues.append(Issue(code, message))

    def __iter__(self):
        return iter(self.issues)

    def __str__(self) -> str:
        return "\n".join(str(issue) for issue in self.issues)


def schema_dir() -> Path:
    here = Path(__file__).resolve().parent
    for candidate in (here / "schemas", here.parent / "schemas" / "core"):
        if (candidate / "emdp-profile.json").exists():
            return candidate
    raise FileNotFoundError("EMDP table schemas are not installed")


def profile_schema() -> dict:
    return json.loads((schema_dir() / "emdp-profile.json").read_text())


def load_json(path: Path) -> object:
    return json.loads(path.read_text())


def empty(value: str | None) -> bool:
    return value is None or value.strip() in MISSING


def validate_profile_document(package: dict, report: Report) -> None:
    validator = Draft202012Validator(profile_schema())
    for err in sorted(validator.iter_errors(package), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "(root)"
        report.add("schema", f"{loc}: {err.message}")

    names = [r.get("name") for r in package.get("resources") or [] if isinstance(r, dict)]
    if len(names) != len(set(names)):
        report.add("unique-resource-names", f"duplicate resource names: {names}")


def resolve_schema(package_dir: Path, resource_name: str, schema_ref: str | None) -> dict:
    if schema_ref:
        path = Path(schema_ref)
        if not path.is_absolute():
            path = (package_dir / schema_ref).resolve()
        if path.exists():
            return json.loads(path.read_text())
    bundled = BUNDLED_BY_RESOURCE.get(resource_name)
    if bundled:
        fallback = schema_dir() / bundled
        if fallback.exists():
            return json.loads(fallback.read_text())
    raise FileNotFoundError(schema_ref or resource_name)


def cast_ok(value: str, field: dict) -> str | None:
    ftype = field.get("type")
    constraints = field.get("constraints") or {}
    if empty(value):
        if constraints.get("required"):
            return f"required field {field['name']} is empty"
        return None
    if ftype == "boolean" and value.lower() not in {"true", "false"}:
        return f"{field['name']} is not a boolean: {value!r}"
    if ftype == "integer":
        try:
            int(value)
        except ValueError:
            return f"{field['name']} is not an integer: {value!r}"
    if ftype == "number":
        try:
            float(value)
        except ValueError:
            return f"{field['name']} is not a number: {value!r}"
    if ftype == "datetime" or field.get("format") == "%Y-%m-%dT%H:%M:%S%z":
        if not ISO_DT.match(value):
            return f"{field['name']} is not ISO 8601 datetime: {value!r}"
    elif ftype == "date" or field.get("format") == "%Y-%m-%d":
        if not ISO_DATE.match(value):
            return f"{field['name']} is not ISO 8601 date: {value!r}"
    if "enum" in constraints and value not in constraints["enum"]:
        return f"{field['name']} value {value!r} not in enum"
    pattern = constraints.get("pattern")
    if pattern and not re.match(pattern, value):
        return f"{field['name']} does not match {pattern}: {value!r}"
    if ftype in {"number", "integer"}:
        number = float(value)
        minimum = constraints.get("minimum")
        maximum = constraints.get("maximum")
        if minimum is not None and number < minimum:
            return f"{field['name']} below minimum {minimum}"
        if maximum is not None and number > maximum:
            return f"{field['name']} above maximum {maximum}"
    return None


def read_table(package_dir: Path, resource: dict) -> tuple[list[str], list[dict]]:
    path = package_dir / resource["path"]
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def validate_tables(package_dir: Path, package: dict, report: Report) -> None:
    resources = {r["name"]: r for r in package.get("resources") or [] if "name" in r}
    tables: dict[str, tuple[dict, list[dict]]] = {}

    for name, resource in resources.items():
        try:
            schema = resolve_schema(package_dir, name, resource.get("schema"))
        except Exception as exc:
            report.add("schema-ref", f"{name}: cannot load schema: {exc}")
            continue
        try:
            headers, rows = read_table(package_dir, resource)
        except FileNotFoundError as exc:
            report.add("missing-file", str(exc))
            continue

        fields = schema.get("fields") or []
        missing_cols = [f["name"] for f in fields if f["name"] not in headers]
        if missing_cols:
            report.add("headers", f"{name}: missing columns {missing_cols}")
            continue

        tables[name] = (schema, rows)
        seen: dict[str, set[str]] = {
            f["name"]: set() for f in fields if (f.get("constraints") or {}).get("unique")
        }
        primary = schema.get("primaryKey")
        if primary:
            seen.setdefault(primary, set())

        for index, row in enumerate(rows, start=2):
            for field_spec in fields:
                message = cast_ok(row.get(field_spec["name"], ""), field_spec)
                if message:
                    report.add("row", f"{name}:{index} {message}")
                value = row.get(field_spec["name"], "")
                if field_spec["name"] in seen and not empty(value):
                    if value in seen[field_spec["name"]]:
                        report.add(
                            "duplicate-id",
                            f"{name}:{index} duplicate {field_spec['name']}={value}",
                        )
                    seen[field_spec["name"]].add(value)

            if name == "measurements":
                parents = [row.get(k, "") for k in ("deploymentID", "observationID", "mediaID")]
                if all(empty(p) for p in parents):
                    report.add(
                        "measurement-parent",
                        f"{name}:{index} must reference deploymentID, observationID, or mediaID",
                    )

    for name, (schema, rows) in tables.items():
        for fk in schema.get("foreignKeys") or []:
            src = fk["fields"]
            ref_resource = fk["reference"]["resource"]
            ref_field = fk["reference"]["fields"]
            if ref_resource not in tables:
                continue
            allowed = {
                row.get(ref_field, "")
                for row in tables[ref_resource][1]
                if not empty(row.get(ref_field, ""))
            }
            for index, row in enumerate(rows, start=2):
                value = row.get(src, "")
                if empty(value):
                    continue
                if value not in allowed:
                    report.add(
                        "foreign-key",
                        f"{name}:{index} {src}={value} not in {ref_resource}.{ref_field}",
                    )


def validate_package(package_dir: str | Path) -> Report:
    """Validate a directory that contains datapackage.json."""
    path = Path(package_dir)
    report = Report(path)
    manifest = path / "datapackage.json" if path.is_dir() else path
    if manifest.name != "datapackage.json":
        manifest = path / "datapackage.json"
    package_root = manifest.parent
    report.path = package_root
    if not manifest.exists():
        report.add("missing-file", str(manifest))
        return report
    try:
        package = load_json(manifest)
    except json.JSONDecodeError as exc:
        report.add("json", f"{manifest}: {exc}")
        return report
    if not isinstance(package, dict):
        report.add("json", "datapackage.json must be an object")
        return report
    validate_profile_document(package, report)
    validate_tables(package_root, package, report)
    return report
