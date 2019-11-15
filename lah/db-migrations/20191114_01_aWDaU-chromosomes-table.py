"""
chromosomes table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS chromosomes (id INTEGER PRIMARY KEY, name VARCHAR(16) NOT NULL, haplotigs_fn VARCHAR(128) NOT NULL)",
        "DROP TABLE chromosomes"
    ),
    step("CREATE INDEX IF NOT EXISTS chr_name_idx ON chromosomes (name)", "DROP INDEX chr_name_idx"),
]
