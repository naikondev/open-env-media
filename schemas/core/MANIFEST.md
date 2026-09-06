# EMDP core manifest specification

Working draft for `datapackage.json`.

## Minimum contract

- Valid JSON satisfying `emdp-profile.json`
- Canonical package `id` (prefer a URI; local row IDs are scoped to it)
- `profile` set to this EMDP profile version
- Exactly one resource named `deployments`, exactly one `media`, and exactly one `observations`
- Each of those three is a `tabular-data-resource` with `path` and `schema`
- Resource `name` values are unique across the package
- `created`, `contributors`, `project`, `spatial`, `temporal`

Recommended:

- `homepage`: resolvable landing page
- `emdpProfiles`: `land`, `rpdp`, `water`, `atmosphere`, `dark-sky`, `climate`, and/or `attribution`
- `licenses` with `scope` `data` and `media`
- `measurements` whenever values exist
- `coordinatePrecision` when published coordinates were coarsened

A package with three `deployments` resources and no `media` is invalid.

## Identifiers

Local IDs (`obs1`, `m1`) are unique within the package. A global handle MAY be `{package.id}/{resource}/{localID}`. Re-exports of the same evidence SHOULD keep `id` stable and bump `version`.

## `project` object

Required: `title`, `captureMethod`, `observationTypes`.

There is no `taxonomic` block. That belongs in Camtrap DP.

## Required fields (core)

### deployments

`deploymentID`, `deploymentStart`, `deploymentEnd`

`latitude` and `longitude` are required unless `spatialPrivacy` is `withheld`.

### media

`mediaID`, `deploymentID`, `timestamp`, `filePath`, `filePublic`, `fileMediatype`

### observations

`observationID`, `deploymentID`, `eventStart`, `eventEnd`, `observationLevel`, `observationType`

`mediaID` is required when `observationLevel` is `media`.

### measurements

`measurementID`, `measurementType`, `measurementValue`, `measurementSource`

At least one of `deploymentID`, `observationID`, `mediaID` MUST be present.

`measurementValue` is lexical. Consumers MUST interpret datatype from `measurementType`, `measurementUnit`, and `measurementScheme`.

## Validation

1. Manifest satisfies `emdp-profile.json` (including exactly-once core resources).
2. Resource names are unique.
3. Every declared path exists.
4. Each table validates against its Table Schema.
5. Foreign keys hold when the referencing cell is not empty.
6. Measurement parent rule holds.
7. Wildlife/taxon rows are absent.

Run `emdp validate <package-dir>`. Repo fixtures: `python3 scripts/validate.py`.

## Status

Draft 0.3.
