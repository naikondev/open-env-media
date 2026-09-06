# STAC and EMDP

[STAC](https://stacspec.org/) (SpatioTemporal Asset Catalog) standardizes how geospatial asset metadata is structured and queried. It is backed by NASA, Radiant Earth, OGC, and a large industry coalition. This document describes how the two standards relate.

STAC and EMDP solve different problems. They can be used together.

## Difference

STAC catalogs assets so they can be discovered and fetched.
EMDP packages interpreted field evidence from a survey so it can be validated, archived, and cited.

The split is the same kind used elsewhere: Camtrap DP versus a Darwin Core Archive, or a STAC Collection versus an ISO 19115 record. One object is for search. The other is a closed, relational dataset.

| | STAC | EMDP |
| --- | --- | --- |
| Unit of exchange | Catalog → Collection → Item → Asset | One Data Package (a zip) |
| Grain | One spatiotemporal asset (scene, clip, cloud) | One survey: visits, files, assertions, facts |
| Job | Structure and query geospatial asset metadata | Archive a Camtrap-shaped evidence graph |
| Typical consumer | STAC API, cloud EO pipelines, QGIS | Domain archive, CMS exporter, citation |
| Semantics prescribed | Place, time, asset, plus optional extensions | Deployment, observation, measurement, join |
| What “measurement” means | Properties on an Item or Asset | A row in `measurements` with a required parent |

STAC defines a spatiotemporal asset as a file about the Earth at a place and time. The original focus was satellite scenes; the spec now also covers drones, video, point clouds, labels, and composites. The model stays asset-centric. Surveys, visits, assertions, facts, and joins are EMDP tables.

## STAC extensions add Item fields

A STAC extension adds fields to an Item, Collection, or Asset. That fits when the object is still one file at one footprint and datetime.

EMDP’s object is a closed package:

```text
deployment (visit or station)
  ├── measurement          # logger; no photograph required
  └── media
        ├── alignment      # corresponding-scene pair
        └── observation    # assertion (algal bloom, canopy loss)
              ├── measurement
              └── contextJoin   # OpenAQ / ERA5 / a STAC Item
```

Foreign keys, required resource sets, and package-level validation live in EMDP tables. Hanging `emdp:condition` and `emdp:secchiDepth` on a STAC Item would rewrite that contract in GeoJSON and drop the Camtrap DP dual-export path.

Three mismatches:

1. **Query vs deposit.** STAC (and STAC API) searches large holdings. EMDP validates one deposit: exactly one `deployments`, `media`, and `observations` table, then optional facts.
2. **Assertion, fact, and join are separate tables.** STAC can carry derived values (EO, raster, classification extensions). EMDP requires `condition = algal bloom`, `chlorophyllA = 42`, and a Sentinel-5P NO₂ join to be different kinds of row.
3. **Existing exporters already emit tables.** Platforms that ship Camtrap DP already have `survey → deployment → media → observation`. EMDP is the second zip from that graph. A STAC extension would be a third egress for the same field work.

## What each standard should do

| Work | Standard |
| --- | --- |
| Index Sentinel, NAIP, drone orthomosaics, point clouds for search | STAC |
| Publish a shoreline survey with photos, Secchi, and a logger | EMDP |
| Publish camera-trap taxon records | Camtrap DP |
| Point an EMDP observation at a Copernicus granule | EMDP `contextJoins` (the join may cite a STAC Item URI) |
| List an EMDP zip as a downloadable asset | STAC Item/Collection linking to the package |

`contextJoins` store the retrieved value and its source. The remote object may be a STAC Item. Copernicus archives and STAC catalogs stay where they are.

## Coexistence

Expected:

- `contextJoins.sourceURI` or `datasetID` points at a STAC Item, Collection, or API search.
- A STAC Collection lists an EMDP package (`datapackage.json` or the zip) as an asset with a documented media type.
- The same photograph can be a STAC Item (discovery) and an EMDP `media` row (survey graph). Those are two descriptions of one file.

Claims that are out of scope:

- EMDP as a STAC replacement
- A ban on field photos in STAC
- A STAC extension of EMDP properties as the interchange format

A later RFC may add a STAC encoding of an EMDP package (Items generated from `media` rows, with a link back to the zip). That would be an adapter. The Table Schema contract remains the interchange format.

## Related reading

- [STAC specification](https://github.com/radiantearth/stac-spec)
- [Camtrap DP and EMDP](CAMTRAP-CROSSWALK.md): same graph, different payload
- [EMDP evidence model](MODEL.md)
