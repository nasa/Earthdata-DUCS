# Contributing

The project is in its setup phase; process will firm up as the pipeline lands.
What follows is what CI enforces today.

## Local setup

Install [uv](https://docs.astral.sh/uv/), then:

```bash
uv sync --group dev
uv run pre-commit install
```

To run every check by hand, the way CI does:

```bash
uv run pre-commit run --all-files
```

## What CI checks

Two jobs, both secret-free so they work on pull requests from forks:

| Job | What it does |
|---|---|
| `lint & workflow audit` | Every pre-commit hook: `ruff` lint and format, `codespell`, YAML/TOML/JSON validity, `actionlint`, and the `zizmor` security audit |
| `secret scan` | `gitleaks` over full git history |

Credentials are checked two independent ways, because they leak two different
ways: `gitleaks` looks at file *contents*, and a `pre-commit` rule rejects
credential-shaped *filenames* (`.netrc`, `.env`, `*.pem`, `*.key`, …). The
`.gitignore` lists those too, but `.gitignore` prevents accidents rather than a
deliberate `git add -f`.

Earthdata Login credentials belong in a local `~/.netrc`, or in GitHub Actions
secrets for workflows. Never in the repository — note that GitHub's free
secret scanning does **not** detect EDL username/password pairs, so the hooks
here are the only thing standing between a mistake and a public commit.

## Writing a workflow

Two rules the `zizmor` audit enforces, both of which will fail CI:

**1. Declare `permissions:` explicitly.** A workflow with no `permissions:`
block inherits broad default credentials. Set the narrowest thing that works, at
the top level so later jobs inherit it:

```yaml
permissions:
  contents: read
```

**2. Pin actions to a full commit SHA, not a tag.** Tags are mutable; a commit
SHA is not. Add the version as a trailing comment — Dependabot reads it and
keeps both the SHA and the comment current, so this is a one-time cost:

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
```

To find the SHA for a tag:

```bash
gh api repos/actions/checkout/commits/v7.0.1 --jq .sha
```

## Scope note

`.github/workflows/ci.yml` keeps the *codebase* healthy. The DUCS
generate/validate pipeline and its scheduled re-validation are separate
workflows with separate triggers, and they are the only ones that use Earthdata
Login credentials.
