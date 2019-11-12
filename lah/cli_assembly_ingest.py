import click, os
from lah.assembly import Assembly
from lah.db import LahDb

@click.command(short_help="create and ingest haplotigs into a database")
@click.option("--asm-dir", required=False, type=click.STRING, help="Top level directory to create subdirs of halpotypes for assembly, if different than the database file directory.")
@click.option("--dbfile", required=True, type=click.STRING, help="Dataabse file to ingest haplotigs. The directory of this file will be used as the assembly top level directory unlesss otherwise specified.")
@click.option("--read-groups", required=True, type=click.STRING, help="File of haplotigs. See main help for supported formats.")
def lah_asm_ingest_cmd(asm_dir, dbfile, haplotigs):
    """
    Create haplotigs Database

    ** REQUIRED PARAMETERS **
    dbfile: The database file to ingest read groups. The directory location will be used as the assembly directory.
    read groups: A file of read groups.

    ** OPTIONAL PARAMETERS **
    asm-dir: The top level directory location of read groups, if different from dbfile directory name.

    """
    if not os.path.exists(haplotigs):
        raise Exception("haplotig file {} does not exist!".format(haplotigs))
    if not asm_dir:
        asm_dir = os.path.dirname(dbfile)
    print("Create DB...")
    print("Assembly directory: {}".format(asm_dir))
    print("haplotigs: {}".format(haplotigs))
    db = LahDb(dbfile=dbfile)
    if not os.path.exists(dbfile):
        db.create()

    sessionmaker = db.connect()
    session = sessionmaker()

    assembly = Assembly(directory=asm_dir)
    session.add(assembly)
    assembly.ingest(session=session, haplotigs_fn=haplotigs)
    session.commit()
    # TODO fetch and print assembly stats

#-- lah_asm_ingest_cmd
