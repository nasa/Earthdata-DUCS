# Step 2: Spatiotemporal Search

The second step of every snippet finds the **granules** (files) within the data collection, filtered by a time window and an area of interest. The step uses [`earthaccess.search_data()`](https://earthaccess.readthedocs.io/en/latest/user-reference/api/api/#earthaccess.api.search_data).

## Background: Data Collection and Granules in CMR
- *Data collection* is usually defined by a data `version` (e.g., "003"), digital object identifier or `doi` value (e.g., "10.5067/GEDI/GEDI02_A.003"), `short_name` (e.g., "GEDI02_A"), and a `concept ID`. In NASA CMR, concept id is in the format `<concept-type-prefix> <unique-number> "-" <provider-id>` (e.g., C3974616071-LPCLOUD)
- A data collection is made of at least one but usually many *granules*. Each granules are have spatial and temporal extents defined in one of the following ways.
    -  `TemporalExtent` are defined in terms of `RangeDateTime` or `SingleDateTime`
    -  `SpatialExtent` are usually defined in horizontal spatial geometry, which can be `Points`, `BoundingRectangles`, `GPolygons`, or `Lines`.

## Generic Code

Values in `{{ }}` are filled in for each collection. The rest of the block, comments included, is the same for every collection.

```python
# ---------------------------------------------------------------------------
# Search for granules by time and location
# ---------------------------------------------------------------------------
# Collection: {{ entry_title }}, version {{ version }}, or 
# DOI: https://doi.org/{{ doi }}
#
# earthaccess.search_data() returns granules in one collection that 
# match all of the filters below.
granules = earthaccess.search_data(
    # dataset doi
    doi="{{ doi }}",
    # Time window as (start, end). Dates are ISO 8601 and both ends are
    # inclusive; an end date with no time of day includes the whole day.
    temporal=("{{ start_date }}", "{{ end_date }}"),
    # Area of interest as (west, south, east, north) in decimal degrees,
    # longitude first. This selects granules that overlap the box
    bounding_box=({{west}}, {{south}}, {{east}}, {{north}}),
    # Return at most 20 granules, so a broad search doesn't list thousands of files
    count=20,
)

# print error if nothing matched
print(f"Spatiotemporal search retrieved {len(granules)} granule(s)")

if not granules:
    raise RuntimeError(
        "No granules matched this search. Try a wider time window or bounding "
        "box, and check that both fall within the collection's coverage."
    )
```

`import earthaccess` and `earthaccess.login()` come from [Step 1: Authentication](STEP-1-authentication.md).

### Worked example (HLSL30 v2.0)

This is the template filled in for [Harmonized Landsat Sentinel-2 surface reflectance (HLSL30)](https://doi.org/10.5067/HLS/HLSL30.002). It returns 8 granules, which was checked against CMR on 2026-10-28.

```python
# ---------------------------------------------------------------------------
# Search for granules by time and location
# ---------------------------------------------------------------------------
# Collection: HLS Landsat Operational Land Imager Surface Reflectance and 
#             TOA Brightness Daily Global 30m v2.0
# DOI: https://doi.org/10.5067/HLS/HLSL30.002
#
# earthaccess.search_data() returns granules in one collection that 
# match all of the filters below.
granules = earthaccess.search_data(
    # dataset doi
    doi="10.5067/HLS/HLSL30.002",
    # Time window as (start, end). Dates are ISO 8601 and both ends are
    # inclusive; an end date with no time of day includes the whole day.
    temporal=("2025-07-01", "2025-07-31"),
    # Area of interest as (west, south, east, north) in decimal degrees,
    # longitude first. This selects granules that overlap the box
    bounding_box=(-122.097, 39.892, -122.035, 39.923),
    # Return at most 20 granules, so a broad search can't list thousands of files
    count=20,
)

print(f"Spatiotemporal search retrieved {len(granules)} granule(s)")

# print error if nothing matched
if not granules:
    raise RuntimeError(
        "No granules matched this search. Try a wider time window or bounding "
        "box, and check that both fall within the collection's coverage."
    )
```

## Alternative ways to query

These are for collections where the default pattern doesn't fit.

### Choosing a collection identifier

- **DOI:** e.g., `doi="10.5067/HLS/HLSL30.002"`.  `earthaccess` resolves it to a concept ID and uses the first collection CMR returns. To be used only when the DOI maps to exactly one collection. Not every collection has a DOI.
- **short_name + version:** e.g.,  `short_name="HLSL30", version="2.0"`. Always pass `version`, e.g.,  `short_name="MOD09GA"` alone matches both `061` (LPCLOUD) and `6.1NRT` (LANCEMODIS). Add `provider=` if the same short name and version exist at more than one provider.
- **concept_id:** e.g., `concept_id="C2021957657-LPCLOUD"`. Use it as the fallback when neither of the others resolves to exactly one collection.

### Spatial filters

All coordinates are **longitude first** and in counter-clockwise order for polygons.

```python
bounding_box = (west, south, east, north)  # rectangle (default)
point = (lon, lat)  # granules containing a point
circle = (lon, lat, radius_m)  # radius 10 m to 6,000 km; center not at a pole
polygon = [(lon1, lat1), (lon2, lat2), ..., (lon1, lat1)]  # counter-clockwise, closed
line = [(lon1, lat1), (lon2, lat2), ...]  # e.g. a ship track or flight path
```

### Temporal filters

```python
temporal = ("2025-07-01", "2025-07-31")  # date range (default)
temporal = ("2025-07-13", "2025-07-13")  # one whole day
temporal = ("2025-07-13T10:00:00Z", "2025-07-13T14:00:00Z")  # a few hours
```

### Recurring timeframe
`search_data()` takes only one range, but the `DataGranules` query builder combines repeated `.temporal()` calls

```python
query = earthaccess.DataGranules().doi("10.5067/HLS/HLSL30.002")
query = query.bounding_box(-122.097, 39.892, -122.035, 39.923)
# Four years from 2023-2026
for year in range(2023, 2026):
    # July 1-10 of each year
    query = query.temporal(f"{year}-07-01", f"{year}-07-10")
granules = query.get(20)
```

### Valid temporal range

- The temporal range must fall inside one of the `TemporalExtents[].RangeDateTimes[]` ranges. A collection can have several ranges with gaps between them.
- If the collection only has `SingleDateTimes`, use one of those dates.
- For active collections (`EndsAtPresentFlag: true`), end the window at least a few weeks before today, because recent granules may not be ingested yet.

The **temporal range length** should scaled to how often granules are produced. Use the `TemporalResolution` value if it is set. Otherwise infer the cadence from the processing level and the collection description, e.g, a monthly level 3 dataset must have at least 1 month of temporal range.

### Valid bounding box

- If `GranuleSpatialRepresentation` is `NO_SPATIAL`, omit the spatial query and only do temporal query.
- The box must overlap the collection's `BoundingRectangles` or `GPolygons`. It must have west < east and south < north, and it must not cross the antimeridian.
- A global collection extent does not mean every granule is global. e.g., HLSL30 is a global dataset but its granules are divided into smaller tiles. Spatial query can be omitted when each granule covers the globe, as with as with gridded global L3/L4 products like SMAP or MERRA-2.

We can have the AI pipeline choose a small location where the variable is meaningful, e.g., ocean for sea surface temperature or snow or ice for cryosphere products. A box a few kilometers to tens of kilometers across, so that it falls inside one tile or a few swaths.

### Granule Counts

The template caps results with `count=20`. The AI pipeline should check the real match count before generating the rest of the snippet using `hits()`.

```python
hits = (
    earthaccess.DataGranules()
    .concept_id(concept_id)
    .temporal(start, end)
    .bounding_box(*bbox)
    .hits()
)
```

If **0 hits**,  widen the time range first, then the spatial bounding box. If **1 to 20 hits**, accept the query.If **more than 20 hits**, narrow the time range first, then the spatial bounding box. 