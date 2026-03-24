SELECT
    manager,
    COUNT(*) AS dependency_count,
    COUNT(DISTINCT repository) AS repository_count
FROM "{table}"
GROUP BY manager
ORDER BY dependency_count DESC, manager;
