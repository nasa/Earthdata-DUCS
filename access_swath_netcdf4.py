# Access swath NetCDF4 data (script)
#
#
#
#
#

# 9/17/2026 EB


import earthaccess
import xarray as xr


# For VJ102IMG.021 the geolocation data is also required to work with the data
# Define Search Parameters for both VJ102IMG.021 Radiance and VJ103IMG.021 Geolocation
doi = "10.5067/VIIRS/VJ102IMG.021"
geo_doi = "10.5067/VIIRS/VJ103IMG.021"
# Temporal Range
temporal = ('2026-09-06T20:00:00', '2026-09-07T21:00:00')
# Bounding Box (LL Lon, LL Lat, UR Lon, UR Lat)
bounding_box = (-116.43, 32.67, -114.96, 34.02)

# EDL auth using earthaccess
auth = earthaccess.login()
print("Authenticated with Earthdata Login credentials")

# Data search using earthaccess
print(f"Searching for {doi} radiance granules with earthaccess...")
results = earthaccess.search_data(
    doi = doi,
    temporal = temporal,
    bounding_box = bounding_box,
)

print(f"Searching for matching {geo_doi} geolocation granules with earthaccess...")
geo_results = earthaccess.search_data(
    doi = geo_doi,
    temporal = temporal,
    bounding_box = bounding_box,
)
print(f"{doi} Radiance granules found: {len(results)} \n"
    f"{geo_doi} Geolocation granules found: {len(geo_results)}")

rad_fs = earthaccess.open(results)
geo_fs = earthaccess.open(geo_results)

# Radiance/reflectance bands live under the "observation_data" group
rad_dt = xr.open_datatree(rad_fs[0], engine="h5netcdf")
print("Opened L1B swath NetCDF4 'observation_data' group in xarray")

# Latitude/longitude/geometry live in the companion product's "geolocation_data" group
geo_dt = xr.open_datatree(geo_fs[0], engine="h5netcdf")
print("Opened companion VJ103IMG 'geolocation_data' group in xarray")

# File structure navigation
print(rad_dt)
print(geo_dt)

# Select a radiance/reflectance band from the "observation_data" group
var_name = "I01"
da = rad_dt["observation_data"][var_name]

# Assign latitude/longitude coordinates from the companion geolocation product
da = da.assign_coords(
    latitude=geo_dt["geolocation_data"]["latitude"],
    longitude=geo_dt["geolocation_data"]["longitude"],
)

print(da)
