import click, os, yaml
from Bio import SeqIO

from lah.db import LahDb
from lah.models import *

@click.command(short_help="merge haplotig assemblies")
@click.option("--output", "-o", type=click.STRING, help="Output merged assembly to this files instead to <BASE_DIR>/asm.merged.fasta.")
def haplotig_merge_cmd(output=None):
    """
    Merge Haplotig haplotigs Fastas

    ** NOTES **
    The merged haplotigs will be in the haplotigs directory.
    Haplotigs with one read with be skipped.
    All contigs in haplotig assmebled fasta will be used.
    Haplotig contigs will be renamed to includ the haplotig id.

    """
    print("Merge haplotig assemblies...")

    session = LahDb.session()
    print("HERE")
    dn = session.query(Metadata).filter_by(name="directory").one().value
    print("HERE")
    merged_fn = Haplotig.merged_fn(dn)
    print("HERE")
    if output is not None:
        merged_fn = output
    print("Output file: {}".format(merged_fn))
    if os.path.exists(merged_fn):
        os.remove(merged_fn)
    metrics = {
        "NOASM": 0,
        "TOTAL": 0,
    }
 
    with open(merged_fn, "a+") as asm_sq_f:
        for haplotig in session.query(Haplotig).all():
            asm_fn = haplotig.asm_fn(dn)
            if not os.path.exists(asm_fn) or os.path.getsize(asm_fn) == 0:
                metrics["NOASM"] += 1
                continue

            cnt = 0
            metrics["TOTAL"] += 1
            for seq in SeqIO.parse(asm_fn, "fasta"):
                cnt += 1
                seq.id = ".".join([haplotig.name, str(cnt)])
                SeqIO.write(seq, asm_sq_f, "fasta")
    print("Metrics:\n{}".format(yaml.dump(metrics, sort_keys=True, indent=4)))
