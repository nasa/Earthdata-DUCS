# Access gridded NetCDF4 data (script)
#
# 9/11/2026 JRS
# Performs the four DUCS workflow steps for the M2I3NPASM MERRA-2 collection, which are gridded data stored in daily NetCDF4 granules

import earthaccess
import xarray as xr

shortname = "M2I3NPASM"
version = "5.12.4"

# EDL auth using earthaccess
auth = earthaccess.login()
print("Authenticated with Earthdata Login credentials")

# Data search using earthaccess
print("Searching for granules with earthaccess...")
results = earthaccess.search_data(
    short_name=shortname,
    version=version,
    temporal=("2025-07-01", "2025-07-01"),
    bounding_box=(-99.85886, 29.78140, -98.91769, 30.29064),
)

# Data access
fs = earthaccess.open(results)  # Extracts URLs from the results variable
ds = xr.open_mfdataset(fs, engine="h5netcdf")  # Open granules in xarray
# Note: engine is explicit so the backend does not depend on which libraries happen to be
#       installed -- h5netcdf is the one that can read the file-like objects earthaccess returns
print("Opened L3/L4 NetCDF4 dataset in xarray")

# File structure navigation
print(ds)

print("\n--- Data Variables ---")
# List all the physical variables (e.g., Temperature, Wind, etc.) available in the file
for var_name in ds.data_vars:
    print(f"{var_name}: {ds[var_name].attrs.get('long_name', 'No long name')}")

print("\n--- Coordinates ---")
# List the axes (e.g., lat, lon, lev, time)
print(list(ds.coords.keys()))

# Example: Accessing a specific variable's structure (e.g., Air Temperature 'T' or Specific Humidity 'QV')
print("\n--- Structure of Temperature (T) ---")
temperature = ds["T"]
print(temperature)

# The array read from the granule.
# Note: the bounding_box above filters which *granules* match -- it does not subset them, so
#       MERRA-2 granules are still the full global grid (8 x 42 x 361 x 576, ~279 MB). One
#       time step and one level is a real read of the data without pulling the whole variable.
data = temperature.isel(time=0, lev=0)
