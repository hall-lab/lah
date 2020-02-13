"""
metrics
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS metrics (name TEXT NOT NULL, value TEXT NOT NULL, PRIMARY KEY(name, value))",
        "DROP TABLE metrics",
    ),
    step(
        "CREATE INDEX IF NOT EXISTS met_name_idx on metrics(name)",
        "DROP INDEX met_name_idx",
    ),
]
