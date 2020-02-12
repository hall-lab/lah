"""
haplotigs table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS haplotigs (id INTEGER PRIMARY KEY, name TEXT, file_pos INT NOT NULL, read_cnt INT NOT NULL, length INT)",
        "DROP TABLE haplotigs",
    ),
    step("CREATE UNIQUE INDEX IF NOT EXISTS hap_name_idx ON haplotigs (name)", "DROP INDEX hap_name_idx"),
]
