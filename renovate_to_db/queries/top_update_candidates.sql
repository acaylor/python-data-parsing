SELECT
    repository,
    dep_name,
    current_version,
    latest_version,
    json_extract(dep_json, '$.updates[0].updateType') AS first_update_type,
    json_extract(dep_json, '$.updates[0].releaseTimestamp') AS first_release_timestamp
FROM "{table}"
WHERE latest_version IS NOT NULL
  AND current_version IS NOT NULL
  AND latest_version != current_version
ORDER BY repository, dep_name;
