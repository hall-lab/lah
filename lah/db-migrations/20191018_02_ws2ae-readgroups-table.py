"""
ReadGroups table
"""

from yoyo import step

__depends__ = {'20191018_01_JkemK-assemblies-table'}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS read_groups (id INTEGER PRIMARY KEY, name VARCHAR(16), assembly_id INT, length INT, reads_cnt INT, FOREIGN KEY (assembly_id) REFERENCES assemblies(id))",
        "DROP TABLE read_groups",
    ),
    step("CREATE INDEX IF NOT EXISTS asmid_idx ON read_groups (assembly_id)", "DROP INDEX asmid_idx"),
    step("CREATE UNIQUE INDEX IF NOT EXISTS name_asm_uniq ON read_groups (name, assembly_id)", "DROP INDEX name_asm_uniq"),
]
