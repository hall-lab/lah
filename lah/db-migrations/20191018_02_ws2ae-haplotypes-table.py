"""
Haplotypes table
"""

from yoyo import step

__depends__ = {'20191018_01_JkemK-assemblies-table'}

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS haplotypes (id INT, name VARCHAR(16), assembly_id INT, length INT, reads_cnt INT, PRIMARY KEY (id), FOREIGN KEY (assembly_id) REFERENCES assemblies(id))",
        "DROP TABLE haplotypes",
    ),
    step("CREATE INDEX IF NOT EXISTS asmid_idx ON haplotypes (assembly_id)", "DROP INDEX asmid_idx"),
    step("CREATE UNIQUE INDEX IF NOT EXISTS name_asm_uniq ON haplotypes (name, assembly_id)", "DROP INDEX name_asm_uniq"),
]
