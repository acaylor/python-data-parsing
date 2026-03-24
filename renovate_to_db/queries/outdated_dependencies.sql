SELECT
    repository,
    manager,
    package_file,
    dep_name,
    current_version,
    latest_version
FROM "{table}"
WHERE latest_version IS NOT NULL
  AND current_version IS NOT NULL
  AND latest_version != current_version
ORDER BY repository, manager, package_file, dep_name;
