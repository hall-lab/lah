import click, jinja2, os
from lah.db import LahDb
from lah.assembly import Assembly

@click.command(short_help="prepare haplotypes for assembly")
@click.option("--dbfile", required=True, type=click.STRING, help="Database of haplotypes.")
def lah_asm_prepare_cmd(dbfile):
    """
    Prepare Haplotypes for Local Assembly
    """
    print("Prepare haplotypes for assembly...")
    print("DB File: {}".format(dbfile))
    if not os.path.exists(dbfile):
        raise Exception("Haplotype source {} does not exist!".format(source))
    db = LahDb(dbfile=dbfile)
    sessionmaker = db.connect()
    session = sessionmaker()
    assembly = session.query(Assembly).first() # FIXME may be multiple asemblies
    assembly.prepare(session)

#-- lah_asm_prepare_cmd
