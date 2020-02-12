import click, os, tabulate
from Bio import SeqIO

from lah.db import LahDb
from lah.haplotig import Haplotig

# asm [haplotigs assemblies]
# - merge
# - metrics

@click.group()
def asm_cli():
    """
    Work with Assembled Haplotigs
    """
    pass

#[merge]
from lah.cli_asm_merge import asm_merge_cmd
asm_cli.add_command(asm_merge_cmd, name="merge")

# [metrics]
@click.command(short_help="show haplotigs metrics")
def asm_metrics_cmd():
    """
    Show Haplotigs Assembly Metrics
    """
    session = LahDb.session()
    dn = os.path.dirname(os.path.abspath(LahDb.dbfile()))
    if not os.path.exists(dn):
        raise Exception("Directory does not exist: {}".format(dn))

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
    print( tabulate.tabulate(rows, ["NAME", "RDS", "COUNT", "TOTAL", "MAX", "CTGS"], tablefmt="presto") )
asm_cli.add_command(asm_metrics_cmd, "metrics")
