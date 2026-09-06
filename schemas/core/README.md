# EMDP core schemas

Table Schemas and a Frictionless Data Package profile. Validate these **before** applying a domain profile.

## Package profile

- `emdp-profile.json` — Data Package constraints (required resources, `project`, `spatial`, `temporal`, `emdpProfiles`)

## Required tables

| File | Resource name | Role |
| --- | --- | --- |
| `deployments-table-schema.json` | `deployments` | Site visit or fixed station |
| `media-table-schema.json` | `media` | Files |
| `observations-table-schema.json` | `observations` | Environmental claims |

## Recommended / profile tables

| File | Resource name | When |
| --- | --- | --- |
| `measurements-table-schema.json` | `measurements` | Any quantitative or coded fact |
| `alignments-table-schema.json` | `alignments` | Repeat-photo (`rpdp`) |
| `context-joins-table-schema.json` | `contextJoins` | Satellite or station overlay |
| `impact-records-table-schema.json` | `impactRecords` | CMS attribution profile |

## Vocabularies

- `vocabularies/measurement-types.json`
- `vocabularies/context-datasets.json`

Field names are camelCase and overlap Camtrap DP where the concept is the same. See `docs/CAMTRAP-CROSSWALK.md`.
