import click, tabulate

from lah.db import LahDb
from lah.models import *

# metrics
# - asm
# - generate
# - haplotigs
# - seqfiles
# - unbinned

@click.group()
def metrics_cli():
    """
    Generate and show metrics
    """
    pass

# [asm]
@click.command(short_help="show haplotig assembly metrics from the DB")
def metrics_asm_cmd():
    """
    Show Merged Assembly Metrics
    """
    session = LahDb.session()
    rows = []
    cnt = 0
    for metric in session.query(Metric).filter_by(grp="asm"): # grp_id=1
        rows += [[ metric.name, metric.value ]]
    if len(rows) == 0:
        raise Exception("No merged assembly metrics found in the DB. Use the 'generate' command to create and save them.")
    print( tabulate.tabulate(rows, ["NAME", "VALUE"], tablefmt="simple") )
metrics_cli.add_command(metrics_asm_cmd, name="asm")

# [haplotigs]
@click.command(short_help="show haplotig assembly metrics from the DB")
def metrics_haplotigs_cmd():
    """
    Show Haplotigs Assembly Metrics
    """
    session = LahDb.session()
    rows = {}
    cnt = 0
    for metric in session.query(Metric).filter_by(grp="haplotig").filter_by(name="contig lengths"):
        if metric.value == "0":
            #rows += [[ metric.grp_id, "NO_ASM", "NA", "NA", "NA" ]]
            rows[metric.grp_id] = [ metric.grp_id, "NO_ASM", "NA", "NA", "NA" ]
        else:
            contig_lengths = list(map(int, metric.value.split(",")))
            #rows += [[ metric.grp_id, str(len(contig_lengths)), str(sum(contig_lengths)), str(max(contig_lengths)), metric.value ]]
            rows[metric.grp_id] = [ metric.grp_id, str(len(contig_lengths)), str(sum(contig_lengths)), str(max(contig_lengths)), metric.value ]
    for metric in session.query(Metric).filter_by(grp="haplotig").filter_by(name="reads cnt"):
            rows[metric.grp_id].append(metric.value)
    if len(rows) == 0:
        raise Exception("No contig lengths metrics found in the DB. Use the 'generate' command to create and save them.")
    print( tabulate.tabulate(rows.values(), ["NAME", "COUNT", "TOTAL", "MAX", "CTGS", "RDS"], tablefmt="presto") )
metrics_cli.add_command(metrics_haplotigs_cmd, name="haplotigs")

# [generate]
from lah.metrics_generate import metrics_generate_cmd
metrics_cli.add_command(metrics_generate_cmd, name="generate")

# [seqfiles]
@click.command(short_help="show haplotig assembly metrics from the DB")
def metrics_seqfiles_cmd():
    """
    Show Read Metrics
    """
    session = LahDb.session()
    seqfiles = {}
    for seqfile in session.query(Seqfile):
        seqfiles[str(seqfile.id)] = seqfile
    rows = []
    cnt = 0
    for metric in session.query(Metric).filter_by(grp="seqfile"):
        rows += [[ seqfiles[metric.grp_id].fn, metric.name, metric.value ]]
    if len(rows) == 0:
        raise Exception("No read metrics found in the DB. Use the 'generate' command to create and save them.")
    print( tabulate.tabulate(rows, ["SEQFILE", "METRIC", "VALUE"], tablefmt="presto") )
metrics_cli.add_command(metrics_seqfiles_cmd, name="seqfiles")

# [unbinned]
