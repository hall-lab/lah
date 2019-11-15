"""
Sequence files table
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS seqfiles (id INTEGER PRIMARY KEY, fn VARCHAR(128) NOT NULL)",
        "DROP TABLE seqfiles",
    )
]
