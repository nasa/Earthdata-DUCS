# /// script
# requires-python = ">=3.12"
# dependencies = ["earthaccess>=0.15", "pyhdf==0.11.7", "numpy>=2"]
# ///
# Data Use Code Snippet (DUCS): CALIPSO Lidar Level 1B -- along-track lidar profiles (HDF4)
# Collection: CAL_LID_L1-Standard-V4-51
# Landing page: https://www.earthdata.nasa.gov/data/catalog/larc-cloud-cal-lid-l1-standard-v4-51-v4-51
#
# This code snippet demonstrates common data access workflow steps including authentication,
# spatiotemporal search, data access, and data structure navigation.
#
# Note: this dataset is distributed in HDF4. HDF4 files cannot be streamed, so Step 3 downloads
# the granule instead of opening it in place, and Step 4 uses pyhdf instead of xarray.
#
# Run:  uv run access_profile_hdf4.py
#   or: pip install "earthaccess>=0.15" "pyhdf==0.11.7" "numpy>=2" && python access_profile_hdf4.py

# ----------------------------------------------
# Step 0: Environment Setup (Import Packages) |
# ---------------------------------------------
# Import Required Packages
import earthaccess  # searching for and accessing NASA Earthdata
import numpy as np  # working with the numeric arrays pyhdf returns
import pyhdf.VS  # noqa: F401 -- registers the vdata reader used in Step 4
from pyhdf.HDF import HDF  # reader for vdata tables (the altitude values)
from pyhdf.SD import SD, SDC  # reader for scientific datasets (the measurements)

# -------------------------
# Step 1: Authentication |
# ------------------------
# Authenticate using earthaccess and your Earthdata Login Account
# Note: If you do not have an Earthdata Login Account, you can create one at: urs.earthdata.nasa.gov
# Note: earthaccess will read your Earthdata Login from a .netrc file if available, and can also help
#       you set one up, otherwise you will be prompted for your username and password
if earthaccess.login(persist=True).authenticated:
    print("Authentication Completed")

# --------------------------------
# Step 2: Spatiotemporal Search |
# -------------------------------
# Use the earthaccess search_data function to search for granules in this collection using its DOI,
# for a defined temporal time period
# Note: CALIPSO stopped acquiring data in 2023, so the temporal range must fall within the mission
granules = earthaccess.search_data(
    doi="10.5067/CALIOP/CALIPSO/CAL_LID_L1-Standard-V4-51",
    temporal=("2023-06-15", "2023-06-16"),
)
print(f"Spatiotemporal search retrieved {len(granules)} granule(s)")

if not granules:
    raise SystemExit("No granules found -- try widening the temporal range")

# ----------------------
# Step 3: Data Access |
# ---------------------
# Use the earthaccess download function to download the first granule returned by the search above
# Note: most NASA datasets can be streamed with earthaccess.open(), but the HDF4 library can only
#       read from a file on disk, so this granule is downloaded first (~450 MB)
# Note: earthaccess skips the download if the file is already in the folder
print(f"Accessing Granule: {granules[0].data_links()[0]}")
paths = earthaccess.download(granules[0:1], local_path="./data")
granule = str(paths[0])
print(f"Downloaded to: {granule}")

# ------------------------------------
# Step 4: Data Structure Navigation |
# -----------------------------------
# Open the downloaded file and list the variables (called "scientific datasets" in HDF4)
sd = SD(granule, SDC.READ)
variables = sd.datasets()
print(f"\nFile contains {len(variables)} variables, including:")
for name in sorted(variables)[:10]:
    print(f"  {name}: shape={variables[name][1]}")

# Variable Subsetting: Select the 532 nm backscatter variable and read the first 1000 profiles
# Note: the full variable is ~130 MB, so this reads a slice instead of the whole array
sds = sd.select("Total_Attenuated_Backscatter_532")
attributes = sds.attributes()
backscatter = sds[:1000, :]
latitude = sd.select("Latitude")[:1000, 0]
print(f"\nSelected Total_Attenuated_Backscatter_532 with shape {backscatter.shape}")
print(f"  (1000 profiles along the ground track x {backscatter.shape[1]} altitudes per profile)")
print(f"  latitude span: {latitude.min():.2f} to {latitude.max():.2f} degrees North")

# The altitude values are not stored as a variable -- they live in a separate HDF4 structure
# called a vdata table, which needs the second reader imported in Step 0
hdf = HDF(granule)
vs = hdf.vstart()
vd = vs.attach(vs.find("metadata"))
vd.setfields("Lidar_Data_Altitudes")
altitudes = np.array(vd.read(nRec=1)[0][0])
vd.detach()
vs.end()
hdf.close()
print(
    f"\nAltitudes for the vertical axis: {altitudes.size} values, "
    f"{altitudes.min():.2f} to {altitudes.max():.2f} km"
)

# Replace the fill value with "not a number" so it is excluded from the statistics below
fill_value = attributes.get("fillvalue", attributes.get("_FillValue"))
data = np.where(backscatter == fill_value, np.nan, backscatter)
units = attributes.get("units", "")
print(f"\nThe mean value in this variable is: {np.nanmean(data):.3e} {units}")
print(f"The median value in this variable is: {np.nanmedian(data):.3e} {units}")

sd.end()

# ------------------------------
# Step 5: Additional Resources |
# ------------------------------
# Earthdata Cloud Cookbook:  https://nasa-openscapes.github.io/earthdata-cloud-cookbook/
# earthaccess documentation: https://earthaccess.readthedocs.io/
# pyhdf documentation:       https://pyhdf.readthedocs.io/
