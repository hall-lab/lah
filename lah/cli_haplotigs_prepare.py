import click, jinja2, os
from lah.db import LahDb
from lah.sample import Sample

@click.command(short_help="prepare haplotigs for haplotigs")
@click.option("--dbfile", required=True, type=click.STRING, help="Database of haplotigs.")
def lah_hap_prepare_cmd(dbfile):
    """
    Prepare Haplotigs for Local haplotigs
    """
    print("Prepare haplotigs for haplotigs...")
    print("DB File: {}".format(dbfile))
    if not os.path.exists(dbfile):
        raise Exception("Haplotig source {} does not exist!".format(source))
    db = LahDb(dbfile=dbfile)
    sessionmaker = db.connect()
    session = sessionmaker()
    sample = session.query(Sample).first() # FIXME may be multiple asemblies
    sample.prepare(session)
