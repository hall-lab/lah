import click, os, tabulate
from Bio import SeqIO

from lah.db import LahDb
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig

# unbinned
# - asm
# - list
# - seqfile

@click.group()
def ub_cli():
    """
    Work with Unbinned Reads
    """
    pass

# [list]
@click.command()
@click.option("--dbfile", "-d", required=True, type=click.STRING, help="Database file.")
def ub_list(dbfile):
    """
    List unbinned read names
    """
    dn = os.path.dirname(dbfile)
    if not os.path.exists(dn):
        raise Exception("Directory does not exist: {}".format(dn))
    LahDb.connect(dbfile)
    session = LahDb.session()

    for haplotig in session.query(Haplotig).all():
        asm_fn = haplotig.asm_fn(haplotigs_asm_dn)
        ctgs = {}
        if os.path.exists(asm_fn):
            for seq in  SeqIO.parse( asm_fn, "fasta"):
                ctgs[seq.name] = len(seq)
        m_rows.append([ haplotig.name, str(haplotig.read_cnt), str(len(ctgs)), str(sum(ctgs.values())), str(max(ctgs.values())), ",".join(map(str, ctgs.values())) ])

    unbinned_rds = set()
    for seqfile in session.query(Seqfile).all():
        if 
        unbinned_rds.add 
    print( tabulate.tabulate(m_rows, ["NAME", "RDS", "COUNT", "TOTAL", "MAX", "CTGS"], tablefmt="simple") )
asm_cli.add_command(asm_metrics_cmd, "metrics")
