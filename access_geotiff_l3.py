# Access GeoTIFF data (script)
#
# 9/21/2026 RS
# Performs the four DUCS workflow steps for the HLSL30 collection, which are level-3 data stored in cloud optimized GeoTIFF

import earthaccess
import rioxarray as rxr


# EDL auth using earthaccess
auth = earthaccess.login()
print("Authenticated with Earthdata Login credentials")

# Data search using earthaccess
print("Searching for granules with earthaccess...")
results = earthaccess.search_data(
    doi="10.5067/HLS/HLSL30.002",
    temporal=("2025-07-13", "2025-07-13"),
    bounding_box= (-122.09684570249401,39.89193960036616,-122.03465069273044,39.92326328372664)
)
print(f"Total granules found: {len(results)}")

# Data access
fs = earthaccess.open(results)  # Extracts URLs from the results variable

# Open the first granule with rioxarray open_rasterio
dt = rxr.open_rasterio(fs[0], masked=True).squeeze('band', drop=True)
print(dt)