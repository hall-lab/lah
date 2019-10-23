"""
Assemblies table
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS assemblies (id INTEGER PRIMARY KEY, directory VARCHAR(128))",
        "DROP TABLE assemblies"
    ),
]
