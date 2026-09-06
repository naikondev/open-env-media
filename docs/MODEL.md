# EMDP evidence model

EMDP is a portable evidence package: media bound to deployments, assertions, measurements, external context, and optional funding provenance.

```text
                         PACKAGE (id)
                              |
                    +---------+---------+
                    |                   |
                  MEDIA            DEPLOYMENT
                    |                   |
                    +---------+---------+
                              |
                         OBSERVATION
                         (assertion)
                              |
                 +------------+------------+
                 |                         |
           MEASUREMENT               CONTEXT JOIN
           (fact)                    (external fact)

Measurements may also hang directly off a deployment or media file.

ALIGNMENT connects media to media.
ATTRIBUTION (CMS profile only) connects an economic action to evidence.
```

## Three kinds of claim

| Object | Meaning | Example |
| --- | --- | --- |
| **Observation** | An assertion or interpretation | `condition = algal bloom` |
| **Measurement** | A quantified or coded fact | `chlorophyllA = 42` `ug/L` |
| **Context join** | A fact retrieved from an external dataset | OpenAQ PM2.5 at this place and hour |

Keep these as separate rows. A qualitative label, an in-situ concentration, and a satellite pixel are different kinds of claim.

Classification audit fields (`classificationMethod`, `classifiedBy`, `classificationProbability`) and bounding boxes on observations record how the assertion was produced or localized.

## Measurements can hang off a deployment or media file

A logger on a deployment may record temperature with no photograph-derived claim:

```text
deployment
  ├── measurement (pH, in situ)
  ├── measurement (waterTemperature, in situ)
  └── media
        └── observation (algal bloom)
              └── measurement (secchiDepth)
```

A measurement MUST reference at least one of `deploymentID`, `observationID`, or `mediaID`.

`measurementValue` is a string, following Darwin Core MeasurementOrFact. Consumers MUST interpret type from `measurementType`, `measurementUnit`, and `measurementScheme`.

## Alignments

An alignment is a geometric relationship between two media resources of the same or corresponding scene. Repeat photography (`rpdp`) is the common profile. Restoration pairs, shoreline series, and drone-to-drone registration use the same table.

## Attribution lives in an optional profile

`attributionRecords` live in the `attribution` profile. They connect an economic action to activity and evidence. `status` is the allocation state. Scientists validating the core may ignore this profile.

## Identifiers

| Level | Field | Role |
| --- | --- | --- |
| Package | `datapackage.json` `id` | Canonical package identifier. Prefer a URI. |
| Package | `homepage` | Optional resolvable landing page |
| Row | `deploymentID`, `mediaID`, … | Local, unique within the package |

A global handle MAY be formed as `{package.id}/{resource}/{localID}`, for example `urn:emdp:example-north-basin/observations/obs1`. Platforms that re-export the same evidence SHOULD keep `id` stable across revisions and bump `version`.

## Privacy and rights

| Concern | Where |
| --- | --- |
| Location | `spatialPrivacy`, `coordinateUncertainty`, `embargoUntil` on deployments |
| File access | `media.filePublic`, `media.embargoUntil` |
| Reuse | `licenses` with `scope` `data` and `media` |

Withholding coordinates is recorded as `spatialPrivacy=withheld`. Empty latitude and longitude are valid in that state.

## Adjacent standards

| Standard | Role relative to this model |
| --- | --- |
| Camtrap DP | Same graph; observation is a taxon record |
| STAC | Catalogs the file or a satellite granule behind a join |

A STAC Item may describe the same photograph or the granule behind a `contextJoin`. The survey graph stays in the EMDP package. See `docs/STAC.md`.
