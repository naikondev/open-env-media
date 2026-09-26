# Contributing to EMDP

Contributions are welcome from researchers, conservation practitioners, engineers, platform builders, and data stewards.

## How to contribute

1. Open an issue for a validator bug, a broken example, or a small docs fix.
2. For a new profile, a dropped profile, or a breaking schema change, open an RFC with [the RFC issue template](.github/ISSUE_TEMPLATE/rfc.md). See `CHARTER.md` for who decides, the 7-day wait, and how an RFC is accepted.
3. After the RFC is accepted (or for a change that does not need one), add or update a package in `examples/`.
4. Add a negative fixture under `examples/invalid/` if the change tightens validation.
5. Submit a pull request against the relevant schema or profile. Link the RFC issue.
6. Confirm `emdp validate examples/water-package` and `python3 scripts/validate.py` pass.

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
- Profile `measurementTypes` must exist in `schemas/core/vocabularies/measurement-types.json`
- Known types must use the registry unit (`sqm` is `mag/arcsec2`, not `%`)
- No platform-specific pipeline requirements in the schema

## Validation

```text
pip install -e .
emdp validate examples/water-package
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
