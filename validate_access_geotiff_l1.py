# /// script
# requires-python = ">=3.12"
# dependencies = ["earthaccess>=0.15", "rioxarray>=0.15", "numpy>=2"]
# ///
# CI validation for access_geotiff_l1.py -- not published to the audience.
# Dependencies must match the snippet's, since runpy executes it in this interpreter.
# numpy is listed for ducs_validation itself, which asserts `data` is a numeric array;
# the snippet does not import it directly.
from ducs_validation import validate

validate("access_geotiff_l1.py")
