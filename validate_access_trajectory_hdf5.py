# /// script
# requires-python = ">=3.12"
# dependencies = ["earthaccess>=0.15", "xarray>=2024.10", "h5netcdf>=1.4", "h5py", "numpy>=2"]
# ///
# CI validation for access_trajectory_hdf5.py -- not published to the audience.
# Dependencies must match the snippet's, since runpy executes it in this interpreter.
# numpy is listed for ducs_validation itself, which asserts `data` is a numeric array;
# the snippet does not import it directly.
# xarray>=2024.10 is the floor for open_datatree; h5py is separate because h5netcdf
# made it an optional extra in 1.8.0.
from ducs_validation import validate

validate("access_trajectory_hdf5.py")
