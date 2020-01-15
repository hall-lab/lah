import click, os, tabulate
from lah.db import LahDb
from lah.seqfiles import Seqfile

@click.group()
def seqfiles_cli():
    """
    Manipulate the Sequence Files Registered to the Database
    """
    pass

# [add]
@click.command(short_help="add sequence files to the db")
@click.argument("seqfiles", required=True, type=click.STRING, nargs=-1)
@click.option("--dbfile", required=True, type=click.STRING)
def seqfiles_add_cmd(seqfiles, dbfile):
    """
    Add Haplotig Sequence Files to the Database
    """
    print("Add seqfiles to {}".format(dbfile))
    LahDb.connect(dbfile)
    session = LahDb.session()
    for fn in seqfiles:
        print("{}".format(fn))
        session.add(Seqfile(fn=os.path.abspath(fn)))
    session.commit()
seqfiles_cli.add_command(seqfiles_add_cmd, name="add")

# [list]
@click.command(short_help="list seqfiles in the db")
@click.option("--dbfile", required=True, type=click.STRING)
def seqfiles_list_cmd(dbfile):
    """
    List Haplotig Sequence Files in the Database
    """
    LahDb.connect(dbfile)
    session = LahDb.session()
    rows = []
    for seqfile in session.query(Seqfile).all():
        rows.append([seqfile.id, seqfile.fn])
    print( tabulate.tabulate(rows, ["ID", "SEQFILE"], tablefmt="simple") )
seqfiles_cli.add_command(seqfiles_list_cmd, name="list")
