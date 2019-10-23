import click, os
from lah.assembly import Assembly
from lah.db import LahDb

@click.command(short_help="create and ingest haplotypes into a database")
@click.option("--asm-dir", required=False, type=click.STRING, help="Top level directory to create subdirs of halpotypes for assembly, if different than the database file directory.")
@click.option("--dbfile", required=True, type=click.STRING, help="Dataabse file to ingest haplotypes. The directory of this file will be used as the assembly top level directory unlesss otherwise specified.")
@click.option("--haplotypes", required=True, type=click.STRING, help="File of haplotypes. See main help for supported formats.")
def lah_asm_ingest_cmd(asm_dir, dbfile, haplotypes):
    """
    Create Haplotypes Database

    ** REQUIRED PARAMETERS **
    dbfile: The database file to ingest haplotypes. The directory location will be used as the assembly directory.
    haplotypes: A file of haplotypes. Supported formats: edge map

    ** OPTIONAL PARAMETERS **
    asm-dir: The top level directory location of haplotypes, if different from dbfile directory name.

    """
    if not os.path.exists(haplotypes):
        raise Exception("Haplotype file {} does not exist!".format(haplotypes))
    if not asm_dir:
        asm_dir = os.path.dirname(dbfile)
    print("Create DB...")
    print("Assembly directory: {}".format(asm_dir))
    print("Haplotypes: {}".format(haplotypes))
    db = LahDb(dbfile=dbfile)
    if not os.path.exists(dbfile):
        db.create()

    sessionmaker = db.connect()
    session = sessionmaker()

    assembly = Assembly(directory=asm_dir)
    session.add(assembly)
    assembly.ingest(session=session, haplotypes_fn=haplotypes)
    session.commit()
    # TODO fetch and print assembly stats

#-- lah_asm_ingest_cmd
