# Environmental Media Data Package (EMDP)

Draft **0.2** — an open exchange format for conservation and environmental media that is **not** wildlife-occurrence data.

EMDP is a [Frictionless Data Package](https://specs.frictionlessdata.io/) and a **sister standard to [Camtrap DP](https://camtrap-dp.tdwg.org/)**. Same package shape. Different observation semantics.

| Standard | What an observation is | Typical egress |
| --- | --- | --- |
| Camtrap DP + Darwin Core | A taxon at a place and time | GBIF, Wildlife Insights |
| EMDP | A condition, process, or abiotic measurement at a place and time | Domain archives, CMS evidence, research packages |

A CMS that already exports Camtrap DP (for example ArtInStack) can add EMDP as a second exporter from the same survey → deployment → media graph. Mixed projects emit **two packages**, not one hybrid table of species and smog.

## Why this exists

Wildlife photography maps cleanly onto biological schemas. Water, air, land-cover change, climate extremes, and dark-sky work do not. Those workflows are stuck in EXIF, spreadsheets, and private site databases.

The photograph is not the scientific object. The object is the **media file plus structured context**: where it was made, under what conditions, what was claimed, what was measured, and which external dataset was joined.

Platform features (CoralNet overlays, Sentinel tiles, auto-alignment) belong in the CMS. This standard records the **outputs** of those features so the package remains usable without the platform.

## Package contract

A compliant package is a Data Package whose `profile` points at the EMDP profile, with three required tabular resources:

```text
emdp-package/
├── datapackage.json
├── deployments.csv
├── media.csv
├── observations.csv
├── measurements.csv      # recommended
├── alignments.csv        # repeat photo
├── context-joins.csv     # satellite / station joins
├── impact-records.csv    # optional CMS attribution
└── media/                # optional local files
```

CSV paths may live under `resources/` if `datapackage.json` says so. Root-level names match Camtrap DP so dual exporters stay simple.

```text
deployments 1──* media 1──* observations 1──* measurements
                 │                │
                 └── contextJoins ┘
```

- **deployments** — site visits, fixed stations, or repeat-photo points. Handheld work still gets a deployment row (the visit).
- **media** — files (local path or URL). Coordinates on media are optional; privacy can withhold them.
- **observations** — interpreted environmental claims (`landCover`, `waterQuality`, `airQuality`, …). No `scientificName`.
- **measurements** — Darwin Core MeasurementOrFact analogue. Taxon is to Camtrap as measurement is to EMDP.
- **contextJoins** — a value pulled from OpenAQ, Sentinel-5P, ERA5, VIIRS, etc. at that place and time. The package stores the join, not the remote archive.
- **alignments** — geometric relationship between two frames of the same fixed point.

## Domain profiles

Profiles add vocabularies and optional resources. They do not replace the core tables.

| Profile | For | Typical measurements / joins |
| --- | --- | --- |
| `land` | Land cover, habitat, erosion, fire recovery | `landCoverClass`, canopy %, GFW / WorldCover joins |
| `rpdp` | Fixed-point repeat photography | `alignments` + reused `locationID` |
| `water` | Rivers, lakes, marine habitat | SST, Secchi, salinity, CoralNet cover |
| `atmosphere` | Air quality, flares, haze | PM2.5, NO2, OpenAQ / Sentinel-5P |
| `dark-sky` | Light pollution | SQM, Bortle, VIIRS DNB |
| `climate` | Extremes and attribution context | ERA5 anomalies, flood stage |
| `impact-record` | CMS money → activity provenance | `impactRecords` (not a science table) |

A core-only package (three tables, qualitative `condition`) is valid. Measurements and joins make it comparable.

## Design rules

1. **Do not compete with Camtrap DP.** Species stay there.
2. **Package-first.** Validate structure before arguing about field lists.
3. **Measurements over free text.** `condition=algal bloom` is a label; `chlorophyllA=42 ug/L` is a fact.
4. **Joins over warehouses.** EMDP is not a Copernicus mirror.
5. **Privacy is a first-class column.** `spatialPrivacy` may be `exact`, `generalized`, or `withheld`. Latitude/longitude are not required when withheld.
6. **Impact records do not claim outcomes.** Allocation status ≠ restoration success.

## Repository layout

- `schemas/core` — Data Package profile and Table Schemas
- `schemas/core/vocabularies` — measurement types and context dataset IDs
- `schemas/profiles` — domain extensions
- `examples/sample-package` — water-quality reference package
- `docs/CAMTRAP-CROSSWALK.md` — mapping for platforms that already ship Camtrap DP
- `CHARTER.md` — scope and governance
- `CONTRIBUTING.md` — RFC process

## Quickstart

1. Create `datapackage.json` with `profile` set to this EMDP version.
2. Add `deployments`, `media`, and `observations` as `tabular-data-resource` rows.
3. Declare `emdpProfiles` (e.g. `["water"]`) when a domain applies.
4. Add `measurements` and `contextJoins` for anything quantitative or joined.
5. Validate with a Frictionless Table Schema validator.

See `examples/sample-package` for a complete water-quality bundle.

## Status

Working draft. Field lists and profile identifiers will change through public review. Identifiers under `schemas/` are not yet published at a stable URL.

## License

- Schema and specification: CC BY 4.0 (`LICENSE-SCHEMA`)
- Reference tooling and validation code: MIT (`LICENSE-CODE`)
