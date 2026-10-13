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

## Validation (external to snippet)

- snippet runs to completion
- snippet produces real numbers (stored in a variable named `data`)
  - numeric check is performed on unmasked/unfiltered data (to avoid depending on any science thresholds or analytic manipulations)

# Out of scope:

- Visualization or plotting
<<<<<<< HEAD
=======

# CRITICAL INSTRUCTIONS:
- Return ONLY valid, executable Python code.
- DO NOT wrap the code in markdown tags (do not use ``` or ```python).
- DO NOT include any conversational text, preambles, or explanations.
- Your entire output will be piped directly into a .py file and executed.
>>>>>>> 7b80c51 (added snippet generation pipeline.py)
