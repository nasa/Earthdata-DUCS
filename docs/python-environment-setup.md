# Python Environment Setup

Every DUCS snippet is written in Python and needs an environment with the right packages installed. This page covers the steps that are the same for every snippet: installing Python, creating an environment, and getting an Earthdata Login account. Each snippet also tells you which packages it needs; you add those in step 2.

## 1. Install Miniforge

[Miniforge](https://github.com/conda-forge/miniforge) is a minimal installer for conda that uses the community-run `conda-forge` channel by default. It is free to use, including in government and institutional settings. If you already have conda or mamba installed, skip to step 2 and make sure you use `conda-forge` (not `defaults`) as your channel.

Download the installer for your operating system from the [Miniforge releases page](https://github.com/conda-forge/miniforge/releases/latest) and run it. Then open a new terminal (Windows: "Miniforge Prompt") and confirm it works:

```bash
conda --version
```

## 2. Create an environment

Every snippet uses [`earthaccess`](https://earthaccess.readthedocs.io/) to search for and download NASA data, so it is included in every environment. Snippets then need different packages depending on the data format and how you want to work with it, so the snippet lists its own package set alongside the code.

Create an environment with `earthaccess` plus the packages listed for your snippet:

```bash
conda create -n ducs -c conda-forge --override-channels python earthaccess <snippet packages>
conda activate ducs
```

`<snippet packages>` is a placeholder. Copy the complete command from your snippet, which already has it filled in.

Some data formats (for example HDF4 or GeoTIFF) depend on compiled libraries such as GDAL. Installing from `conda-forge` brings those along automatically, which is the main reason we recommend conda over `pip` alone.

If you later run a different snippet, either create a new environment for it or add its packages to this one with `conda install -n ducs -c conda-forge --override-channels <packages>`. Separate environments avoid version conflicts.

## 3. Create an Earthdata Login account

NASA requires a free Earthdata Login (EDL) account to download data.

1. Register at <https://urs.earthdata.nasa.gov/users/new>.
2. Sign in and accept the end-user license agreements (EULAs) for the data providers you plan to use. Some datasets return "access denied" errors until you do (Applications → Authorized Apps).

The snippets use `earthaccess` to log in. The first time you run a snippet it prompts for your username and password, then saves them to a `~/.netrc` file so you aren't asked again. Alternatives, if you don't want credentials stored on disk:

- Set the `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` environment variables, or
- Generate an EDL token from your profile page and set `EARTHDATA_TOKEN`.

Never paste your credentials into a snippet or commit them to version control.

## 4. Run a snippet

Paste the snippet into a file or a Jupyter notebook cell within the activated environment and run it. If authentication succeeds you will see `Authentication Completed`.

## Troubleshooting

- **`ModuleNotFoundError`**: the environment isn't activated, or a package from the snippet's list wasn't installed. Run `conda activate ducs` and re-check the list.
- **Login prompt doesn't appear / 401 errors**: check your username and password at <https://urs.earthdata.nasa.gov>, and confirm you have accepted the EULA for the dataset.
