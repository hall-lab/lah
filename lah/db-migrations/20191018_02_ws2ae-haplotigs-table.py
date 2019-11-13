"""
Haplotigs table
"""

from yoyo import step

__depends__ = {'20191018_01_JkemK-samples-table'}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS haplotigs (id INTEGER PRIMARY KEY, name VARCHAR(16) NOT NULL, sample_id INT NOT NULL, length INT, reads_cnt INT, FOREIGN KEY (sample_id) REFERENCES samples(id))",
        "DROP TABLE haplotigs",
    ),
    step("CREATE INDEX IF NOT EXISTS samid_idx ON haplotigs (sample_id)", "DROP INDEX samid_idx"),
    step("CREATE UNIQUE INDEX IF NOT EXISTS name_sam_uniq ON haplotigs (name, sample_id)", "DROP INDEX name_sam_uniq"),
]
