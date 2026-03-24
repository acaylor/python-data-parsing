SELECT
    repository,
    manager,
    package_file,
    dep_name,
    current_value,
    current_version,
    json_extract(dep_json, '$.skipReason') AS skip_reason
FROM "{table}"
WHERE current_version IS NULL
   OR json_extract(dep_json, '$.skipReason') IS NOT NULL
ORDER BY repository, manager, package_file, dep_name;
