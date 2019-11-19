import click, os, sys, tempfile

import inspect

from lah.db import LahDb
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile
from sx.subset import by_name

@click.command(short_help="generate haplotig seqfile")
@click.option("--hid", required=True, type=click.STRING)
@click.option("--output", required=True, type=click.STRING)
@click.option("--dbfile", required=True, type=click.STRING)
def haplotig_seqfile_cmd(hid, output, dbfile):
    """
    Generate Haplotig Seqfile

    """
    print("Generate haplotig seqfile ...")
    print("Haplotig ID: {}".format(hid))
    print("DB: {}".format(dbfile))
    if not os.path.exists(dbfile):
        raise Exception("DB file does not exist!")

    db = LahDb(dbfile)
    sm = db.connect()
    session = sm()
    haplotig = session.query(Haplotig).get(hid)
    if not haplotig:
        raise Exception("Failed to get haplotig {} from db!".format(hid))

    chromosome = haplotig.chromosome
    chromosome.load_haplotig(haplotig)
    if not hasattr(haplotig, "reads"):
        raise Exception("Haplotig {} has no reads!".format(hid))

    source_seqfiles = session.query(Seqfile).all()
    if not len(source_seqfiles):
        raise Exception("No seqfiles fround in database!")

    print("Output: {}".format(output))
    haplotig.seqfile(sources=source_seqfiles, output=output)
    print("Generate haplotig seqfile ... OK")
