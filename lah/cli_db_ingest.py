import click, os
from lah.sample import Sample
from lah.db import LahDb
from lah.haplotig_iters import HaplotigIterator

@click.command(short_help="create and ingest haplotigs into a database")
@click.option("--sample-name", "-n", required=False, type=click.STRING, help="Sample name.")
@click.option("--sample-dir", "-d", required=False, type=click.STRING, help="Top level directory to create subdirs of halpotypes for haplotigs, if different than the database file directory.")
@click.option("--dbfile", required=True, type=click.STRING, help="Dataabse file to ingest haplotigs. The directory of this file will be used as the haplotigs top level directory unlesss otherwise specified.")
@click.option("--haplotigs", "-f", required=True, type=click.STRING, help="File of haplotigs. See main help for supported formats.")
@click.option("--headers", "-g", required=True, type=click.STRING, help="Headers for haplotigs file. Give as a comma separated list.")
def db_ingest_cmd(sample_name, sample_dir, dbfile, haplotigs, headers):
    """
    Create haplotigs Database

    ** REQUIRED PARAMETERS **
    dbfile: The database file to ingest read groups. The directory location will be used as the haplotigs directory.
    read groups: A file of read groups.

    ** OPTIONAL PARAMETERS **
    sample-dir: The top level directory location of read groups, if different from dbfile directory name.

    """
    headers = headers.split(",")
    HaplotigIterator.validate_headers(headers)
    if not os.path.exists(haplotigs):
        raise Exception("haplotig file {} does not exist!".format(haplotigs))
    if not sample_dir:
        sample_dir = os.path.dirname(dbfile)
    print("Create DB...")
    print("haplotigs directory: {}".format(sample_dir))
    print("haplotigs: {}".format(haplotigs))
    db = LahDb(dbfile=dbfile)
    if not os.path.exists(dbfile):
        db.create()

    sessionmaker = db.connect()
    session = sessionmaker()

    sample = Sample(name=sample_name, directory=sample_dir)
    session.add(sample)
    session.commit()

    haplotig_iter = HaplotigIterator(in_fn=haplotigs, headers=headers)
    sample.ingest(session=session, haplotig_iter=haplotig_iter)
    session.commit()

    # TODO fetch and print haplotigs stats
