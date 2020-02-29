import click, os

from lah.db import LahDb
from lah.models import Haplotig
import lah.unbinned

@click.command(short_help="initialize a new local assembly of haplotigs directory")
@click.option("--only-dbfile", "-o", is_flag=True, default=False)
def init_cmd(only_dbfile):
    """
    Initialize a [L]ocal [A]ssembly of [H]aplotigs Directory

    Creates the SQLite database and directory structure.
    Provide the database file name to the base lah command with "--dbfile" or "-d".
    Use "--only-db" to only create the database.
    """
    db = LahDb.current()
    dbfile = getattr(db, "dbfile", None)
    if dbfile is None:
        raise Exception('Provide the database file name to the base lah command with "--dbfile" or "-d".')
    print("Generate SQLite DB in {}".format(db.dbfile))
    db.create()
    if not only_dbfile:
        print("Create directory structure...")
        dn = os.path.dirname(dbfile)
        os.makedirs( os.path.join(dn, Haplotig.asm_files_sdn()), exist_ok=True )
        os.makedirs( os.path.join(dn, Haplotig.asm_sdn()), exist_ok=True )
        os.makedirs( os.path.join(dn, Haplotig.seqfile_sdn()), exist_ok=True )
        os.makedirs( os.path.join(dn, lah.unbinned.subd()), exist_ok=True )
    print("Intialize LAH ... OK")

#-- init_cmd
