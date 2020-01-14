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

#[merge]
from lah.cli_asm_merge import asm_merge_cmd
asm_cli.add_command(asm_merge_cmd, name="merge")

# [metrics]
@click.command(short_help="show haplotigs metrics")
@click.option("--dbfile", "-d", required=True, type=click.STRING, help="Database file.")
def asm_metrics_cmd(dbfile):
    """
    Show Haplotigs Assembly Metrics
    """
    dn = os.path.dirname(os.path.abspath(dbfile))
    if not os.path.exists(dn):
        raise Exception("Directory does not exist: {}".format(dn))
    LahDb.connect(dbfile)
    session = LahDb.session()

    haplotigs_asm_dn = os.path.join(dn, "assemblies")
    rows = [] # metrics
    cnt = 0
    for haplotig in session.query(Haplotig).all():
        asm_fn = haplotig.asm_fn(haplotigs_asm_dn)
        ctg_lens = []
        row = [ haplotig.name, str(haplotig.read_cnt) ]
        if os.path.exists(asm_fn):
            for seq in SeqIO.parse( asm_fn, "fasta"):
                ctg_lens.append(len(seq))
            if len(ctg_lens) == 0:
                row += [ "NOCTGS", "NA", "NA", "NA" ]
            else:
                row += [ str(len(ctg_lens)), str(sum(ctg_lens)), str(max(ctg_lens)), ",".join(map(str, ctg_lens)) ]
        else:
            row += [ "NOASM", "NA", "NA", "NA" ]
        rows.append(row)
        print("\t".join(row))
    #print( tabulate.tabulate(rows, ["NAME", "RDS", "COUNT", "TOTAL", "MAX", "CTGS"], tablefmt="presto") )
asm_cli.add_command(asm_metrics_cmd, "metrics")

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
    LahDb.connect(dbfile)
    session = LahDb.session()

    haplotigs_asm_dn = os.path.join(dn, "assemblies")
    m_rows = [] # metrics
    for haplotig in session.query(Haplotig).all():
        asm_fn = haplotig.asm_fn(haplotigs_asm_dn)
        ctgs = {}
        if os.path.exists(asm_fn):
            for seq in  SeqIO.parse( asm_fn, "fasta"):
                ctgs[seq.name] = len(seq)
        m_rows.append([ haplotig.name, str(haplotig.read_cnt), str(len(ctgs)), str(sum(ctgs.values())), str(max(ctgs.values())), ",".join(map(str, ctgs.values())) ])
    print( tabulate.tabulate(m_rows, ["NAME", "RDS", "COUNT", "TOTAL", "MAX", "CTGS"], tablefmt="simple") )
asm_cli.add_command(asm_metrics_cmd, "metrics")
