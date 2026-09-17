# Access scripts
#
# 9/16/2026 JRS
# Contains format-specific data access functions based on example data access scripts

import earthaccess
import xarray as xr


def access_netcdf(conceptID, umm_metadata):

    # Get temporal, spatial extent, and variable names, if possible, to plug in below
    start_date = "2025-07-01"
    end_date = "2025-07-01"
    lon1 = -99.85886
    lon2 = -98.91769
    lat1 = 29.78140
    lat2 = 30.29064

    # EDL auth using earthaccess
    auth = earthaccess.login()
    print("Authenticated with Earthdata Login credentials")

    # Data search using earthaccess
    print("Searching for granules with earthaccess...")
    results = earthaccess.search_data(
        concept_id=conceptID,
        temporal=(start_date, end_date),
        bounding_box=(lon1, lat1, lon2, lat2),
    )

    # Data access
    fs = earthaccess.open(results)  # Extracts URLs from the results variable
    ds = xr.open_mfdataset(fs)  # Open granules in xarray

    # File structure navigation
    print(ds)

    return {"status": "success", "auth": auth}
