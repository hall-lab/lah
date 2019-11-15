import click, os, yoyo
from lah.db import LahDb

@click.group()
def db_cli():
    """
    Work with the local haplotype assembly SQLite database
    """
    pass

# [create]
@click.command(short_help="make a new local haplotype assembly db")
@click.argument("dbfile", type=click.STRING)
def db_create_cmd(dbfile):
    """
    Generate a New SQLite Database for Local Haplotype Assemblies
    """
    print("Generate SQLite DB in {}".format(dbfile))
    db = LahDb(dbfile=dbfile)
    db.create()
db_cli.add_command(db_create_cmd, name="create")

# [ingest]
from lah.db_ingest_cmd import db_ingest_cmd
db_cli.add_command(db_ingest_cmd, name="ingest")
