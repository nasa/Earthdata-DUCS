# Authentication in Python (Generic earthaccess Login)

Every snippet begins with the same first step: authenticating with **NASA Earthdata Login (EDL)**. This step is identical for all collections and uses [`earthaccess`](https://earthaccess.readthedocs.io/) to handle credentials.

This document defines the generic code block and the credential scenarios. This gives users a consistent, recognizable starting point across all collections.

## Generic Code

```python
import earthaccess

# ---------------------------------------------------------------------------
# Authenticate with NASA Earthdata Login (EDL)
# ---------------------------------------------------------------------------
# An Earthdata Login account is required to access NASA Earthdata.
# Register for free at: https://urs.earthdata.nasa.gov/users/new
#
# earthaccess.login() looks for your credentials in this order and uses the
# first one that works:
#   1. Environment variables: EARTHDATA_TOKEN, or EARTHDATA_USERNAME and
#      EARTHDATA_PASSWORD
#   2. A .netrc file in your home directory (_netrc on Windows), or the file
#      named by the NETRC environment variable
#   3. An interactive prompt asking for your username and password
#
# Never type your username or password directly into this script.
auth = earthaccess.login()

# Stop here with a clear message if no valid credentials were found
if not auth.authenticated:
    raise RuntimeError(
        "Earthdata Login failed. Check your credentials and try again: "
        "https://urs.earthdata.nasa.gov"
    )

print("Authenticated with Earthdata Login credentials")
```


## Setting up credentials

### Option A: Interactive prompt (simplest, first-time users)

Just run the snippet. If no other credentials are found, you'll be asked for your EDL username and password. To save them for next time:

```python
import earthaccess
earthaccess.login(persist=True)
```

### Option B: `.netrc` file

**macOS / Linux** — create `~/.netrc`:

```bash
echo "machine urs.earthdata.nasa.gov login <username> password <password>" >> ~/.netrc
chmod 600 ~/.netrc
```

**Windows** — create `%USERPROFILE%\_netrc` with the same line:

```
machine urs.earthdata.nasa.gov login <username> password <password>
```

To keep the file somewhere else, set the `NETRC` environment variable to its full path.

### Option C: Environment variables (recommended for scripts, CI, and the validation pipeline)

```bash
export EARTHDATA_USERNAME=<username>
export EARTHDATA_PASSWORD=<password>
# or, instead of username/password:
export EARTHDATA_TOKEN=<token>
```

If `EARTHDATA_TOKEN` is set, it takes precedence over username/password.
