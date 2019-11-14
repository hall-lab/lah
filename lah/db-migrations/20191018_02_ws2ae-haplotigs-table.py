"""
Haplotigs table
"""

from yoyo import step

__depends__ = {'20191018_01_JkemK-samples-table'}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS haplotigs (id VARCHAR(16) PRIMARY KEY, sample_id INT NOT NULL, length INT, FOREIGN KEY (sample_id) REFERENCES samples(id))",
        "DROP TABLE haplotigs",
    ),
    step("CREATE INDEX IF NOT EXISTS samid_idx ON haplotigs (sample_id)", "DROP INDEX samid_idx"),
]
