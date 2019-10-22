"""
Assemblies table
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS assemblies (id INT, directory VARCHAR(128), PRIMARY KEY(id))",
        "DROP TABLE assemblies"
    ),
]
