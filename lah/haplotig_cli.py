import click, natsort, os, subprocess, sys, tabulate

from lah.db import LahDb
from lah.haplotig_iters import HaplotigIterator
from lah.models import *

# haplotig [hap]
# - ams
# - ingest
# - list
# - merge
# - seqfile
# - reads

@click.group()
def hap_cli():
    """
    Work with Haplotigs
    """
    pass

# [asm]
from lah.haplotig_asm import haplotig_asm_cmd
hap_cli.add_command(haplotig_asm_cmd, name="asm")

# [ingest]
from lah.haplotig_ingest import haplotig_ingest_cmd
hap_cli.add_command(haplotig_ingest_cmd, name="ingest")

# [seqfile]
from lah.haplotig_seqfile import haplotig_seqfile_cmd
hap_cli.add_command(haplotig_seqfile_cmd, name="seqfile")

@click.command(short_help="list haplotigs")
def hap_list_cmd():
    """
    List Haplotigs
    """
    session = LahDb.session()
    rows = []
    for hap in session.query(Haplotig).all():
        rows += [[ hap.id, hap.name, hap.read_cnt ]]
    #rows = natsort.natsorted(rows, key=lambda x:x[1])
    sys.stdout.write( tabulate.tabulate(rows, ["ID", "NAME", "READS"], tablefmt="simple") + "\n")
hap_cli.add_command(hap_list_cmd, name="list")

@click.command(short_help="show haplotig reads")
@click.argument("hids", type=click.STRING, nargs=-1)
def hap_reads_cmd(hids):
    """
    Show Reads for a Haplotig
    """
    session = LahDb.session()
    directory = session.query(Metadata).filter_by(name="directory").one().value
    haplotigs_bn = session.query(Metadata).filter_by(name="haplotigs_fn").one().value
    haplotigs_headers = session.query(Metadata).filter_by(name="haplotigs_headers").one().value
    hi = HaplotigIterator(in_fn=os.path.join(directory, haplotigs_bn), headers=haplotigs_headers.split(","))
    reads = []
    for hid in hids:
        haplotig = session.query(Haplotig).filter_by(name=hid).one()
        hi.load_haplotig_reads(haplotig)
        reads += haplotig.reads
    print("\n".join(reads))
hap_cli.add_command(hap_reads_cmd, name="reads")
import click

# [merge]
from lah.haplotig_merge import haplotig_merge_cmd
hap_cli.add_command(haplotig_merge_cmd, name="merge")
