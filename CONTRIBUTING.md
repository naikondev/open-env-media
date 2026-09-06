# Contributing to EMDP

Contributions are welcome from researchers, conservation practitioners, engineers, platform builders, and data stewards.

## How to contribute

1. Open an issue describing the gap.
2. Draft an RFC: problem, proposed Table Schema change, Camtrap DP compatibility impact, and an example row.
3. Add or update a package in `examples/`.
4. Add a negative fixture under `examples/invalid/` if the change tightens validation.
5. Submit a pull request against the relevant schema or profile.
6. Confirm `emdp validate examples/sample-package` and `python3 scripts/validate.py` pass.

## Profile proposal

A profile must include:

- use-case description
- `observationTypes` and `measurementTypes` it expects
- required vs recommended resources
- compatibility notes with the core model
- at least one example package or CSV excerpt

Taxon and Darwin Core occurrence fields belong in a Camtrap DP export.

Satellite granules and model cubes belong in `contextJoins` (`datasetID`, optional STAC Item URI). See `docs/STAC.md`.

## Standards expectations

- Frictionless Table Schema, camelCase field names
- Overlap Camtrap DP names when the concept is the same
- Clear required vs optional constraints
- Units on numeric fields
- No platform-specific pipeline requirements in the schema

## Validation

```text
pip install -e .
emdp validate examples/sample-package
python3 scripts/validate.py
```

CI installs the package and runs both the CLI and the repo fixture suite. A change that claims to reject a class of packages needs a fixture under `examples/invalid/`.

## Review checklist

- Fits EMDP scope (environmental field evidence)
- Core package contract remains stable (`deployments`, `media`, `observations` exactly once)
- Fields are minimally redundant with measurements or joins
- Example rows validate
- Negative fixtures still fail for the expected code
- Crosswalk implications for dual Camtrap/EMDP exporters are noted
