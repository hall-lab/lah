import click, os

from lah.db import LahDb
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig
from lah.haplotig_iters import HaplotigIterator

@click.command(short_help="create and ingest haplotigs into a database")
@click.option("--chromosome-name", "-n", required=False, type=click.STRING, help="Chromosome name.")
@click.option("--dbfile", "-d", required=True, type=click.STRING, help="Database file to ingest haplotigs.")
@click.option("--haplotigs_fn", "-f", required=True, type=click.STRING, help="File of haplotigs.")
@click.option("--headers", "-g", required=True, type=click.STRING, help="Headers for haplotigs file. Give as a comma separated list.")
def db_ingest_cmd(chromosome_name, dbfile, haplotigs_fn, headers):
    """
    Ingest a Chromosome's Haplotigs

    """
    print("Ingest chromosome {}...".format(chromosome_name))

    haplotigs_fn = os.path.abspath(haplotigs_fn)
    print("Haplotigs file: {}".format(haplotigs_fn))
    if not os.path.exists(haplotigs_fn):
        raise Exception("haplotig file {} does not exist!".format(haplotigs_fn))
    headers_str = headers
    headers = headers.split(",")
    HaplotigIterator.validate_headers(headers)

    print("DB: {}".format(dbfile))
    if not os.path.exists(dbfile):
        print("Creating DB...")
        LahDb.create(dbfile)

    print("Connecting to DB...")
    LahDb.connect(dbfile)
    session = LahDb.session()

    chromosome = Chromosome(name=chromosome_name, haplotigs_fn=haplotigs_fn, haplotig_hdrs=headers_str)
    session.add(chromosome)
    session.flush() # sets chromosome id
    print("Chromsome: {} {}".format(chromosome.id, chromosome.name))

    print("Ingesting haplotigs...")
    haplotig_iter = HaplotigIterator(in_fn=haplotigs_fn, headers=headers)
    metrics = { "total": 0, "reads": 0 }
    for raw in haplotig_iter:
        haplotig = Haplotig(name=raw["hid"], chromosome_id=chromosome.id, file_pos=raw["file_pos"], read_cnt=len(raw["rids"]))
        session.add(haplotig)
        metrics["total"] += 1
        metrics["reads"] += haplotig.read_cnt
        if metrics["total"] % 2000 == 0:
            print(" {} ...".format(metrics["total"]))
            session.commit()
            session = LahDb.session()
    session.commit()

    print("Haplotigs: {}".format(metrics["total"]))
    print("Reads: {}".format(metrics["reads"]))
    print("Ingest chromosome ... DONE")
