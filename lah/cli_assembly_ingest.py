import click, os
import lah.assembly
from lah.db import LahDb

@click.command(short_help="create and ingest haplotypes into a database")
@click.option("--asm-dir", required=False, type=click.STRING, help="Top level directory to create subdirs of halpotypes for assembly, if different than the database file directory.")
@click.option("--dbfile", required=True, type=click.STRING, help="Dataabse file to ingest haplotypes. The directory of this file will be used as the assembly top level directory unlesss otherwise specified.")
@click.option("--haplotypes", required=True, type=click.STRING, help="File of haplotypes. See main help for supported formats.")
def lah_asm_ingest_cmd(asm_dir, dbfile, haplotypes):
    """
    Create Haplotypes Database

    ** REQUIRED PARAMETERS **
    directory:  The base directory location of haplotypes
    haplotypes: A file of haplotypes. Supported formats: edge map

    ** OPTIONAL PARAMETERS **
    asm-dir: The top level directroy for the  assemvbly, if not the database file's directory.

    """
    if not os.path.exists(haplotypes):
        raise Exception("Haplotype file {} does not exist!".format(haplotypes))
    if not asm_dir:
        asm_dir = os.path.dirname(haplotypes)
    print("Create DB...")
    print("Assembly directory: {}".format(asm_dir))
    print("Haplotypes: {}".format(haplotypes))
    db = LahDb(dbfile=dbfile)
    if not os.path.exists(dbfile):
        db.create()
    sessionmaker = db.connect()
    session = sessionmaker()
    lah.assembly.ingest(asm_dir=asm_dir, session=session, haplotypes_fn=haplotypes)
    # TODO fetch and print assembly stats

#-- lah_asm_ingest_cmd
