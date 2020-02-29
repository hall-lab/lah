import click, os

from lah.db import LahDb
from lah.models import *
from lah.haplotig_iters import HaplotigIterator
import lah.unbinned

@click.command(short_help="create and ingest haplotigs into a database")
@click.option("--haplotigs_fn", "-f", required=True, type=click.STRING, help="File of haplotigs.")
@click.option("--headers", "-g", required=True, type=click.STRING, help="Headers for haplotigs file. Give as a comma separated list.")
def haplotig_ingest_cmd(haplotigs_fn, headers):
    """
    Ingest Haplotigs
    """
    haplotigs_fn = os.path.abspath(haplotigs_fn)
    print("Haplotigs file: {}".format(haplotigs_fn))
    if not os.path.exists(haplotigs_fn):
        raise Exception("haplotig file {} does not exist!".format(haplotigs_fn))

    print("Connecting to DB...")
    session = LahDb.session()

    metadata = {
        "directory": os.path.dirname(haplotigs_fn),
        "haplotigs_fn": haplotigs_fn,
        "haplotig_headers": headers,
    }
    print("Setting metadata...")
    for k in metadata.keys():
        m = Metadata(name=k, value=metadata[k])
        session.add(m)
        print("Metadata: {} {}".format(m.name, m.value))
    session.flush()

    headers = headers.split(",")
    HaplotigIterator.validate_headers(headers)

    print("Ingesting haplotigs...")
    haplotig_iter = HaplotigIterator(in_fn=haplotigs_fn, headers=headers)
    metrics = { "total": 0, "reads": 0 }
    for raw in haplotig_iter:
        haplotig = Haplotig(name=raw["hid"], file_pos=raw["file_pos"], read_cnt=len(raw["rids"]))
        session.add(haplotig)
        metrics["total"] += 1
        metrics["reads"] += haplotig.read_cnt
        if metrics["total"] % 2000 == 0:
            print(" {} ...".format(metrics["total"]))
            session.commit()
            session = LahDb.session()
    session.commit()

    print("Haplotigs: {}\nReads: {}\nIngest haplotigs ... DONE".format(metrics["total"], metrics["reads"]))

#-- haplotig_ingest_cmd
