import click, os
from lah.assembly import Assembly
from lah.db import LahDb

@click.command(short_help="create and ingest read_groups into a database")
@click.option("--asm-dir", required=False, type=click.STRING, help="Top level directory to create subdirs of halpotypes for assembly, if different than the database file directory.")
@click.option("--dbfile", required=True, type=click.STRING, help="Dataabse file to ingest read_groups. The directory of this file will be used as the assembly top level directory unlesss otherwise specified.")
@click.option("--read-groups", required=True, type=click.STRING, help="File of read_groups. See main help for supported formats.")
def lah_asm_ingest_cmd(asm_dir, dbfile, read_groups):
    """
    Create read_groups Database

    ** REQUIRED PARAMETERS **
    dbfile: The database file to ingest read groups. The directory location will be used as the assembly directory.
    read groups: A file of read groups. Supported formats: edge map

    ** OPTIONAL PARAMETERS **
    asm-dir: The top level directory location of read groups, if different from dbfile directory name.

    """
    if not os.path.exists(read_groups):
        raise Exception("read_group file {} does not exist!".format(read_groups))
    if not asm_dir:
        asm_dir = os.path.dirname(dbfile)
    print("Create DB...")
    print("Assembly directory: {}".format(asm_dir))
    print("read_groups: {}".format(read_groups))
    db = LahDb(dbfile=dbfile)
    if not os.path.exists(dbfile):
        db.create()

    sessionmaker = db.connect()
    session = sessionmaker()

    assembly = Assembly(directory=asm_dir)
    session.add(assembly)
    assembly.ingest(session=session, read_groups_fn=read_groups)
    session.commit()
    # TODO fetch and print assembly stats

#-- lah_asm_ingest_cmd
