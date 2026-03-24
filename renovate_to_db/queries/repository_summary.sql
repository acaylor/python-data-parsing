SELECT
    repository,
    COUNT(*) AS dependency_count,
    SUM(CASE
        WHEN latest_version IS NOT NULL
         AND current_version IS NOT NULL
         AND latest_version != current_version
        THEN 1 ELSE 0 END
    ) AS outdated_count
FROM "{table}"
GROUP BY repository
ORDER BY outdated_count DESC, dependency_count DESC, repository;
