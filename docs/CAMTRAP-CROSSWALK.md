# Camtrap DP ↔ EMDP crosswalk

ArtInStack and similar CMS tools already model survey → deployment → media → observation and export [Camtrap DP](https://camtrap-dp.tdwg.org/) for GBIF. EMDP follows that package graph with environmental assertions, measurements, and optional joins. Wildlife observations stay in Camtrap DP.

## Two packages from one survey

If a survey contains both a fox and an algal bloom:

| Observation | Export |
| --- | --- |
| Taxon, count, sex, life stage, behavior | Camtrap DP `observations.csv` |
| Water condition, Secchi depth, SST join | EMDP `observations.csv` + `measurements.csv` |

Keep `scientificName` in Camtrap DP. Keep `secchiDepth` in EMDP. Two zips from one survey is the intended ArtInStack shape.

## Shared columns

Reuse names and types so one exporter can fill both packages.

| Concept | Camtrap DP | EMDP |
| --- | --- | --- |
| Placement / visit | `deployments.deploymentID` | same |
| Place | `locationID`, `locationName` | same |
| Coordinates | `latitude`, `longitude`, `coordinateUncertainty` | same, plus `spatialPrivacy`, `embargoUntil` |
| Aiming | `cameraHeading`, `cameraTilt` | same, plus `cameraRoll`, `focalLength`, `fixedPoint` |
| File | `mediaID`, `deploymentID`, `timestamp`, `filePath`, `filePublic`, `fileMediatype` | same |
| Classification audit | `classificationMethod`, `classifiedBy`, `classificationProbability` | same |
| Observation grain | `observationLevel` = `media` \| `event` | same |

## Divergent columns

| Camtrap DP | EMDP |
| --- | --- |
| `observationType`: animal, human, blank, … | `observationType`: landCover, waterQuality, airQuality, … |
| `scientificName`, `count`, `lifeStage`, `sex`, `behavior`, `individualID` | `condition` + `measurements` |
| `project.taxonomic` | omitted |
| `project.individualAnimals` | omitted |
| `captureMethod`: activityDetection, timeLapse | handheld, fixedPoint, aerial, underwater, … |

## Suggested CMS mapping (ArtInStack)

Keep the current bio-asset objects. Add an observation domain (wildlife vs environmental) on the existing DAM.

| Platform object | Camtrap DP | EMDP |
| --- | --- | --- |
| `conservation_projects` | `package.project` | `package.project` |
| `conservation_deployments` | `deployments` | `deployments` (`fixedPoint` for repeat-photo stakes) |
| `media` + `geo_*` | `media` | `media` (apply the same spatial resolver / embargo) |
| `media_observations` with taxon | `observations` | skip |
| `media_observations` with environmental type | skip | `observations` |
| New: measurement rows | | `measurements` |
| New: dataset joins at ingest | | `contextJoins` |
| Attribution / allocation rows | | `attributionRecords` (`attribution` profile only) |

Spatial governance already applied to Camtrap/GBIF (`coordinateUncertainty`, omit, embargo) should run on EMDP with the same resolver. `spatialPrivacy=withheld` means published coordinates are omitted.

## What not to build in the standard

These are CMS features. Persist their results as measurements, alignments, or joins:

- CoralNet / habitat CV pipelines → `measurements` (`liveCoralCover`, `imageDerived`)
- Sentinel-5P or OpenAQ overlays → `contextJoins`
- Repeat-photo auto-align → `alignments.transform`
- ERA5 “30-year deficit” copy → `contextJoins` + optional `precipAnomaly` measurement

## Validation

A dual exporter can validate Camtrap packages against the TDWG profile and EMDP packages against `schemas/core/emdp-profile.json` independently. Sharing a zip or a `resources` array between the two profiles will fail validation. Keep the bundles separate.

For Earth-observation catalogs (STAC), see `docs/STAC.md`. Keep Camtrap DP, EMDP, and STAC as separate egress formats.
