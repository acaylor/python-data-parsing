from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS "{table_name}" (
    repository TEXT,
    manager TEXT NOT NULL,
    package_file TEXT,
    dep_name TEXT,
    package_name TEXT,
    current_value TEXT,
    current_version TEXT,
    latest_version TEXT,
    datasource TEXT,
    versioning TEXT,
    dep_json TEXT NOT NULL CHECK (json_valid(dep_json))
) STRICT
"""

INSERT_ROW_SQL = """
INSERT INTO "{table_name}" (
    repository,
    manager,
    package_file,
    dep_name,
    package_name,
    current_value,
    current_version,
    latest_version,
    datasource,
    versioning,
    dep_json
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


@dataclass(frozen=True)
class IngestResult:
    database_path: Path
    table_name: str
    rows_inserted: int


def as_optional_text(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


def parse_run_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def build_database_path(output_dir: Path, run_timestamp: datetime) -> Path:
    stamp = run_timestamp.strftime("%Y-%m-%d-%H%M%S")
    return output_dir / f"renovate-run-{stamp}.sqlite3"


def build_table_name(run_timestamp: datetime) -> str:
    return f"run_{run_timestamp.strftime('%Y_%m_%d_%H%M%S')}"


def choose_latest_version(dep: dict) -> str | None:
    updates = dep.get("updates")
    current_version = dep.get("currentVersion")
    current_value = dep.get("currentValue")

    if isinstance(updates, list) and updates:
        timestamped_updates = [
            update
            for update in updates
            if isinstance(update, dict) and update.get("releaseTimestamp")
        ]
        if timestamped_updates:
            chosen = max(
                timestamped_updates,
                key=lambda update: str(update["releaseTimestamp"]),
            )
            return chosen.get("newVersion") or chosen.get("newValue")

        for update in reversed(updates):
            if isinstance(update, dict):
                chosen = update
                return chosen.get("newVersion") or chosen.get("newValue")

    return current_version or current_value


def find_run_timestamp(log_file: Path) -> datetime:
    with log_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            if isinstance(obj, dict) and isinstance(obj.get("time"), str):
                return parse_run_timestamp(obj["time"])

    raise ValueError(f"No valid JSON line with a time field found in {log_file}")


def iter_dependency_rows(log_file: Path):
    with log_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            if not isinstance(obj, dict):
                continue

            config = obj.get("config")
            if not isinstance(config, dict):
                continue

            repository = obj.get("repository")
            for manager, entries in config.items():
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    deps = entry.get("deps")
                    if not isinstance(deps, list):
                        continue
                    package_file = entry.get("packageFile")
                    for dep in deps:
                        if not isinstance(dep, dict):
                            continue
                        yield (
                            as_optional_text(repository),
                            as_optional_text(manager),
                            as_optional_text(package_file),
                            as_optional_text(dep.get("depName")),
                            as_optional_text(dep.get("packageName")),
                            as_optional_text(dep.get("currentValue")),
                            as_optional_text(dep.get("currentVersion")),
                            as_optional_text(choose_latest_version(dep)),
                            as_optional_text(dep.get("datasource")),
                            as_optional_text(dep.get("versioning")),
                            json.dumps(dep, sort_keys=True),
                        )


def ingest_log_to_db(log_file: Path, output_dir: Path) -> IngestResult:
    log_file = log_file.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    run_timestamp = find_run_timestamp(log_file)
    iterator = iter_dependency_rows(log_file)
    rows_inserted = 0

    database_path = build_database_path(output_dir, run_timestamp)
    table_name = build_table_name(run_timestamp)

    with sqlite3.connect(database_path) as conn:
        conn.execute(CREATE_TABLE_SQL.format(table_name=table_name))
        for row in iterator:
            conn.execute(INSERT_ROW_SQL.format(table_name=table_name), row)
            rows_inserted += 1
        conn.commit()

    return IngestResult(
        database_path=database_path,
        table_name=table_name,
        rows_inserted=rows_inserted,
    )
