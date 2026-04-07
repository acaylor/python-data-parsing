# renovate-to-db

Convert Renovate NDJSON logs into per-run SQLite databases.

## Installation

Install and run in a virtual environment using [uv](https://docs.astral.sh/uv/):

```bash
# Create a venv and install the package in editable mode
uv venv
source .venv/bin/activate
uv pip install -e .
```

The `renovate-to-db` command is now available in the activated venv:

```bash
renovate-to-db --log-file path/to/renovate.ndjson --output-dir ./db
```

Alternatively, use `uv run` to execute without manually activating the venv:

```bash
uv run renovate-to-db --log-file path/to/renovate.ndjson --output-dir ./db
```

## Helper Queries

Run a bundled query against a generated database:

```bash
python3 scripts/run_query.py --db ../db/renovate-run-2026-01-19-162052.sqlite3 --query outdated_dependencies
```

Available queries live in `queries/`:

- `outdated_dependencies`
- `dependencies_by_manager`
- `repository_summary`
- `skipped_or_unversioned`
- `top_update_candidates`
