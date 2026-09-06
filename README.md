# Environmental Media Data Package (EMDP)

Draft **0.3**. An open format for packaging conservation and environmental media: water, air, land-cover change, climate extremes, and dark-sky work.

An EMDP package binds media files to place, time, assertions, measurements, and optional joins to external datasets.

EMDP is a [Frictionless Data Package](https://specs.frictionlessdata.io/). It follows the [Camtrap DP](https://camtrap-dp.tdwg.org/) package graph (`deployment → media → observation`) and defines an observation model for environmental assertions, measurements, and joins. Taxon records stay in Camtrap DP.

| Standard | What the object is | Typical egress |
| --- | --- | --- |
| Camtrap DP + Darwin Core | A taxon at a place and time | GBIF, Wildlife Insights |
| [STAC](https://stacspec.org/) | A geospatial asset at a place and time (search/catalog) | STAC API, EO pipelines |
| EMDP | A survey evidence package (assertions, facts, joins) | Domain archives, CMS, citation |

A CMS that already exports Camtrap DP (for example ArtInStack) can add EMDP as a second exporter from the same survey → deployment → media graph. Mixed projects emit two packages.

See `docs/MODEL.md` for the evidence model, `docs/CAMTRAP-CROSSWALK.md` for dual Camtrap export, and `docs/STAC.md` for how EMDP relates to STAC.

## Why this exists

Wildlife photography maps onto biological schemas. Water, air, land-cover change, climate extremes, and dark-sky work still live in EXIF, spreadsheets, and private databases.

[STAC](https://stacspec.org/) already catalogs files about the Earth at a place and time. STAC is how you find a Sentinel scene or a drone clip. EMDP is how you deposit a survey of interpreted field evidence, in the same sense that Camtrap DP is a deposit format and a Darwin Core Archive is a deposit format. See `docs/STAC.md`.

Platform features (CoralNet overlays, Sentinel tiles, auto-alignment) belong in the CMS. This standard records their outputs so an exported package stays usable on its own.

## Evidence graph

```text
                         PACKAGE (id)
                              │
                    ┌─────────┴─────────┐
                    │                   │
                  MEDIA            DEPLOYMENT
                    │                   │
                    └─────────┬─────────┘
                              │
                         OBSERVATION     ← assertion
                              │
                 ┌────────────┴────────────┐
                 │                         │
           MEASUREMENT               CONTEXT JOIN
           (in situ /                (OpenAQ, ERA5,
            image-derived /           Sentinel, VIIRS)
            model output)
```

**Observation**: assertion (`condition = algal bloom`).
**Measurement**: fact (`chlorophyllA = 42 ug/L`).
**Context join**: value retrieved from an external dataset. The package stores the join.

Measurements may also hang directly off a deployment or media file, including a shoreline logger with no observation row.

**Alignments** connect media to media (repeat photo, restoration before/after, shoreline pairs).
**Attribution records** belong to the CMS `attribution` profile. They record funding provenance.

Media roles (`primary`, `raw`, `derived`, `thumbnail`, `calibration`) distinguish observation frames from camera originals, derivatives, and reference targets such as a color card, SQM, or scale bar.

## Package contract

A compliant package has a canonical `id` and exactly one of each core resource:

```text
emdp-package/
├── datapackage.json
├── deployments.csv      # required, once
├── media.csv            # required, once
├── observations.csv     # required, once
├── measurements.csv     # recommended
├── alignments.csv       # corresponding-scene pairs
├── context-joins.csv    # satellite / station joins
├── attribution-records.csv  # attribution profile only
└── media/
```

Three `deployments` resources do not satisfy the profile. Additional uniquely named resources are allowed.

## Domain profiles

Profiles add vocabularies and optional resources on top of the core tables.

| Profile | For | Typical measurements / joins |
| --- | --- | --- |
| `land` | Land cover, habitat, erosion, fire recovery | `landCoverClass`, canopy %, WorldCover |
| `rpdp` | Fixed-point repeat photography | `alignments` + reused `locationID` |
| `water` | Rivers, lakes, marine habitat | SST, Secchi, salinity, CoralNet cover |
| `atmosphere` | Air quality, flares, haze | PM2.5, NO2, OpenAQ / Sentinel-5P |
| `dark-sky` | Light pollution | SQM, Bortle, VIIRS DNB |
| `climate` | Extremes and event context | ERA5 anomalies, flood stage |
| `attribution` | CMS money-to-activity provenance | `attributionRecords` |

A core-only package (three tables, qualitative `condition`) is valid. Measurements and joins make it comparable.

## Design rules

1. **Camtrap DP for taxa.** Species observations stay in Camtrap DP.
2. **STAC for catalogs.** Asset search stays in STAC. Join to STAC Items; keep the evidence graph in EMDP tables.
3. **Package-first.** The profile rejects missing or duplicate core resources.
4. **Keep assertion, fact, and join separate.**
5. **Joins over warehouses.** Store a retrieved value and its source. Leave Copernicus and station networks where they are.
6. **Privacy is a column.** `spatialPrivacy` may be `exact`, `generalized`, or `withheld`.
7. **Attribution records allocation state.** Status means the money was allocated, in progress, or completed.

## Repository layout

- `schemas/core`: Data Package profile and Table Schemas
- `schemas/core/vocabularies`: measurement types and context dataset IDs
- `schemas/profiles`: domain extensions
- `examples/sample-package`: water-quality reference
- `examples/repeat-photo-package`: multi-year fixed-point example
- `examples/invalid`: fixtures the validator must reject
- `docs/MODEL.md`: evidence model
- `docs/CAMTRAP-CROSSWALK.md`: Camtrap dual-export mapping
- `docs/STAC.md`: relationship to STAC
- `emdp/`: reference Python validator and `emdp` CLI
- `CHARTER.md`: scope and governance

## Reference CLI

Install the validator and point it at a package:

```text
pip install -e .
emdp validate examples/sample-package
emdp validate path/to/my-package
```

`emdp validate` exits `0` if the package is valid and `1` if it is not. `--json` prints machine-readable issues. `python -m emdp` is the same command.

This is the adoption path Camtrap DP used: a checkable contract plus a tool that rejects bad packages. A read/write library (R package, `read_emdp()`) can follow once the tables stabilize.

Repo CI also runs `python3 scripts/validate.py`, which uses the same library against the valid examples and the negative fixtures.

## Quickstart

1. Create `datapackage.json` with a stable `id` and `profile` set to this EMDP version.
2. Add exactly one `deployments`, `media`, and `observations` resource.
3. Declare `emdpProfiles` (e.g. `["water"]`) when a domain applies.
4. Add `measurements` and `contextJoins` for facts and joins.
5. Run `emdp validate .`

## Status

Working draft. Field lists and profile identifiers will change through public review. Schema `$id` URLs are not yet hosted.

## License

- Schema and specification: CC BY 4.0 (`LICENSE-SCHEMA`)
- Reference tooling and validation code: MIT (`LICENSE-CODE`)
