import click, tabulate

from lah.db import LahDb
from lah.models import *

# metrics
# - ctg-lengths
# - generate
# - reads
# - unbinned

@click.group()
def metrics_cli():
    """
    Generate and show metrics
    """
    pass

# [ctg-lengths]
@click.command(short_help="show haplotig assembly metrics from the DB")
def metrics_ctglens_cmd():
    """
    Show Haplotigs Assembly Metrics
    """
    session = LahDb.session()
    rows = []
    cnt = 0
    for metric in session.query(Metric).filter_by(name="contig lengths"):
        if metric.value == "0":
            rows += [[ metric.grp, "NO_ASM", "NA", "NA", "NA" ]]
        else:
            contig_lengths = list(map(int, metric.value.split(",")))
            rows += [[ metric.grp, str(len(contig_lengths)), str(sum(contig_lengths)), str(max(contig_lengths)), metric.value ]]
    if len(rows) == 0:
        raise Exception("No contig lengths metrics found in the DB. Use the 'generate' command to create and save them.")
    print( tabulate.tabulate(rows, ["NAME", "RDS", "COUNT", "TOTAL", "MAX", "CTGS"], tablefmt="presto") )
metrics_cli.add_command(metrics_ctglens_cmd, name="ctg-lengths")

# [generate]
from lah.metrics_generate import metrics_generate_cmd
metrics_cli.add_command(metrics_generate_cmd, name="generate")

# [reads]
# [unbinned]
