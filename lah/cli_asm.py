import click, os, tabulate
from Bio import SeqIO

from lah.db import LahDb
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig

# asm [haplotigs assemblies]
# - metrics
# - merge

@click.group()
def asm_cli():
    """
    Work with Haplotig Assemblies
    """
    pass

# [merge]
#from lah.cli_haplotigs_merge import lah_hap_merge_cmd
#asm_cli.add_command(lah_hap_merge_cmd, name="merge")

# [metrics]
@click.command(short_help="show haplotigs metrics")
@click.option("--dbfile", "-d", required=True, type=click.STRING, help="Database file.")
def asm_metrics_cmd(dbfile):
    """
    Show Haplotigs Assembly Metrics
    """
    dn = os.path.dirname(dbfile)
    if not os.path.exists(dn):
        raise Exception("Directory does not exist: {}".format(dn))
    db = LahDb(dbfile)
    sm = db.connect()
    session = sm()

    haplotigs_asm_dn = os.path.join(dn, "assemblies")
    m_rows = [] # metrics
    for haplotig in session.query(Haplotig).all():
        asm_fn = haplotig.asm_fn(haplotigs_asm_dn)
        ctgs = {}
        row = [ haplotig.name, str(haplotig.read_cnt) ]
        if os.path.exists(asm_fn):
            for seq in  SeqIO.parse( asm_fn, "fasta"):
                ctgs[seq.name] = len(seq)
            row += [ str(len(ctgs)), str(sum(ctgs.values())), str(max(ctgs.values())), ",".join(map(str, ctgs.values())) ]
        else:
            row += [ "NA", "NA", "NA", "NA" ]
        m_rows.append(row)
    print( tabulate.tabulate(m_rows, ["NAME", "RDS", "COUNT", "TOTAL", "MAX", "CTGS"], tablefmt="simple") )
asm_cli.add_command(asm_metrics_cmd, "metrics")

