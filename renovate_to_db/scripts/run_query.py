from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


QUERY_DIR = Path(__file__).resolve().parent.parent / "queries"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a helper SQL query against a renovate-to-db SQLite database."
    )
    parser.add_argument("--db", required=True, type=Path, help="Path to the SQLite database.")
    parser.add_argument(
        "--query",
        required=True,
        help="Query name from the queries directory, without the .sql suffix.",
    )
    parser.add_argument(
        "--table",
        help="Run table name. If omitted, the script uses the only table in the database.",
    )
    return parser


def resolve_table_name(conn: sqlite3.Connection, requested_table: str | None) -> str:
    if requested_table:
        return requested_table

    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()
    table_names = [row[0] for row in rows]
    if len(table_names) != 1:
        raise ValueError(
            f"Expected exactly one table in database, found {len(table_names)}. "
            "Pass --table explicitly."
        )
    return table_names[0]


def load_query(query_name: str) -> str:
    query_path = QUERY_DIR / f"{query_name}.sql"
    if not query_path.exists():
        available = ", ".join(sorted(path.stem for path in QUERY_DIR.glob("*.sql")))
        raise ValueError(f"Unknown query {query_name!r}. Available queries: {available}")
    return query_path.read_text(encoding="utf-8")


def print_rows(cursor: sqlite3.Cursor) -> None:
    if cursor.description is None:
        return

    headers = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    widths = [len(header) for header in headers]
    for row in rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len("" if value is None else str(value)))

    print(" | ".join(header.ljust(widths[idx]) for idx, header in enumerate(headers)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(
            " | ".join(
                ("" if value is None else str(value)).ljust(widths[idx])
                for idx, value in enumerate(row)
            )
        )


def main() -> int:
    args = build_parser().parse_args()
    query_sql = load_query(args.query)

    with sqlite3.connect(args.db) as conn:
        table_name = resolve_table_name(conn, args.table)
        cursor = conn.execute(query_sql.format(table=table_name))
        print_rows(cursor)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
