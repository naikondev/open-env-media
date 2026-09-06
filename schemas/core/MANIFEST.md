# EMDP core manifest specification

Working draft for `datapackage.json`.

## Minimum contract

- Valid Frictionless Data Package
- `profile` set to this EMDP profile version
- Resources named `deployments`, `media`, and `observations`, each a `tabular-data-resource` with a schema URL or path
- `created`, `contributors`, `project`, `spatial`, `temporal`

Recommended:

- `emdpProfiles` — one or more of `land`, `rpdp`, `water`, `atmosphere`, `dark-sky`, `climate`, `impact-record`
- `licenses` with `scope` `data` and `media`
- `measurements` resource whenever values exist
- `coordinatePrecision` when published coordinates were coarsened

## `project` object

Required:

- `title`
- `captureMethod` — `handheld` | `fixedPoint` | `timeLapse` | `activityDetection` | `aerial` | `underwater` | `other`
- `observationTypes` — subset of the observation-type vocabulary

There is no `taxonomic` block. That belongs in Camtrap DP.

## Resource example

```json
{
  "name": "media",
  "path": "media.csv",
  "profile": "tabular-data-resource",
  "schema": "https://example.org/emdp/0.2/media-table-schema.json"
}
```

Until a stable URL exists, examples in this repository use relative paths into `schemas/core`.

## Required fields (core)

### deployments

`deploymentID`, `deploymentStart`, `deploymentEnd`

`latitude` and `longitude` are required unless `spatialPrivacy` is `withheld`.

### media

`mediaID`, `deploymentID`, `timestamp`, `filePath`, `filePublic`, `fileMediatype`

### observations

`observationID`, `deploymentID`, `eventStart`, `eventEnd`, `observationLevel`, `observationType`

`mediaID` is required when `observationLevel` is `media`.

## Validation

1. Manifest is valid JSON and satisfies `emdp-profile.json`.
2. Every declared path exists.
3. Each table validates against its Table Schema (types, required, foreign keys).
4. Declared `emdpProfiles` only use listed observation and measurement types as recommended terms (additional types allowed, not required).
5. Wildlife/taxon rows are absent.

## Status

Draft 0.2. Breaking changes will increment the minor version until 1.0.
