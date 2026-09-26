# /// script
# requires-python = ">=3.12"
# dependencies = ["earthaccess>=0.15", "pyhdf==0.11.7", "numpy>=2"]
# ///
# CI validation for access_profile_hdf4.py -- not published to the audience.
# Dependencies must match the snippet's, since runpy executes it in this interpreter.
from pathlib import Path

from ducs_validation import validate

validate(str(Path(__file__).with_name("access_profile_hdf4.py")))
