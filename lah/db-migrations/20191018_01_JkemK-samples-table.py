"""
Samples table
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS samples (id INTEGER PRIMARY KEY, name VARCHAR(32) NOT NULL, directory VARCHAR(128) NOT NULL)",
        "DROP TABLE samples"
    ),
]
