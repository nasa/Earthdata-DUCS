"""Generic DUCS snippet validation: did the access workflow actually work?

Shared by every DUCS validator. Deliberately dataset-agnostic: asserts only that the
snippet ran to completion and produced real numbers. Product-specific expectations
(grid sizes, variable names, value ranges) are intentionally NOT checked here -- they
change on reprocessing and turn into false CI failures.

Contract: every DUCS snippet assigns the array it read to a variable named `data`.

Run validators from the repository root; snippet paths are resolved relative to the
current working directory.
"""

import runpy

import numpy as np


def validate(snippet: str) -> None:
    ns = runpy.run_path(snippet)  # 1. snippet runs end to end, or this raises

    if "data" not in ns:
        raise SystemExit(f"FAIL  {snippet} must assign what it read to `data`")

    try:
        values = np.asarray(ns["data"], dtype="float64")
    except (TypeError, ValueError) as err:
        raise SystemExit(f"FAIL  {snippet} `data` is not a numeric array: {err}") from err

    checks = {
        "snippet ran to completion": True,  # reaching this line proves it
        "data array is not empty": values.size > 0,
        "data contains finite values (not all fill)": bool(np.isfinite(values).any()),
    }
    for label, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}  {label}")

    failed = [label for label, passed in checks.items() if not passed]
    if failed:
        raise SystemExit(f"\nValidation failed: {'; '.join(failed)}")
    print(f"\nValidation passed: {snippet} accessed real data")
