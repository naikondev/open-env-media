# EMDP core schemas

Table Schemas and a Frictionless Data Package profile. Validate these before applying a domain profile.

## Package profile

- `emdp-profile.json`: requires `id` and exactly one `deployments`, `media`, and `observations` resource

## Required tables

| File | Resource name | Role |
| --- | --- | --- |
| `deployments-table-schema.json` | `deployments` | Site visit or fixed station |
| `media-table-schema.json` | `media` | Evidence files (`mediaRole` includes calibration) |
| `observations-table-schema.json` | `observations` | Assertions |

## Recommended / profile tables

| File | Resource name | When |
| --- | --- | --- |
| `measurements-table-schema.json` | `measurements` | Facts (may hang off deployment, media, or observation) |
| `alignments-table-schema.json` | `alignments` | Corresponding-scene pairs |
| `context-joins-table-schema.json` | `contextJoins` | Satellite or station overlay |
| `attribution-records-table-schema.json` | `attributionRecords` | CMS `attribution` profile only |

## Vocabularies

- `vocabularies/measurement-types.json`
- `vocabularies/context-datasets.json`

See `docs/MODEL.md` and `docs/CAMTRAP-CROSSWALK.md`.
