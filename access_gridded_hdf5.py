# Access gridded HDF5 data (script)
#
# 9/17/2026 RS
# Performs the four DUCS workflow steps for the SPL3SMP_E collection, which are gridded data stored in daily HDF5 granules

import earthaccess
import xarray as xr

shortname = "SPL3SMP_E"
version = "006"

# EDL auth using earthaccess
auth = earthaccess.login()
print("Authenticated with Earthdata Login credentials")

# Data search using earthaccess
print("Searching for granules with earthaccess...")
results = earthaccess.search_data(
    short_name=shortname,
    version=version,
    temporal=("2025-07-01", "2025-07-01"),
)
print(f"Total granules found: {len(results)}")

# Data access
fs = earthaccess.open(results)  # Extracts URLs from the results variable
# Open the first granule with xarray datatree 
# since SPL3SMP_E has hierarchical groupings
dt = xr.open_datatree(fs[0])  
print("Opened L3 dataset in xarray")

# File structure navigation
print(dt)

# Example: Accessing a specific variable's structure (e.g., soil moisture for the AM pass)
print("\n--- Soil Moisture Data Structure AM ---")
ds_am = dt.Soil_Moisture_Retrieval_Data_AM
# Assign coordinates 
ds_am = ds_am.assign_coords(
    lat=ds_am.latitude,
    lon=ds_am.longitude
)
print(ds_am.soil_moisture)
