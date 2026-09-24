# Import required packages (pip install earthaccess xarray h5netcdf)
import earthaccess  # search and access NASA Earthdata
import xarray as xr  # load and analyze N-dimensional array data

# Authentication
earthaccess.login()  # log in with Earthdata credentials (prompts, or uses env vars/.netrc)

# Data search
data_doi = "10.5067/ATLAS/ATL03.007"  # ATL03 v7, specified by Digital Object Identifier (DOI)

results = earthaccess.search_data(
    doi=data_doi,  # search by dataset DOI
    temporal=("2025-01-01", "2025-12-31"),  # one-year temporal extent
    bounding_box=(-108.3, 38.9, -107.8, 39.1),  # small area over Grand Mesa, CO, USA
)
print(f"Granules found: {len(results)}")

# Data access
files = earthaccess.open(results[:1])  # stream the first granule without downloading it
dt = xr.open_datatree(files[0], engine="h5netcdf", phony_dims="access")  # open as a tree of groups

# Optional: download the first granule instead (ATL03 files are often several GB)
# downloaded_files = earthaccess.download(results[:1], local_path=".")
# dt = xr.open_datatree(downloaded_files[0], engine="h5netcdf", phony_dims="access")

# Inspect file contents
print(dt)

# Subset variables
photons = dt["gt1l/heights"].ds[["h_ph", "lat_ph", "lon_ph", "signal_conf_ph"]]  # photon height, lat, lon, and confidence flag from one beam

# Mean height of signal photons
conf = photons["signal_conf_ph"].isel({photons["signal_conf_ph"].dims[1]: 0})  # pick the land column (0) from the per-surface-type confidence scores, giving one score per photon
mean_height = photons["h_ph"].where(conf >= 3).mean().item()  # mean height of medium/high-confidence photons (conf >= 3)

print(f"Mean signal photon height along this beam: {mean_height:.1f} m")  # covers the full beam track in the granule, not just the bounding box