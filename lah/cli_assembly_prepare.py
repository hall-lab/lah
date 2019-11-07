import click, jinja2, os
from lah.db import LahDb
from lah.assembly import Assembly

@click.command(short_help="prepare read_groups for assembly")
@click.option("--dbfile", required=True, type=click.STRING, help="Database of read_groups.")
def lah_asm_prepare_cmd(dbfile):
    """
    Prepare ReadGroups for Local Assembly
    """
    print("Prepare read_groups for assembly...")
    print("DB File: {}".format(dbfile))
    if not os.path.exists(dbfile):
        raise Exception("ReadGroup source {} does not exist!".format(source))
    db = LahDb(dbfile=dbfile)
    sessionmaker = db.connect()
    session = sessionmaker()
    assembly = session.query(Assembly).first() # FIXME may be multiple asemblies
    assembly.prepare(session)

#-- lah_asm_prepare_cmd
