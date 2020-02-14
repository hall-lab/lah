"""
metrics
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS metrics (name TEXT NOT NULL, value TEXT NOT NULL, grp TEXT NOT NULL, PRIMARY KEY(name, value, grp))",
        "DROP TABLE metrics",
    ),
    step(
        "CREATE INDEX IF NOT EXISTS met_grp_idx on metrics(grp)",
        "DROP INDEX met_grp_idx",
    ),
]
