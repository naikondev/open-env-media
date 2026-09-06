# Contributing to EMDP

Contributions are welcome from researchers, conservation practitioners, engineers, platform builders, and data stewards.

## How to contribute

1. Open an issue describing the gap.
2. Draft an RFC: problem, proposed Table Schema change, Camtrap DP compatibility impact, and an example row.
3. Add or update a package in `examples/`.
4. Submit a pull request against the relevant schema or profile.
5. Participate in review.

## Profile proposal

A profile must include:

- use-case description
- `observationTypes` and `measurementTypes` it expects
- required vs recommended resources
- compatibility notes with the core model
- at least one example package or CSV excerpt

Do not add taxon or Darwin Core occurrence fields to core. Propose a Camtrap DP export instead.

Do not add satellite granules or model cubes as package resources. Propose a `contextJoins.datasetID` term.

## Standards expectations

- Frictionless Table Schema, camelCase field names
- Overlap Camtrap DP names when the concept is the same
- Clear required vs optional constraints
- Units on numeric fields
- No platform-specific pipeline requirements in the schema

## Review checklist

- Fits EMDP scope (not wildlife occurrence)
- Core package contract remains stable
- Fields are minimally redundant with measurements or joins
- Example rows validate
- Crosswalk implications for dual Camtrap/EMDP exporters are noted
