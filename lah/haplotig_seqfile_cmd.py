import click, os, sys, tempfile

import inspect

from lah.db import LahDb
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile

@click.command(short_help="generate haplotig seqfile")
@click.option("--hid", required=True, type=click.STRING)
@click.option("--output", required=True, type=click.STRING)
def haplotig_seqfile_cmd(hid, output):
    """
    Generate Haplotig Seqfile

    """
    print("Generate haplotig seqfile ...")
    print("Haplotig ID: {}".format(hid))

    session = LahDb.session()
    haplotig = session.query(Haplotig).get(hid)
    if not haplotig:
        raise Exception("Failed to get haplotig {} from db!".format(hid))

    haplotig.load_reads()
    if not hasattr(haplotig, "reads"):
        raise Exception("Haplotig {} has no reads!".format(hid))

    source_seqfiles = session.query(Seqfile).all()
    if not len(source_seqfiles):
        raise Exception("No seqfiles fround in database!")

    print("Output: {}".format(output))
    haplotig.seqfile(sources=source_seqfiles, output=output)
    print("Generate haplotig seqfile ... OK")
