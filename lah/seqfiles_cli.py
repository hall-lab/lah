import click, os, tabulate
from lah.db import LahDb
from lah.seqfiles import Seqfile

@click.group()
def cli():
    """
    Manipulate the Sequence Files Registered to the Database
    """
    pass

# [add]
@click.command(short_help="add sequence files to the db")
@click.argument("seqfiles", required=True, type=click.STRING, nargs=-1)
def seqfiles_add_cmd(seqfiles):
    """
    Add Haplotig Sequence Files to the Database
    """
    session = LahDb.session()
    for fn in seqfiles:
        print("{}".format(fn))
        session.add(Seqfile(fn=os.path.abspath(fn)))
    session.commit()
cli.add_command(seqfiles_add_cmd, name="add")

# [list]
@click.command(short_help="list seqfiles in the db")
def seqfiles_list_cmd():
    """
    List Haplotig Sequence Files in the Database
    """
    session = LahDb.session()
    rows = []
    for seqfile in session.query(Seqfile).all():
        rows.append([seqfile.id, seqfile.fn])
    print( tabulate.tabulate(rows, ["ID", "SEQFILE"], tablefmt="simple") )
cli.add_command(seqfiles_list_cmd, name="list")

# [subset]
from lah.seqfiles_subset import by_names_cmd
cli.add_command(by_names_cmd, "subset")
