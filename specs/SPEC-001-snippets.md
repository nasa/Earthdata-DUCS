# Initial draft snippet specs

## Authentication

### Requirements

- include generic inline comments describing code
- print a successful authentication

### Template
```python
if earthaccess.login(persist=True).authenticated:
    print("Authentication Completed")
```

## Spatiotemporal Search

### Requirements

- simple spatial bounding box for any collection that isn't global
- simple temporal range within the collections' time range
- use most recent granule?

### Template
```python
granules = earthaccess.search_data(
    doi="<collection doi>",
    temporal=("<start date>", "<end date>"),
    bounding_box=[<coordinates of bounding box>]
)
print(f"Spatiotemporal search retrieved {len(granules)} granule(s)")
```

## Data Access

- variable subsetting - pick out a meaningful variable
- show a mean/median, comment explaining lacking of quality filtering

## Dataset Structure Navigation
-

# Out of scope:

- Visualization or plotting
