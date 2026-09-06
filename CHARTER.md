# EMDP Charter

## Mission

EMDP is an open exchange format for environmental media that falls **outside** the wildlife-tracking stack. It links media files to place, time, interpreted condition, measurements, and optional joins to external environmental datasets.

Wildlife occurrence data already has Camtrap DP and Darwin Core. EMDP exists so water, air, land-cover, climate, and dark-sky media can be packaged with the same seriousness — without inventing a second species standard.

## Scope

In scope:

- repeat photography for land cover, habitat, glacier, and shoreline change
- water-quality and hydrological documentation
- air-quality and atmospheric hazard documentation
- dark-sky and light-pollution assessments
- climate-extreme and disturbance documentation
- restoration and intervention records as **conditions**, not claimed outcomes
- optional provenance records that link economic actions to activity (CMS profile)

Out of scope:

- taxon occurrences, camera-trap animal classifications, or a GBIF competitor
- storing satellite archives, climate model cubes, or station networks
- specifying computer-vision or alignment algorithms
- treating allocation or donation records as proof of ecological success

## Goals

- A predictable, validatable package isomorphic to Camtrap DP
- A measurement table that plays the role taxon plays for wildlife
- Domain profiles that do not fragment the core
- Privacy and embargo that do not break interchange
- A governance process suitable for open scientific and conservation data

## Principles

1. **Open by default**
2. **Package-first** — structure before field arguments
3. **Sister to Camtrap DP** — same graph, different observation payload
4. **Extensible by profile** — vocabularies and optional resources, not forked cores
5. **Temporal and spatial integrity** — including the right to withhold coordinates
6. **Evidence quality and provenance** — hashes, licenses, classification audit
7. **Joins, not warehouses** — name the dataset and store the retrieved value
8. **Compatible with Data Package / Table Schema conventions**

## Package model

Minimum compliant package:

- `datapackage.json` using the EMDP profile
- `deployments`, `media`, `observations` tabular resources
- declared `project`, `spatial`, and `temporal` metadata

Optional resources (`measurements`, `alignments`, `contextJoins`, `impactRecords`) are added by need or profile.

## Governance

- RFC for new profiles or breaking changes
- Version-controlled schema updates
- Compatibility review for core package changes
- Required vs recommended fields stated in Table Schema
- Public examples

## Versioning

Semantic versioning. Breaking core contract changes require a major version after 1.0. Until 1.0, minor versions may break.

## Licensing

- Schemas and specification: CC BY 4.0
- Reference tooling and validation code: MIT

## Status

Draft 0.2 direction. Intended to evolve through public review and a reference implementation (including a Camtrap-capable CMS exporter).
