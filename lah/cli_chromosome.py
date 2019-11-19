import click, os, tabulate

from lah.db import LahDb
from lah.chromosome import Chromosome

# chr [chromosome]
# - list
# - merge

@click.group()
def chr_cli():
    """
    Work with Chromosomes
    """
    pass

# [merge]
#from lah.cli_haplotigs_merge import lah_hap_merge_cmd
#chr_cli.add_command(lah_hap_merge_cmd, name="merge")

@click.command(short_help="list chromosomes in the database")
@click.option("--dbfile", "-d", required=True, type=click.STRING, help="Database file.")
def chr_list_cmd(dbfile):
    """
    List Chromosomes
    """
    db = LahDb(dbfile=dbfile)
    sm = db.connect()
    session = sm()
    db = LahDb(dbfile=dbfile)
    rows = []
    for c in session.query(Chromosome).all():
        rows += [[ c.id, c.name, len(c.haplotigs) ]]
    print( tabulate.tabulate(rows, ["ID", "NAME", "HAPLOTIG_CNT"], tablefmt="simple") )
chr_cli.add_command(chr_list_cmd, name="list")
