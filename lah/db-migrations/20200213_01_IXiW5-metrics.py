"""
metrics
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY, grp TEXT NOT NULL, grp_id TEXT NOT NULL, name TEXT NOT NULL, value TEXT NOT NULL)",
        "DROP TABLE metrics",
    ),
    step(
        "CREATE INDEX IF NOT EXISTS met_grp_idx on metrics(grp)",
        "DROP INDEX met_grp_idx",
    ),
]
