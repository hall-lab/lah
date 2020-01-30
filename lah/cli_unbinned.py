import click

from lah.db import LahDb
from lah.unbinned import read_names

# unbinned
# - list
# - seqfile

@click.group()
def unbinned_cli():
    """
    Work with Unbinned Reads
    """
    pass

# [list]
@click.command()
@click.option("--dbfile", "-d", required=True, type=click.STRING, help="Database file.")
def unbinned_list_cmd(dbfile):
    """
    List unbinned read names
    """
    LahDb.connect(dbfile)
    print("\n".join(read_names()))
unbinned_cli.add_command(unbinned_list_cmd, "list")
