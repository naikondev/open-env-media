# Negative fixtures

Each subdirectory is a package the validator must reject. `expected.json` names the error code that must appear.

These exist so the profile cannot be satisfied by three `deployments` resources, and so row-level rules (enums, foreign keys, measurement parents) are actually enforced.
