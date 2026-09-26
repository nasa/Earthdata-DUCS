# Earthdata DUCS

**Data Use Code Snippets (DUCS)** — trusted, dataset-specific **Python and R**
code examples for NASA Earthdata datasets, generated with AI, **verified by
actually running them against real data**.

> [!NOTE]
> **Status: early planning.** The pipeline described
> below is **not yet implemented**, and the documents here are drafts intended to
> seed team discussion rather than settled decisions.

## The problem

NASA's Earthdata archive holds **11,000+ datasets**. A researcher who finds the
right dataset still faces potential challenges: how do you authenticate, search this
particular collection, navigate *its particular* file structure, and read *its particular* format?

Good examples exist, but only for a small fraction of the archive. Hand-writing
and maintaining dataset-specific examples for every dataset, and keeping them
working as libraries and data formats change, is not feasible manually.

## The approach

Alongside code generation, DUCS treats "does this code actually run?" as a core value. Every snippet is executed against a real granule before publication.

1. **Generate** — dataset metadata (CMR/UMM-C), a format→library lookup table,
   and validated prior examples are assembled into a prompt; an LLM writes a
   snippet covering **authentication · search · file-structure navigation ·
   data access**.
2. **Validate** — the snippet runs in a version-pinned environment against a
   real granule. On failure, the traceback is fed back for a bounded number of
   correction attempts.
3. **Review** — snippets that never converge go to a human review queue rather
   than being published broken.
4. **Publish** — verified snippets are committed here alongside a
   machine-readable index.

Re-validation runs on a schedule, so snippets that break due to upstream changes
are caught rather than degrading without notice.

## Prototypes

The `prototype/` directory contains the experimental access snippets, their
validation helpers, and the straw-man generator. Environment definitions remain
in `envs/`; the corresponding manual workflows are in `.github/workflows/`.

From the repository root, run the CALIPSO example or its validation entry point:

```bash
uv run --script prototype/access_profile_hdf4.py
uv run --script prototype/validate_access_profile_hdf4.py
```

The validator locates its sibling snippet independently of the working directory.
The MERRA-2 workflow uses `prototype/access_gridded_netcdf4.py` with
`envs/gridded_netcdf4.yml`. The generator can be run with
`python prototype/strawman_ducs.py --seed 1`; its output goes to the ignored
`prototype/out/` directory.

These scripts access Earthdata and require the dependencies and credentials
described in each script or environment file. Do not commit credentials or
downloaded granules.

## Contributing

The project is in its setup phase; contribution guidelines are still being
written.

## About

Funded under the **2026 NASA ESDS AI Innovation Call**, as a collaboration across
NASA DAACs and the Earthdata community.

## License

Not yet finalized.
