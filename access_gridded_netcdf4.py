# Access gridded NetCDF4 data
#
# 9/11/2026 JRS
# Performs the four DUCS workflow steps for a MERRA-2 collection

import earthaccess
import xarray as xr

shortname = "M2I3NPASM"
version = "5.12.4"

# EDL auth using earthaccess
auth = earthaccess.login()

# Data search using earthaccess
results = earthaccess.search_data(
    short_name = shortname,
    version = version,
    temporal = ('2025-07-01', '2025-07-04'), # This will stream one granule, but can be edited for a longer temporal extent
    bounding_box = (-99.85886, 29.78140, -98.91769, 30.29064)
)

# Data access
fs = earthaccess.open(results) # Extracts URLs from the results variable
ds = xr.open_mfdataset(fs) # Open granules in xarray

# File structure navigation
print(ds)
