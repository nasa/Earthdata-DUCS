# /// script
# requires-python = ">=3.12"
# dependencies = ["earthaccess>=0.15", "xarray>=2024.10", "dask[array]", "h5netcdf>=1.4", "h5py", "numpy>=2"]
# ///
# CI validation for access_gridded_netcdf4.py -- not published to the audience.
# Dependencies must match the snippet's, since runpy executes it in this interpreter.
# numpy is listed for ducs_validation itself, which asserts `data` is a numeric array;
# the snippet does not import it directly.
# xarray>=2024.10 is the floor for open_datatree. dask is required by open_mfdataset.
# netcdf4 and bottleneck are deliberately absent: the snippet pins engine="h5netcdf",
# and it performs no xarray reduction for bottleneck to accelerate.
from ducs_validation import validate

validate("access_gridded_netcdf4.py")
