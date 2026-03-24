# renovate-to-db

Convert Renovate NDJSON logs into per-run SQLite databases.

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
