"""
haplotigs table
"""

from yoyo import step

__depends__ = {'20191114_01_aWDaU-chromosomes-table'}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS haplotigs (id INTEGER PRIMARY KEY, name VARCHAR(16), chromosome_id INT NOT NULL, file_pos INT NOT NULL, read_cnt INT NOT NULL, length INT, FOREIGN KEY (chromosome_id) REFERENCES chromosomes(id))",
        "DROP TABLE haplotigs",
    ),
    step("CREATE UNIQUE INDEX IF NOT EXISTS hap_namechr_idx ON haplotigs (name, chromosome_id)", "DROP INDEX hap_namechr_idx"),
    step("CREATE INDEX IF NOT EXISTS hap_chr_idx ON haplotigs (chromosome_id)", "DROP INDEX hap_chr_idx"),
]
