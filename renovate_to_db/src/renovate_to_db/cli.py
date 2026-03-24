from __future__ import annotations

import argparse
from pathlib import Path

from .ingest import ingest_log_to_db


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a Renovate NDJSON log into a per-run SQLite database."
    )
    parser.add_argument(
        "--log-file",
        required=True,
        type=Path,
        help="Path to the Renovate NDJSON log file.",
    )
    parser.add_argument(
        "--output-dir",
        default=Path.cwd(),
        type=Path,
        help="Directory where the SQLite database will be created.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = ingest_log_to_db(args.log_file, args.output_dir)
    print(result.database_path)
    print(result.table_name)
    print(result.rows_inserted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
