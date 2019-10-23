import click, os, yoyo
from lah.db import LahDb

@click.group()
def lah_db_cli():
    """
    Work with the haplotype SQLite database
    """
    pass

@click.command(short_help="make a new haplotype assembly db")
@click.argument("dbfile", type=click.STRING)
def lah_db_create_cmd(dbfile):
    """
    Generate a New SQLite Database for Haplotypes Asseemblies
    """
    print("Generate SQLite DB in {}".format(dbfile))
    db = LahDb(dbfile=dbfile)
    db.create()
lah_db_cli.add_command(lah_db_create_cmd, name="create")

#-- lah_db_create_cmd
