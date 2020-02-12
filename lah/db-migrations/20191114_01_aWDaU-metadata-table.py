"""
metadata table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS metadata (name TEXT PRIMARY KEY, value TEXT NOT NULL)",
        "DROP TABLE metadata",
    ),
]
