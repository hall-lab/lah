"""
Haplotig Reads table
"""

from yoyo import step

__depends__ = {'20191018_02_ws2ae-haplotigs-table'}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS haplotig_reads (id VARCHAR(64) PRIMARY KEY, haplotig_id INT NOT NULL, FOREIGN KEY (haplotig_id) REFERENCES haplotigs(id))",
        "DROP TABLE haplotig_reads",
    ),
    step("CREATE INDEX IF NOT EXISTS haprds_hapid_idx ON haplotig_reads (haplotig_id)", "DROP INDEX haprds_hapid_idx"),
]
