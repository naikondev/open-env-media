# EMDP Charter

## Mission

EMDP is a portable evidence package for environmental media outside the wildlife-tracking stack. It binds media to place, time, assertions, measurements, and optional joins to external datasets.

Wildlife occurrence data already has Camtrap DP and Darwin Core. Geospatial asset catalogs already have [STAC](https://stacspec.org/). EMDP follows the Camtrap package graph for interpreted field evidence. See `docs/STAC.md`.

## Scope

In scope:

- repeat photography and other corresponding-scene media
- water-quality and hydrological documentation
- air-quality and atmospheric hazard documentation
- dark-sky and light-pollution assessments
- climate-extreme and disturbance documentation
- restoration and intervention records recorded as observed conditions
- optional funding-attribution records (CMS profile only)

Out of scope:

- taxon occurrences, camera-trap animal classifications, or a GBIF competitor
- replacing STAC or cataloging Earth-observation archives for search
- storing satellite archives, climate model cubes, or station networks
- specifying computer-vision or alignment algorithms
- treating allocation or donation records as proof of ecological success
- defining EMDP's identity in terms of commerce or impact

## Goals

- A predictable, validatable package that follows the Camtrap DP graph
- A reference validator (`emdp validate`) so packages can be checked with a tool
- A measurement table for quantitative and coded environmental facts
- Domain profiles that keep the core package contract intact
- Privacy and embargo fields that remain validatable
- A governance process suitable for open scientific and conservation data

## Principles

1. **Open by default**
2. **Package-first.** The profile requires `deployments`, `media`, and `observations` exactly once.
3. **Follow the Camtrap graph; keep Camtrap observation semantics in Camtrap DP**
4. **Catalog assets with STAC; deposit survey evidence with EMDP; join the two.**
5. **Assertion, fact, and join stay separate**
6. **Extensible by profile.** Vocabularies and optional resources, one core.
7. **Temporal and spatial integrity**, including the right to withhold coordinates
8. **Store joins; leave remote archives in place**
9. **Compatible with Data Package / Table Schema conventions**
10. **The `attribution` profile is optional and outside the core.**

## Package model

Minimum compliant package:

- `datapackage.json` using the EMDP profile, with a canonical `id`
- exactly one `deployments`, `media`, and `observations` resource
- declared `project`, `spatial`, and `temporal` metadata

Optional resources (`measurements`, `alignments`, `contextJoins`, `attributionRecords`) are added by need or profile.

## Governance

- RFC for new profiles or breaking changes
- Version-controlled schema updates
- Compatibility review for core package changes
- Required vs recommended fields stated in Table Schema
- Public examples and negative fixtures
- CI must reject invalid packages via the reference CLI

## Versioning

Semantic versioning. Breaking core contract changes require a major version after 1.0. Until 1.0, minor versions may break.

## Licensing

- Schemas and specification: CC BY 4.0
- Reference tooling and validation code: MIT

## Status

Draft 0.3. Intended to evolve through public review and a reference implementation (including a Camtrap-capable CMS exporter).
